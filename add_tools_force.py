import json
import sqlite3

TOOLS = [
    {
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

def add():
    with open('tools.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    tlist = data
    
    seen_names = [t.get("name") for t in tlist]
    
    # We ignore previous additions. We just append.
    max_id = max([int(t.get("id", 0)) for t in tlist]) if tlist else 0
            
    added = 0
    for t in TOOLS:
        if t["name"] not in seen_names:
            max_id += 1
            t_copy = t.copy()
            t_copy["id"] = max_id
            tlist.append(t_copy)
            added += 1
            seen_names.append(t["name"])
            
    with open('tools.json', 'w', encoding='utf-8') as f:
        json.dump(tlist, f, indent=4, ensure_ascii=False)

    conn = sqlite3.connect('tools.db')
    c = conn.cursor()
    c.execute('SELECT name FROM tools')
    db_names = [row[0] for row in c.fetchall()]
    
    c.execute('SELECT MAX(id) FROM tools')
    db_max_id = c.fetchone()[0] or 0

    added_db = 0
    for t in TOOLS:
        if t["name"] not in db_names:
            db_max_id += 1
            c.execute('''
                INSERT INTO tools (id, name, category, description, pricing, tags, icon_emoji, icon_bg_color, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                db_max_id, t['name'], t['category'], t['description'],
                t['pricing'], json.dumps(t['tags']),
                t['icon_emoji'], t['icon_bg_color'], t['rating']
            ))
            added_db += 1

    conn.commit()
    conn.close()
    
    print(f"Added {added} tools to json, {added_db} to db.")

add()
