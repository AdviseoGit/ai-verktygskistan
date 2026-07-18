import sqlite3
import json
import os

TOOLS = [
    {
        "id": 55,
        "name": "Apple Intelligence",
        "category": "produktivitet",
        "description": "Apples djupt integrerade AI-system i iOS 18 och macOS Sequoia. Genererar text och bilder, förstår personlig kontext och förbättrar Siri kraftigt, med starkt fokus på on-device privacy.",
        "pricing": "Gratis (på kompatibla enheter)",
        "rating": 4.5,
        "gdpr_status": "GDPR-klar",
        "tags": ["produktivitet", "apple", "ios", "assistent"],
        "icon_emoji": "🍎",
        "icon_bg_color": "bg-gray-800"
    }
]

def update_db():
    conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
    c = conn.cursor()
    
    for tool in TOOLS:
        c.execute('''
            INSERT OR REPLACE INTO tools 
            (id, name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            tool["id"], tool["name"], tool["category"], tool["description"], 
            tool["pricing"], tool["rating"], tool["gdpr_status"], 
            json.dumps(tool["tags"]), tool["icon_emoji"], tool["icon_bg_color"]
        ))
        print(f"Added/Updated DB: {tool['name']}")
    
    conn.commit()
    conn.close()

def update_json():
    json_path = '/data/workspace/projects/ai-verktygskistan/tools.json'
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []
        
    for tool in TOOLS:
        exists = False
        for i, t in enumerate(data):
            if t.get('name') == tool['name'] or t.get('id') == tool['id']:
                exists = True
                data[i] = dict(tool)
                data[i]["tags"] = ','.join(tool["tags"])
                break
        if not exists:
            tool_json = dict(tool)
            tool_json["tags"] = ','.join(tool["tags"])
            data.append(tool_json)
        
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Updated JSON. Total tools: {len(data)}")

if __name__ == '__main__':
    update_db()
    update_json()
