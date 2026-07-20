import json
import sqlite3

def main():
    conn = sqlite3.connect("tools.db")
    c = conn.cursor()
    
    # Get highest id
    c.execute("SELECT MAX(id) FROM tools")
    max_id_result = c.fetchone()
    next_id = (max_id_result[0] or 0) + 1

    new_tools = [
        {
            "name": "Google NotebookLM",
            "category": "produktivitet",
            "description": "Ett AI-drivet anteckningsverktyg från Google som låter dig ladda upp källor (PDF:er, Google Docs) och sedan ställa frågor, skapa sammanfattningar eller generera insikter baserat enbart på ditt material.",
            "pricing": "Gratis",
            "rating": 4.6,
            "gdpr_status": "Oklart",
            "tags": ["anteckningar", "sammanfattning", "research", "google", "studenter", "forskning"],
            "icon_emoji": "📓",
            "icon_bg_color": "bg-blue-100"
        },
        {
            "name": "Descript",
            "category": "ljud_och_video",
            "description": "Ett kraftfullt verktyg för att redigera video och ljud genom att redigera text. Skapar automatiskt transkriptioner och låter dig klippa, lägga till effekter och generera AI-röster direkt i manus-vyn.",
            "pricing": "Freemium",
            "rating": 4.8,
            "gdpr_status": "Klar",
            "tags": ["videoredigering", "podd", "transkribering", "ljudredigering", "ai-röster"],
            "icon_emoji": "🎙️",
            "icon_bg_color": "bg-purple-100"
        },
        {
            "name": "HeyGen",
            "category": "ljud_och_video",
            "description": "Ledande plattform för att skapa AI-videor med realistiska avatarer. Låter dig skriva ett manus och omedelbart få en video med en AI-presentatör, inklusive stöd för röstkloning och översättning.",
            "pricing": "Freemium",
            "rating": 4.7,
            "gdpr_status": "Klar",
            "tags": ["video", "avatar", "presentation", "marknadsföring", "röstkloning"],
            "icon_emoji": "👤",
            "icon_bg_color": "bg-indigo-100"
        },
        {
            "name": "Phind",
            "category": "kod",
            "description": "En AI-sökmotor byggd specifikt för utvecklare och tekniska frågor. Söker på webben och genererar kodexempel och förklaringar baserat på den senaste dokumentationen.",
            "pricing": "Freemium",
            "rating": 4.5,
            "gdpr_status": "Oklart",
            "tags": ["kod", "utvecklare", "sökmotor", "programmering", "felsökning"],
            "icon_emoji": "🔍",
            "icon_bg_color": "bg-slate-100"
        },
        {
            "name": "Copy.ai",
            "category": "text",
            "description": "Ett AI-verktyg specialiserat på copywriting och marknadsföring. Innehåller hundratals mallar för sociala medier, annonser, blogginlägg och e-post.",
            "pricing": "Freemium",
            "rating": 4.4,
            "gdpr_status": "Klar",
            "tags": ["copywriting", "marknadsföring", "blogg", "sociala medier", "textgenerering"],
            "icon_emoji": "✍️",
            "icon_bg_color": "bg-pink-100"
        },
        {
            "name": "Beautiful.ai",
            "category": "produktivitet",
            "description": "Ett presentationsverktyg som använder AI för att automatiskt designa snygga slides. Du lägger in innehållet, och verktyget formaterar det omedelbart med smarta layouter.",
            "pricing": "Premium",
            "rating": 4.6,
            "gdpr_status": "Klar",
            "tags": ["presentationer", "design", "slides", "möten", "pitch"],
            "icon_emoji": "📊",
            "icon_bg_color": "bg-emerald-100"
        }
    ]
    
    added = 0
    for tool in new_tools:
        # Check if exists
        c.execute("SELECT id FROM tools WHERE name = ?", (tool["name"],))
        if c.fetchone() is None:
            tags_json = json.dumps(tool["tags"])
            c.execute("""
                INSERT INTO tools 
                (id, name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (next_id, tool["name"], tool["category"], tool["description"], 
                  tool["pricing"], tool["rating"], tool["gdpr_status"], tags_json,
                  tool["icon_emoji"], tool["icon_bg_color"]))
            next_id += 1
            added += 1
            print(f"Lade till {tool['name']} i databasen.")
            
    conn.commit()
    
    c.execute("SELECT COUNT(*) FROM tools")
    total = c.fetchone()[0]
    conn.close()
    
    print(f"Klar. Lade till {added} nya verktyg. Databasen har nu {total} verktyg totalt.")

if __name__ == "__main__":
    main()
