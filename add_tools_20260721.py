import json
import sqlite3
import datetime

# Ladda befintliga verktyg
with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'r') as f:
    tools = json.load(f)

new_tools = [
    {
        "id": "tavus",
        "name": "Tavus",
        "description": "Programmatisk videogenerering med AI. Skapa personliga videokampanjer i stor skala genom att spela in en basvideo och låta AI anpassa namn, företag och röst till varje mottagare.",
        "category": "Video",
        "price": "Freemium / Från $89/mån",
        "url": "https://www.tavus.io/",
        "tags": ["video", "marknadsföring", "sälj", "AI-avatar", "generativ-AI", "personalisering"],
        "rating": 4.6,
        "isGDPRCompliant": True,
        "gdprNote": "Erbjuder DPA och GDPR-compliance för företagskunder. Data krypteras i vila och under överföring."
    },
    {
        "id": "heygen",
        "name": "HeyGen",
        "description": "Kraftfull plattform för AI-avatarer och videoskapande. Skapa professionella videor med fotorealistiska avatarer och röster på över 40 språk utan kamera eller studio.",
        "category": "Video",
        "price": "Freemium / Från $29/mån",
        "url": "https://www.heygen.com/",
        "tags": ["video", "AI-avatar", "generativ-AI", "text-till-video", "röstkloning", "översättning"],
        "rating": 4.8,
        "isGDPRCompliant": True,
        "gdprNote": "HeyGen är GDPR-kompatibla och erbjuder ett Data Processing Agreement (DPA) för europeiska kunder."
    },
    {
        "id": "fireflies",
        "name": "Fireflies.ai",
        "description": "AI-assistent för möten som automatiskt spelar in, transkriberar, och sammanfattar videomöten (Teams, Zoom, Google Meet). Genererar action items och gör möten sökbara.",
        "category": "Produktivitet",
        "price": "Freemium / Från $10/mån",
        "url": "https://fireflies.ai/",
        "tags": ["möten", "transkribering", "sammanfattning", "produktivitet", "team", "integration"],
        "rating": 4.7,
        "isGDPRCompliant": True,
        "gdprNote": "GDPR-kompatibla med servrar i USA (AWS). EU-baserade företag kan begära DPA och specifik datalagring."
    },
    {
        "id": "zapier-central",
        "name": "Zapier Central",
        "description": "Experimentell AI-arbetsyta från Zapier där du kan lära botar att utföra uppgifter över 6000+ appar via chatt. Som ChatGPT, men med direkt åtkomst till hela din mjukvarustack.",
        "category": "Automation",
        "price": "Gratis under beta / Ingår i Zapier",
        "url": "https://zapier.com/central",
        "tags": ["automation", "AI-agent", "integration", "arbetsflöden", "produktivitet"],
        "rating": 4.5,
        "isGDPRCompliant": True,
        "gdprNote": "Följer Zapiers övergripande GDPR-policy med DPA tillgängligt för företag."
    }
]

tools.extend(new_tools)

# Spara JSON
with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'w') as f:
    json.dump(tools, f, indent=4, ensure_ascii=False)

# Kopiera även till roten för säkerhets skull
with open('/data/workspace/projects/ai-verktygskistan/tools.json', 'w') as f:
    json.dump(tools, f, indent=4, ensure_ascii=False)

# Databas-format är annorlunda, behöver inte inserta dit om det inte matchar, JSON driver frontenden ofta.
# Vi synkar JSON-formatet till DB om det går
try:
    conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
    cursor = conn.cursor()
    # Find max id to increment (id is INTEGER in DB)
    cursor.execute("SELECT MAX(id) FROM tools")
    max_id_row = cursor.fetchone()
    max_id = max_id_row[0] if max_id_row[0] is not None else 0
    
    for tool in new_tools:
        max_id += 1
        gdpr_status = "green" if tool["isGDPRCompliant"] else "red"
        tags_str = ", ".join(tool["tags"])
        cursor.execute('''
            INSERT INTO tools (id, name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            max_id,
            tool["name"],
            tool["category"],
            tool["description"],
            tool["price"],
            tool["rating"],
            gdpr_status,
            tags_str,
            "🚀",
            "bg-blue-100 text-blue-600"
        ))
    conn.commit()
    conn.close()
    print("Database synced as well.")
except Exception as e:
    print(f"Skipped DB sync: {e}")


print(f"Lade till {len(new_tools)} nya verktyg. Total: {len(tools)}")
