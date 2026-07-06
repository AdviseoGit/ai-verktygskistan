import sqlite3
import json

tools_to_add = [
    {
        "name": "Gemini 3.1 Pro",
        "category": "text",
        "description": "Googles mest avancerade multimodala AI-modell. Exceptionell på att förstå och kombinera text, bild, ljud och video i samma prompt. Perfekt för djup research och dataanalys.",
        "pricing": "Gratis / $20/mån (Advanced)",
        "rating": 4.8,
        "gdpr_status": "Enterprise DPA tillgänglig",
        "tags": "Google,Multimodal,Text,Kod,Bild",
        "icon_emoji": "✨",
        "icon_bg_color": "bg-blue-600"
    },
    {
        "name": "Sora",
        "category": "video",
        "description": "OpenAIs banbrytande text-till-video-modell. Genererar upp till 60 sekunder långa, fotorealistiska videor med hög visuell kvalitet och konsekvens baserat på textbeskrivningar.",
        "pricing": "Pris på förfrågan / Enterprise",
        "rating": 4.9,
        "gdpr_status": "Oklart",
        "tags": "Video,OpenAI,Generativ",
        "icon_emoji": "🎥",
        "icon_bg_color": "bg-purple-600"
    },
    {
        "name": "Claude Sonnet 4.5",
        "category": "text",
        "description": "Anthropics extremt snabba och kapabla modell. Perfekt balans mellan hastighet och intelligens. Utmärkt för kodning, textgenerering och analys av långa dokument.",
        "pricing": "Gratis / $20/mån",
        "rating": 4.8,
        "gdpr_status": "B2B DPA",
        "tags": "Anthropic,Kod,Text",
        "icon_emoji": "🧠",
        "icon_bg_color": "bg-orange-500"
    },
    {
        "name": "Krea AI",
        "category": "bild",
        "description": "Realtidsgenerering av bilder och fantastisk bilduppskalning (upscaling). Du ritar en enkel skiss och AI:n renderar en fotorealistisk bild i realtid. Ett måste för designers.",
        "pricing": "Gratis / $30/mån",
        "rating": 4.7,
        "gdpr_status": "Oklart",
        "tags": "Bild,Design,Real-time",
        "icon_emoji": "🎨",
        "icon_bg_color": "bg-pink-600"
    }
]

def main():
    conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
    cursor = conn.cursor()
    
    for tool in tools_to_add:
        cursor.execute(
            "INSERT INTO tools (name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (tool["name"], tool["category"], tool["description"], tool["pricing"], tool["rating"], tool["gdpr_status"], tool["tags"], tool["icon_emoji"], tool["icon_bg_color"])
        )
    
    conn.commit()
    print(f"Lade till {len(tools_to_add)} verktyg.")
    
    # Export to JSON
    conn.row_factory = sqlite3.Row
    data = [dict(row) for row in conn.execute('SELECT * FROM tools').fetchall()]
    with open('/data/workspace/projects/ai-verktygskistan/tools.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Exporterade tools.json")

    conn.close()

if __name__ == '__main__':
    main()
