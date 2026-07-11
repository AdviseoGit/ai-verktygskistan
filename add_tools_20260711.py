import sqlite3
import json

db_path = "/data/workspace/projects/ai-verktygskistan/tools.db"
json_path = "/data/workspace/projects/ai-verktygskistan/static/tools.json"

new_tools = [
    {
        "name": "Gamma",
        "category": "presentation",
        "description": "Skapa snygga presentationer, dokument och webbsidor snabbt med AI. Perfekt för pitchdeck och rapporter. Svenska stöds.",
        "pricing": "Freemium",
        "rating": 4.8,
        "gdpr_status": "Oklart",
        "tags": '["Presentation", "Design", "Dokument"]',
        "icon_emoji": "📊",
        "icon_bg_color": "bg-pink-100 text-pink-600"
    },
    {
        "name": "ElevenLabs",
        "category": "ljud",
        "description": "Marknadsledande AI-röstkloning och text-till-tal. Generera extremt realistiska röster på svenska och andra språk.",
        "pricing": "Freemium",
        "rating": 4.9,
        "gdpr_status": "Nej",
        "tags": '["Röst", "Ljud", "Text-till-tal"]',
        "icon_emoji": "🎙️",
        "icon_bg_color": "bg-indigo-100 text-indigo-600"
    },
    {
        "name": "Suno AI",
        "category": "ljud",
        "description": "Skapa musik och låtar direkt från textprompts. Suno genererar både musik och sång (även på svenska) utifrån din text.",
        "pricing": "Freemium",
        "rating": 4.7,
        "gdpr_status": "Oklart",
        "tags": '["Musik", "Ljud", "Sång"]',
        "icon_emoji": "🎵",
        "icon_bg_color": "bg-yellow-100 text-yellow-600"
    }
]

def add_tools():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    for tool in new_tools:
        cur.execute("SELECT id FROM tools WHERE name = ?", (tool["name"],))
        if not cur.fetchone():
            cur.execute('''
                INSERT INTO tools (name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (tool["name"], tool["category"], tool["description"], tool["pricing"], tool["rating"], tool["gdpr_status"], tool["tags"], tool["icon_emoji"], tool["icon_bg_color"]))
    
    conn.commit()
    conn.close()

def update_json():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM tools")
    tools = [dict(row) for row in cur.fetchall()]
    conn.close()
    
    for tool in tools:
        if isinstance(tool.get('tags'), str):
            try:
                tool['tags'] = json.loads(tool['tags'])
            except:
                tool['tags'] = []
                
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    add_tools()
    update_json()
    print("Tools added and JSON updated!")
