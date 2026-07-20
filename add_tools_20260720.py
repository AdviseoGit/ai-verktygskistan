import json
import sqlite3

def main():
    with open("tools.json", "r") as f:
        tools = json.load(f)

    new_tools = [
        {
            "id": "notebooklm",
            "name": "Google NotebookLM",
            "category": "produktivitet",
            "description": "Ett AI-drivet anteckningsverktyg från Google som låter dig ladda upp källor (PDF:er, Google Docs) och sedan ställa frågor, skapa sammanfattningar eller generera insikter baserat enbart på ditt material.",
            "price": "Gratis",
            "url": "https://notebooklm.google.com/",
            "is_free": True,
            "has_api": False,
            "gdpr_compliant": True,
            "tags": ["anteckningar", "sammanfattning", "research", "google", "studenter", "forskning"]
        },
        {
            "id": "descript",
            "name": "Descript",
            "category": "ljud-video",
            "description": "Ett kraftfullt verktyg för att redigera video och ljud genom att redigera text. Skapar automatiskt transkriptioner och låter dig klippa, lägga till effekter och generera AI-röster direkt i manus-vyn.",
            "price": "Freemium",
            "url": "https://www.descript.com/",
            "is_free": False,
            "has_api": False,
            "gdpr_compliant": True,
            "tags": ["videoredigering", "podd", "transkribering", "ljudredigering", "ai-röster"]
        },
        {
            "id": "heygen",
            "name": "HeyGen",
            "category": "ljud-video",
            "description": "Ledande plattform för att skapa AI-videor med realistiska avatarer. Låter dig skriva ett manus och omedelbart få en video med en AI-presentatör, inklusive stöd för röstkloning och översättning.",
            "price": "Freemium",
            "url": "https://www.heygen.com/",
            "is_free": False,
            "has_api": True,
            "gdpr_compliant": True,
            "tags": ["video", "avatar", "presentation", "marknadsföring", "röstkloning"]
        },
        {
            "id": "phind",
            "name": "Phind",
            "category": "kod-dev",
            "description": "En AI-sökmotor byggd specifikt för utvecklare och tekniska frågor. Söker på webben och genererar kodexempel och förklaringar baserat på den senaste dokumentationen.",
            "price": "Freemium",
            "url": "https://www.phind.com/",
            "is_free": True,
            "has_api": False,
            "gdpr_compliant": False,
            "tags": ["kod", "utvecklare", "sökmotor", "programmering", "felsökning"]
        },
        {
            "id": "copyai",
            "name": "Copy.ai",
            "category": "text-skrivande",
            "description": "Ett AI-verktyg specialiserat på copywriting och marknadsföring. Innehåller hundratals mallar för sociala medier, annonser, blogginlägg och e-post.",
            "price": "Freemium",
            "url": "https://www.copy.ai/",
            "is_free": False,
            "has_api": True,
            "gdpr_compliant": True,
            "tags": ["copywriting", "marknadsföring", "blogg", "sociala medier", "textgenerering"]
        },
        {
            "id": "beautifulai",
            "name": "Beautiful.ai",
            "category": "produktivitet",
            "description": "Ett presentationsverktyg som använder AI för att automatiskt designa snygga slides. Du lägger in innehållet, och verktyget formaterar det omedelbart med smarta layouter.",
            "price": "Premium",
            "url": "https://www.beautiful.ai/",
            "is_free": False,
            "has_api": False,
            "gdpr_compliant": True,
            "tags": ["presentationer", "design", "slides", "möten", "pitch"]
        }
    ]

    added = 0
    existing_ids = [t["id"] for t in tools]
    
    for tool in new_tools:
        if tool["id"] not in existing_ids:
            tools.append(tool)
            added += 1
            print(f"Lade till {tool['name']}")
    
    with open("tools.json", "w") as f:
        json.dump(tools, f, indent=4, ensure_ascii=False)
        
    print(f"Sparade till tools.json. Lade till {added} verktyg. Totalt nu: {len(tools)}.")

    # Uppdatera databasen
    conn = sqlite3.connect("tools.db")
    c = conn.cursor()
    
    for tool in new_tools:
        try:
            tags_json = json.dumps(tool["tags"])
            c.execute("""
                INSERT OR REPLACE INTO tools 
                (id, name, category, description, price, url, is_free, has_api, gdpr_compliant, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (tool["id"], tool["name"], tool["category"], tool["description"], 
                  tool["price"], tool["url"], tool["is_free"], tool["has_api"], 
                  tool["gdpr_compliant"], tags_json))
        except Exception as e:
            print(f"Fel för {tool['name']}: {e}")
            
    conn.commit()
    conn.close()
    print("Uppdaterade tools.db.")

if __name__ == "__main__":
    main()
