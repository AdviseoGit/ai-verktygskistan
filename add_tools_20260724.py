import sqlite3
import json
import uuid

new_tools = [
    {
        "name": "Opus Clip",
        "description": "AI-verktyg som automatiskt klipper långa videos (YouTube, podcasts) till korta, virala format för TikTok, Shorts och Reels. Lägger till captions, emojis och b-roll helt automatiskt.",
        "category": "video",
        "pricing": "Freemium (från $19/mån)",
        "rating": 4.8,
        "gdpr_status": "Oklart / US",
        "icon_emoji": "✂️",
        "icon_bg_color": "bg-purple-100",
        "tags": "Video, Sociala Medier, Marknadsföring"
    },
    {
        "name": "Guidde",
        "description": "Skapa steg-för-steg videogudier och dokumentation blixtsnabbt med AI. Spela in din skärm, så genererar Guidde en professionell röst och text-instruktioner. Perfekt för onboarding och support.",
        "category": "produktivitet",
        "pricing": "Freemium (från $16/mån)",
        "rating": 4.6,
        "gdpr_status": "SOC2, DPA finns",
        "icon_emoji": "📚",
        "icon_bg_color": "bg-blue-100",
        "tags": "Produktivitet, Utbildning, Support"
    },
    {
        "name": "Framer AI",
        "description": "Bygg snabba, moderna hemsidor genom att skriva en prompt. Framer AI designar layouten, skriver texten och väljer färger på sekunder. Fantastiskt verktyg för snabba landningssidor och marknadsföring.",
        "category": "kod",
        "pricing": "Freemium (från $15/mån)",
        "rating": 4.7,
        "gdpr_status": "Godkänd med DPA",
        "icon_emoji": "🎨",
        "icon_bg_color": "bg-pink-100",
        "tags": "Webbdesign, Kod, Marknadsföring"
    }
]

def add_tools_db():
    conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
    c = conn.cursor()
    
    added_count = 0
    for tool in new_tools:
        # Check if exists
        c.execute("SELECT id FROM tools WHERE name = ?", (tool['name'],))
        if c.fetchone() is None:
            c.execute("""
                INSERT INTO tools (name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (tool['name'], tool['category'], tool['description'], tool['pricing'], tool['rating'], tool['gdpr_status'], tool['tags'], tool['icon_emoji'], tool['icon_bg_color']))
            added_count += 1
            print(f"Added {tool['name']}")
    
    conn.commit()
    conn.close()
    return added_count

def update_json_from_db():
    conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM tools ORDER BY id DESC")
    rows = c.fetchall()
    
    tools = []
    for row in rows:
        tags = [t.strip() for t in row['tags'].split(',')] if row['tags'] else []
        tools.append({
            "id": row['id'],
            "name": row['name'],
            "description": row['description'],
            "category": row['category'],
            "pricing": row['pricing'],
            "rating": row['rating'],
            "gdpr_status": row['gdpr_status'],
            "icon_emoji": row['icon_emoji'],
            "icon_bg_color": row['icon_bg_color'],
            "tags": tags
        })
    
    with open('/data/workspace/projects/ai-verktygskistan/tools.json', 'w', encoding='utf-8') as f:
        json.dump(tools, f, indent=4, ensure_ascii=False)
    conn.close()

if __name__ == "__main__":
    added = add_tools_db()
    if added > 0:
        update_json_from_db()
        print(f"Success: Added {added} tools and updated tools.json")
    else:
        print("No new tools added (maybe they exist).")
