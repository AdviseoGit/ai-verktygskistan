import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
cursor = conn.cursor()

new_tools = [
    {
        "name": "Opus Clip",
        "category": "video",
        "description": "Tar en lång video (t.ex. en podd eller YouTube-video) och klipper automatiskt ut de mest engagerande virala ögonblicken som färdiga korta klipp med textning.",
        "pricing": "Från $19/mån",
        "rating": 4.8,
        "gdpr_status": "Granskning",
        "tags": '["video", "redigering", "sociala-medier", "shorts"]',
        "icon_emoji": "✂️",
        "icon_bg_color": "bg-pink-600"
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
