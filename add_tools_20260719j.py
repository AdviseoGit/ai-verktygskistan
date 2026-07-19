import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
cursor = conn.cursor()

new_tools = [
    {
        "name": "Canva Magic Studio",
        "category": "design",
        "description": "Canvas inbyggda AI-svit. Innehåller allt från AI-bildgenerering och borttagning av bakgrunder till automatiskt genererade presentationer och texter.",
        "pricing": "Ingår i Canva Pro",
        "rating": 4.9,
        "gdpr_status": "GDPR-klar",
        "tags": '["design", "presentation", "bild", "allt-i-ett"]',
        "icon_emoji": "🎨",
        "icon_bg_color": "bg-cyan-500"
    },
    {
        "name": "ElevenLabs",
        "category": "ljud",
        "description": "Marknadsledande AI-röstgenerator (Text-to-Speech). Otroligt realistiska röster som kan uttrycka känslor, och du kan klona din egen röst på sekunder.",
        "pricing": "Freemium",
        "rating": 4.9,
        "gdpr_status": "Granskning",
        "tags": '["ljud", "tts", "röstkloning", "voiceover"]',
        "icon_emoji": "🎙️",
        "icon_bg_color": "bg-black"
    },
    {
        "name": "Tome",
        "category": "design",
        "description": "Generativ AI för presentationer och storytelling. Skriv en prompt och Tome genererar en hel presentation med text, bilder och layout på sekunder.",
        "pricing": "Freemium",
        "rating": 4.6,
        "gdpr_status": "Granskning",
        "tags": '["design", "presentation", "storytelling", "pitch"]',
        "icon_emoji": "📖",
        "icon_bg_color": "bg-purple-800"
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

# Update tools.json
cursor.execute('SELECT * FROM tools ORDER BY name ASC')
columns = [column[0] for column in cursor.description]
tools = []
for row in cursor.fetchall():
    tool = dict(zip(columns, row))
    tool['tags'] = json.loads(tool['tags']) if tool['tags'] else []
    tools.append(tool)
    
with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'w', encoding='utf-8') as f:
    json.dump(tools, f, ensure_ascii=False, indent=2)

print(f"Added {added_count} new tools. Total in DB: {len(tools)}")
