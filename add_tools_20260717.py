import sqlite3
import json
import os

TOOLS = [
    {
        "id": 48,
        "name": "Midjourney V6",
        "category": "bild",
        "description": "Senaste versionen av Midjourney med exceptionell fotorealism och förmåga att rendera text i bilder.",
        "pricing": "Från $10/mån",
        "rating": 4.9,
        "gdpr_status": "Varning (Discord)",
        "tags": ["bild", "design", "ai-konst", "fotorealism"],
        "icon_emoji": "🎨",
        "icon_bg_color": "bg-indigo-900"
    },
    {
        "id": 49,
        "name": "Mistral Large 2",
        "category": "text",
        "description": "Mistrals flaggskeppsmodell som utmanar GPT-4o i resonemang och kodning. Europeiskt företag med starkt fokus på data privacy.",
        "pricing": "API / Le Chat",
        "rating": 4.8,
        "gdpr_status": "GDPR-klar",
        "tags": ["text", "kodning", "europeisk", "llm"],
        "icon_emoji": "🌪️",
        "icon_bg_color": "bg-orange-600"
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
        # Check if exists by name
        exists = False
        for t in data:
            if t.get('name') == tool['name']:
                exists = True
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
