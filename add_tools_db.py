import sys
import os
sys.path.append(os.getcwd())
from database import Base, engine, SessionLocal
from models import Tool

db = SessionLocal()
tools_to_add = [
    {
        "name": "Gamma AI",
        "category": "Presentation & Design",
        "description": "Skapa snygga presentationer, dokument och webbsidor på sekunder med hjälp av AI. Perfekt för snabba pitch decks och rapporter.",
        "pricing": "Freemium (från 8$/mån)",
        "rating": 4.8,
        "gdpr_status": "Oklart",
        "tags": "Presentation,Design,AI,Snabbt",
        "icon_emoji": "✨",
        "icon_bg_color": "bg-purple-100"
    },
    {
        "name": "Synthesia",
        "category": "Video & Ljud",
        "description": "Skapa professionella videor med AI-avatarer från enbart text. Stödjer över 120 språk inklusive svenska. Bra för utbildning och marknadsföring.",
        "pricing": "Från 22$/mån",
        "rating": 4.7,
        "gdpr_status": "GDPR-kompatibel (EU-lagring möjlig)",
        "tags": "Video,Avatar,Text-till-video,Svenska",
        "icon_emoji": "🎬",
        "icon_bg_color": "bg-blue-100"
    },
    {
        "name": "Descript",
        "category": "Video & Ljud",
        "description": "Redigera video och poddar genom att redigera text (transkribering). Inkluderar Overdub för att skapa en AI-klon av din röst.",
        "pricing": "Freemium (från 12$/mån)",
        "rating": 4.9,
        "gdpr_status": "DPA tillgänglig",
        "tags": "Podd,Video,Redigering,Transkribering",
        "icon_emoji": "🎙️",
        "icon_bg_color": "bg-indigo-100"
    }
]

added_count = 0
for tool_data in tools_to_add:
    existing = db.query(Tool).filter(Tool.name == tool_data["name"]).first()
    if not existing:
        new_tool = Tool(**tool_data)
        db.add(new_tool)
        added_count += 1

db.commit()
print(f"Added {added_count} new tools.")
