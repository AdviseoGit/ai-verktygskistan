import os
from fastapi import FastAPI, Depends
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
