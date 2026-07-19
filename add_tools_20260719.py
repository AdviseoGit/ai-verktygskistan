import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
cursor = conn.cursor()

new_tools = [
    {
        "name": "Kling",
        "category": "video",
        "description": "Kinas ledande AI-videogenerator som nyligen lanserats globalt. Genererar otroligt realistiska 1080p-videor från text med fantastisk fysik-simulering och upp till 2 minuters längd.",
        "pricing": "Freemium",
        "rating": 4.8,
        "gdpr_status": "Granskning",
        "tags": '["video", "text-till-video", "realism", "sora-alternativ"]',
        "icon_emoji": "🎬",
        "icon_bg_color": "bg-red-600"
    },
    {
        "name": "ChatGPT 4o mini",
        "category": "text",
        "description": "OpenAI's nya snabba, kostnadseffektiva och extremt kapabla lilla modell (lanserat juli 2026). Slår de flesta äldre stora modeller i prestanda men kostar en bråkdel.",
        "pricing": "Gratis / API $0.15/1M tokens",
        "rating": 4.9,
        "gdpr_status": "GDPR-klar",
        "tags": '["text", "llm", "snabb", "openai"]',
        "icon_emoji": "⚡",
        "icon_bg_color": "bg-green-500"
    },
    {
        "name": "Ideogram 2.0",
        "category": "bild",
        "description": "Bildgenerator med marknadens bästa förmåga att rendera text i bilder korrekt. Oslagbar för logotyper, affischer och typografi-tung design.",
        "pricing": "Freemium",
        "rating": 4.7,
        "gdpr_status": "Granskning",
        "tags": '["bild", "typografi", "design", "logotyp"]',
        "icon_emoji": "🔤",
        "icon_bg_color": "bg-gray-900"
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
