import sqlite3
import json

def update_db():
    conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
    c = conn.cursor()
    
    tools = [
        ("Zapier AI", "affar", "Automatisera arbetsflöden med AI. Zapier kopplar ihop dina appar och låter AI bygga dina automatiseringar. Kraftfullt för att spara tid och minska manuellt arbete.", "Freemium (från 20 USD/mån)", 8.9, "GDPR-klar", "Automatisering,Integrationer,Produktivitet", "⚡", "bg-blue-100"),
        ("Grammarly", "text", "Grammarlys AI-assistent hjälper dig inte bara med stavning utan skriver om meningar, anpassar tonfall och genererar text. Mycket populärt och användarvänligt.", "Freemium (från 12 USD/mån)", 8.7, "Varning", "Rättstavning,Skrivande,Engelska", "📝", "bg-green-100"),
        ("Copy.ai", "text", "Skapad specifikt för marknadsförare och säljare. Genererar blogginlägg, annonstexter och e-postkampanjer snabbt och effektivt. Har arbetsflödesfunktioner för team.", "Freemium (från 36 USD/mån)", 8.5, "Varning", "Marknadsföring,Copywriting,Sälj", "✍️", "bg-orange-100"),
        ("Fireflies.ai", "ljud", "AI-antecknare som spelar in, transkriberar och sammanfattar dina möten (Zoom, Teams, Meet). Kan extrahera action items och söka genom tidigare möteshistorik.", "Freemium (från 10 USD/mån)", 8.8, "GDPR-klar", "Möten,Transkribering,Sammanfattning", "🔥", "bg-purple-100"),
        ("Beautiful.ai", "design", "Skapar fantastiska presentationer på nolltid. AI designar slides automatiskt baserat på ditt innehåll och dina uppmaningar. En dröm för alla som avskyr PowerPoint.", "12 USD/mån", 8.6, "Varning", "Presentationer,Design,Slides", "📊", "bg-pink-100")
    ]
    
    for tool in tools:
        try:
            c.execute('''
                INSERT INTO tools (name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tool)
            print(f"Added {tool[0]} to db")
        except sqlite3.IntegrityError:
            print(f"{tool[0]} already exists in db")
            
    conn.commit()
    conn.close()

def update_json():
    with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    names = [t['name'] for t in data]
    
    new_tools = [
        {
            "name": "Zapier AI",
            "category": "affar",
            "description": "Automatisera arbetsflöden med AI. Zapier kopplar ihop dina appar och låter AI bygga dina automatiseringar. Kraftfullt för att spara tid och minska manuellt arbete.",
            "pricing": "Freemium (från 20 USD/mån)",
            "rating": 8.9,
            "gdpr_status": "GDPR-klar",
            "tags": "Automatisering,Integrationer,Produktivitet",
            "icon_emoji": "⚡",
            "icon_bg_color": "bg-blue-100"
        },
        {
            "name": "Grammarly",
            "category": "text",
            "description": "Grammarlys AI-assistent hjälper dig inte bara med stavning utan skriver om meningar, anpassar tonfall och genererar text. Mycket populärt och användarvänligt.",
            "pricing": "Freemium (från 12 USD/mån)",
            "rating": 8.7,
            "gdpr_status": "Varning",
            "tags": "Rättstavning,Skrivande,Engelska",
            "icon_emoji": "📝",
            "icon_bg_color": "bg-green-100"
        },
        {
            "name": "Copy.ai",
            "category": "text",
            "description": "Skapad specifikt för marknadsförare och säljare. Genererar blogginlägg, annonstexter och e-postkampanjer snabbt och effektivt. Har arbetsflödesfunktioner för team.",
            "pricing": "Freemium (från 36 USD/mån)",
            "rating": 8.5,
            "gdpr_status": "Varning",
            "tags": "Marknadsföring,Copywriting,Sälj",
            "icon_emoji": "✍️",
            "icon_bg_color": "bg-orange-100"
        },
        {
            "name": "Fireflies.ai",
            "category": "ljud",
            "description": "AI-antecknare som spelar in, transkriberar och sammanfattar dina möten (Zoom, Teams, Meet). Kan extrahera action items och söka genom tidigare möteshistorik.",
            "pricing": "Freemium (från 10 USD/mån)",
            "rating": 8.8,
            "gdpr_status": "GDPR-klar",
            "tags": "Möten,Transkribering,Sammanfattning",
            "icon_emoji": "🔥",
            "icon_bg_color": "bg-purple-100"
        },
        {
            "name": "Beautiful.ai",
            "category": "design",
            "description": "Skapar fantastiska presentationer på nolltid. AI designar slides automatiskt baserat på ditt innehåll och dina uppmaningar. En dröm för alla som avskyr PowerPoint.",
            "pricing": "12 USD/mån",
            "rating": 8.6,
            "gdpr_status": "Varning",
            "tags": "Presentationer,Design,Slides",
            "icon_emoji": "📊",
            "icon_bg_color": "bg-pink-100"
        }
    ]
    
    max_id = max((t.get('id', 0) for t in data if isinstance(t.get('id'), int)), default=0)
    
    added = False
    for t in new_tools:
        if t['name'] not in names:
            max_id += 1
            t['id'] = max_id
            data.append(t)
            added = True
            print(f"Added {t['name']} to JSON")
            
    if added:
        with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    update_db()
    update_json()
