import sqlite3
import json

conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
cursor = conn.cursor()

new_tools = [
    {
        "name": "Google NotebookLM",
        "category": "produktivitet",
        "description": "Ett AI-drivet anteckningsverktyg från Google som låter dig ladda upp källor (PDF:er, Google Docs) och sedan ställa frågor, skapa sammanfattningar eller generera insikter baserat enbart på ditt material.",
        "pricing": "Gratis",
        "rating": 4.6,
        "gdpr_status": "Oklart",
        "tags": '["anteckningar", "sammanfattning", "research", "google", "studenter", "forskning"]',
        "icon_emoji": "📓",
        "icon_bg_color": "bg-blue-100"
    },
    {
        "name": "Descript",
        "category": "ljud_och_video",
        "description": "Ett kraftfullt verktyg för att redigera video och ljud genom att redigera text. Skapar automatiskt transkriptioner och låter dig klippa, lägga till effekter och generera AI-röster direkt i manus-vyn.",
        "pricing": "Freemium",
        "rating": 4.8,
        "gdpr_status": "GDPR-klar",
        "tags": '["videoredigering", "podd", "transkribering", "ljudredigering", "ai-röster"]',
        "icon_emoji": "🎙️",
        "icon_bg_color": "bg-purple-100"
    },
    {
        "name": "HeyGen",
        "category": "ljud_och_video",
        "description": "Ledande plattform för att skapa AI-videor med realistiska avatarer. Låter dig skriva ett manus och omedelbart få en video med en AI-presentatör, inklusive stöd för röstkloning och översättning.",
        "pricing": "Freemium",
        "rating": 4.7,
        "gdpr_status": "GDPR-klar",
        "tags": '["video", "avatar", "presentation", "marknadsföring", "röstkloning"]',
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
        "tags": '["kod", "utvecklare", "sökmotor", "programmering", "felsökning"]',
        "icon_emoji": "🔍",
        "icon_bg_color": "bg-slate-100"
    },
    {
        "name": "Copy.ai",
        "category": "text",
        "description": "Ett AI-verktyg specialiserat på copywriting och marknadsföring. Innehåller hundratals mallar för sociala medier, annonser, blogginlägg och e-post.",
        "pricing": "Freemium",
        "rating": 4.4,
        "gdpr_status": "GDPR-klar",
        "tags": '["copywriting", "marknadsföring", "blogg", "sociala medier", "textgenerering"]',
        "icon_emoji": "✍️",
        "icon_bg_color": "bg-pink-100"
    },
    {
        "name": "Beautiful.ai",
        "category": "design",
        "description": "Ett presentationsverktyg som använder AI för att automatiskt designa snygga slides. Du lägger in innehållet, och verktyget formaterar det omedelbart med smarta layouter.",
        "pricing": "Premium",
        "rating": 4.6,
        "gdpr_status": "GDPR-klar",
        "tags": '["presentationer", "design", "slides", "möten", "pitch"]',
        "icon_emoji": "📊",
        "icon_bg_color": "bg-emerald-100"
    }
]

added_count = 0
for tool in new_tools:
    cursor.execute("SELECT id FROM tools WHERE name = ?", (tool['name'],))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO tools (name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (tool['name'], tool['category'], tool['description'], tool['pricing'], tool['rating'], tool['gdpr_status'], tool['tags'], tool['icon_emoji'], tool['icon_bg_color']))
        added_count += 1

conn.commit()

# Update tools.json which we know is served from /static/tools.json
cursor.execute('SELECT * FROM tools ORDER BY name ASC')
columns = [column[0] for column in cursor.description]
tools = []
for row in cursor.fetchall():
    tool = dict(zip(columns, row))
    tool['tags'] = json.loads(tool['tags']) if tool['tags'] else []
    tools.append(tool)
    
with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'w', encoding='utf-8') as f:
    json.dump(tools, f, ensure_ascii=False, indent=2)
    
# also update the root tools.json just in case
with open('/data/workspace/projects/ai-verktygskistan/tools.json', 'w', encoding='utf-8') as f:
    json.dump(tools, f, ensure_ascii=False, indent=2)

print(f"Added {added_count} new tools. Total in DB: {len(tools)}")
