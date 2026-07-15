import json
import sqlite3

TOOLS = [
    {
        "id": "notebooklm",
        "name": "NotebookLM",
        "category": "produktivitet",
        "description": "Googles AI-assistent som 'läser' dina dokument. Du laddar upp PDF:er, Google Docs eller text, och NotebookLM blir en omedelbar expert på precis det materialet. Fantastiskt för research, studier och att sammanfatta stora mängder information med källhänvisningar direkt till din text.",
        "pricing": "Gratis",
        "tags": ["research", "dokument", "sammanfattning", "google"],
        "icon_emoji": "📚",
        "icon_bg_color": "bg-yellow-100",
        "rating": 4.8
    },
    {
        "id": "perplexity-pro",
        "name": "Perplexity Pro",
        "category": "sok",
        "description": "Uppgraderade versionen av Perplexity AI. Ger dig tillgång till premiummodeller som GPT-4o, Claude 3.5 Sonnet och Sonar Large för sökningar. Du kan välja vilken AI som ska svara, ladda upp filer obegränsat och få ännu djupare research-kapacitet. Den ultimata kunskapsmotorn.",
        "pricing": "20$/månad",
        "tags": ["sök", "research", "gpt-4o", "claude"],
        "icon_emoji": "🔍",
        "icon_bg_color": "bg-blue-100",
        "rating": 4.9
    },
    {
        "id": "heygen",
        "name": "HeyGen",
        "category": "video",
        "description": "Skapa videor med fotorealistiska AI-avatarer från text. Extremt hög kvalitet på läppsynk och röstkloning. Kan automatiskt översätta din video till andra språk och behålla din röst och läpprörelser (Video Translate). Revolutionerande för innehållsskapare och global marknadsföring.",
        "pricing": "Freemium / Från 29$/mån",
        "tags": ["avatar", "översättning", "röstkloning", "marknadsföring"],
        "icon_emoji": "👤",
        "icon_bg_color": "bg-emerald-100",
        "rating": 4.7
    }
]

def add_tools():
    # Update JSON
    try:
        with open('tools.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if isinstance(data, dict) and "tools" in data:
        tools_list = data["tools"]
    elif isinstance(data, list):
        tools_list = data
    else:
        tools_list = []

    existing_names = {t.get("name") for t in tools_list}
    
    added_count = 0
    for tool in TOOLS:
        if tool["name"] not in existing_names:
            tools_list.append(tool)
            added_count += 1

    if isinstance(data, dict) and "tools" in data:
        data["tools"] = tools_list
    else:
        data = tools_list

    with open('tools.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"Added {added_count} tools to tools.json")

    # Update DB
    try:
        conn = sqlite3.connect('tools.db')
        c = conn.cursor()
        
        c.execute('SELECT MAX(id) FROM tools')
        max_id = c.fetchone()[0] or 0

        # also get existing from db to avoid constraint fail if name isn't unique but we just don't want duplicates
        c.execute('SELECT name FROM tools')
        db_names = {row[0] for row in c.fetchall()}

        for tool in TOOLS:
            if tool['name'] not in db_names:
                max_id += 1
                try:
                    c.execute('''
                        INSERT INTO tools (id, name, category, description, pricing, tags, icon_emoji, icon_bg_color, rating)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        max_id, tool['name'], tool['category'], tool['description'],
                        tool['pricing'], json.dumps(tool['tags']),
                        tool['icon_emoji'], tool['icon_bg_color'], tool['rating']
                    ))
                except Exception as e:
                    print(e)
                    

        conn.commit()
        conn.close()
        print("Updated tools.db")
    except Exception as e:
        print(f"Error updating DB: {e}")

if __name__ == "__main__":
    add_tools()
