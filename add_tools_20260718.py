import sqlite3
import json
import os

TOOLS = [
    {
        "id": 50,
        "name": "Kling AI",
        "category": "video",
        "description": "Kinas svar på Sora, tillgänglig globalt via webbinterface. Skapar hyperrealistiska 1080p videor på upp till 120 sekunder med fysiskt korrekta simulationer.",
        "pricing": "Freemium (dagliga krediter)",
        "rating": 4.8,
        "gdpr_status": "Varning",
        "tags": ["video", "text-till-video", "kling"],
        "icon_emoji": "🎬",
        "icon_bg_color": "bg-red-600"
    },
    {
        "id": 51,
        "name": "Napkin AI",
        "category": "design",
        "description": "Konverterar text automatiskt till diagram, grafer och mindmaps. Otroligt användbart för presentationer och strategidokument.",
        "pricing": "Freemium",
        "rating": 4.6,
        "gdpr_status": "Granskning",
        "tags": ["design", "mindmap", "presentation", "diagram"],
        "icon_emoji": "📊",
        "icon_bg_color": "bg-yellow-500"
    },
    {
        "id": 52,
        "name": "ElevenLabs Reader",
        "category": "ljud",
        "description": "Lyssningsapp som läser upp artiklar, PDF:er och e-böcker med ElevenLabs hyperrealistiska AI-röster. Perfekt för on-the-go lärande.",
        "pricing": "Gratis (App)",
        "rating": 4.9,
        "gdpr_status": "Granskning",
        "tags": ["ljud", "tts", "mobilapp", "text-till-tal"],
        "icon_emoji": "🎧",
        "icon_bg_color": "bg-blue-900"
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
