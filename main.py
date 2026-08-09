import os
import secrets
import datetime
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException, Header
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn

from database import get_db, engine, Base
from models import Tool

# Ensure tables are created
# Force rebuild
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Verktygslådan")

from pydantic import BaseModel, EmailStr


def require_admin(x_admin_token: str = Header(default="")):
    """Skyddar endpoints som lämnar ut personuppgifter.

    Sätt ADMIN_TOKEN i Railway och skicka den som X-Admin-Token-header.
    Saknas variabeln är exporterna helt stängda – en sajt som säljer sig på
    GDPR ska inte ha öppna endpoints som listar e-postadresser.
    """
    expected = os.environ.get("ADMIN_TOKEN", "")
    if not expected or not secrets.compare_digest(x_admin_token, expected):
        raise HTTPException(status_code=404)


class LeadIn(BaseModel):
    email: EmailStr


def _deliver_aiv(email: str):
    import mailer
    import report_aiv
    pdf = None
    try:
        pdf = report_aiv.build_guide_pdf()
    except Exception as e:
        print(f"[aiv] guide pdf failed: {e}")
    atts = [("AI-GDPR-checklista.pdf", pdf, "application/pdf")] if pdf else None
    mailer.send_email(email, "Din GDPR-checklista for AI-verktyg",
                      report_aiv.user_email_html(), attachments=atts,
                      from_name="AI-Verktygslådan")
    mailer.notify_owner("Ny lead - AI-Verktygslådan",
                        f"<p>Ny lead: <b>{email}</b></p>", reply_to=email,
                        from_name="AI-Verktygslådan")


@app.post("/api/lead/")
@app.post("/api/lead")
async def capture_lead(lead: LeadIn, background: BackgroundTasks, db: Session = Depends(get_db)):
    from models import Lead
    
    # Check if already exists
    existing = db.query(Lead).filter(Lead.email == lead.email).first()
    if not existing:
        new_lead = Lead(email=lead.email, source="web_form")
        db.add(new_lead)
        db.commit()
    
    background.add_task(_deliver_aiv, lead.email)
    return {"status": "success"}

@app.get("/api/stats/leads")
def get_leads_stats(db: Session = Depends(get_db)):
    """Returnerar statistik om lead-flödet (alla typer)."""
    now = datetime.datetime.utcnow()
    seven_days_ago = now - datetime.timedelta(days=7)
    
    # Newsletter leads
    newsletter_total = db.query(models.NewsletterSubscriber).count()
    newsletter_7d = db.query(models.NewsletterSubscriber).filter(models.NewsletterSubscriber.created_at >= seven_days_ago).count()
    
    # B2B leads
    b2b_total = db.query(models.B2BLead).count()
    b2b_7d = db.query(models.B2BLead).filter(models.B2BLead.created_at >= seven_days_ago).count()
    
    # Basic leads (fallback/old system)
    basic_total = db.query(models.Lead).count()
    basic_7d = db.query(models.Lead).filter(models.Lead.created_at >= seven_days_ago).count()
    
    total = newsletter_total + b2b_total + basic_total
    last_7_days = newsletter_7d + b2b_7d + basic_7d
    
    return {
        "total": total,
        "last_7_days": last_7_days,
        "breakdown": {
            "newsletter": {"total": newsletter_total, "last_7_days": newsletter_7d},
            "b2b": {"total": b2b_total, "last_7_days": b2b_7d}
        }
    }

@app.get("/api/admin/leads")
async def get_leads(db: Session = Depends(get_db), _=Depends(require_admin)):
    from models import Lead
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
    return [{"id": l.id, "email": l.email, "source": l.source, "created_at": l.created_at} for l in leads]


class NewsletterIn(BaseModel):
    email: EmailStr
    role: str | None = None
    source: str | None = None


@app.post("/api/newsletter")
async def subscribe_newsletter(data: NewsletterIn, background: BackgroundTasks,
                               db: Session = Depends(get_db)):
    """Anmälan till "Veckans AI-verktyg"."""
    from models import NewsletterSubscriber

    existing = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.email == data.email).first()

    if existing:
        # Uppdatera rollen om prenumeranten anmäler sig igen från en annan sida.
        if data.role and existing.role != data.role:
            existing.role = data.role
            db.commit()
        return {"status": "success", "already_subscribed": True}

    db.add(NewsletterSubscriber(
        email=data.email,
        role=data.role,
        source=data.source or "web_form",
    ))
    db.commit()

    background.add_task(_notify_newsletter, data.email, data.role, data.source)
    return {"status": "success", "already_subscribed": False}


def _notify_newsletter(email: str, role: str | None, source: str | None):
    import mailer
    try:
        mailer.notify_owner(
            "Ny nyhetsbrevsprenumerant - AI-Verktygslådan",
            f"<p><b>{email}</b></p><p>Roll: {role or '-'}<br>Källa: {source or '-'}</p>",
            reply_to=email, from_name="AI-Verktygslådan")
    except Exception as e:
        print(f"[aiv] newsletter notify failed: {e}")


class B2BLeadIn(BaseModel):
    name: str
    email: EmailStr
    company: str
    role: str | None = None
    employees: str | None = None
    need: str | None = None
    source: str | None = None


@app.post("/api/lead/b2b")
async def capture_b2b_lead(data: B2BLeadIn, background: BackgroundTasks,
                           db: Session = Depends(get_db)):
    """Företag som vill ha hjälp att införa AI i organisationen."""
    from models import B2BLead

    lead = B2BLead(
        name=data.name, email=data.email, company=data.company,
        role=data.role, employees=data.employees, need=data.need,
        source=data.source or "web_form",
    )
    db.add(lead)
    db.commit()

    background.add_task(_notify_b2b, data)
    return {"status": "success"}


def _notify_b2b(data: "B2BLeadIn"):
    import mailer
    body = (
        f"<h3>Ny B2B-förfrågan</h3>"
        f"<p><b>{data.name}</b> ({data.email})<br>"
        f"Företag: {data.company}<br>"
        f"Roll: {data.role or '-'}<br>"
        f"Antal anställda: {data.employees or '-'}<br>"
        f"Källa: {data.source or '-'}</p>"
        f"<p><b>Behov:</b><br>{data.need or '-'}</p>"
    )
    try:
        mailer.notify_owner("Ny B2B-lead - AI-Verktygslådan", body,
                            reply_to=data.email, from_name="AI-Verktygslådan")
    except Exception as e:
        print(f"[aiv] b2b notify failed: {e}")


@app.get("/api/admin/newsletter")
async def get_subscribers(db: Session = Depends(get_db), _=Depends(require_admin)):
    from models import NewsletterSubscriber
    rows = db.query(NewsletterSubscriber).order_by(
        NewsletterSubscriber.created_at.desc()).all()
    return [{"id": r.id, "email": r.email, "role": r.role,
             "source": r.source, "created_at": r.created_at} for r in rows]


@app.get("/api/admin/b2b-leads")
async def get_b2b_leads(db: Session = Depends(get_db), _=Depends(require_admin)):
    from models import B2BLead
    rows = db.query(B2BLead).order_by(B2BLead.created_at.desc()).all()
    return [{"id": r.id, "name": r.name, "email": r.email,
             "company": r.company, "role": r.role, "employees": r.employees,
             "need": r.need, "source": r.source, "created_at": r.created_at}
            for r in rows]


class CalcDataIn(BaseModel):
    employees: int
    salary: int
    industry: str
    saved_value: int

@app.post("/api/calc-data")
async def capture_calc_data(data: CalcDataIn, db: Session = Depends(get_db)):
    """Sparar en kalkylatorkörning.

    Skrev tidigare även till data_moat_calc.csv på containerdisken. Den filen
    låg på efemär disk och raderades vid varje deploy, och till skillnad från
    lead-endpointen fanns ingen mejlkopia – all kalkylatordata försvann alltså
    spårlöst inom ett dygn. Databasen är enda lagringen nu.
    """
    from models import CalcData

    db.add(CalcData(
        employees=data.employees,
        salary=data.salary,
        industry=data.industry,
        saved_value=data.saved_value,
    ))
    db.commit()
    return {"status": "success"}


@app.get("/api/admin/calc-data")
async def get_calc_data(db: Session = Depends(get_db), _=Depends(require_admin)):
    from models import CalcData
    rows = db.query(CalcData).order_by(CalcData.created_at.desc()).all()
    return [{"id": r.id, "employees": r.employees, "salary": r.salary,
             "industry": r.industry, "saved_value": r.saved_value,
             "created_at": r.created_at} for r in rows]

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/tools")
def get_tools(db: Session = Depends(get_db)):
    tools = db.query(Tool).all()
    return tools

@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("static/index.html")

@app.get("/robots.txt")
async def robots():
    return FileResponse("static/robots.txt")

@app.get("/sitemap.xml")
async def sitemap():
    return FileResponse("static/sitemap.xml")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.svg")

@app.get("/llms.txt")
async def serve_llms_txt():
    return FileResponse("static/llms.txt")

@app.get("/{page_name}.html", response_class=HTMLResponse)
async def serve_static_html(page_name: str):
    path = f"static/{page_name}.html"
    if not os.path.isfile(path):
        raise HTTPException(status_code=404)
    return FileResponse(path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
