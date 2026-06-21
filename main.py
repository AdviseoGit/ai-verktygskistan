import os
from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn

from database import get_db, engine, Base
from models import Tool

# Ensure tables are created
# Force rebuild
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI-Verktygskistan")

from pydantic import BaseModel, EmailStr


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
                      from_name="AI-Verktygskistan")
    mailer.notify_owner("Ny lead - AI-Verktygskistan",
                        f"<p>Ny lead: <b>{email}</b></p>", reply_to=email,
                        from_name="AI-Verktygskistan")


@app.post("/api/lead")
async def capture_lead(lead: LeadIn, background: BackgroundTasks):
    background.add_task(_deliver_aiv, lead.email)
    return {"status": "success"}


class CalcDataIn(BaseModel):
    employees: int
    salary: int
    industry: str
    saved_value: int

@app.post("/api/calc-data")
async def capture_calc_data(data: CalcDataIn):
    import os
    # Log to a simple file for now to build the data moat
    file_path = "data_moat_calc.csv"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("employees,salary,industry,saved_value\n")
    with open(file_path, "a") as f:
        f.write(f"{data.employees},{data.salary},{data.industry},{data.saved_value}\n")
    return {"status": "success"}

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

@app.get("/{page_name}.html", response_class=HTMLResponse)
async def serve_static_html(page_name: str):
    return FileResponse(f"static/{page_name}.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
