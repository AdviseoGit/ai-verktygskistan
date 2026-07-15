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

# Read what's in DB
conn = sqlite3.connect('tools.db')
c = conn.cursor()
c.execute('SELECT id, name, category, description, pricing, tags, icon_emoji, icon_bg_color, rating FROM tools')

data = []
max_id = 0
for row in c.fetchall():
    tid = row[0]
    if isinstance(tid, int) and tid > max_id:
        max_id = tid
    data.append({
        "id": tid,
        "name": row[1],
        "category": row[2],
        "description": row[3],
        "pricing": row[4],
        "tags": json.loads(row[5]) if row[5] else [],
        "icon_emoji": row[6],
        "icon_bg_color": row[7],
        "rating": row[8]
    })

db_names = {t["name"] for t in data}

for t in TOOLS:
    if t["name"] not in db_names:
        max_id += 1
        t_copy = t.copy()
        t_copy["id"] = max_id
        data.append(t_copy)
        
        c.execute('''
            INSERT INTO tools (id, name, category, description, pricing, tags, icon_emoji, icon_bg_color, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            max_id, t['name'], t['category'], t['description'],
            t['pricing'], json.dumps(t['tags']),
            t['icon_emoji'], t['icon_bg_color'], t['rating']
        ))

conn.commit()
conn.close()

# overwrite JSON with correct list
with open('tools.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Total tools in DB and JSON: {len(data)}")
