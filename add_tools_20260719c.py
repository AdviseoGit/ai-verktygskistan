import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
cursor = conn.cursor()

new_tools = [
    {
        "name": "Mistral NeMo",
        "category": "kod & dev",
        "description": "Liten men extremt kraftfull öppen modell byggd tillsammans med Nvidia. Bara 12B parametrar men presterar ofta i nivå med större system.",
        "pricing": "Open Source",
        "rating": 4.8,
        "gdpr_status": "Lokal körning (GDPR-säker)",
        "tags": '["llm", "open-source", "nemo", "kod"]',
        "icon_emoji": "🐠",
        "icon_bg_color": "bg-blue-400"
    },
    {
        "name": "ElevenLabs Reader App",
        "category": "ljud",
        "description": "Dedikerad app för att lyssna på böcker, artiklar eller egna dokument med marknadens mest realistiska röster.",
        "pricing": "Gratis för tillfället",
        "rating": 4.9,
        "gdpr_status": "Granskning",
        "tags": '["ljud", "läsapp", "tts", "röstkloning"]',
        "icon_emoji": "📱",
        "icon_bg_color": "bg-gray-800"
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
