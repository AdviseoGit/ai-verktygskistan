import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="AI-Verktygskistan")

app.mount("/static", StaticFiles(directory="static"), name="static")

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
