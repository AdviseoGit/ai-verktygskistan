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

# Write safely to db, fetching max ID manually to avoid auto-increment schema issues on integer IDs.

def run():
    conn = sqlite3.connect('tools.db')
    c = conn.cursor()
    c.execute('SELECT name FROM tools')
    existing = {r[0] for r in c.fetchall()}
    
    c.execute('SELECT MAX(id) FROM tools')
    max_id = c.fetchone()[0] or 0
    if not isinstance(max_id, int):
        try: max_id = int(max_id)
        except: max_id = 100

    added = 0
    for t in TOOLS:
        if t["name"] not in existing:
            max_id += 1
            # Using INSERT OR IGNORE just in case
            try:
                c.execute('''
                    INSERT INTO tools (name, category, description, pricing, tags, icon_emoji, icon_bg_color, rating)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    t['name'], t['category'], t['description'],
                    t['pricing'], json.dumps(t['tags']),
                    t['icon_emoji'], t['icon_bg_color'], t['rating']
                ))
                added += 1
            except Exception as e:
                print(f"Failed to insert {t['name']}: {e}")

    conn.commit()
    conn.close()

    # Now rewrite JSON from DB to ensure sync
    conn = sqlite3.connect('tools.db')
    c = conn.cursor()
    c.execute('SELECT id, name, category, description, pricing, tags, icon_emoji, icon_bg_color, rating FROM tools')
    
    data = []
    for row in c.fetchall():
        data.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "description": row[3],
            "pricing": row[4],
            "tags": json.loads(row[5]) if row[5] else [],
            "icon_emoji": row[6],
            "icon_bg_color": row[7],
            "rating": row[8]
        })
    conn.close()

    with open('tools.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Added {added} tools. Total DB/JSON count: {len(data)}")

run()
