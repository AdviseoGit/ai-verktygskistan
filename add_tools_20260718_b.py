import sqlite3
import json
import os

TOOLS = [
    {
        "id": 53,
        "name": "Figma AI",
        "category": "design",
        "description": "Figma's inbyggda AI-verktyg som låter dig generera UI-designer från text, hitta liknande komponenter och automatisera repetitiva uppgifter i designprocessen.",
        "pricing": "Ingår i Figma Pro",
        "rating": 4.7,
        "gdpr_status": "GDPR-klar",
        "tags": ["design", "ui", "ux", "wireframe"],
        "icon_emoji": "🎨",
        "icon_bg_color": "bg-purple-600"
    },
    {
        "id": 54,
        "name": "Synthesia",
        "category": "video",
        "description": "Ledande plattform för AI-avatarer. Skapa professionella utbildnings- och marknadsföringsvideor genom att bara skriva text. Stödjer över 120 språk.",
        "pricing": "Från $22/mån",
        "rating": 4.8,
        "gdpr_status": "GDPR-klar",
        "tags": ["video", "avatar", "utbildning", "presentation"],
        "icon_emoji": "👤",
        "icon_bg_color": "bg-blue-500"
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
