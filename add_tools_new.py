import sqlite3
import json

tools_to_add = [
    {
        "name": "Cursor",
        "category": "kod & dev",
        "description": "Den AI-första kodredigeraren. Byggd på VS Code, men med djupt integrerad AI (Claude 3.5 Sonnet, GPT-4o) som förstår hela din kodbas och kan skriva, refaktorera och debugga kod åt dig.",
        "pricing": "Gratis plan / $20/mån",
        "rating": 4.9,
        "gdpr_status": "Oklart",
        "tags": "Kod,Utveckling,AI,Editor",
        "icon_emoji": "⚡",
        "icon_bg_color": "bg-slate-800"
    },
    {
        "name": "GitHub Copilot",
        "category": "kod & dev",
        "description": "Din AI-parprogrammerare från GitHub och OpenAI. Autokompletterar kod i realtid, föreslår hela funktioner och hjälper till med testskrivning direkt i din IDE.",
        "pricing": "$10/mån",
        "rating": 4.7,
        "gdpr_status": "Enterprise DPA",
        "tags": "Kod,Utveckling,Copilot,IDE",
        "icon_emoji": "🐙",
        "icon_bg_color": "bg-gray-800"
    },
    {
        "name": "V0 by Vercel",
        "category": "kod & dev",
        "description": "Generativt UI-verktyg från Vercel. Beskriv hur du vill att ett gränssnitt ska se ut, och V0 genererar produktionsklar React/Tailwind-kod direkt i webbläsaren.",
        "pricing": "Gratis plan / Premium",
        "rating": 4.8,
        "gdpr_status": "Oklart",
        "tags": "UI,React,Tailwind,Design",
        "icon_emoji": "📐",
        "icon_bg_color": "bg-zinc-900"
    },
    {
        "name": "RobinAI",
        "category": "juridik & HR",
        "description": "AI-verktyg för jurister och legal teams. Hjälper till med att granska, sammanfatta och redigera juridiska kontrakt med hjälp av Anthropic's Claude-modeller.",
        "pricing": "Offert",
        "rating": 4.5,
        "gdpr_status": "GDPR-klar",
        "tags": "Juridik,Kontrakt,Granskning",
        "icon_emoji": "⚖️",
        "icon_bg_color": "bg-blue-900"
    },
    {
        "name": "Lexion",
        "category": "juridik & HR",
        "description": "AI-drivet contract management system. Automatiserar hanteringen av kontrakt, identifierar risker och gör det enkelt att söka i stora mängder avtal.",
        "pricing": "Offert",
        "rating": 4.6,
        "gdpr_status": "GDPR-klar",
        "tags": "Juridik,Avtal,HR",
        "icon_emoji": "📝",
        "icon_bg_color": "bg-indigo-800"
    },
    {
        "name": "Sana",
        "category": "juridik & HR",
        "description": "Svenskgrundad AI-plattform för kunskapshantering och lärande i företag. Hjälper anställda att hitta information, skapa kurser och lära sig snabbare. Mycket starkt fokus på enterprise-säkerhet.",
        "pricing": "Offert",
        "rating": 4.8,
        "gdpr_status": "GDPR-klar",
        "tags": "HR,Lärande,Kunskap,Enterprise",
        "icon_emoji": "🧠",
        "icon_bg_color": "bg-purple-600"
    },
    {
        "name": "Pocketlaw",
        "category": "juridik & HR",
        "description": "Svensk legal tech-plattform med AI-funktioner. Hjälper företag att hantera alla sina juridiska behov, från att skapa anställningsavtal till bolagsrätt, snabbt och säkert.",
        "pricing": "Prenumeration",
        "rating": 4.7,
        "gdpr_status": "GDPR-klar",
        "tags": "Juridik,Avtal,Svenskt",
        "icon_emoji": "💼",
        "icon_bg_color": "bg-emerald-700"
    },
    {
        "name": "Glean",
        "category": "produktivitet",
        "description": "Sökverktyg för enterprise. Ansluter till alla företagets appar (Slack, Drive, Jira etc) och använder AI för att hitta svar på anställdas frågor baserat på företagets interna data.",
        "pricing": "Offert",
        "rating": 4.8,
        "gdpr_status": "Enterprise DPA",
        "tags": "Sök,Enterprise,Produktivitet",
        "icon_emoji": "🔍",
        "icon_bg_color": "bg-rose-500"
    },
    {
        "name": "Devin",
        "category": "kod & dev",
        "description": "Världens första helt autonoma AI-mjukvaruingenjör. Kan planera och utföra komplexa kodningsprojekt, hitta och fixa buggar, och lära sig nya teknologier på egen hand.",
        "pricing": "Tidig åtkomst",
        "rating": 4.6,
        "gdpr_status": "Oklart",
        "tags": "Agent,Kod,Autonom",
        "icon_emoji": "🤖",
        "icon_bg_color": "bg-teal-700"
    },
    {
        "name": "Harvey",
        "category": "juridik & HR",
        "description": "Generativ AI speciellt byggd för professionella jurister. Hjälper till med juridisk research, due diligence, kontraktsanalys och drafting. Används av världens största byråer.",
        "pricing": "Enterprise",
        "rating": 4.7,
        "gdpr_status": "GDPR-klar",
        "tags": "Juridik,Research,Enterprise",
        "icon_emoji": "🏛️",
        "icon_bg_color": "bg-slate-700"
    }
]

def add_tools():
    conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
    cursor = conn.cursor()
    
    # Check existing tools
    cursor.execute('SELECT name FROM tools')
    existing_tools = [row[0] for row in cursor.fetchall()]
    
    added_count = 0
    for tool in tools_to_add:
        if tool['name'] not in existing_tools:
            cursor.execute('''
                INSERT INTO tools (name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tool['name'], tool['category'], tool['description'], tool['pricing'], 
                tool['rating'], tool['gdpr_status'], tool['tags'], tool['icon_emoji'], tool['icon_bg_color']
            ))
            added_count += 1
            print(f"Added {tool['name']}")
    
    conn.commit()
    conn.close()
    print(f"Total tools added: {added_count}")
    
    # Also update tools.json statically
    update_static_json()

def update_static_json():
    conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tools')
    rows = cursor.fetchall()
    
    tools = []
    for row in rows:
        tools.append(dict(row))
        
    with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'w') as f:
        json.dump(tools, f, indent=4)
        
    print("static/tools.json updated")
    conn.close()

if __name__ == "__main__":
    add_tools()
