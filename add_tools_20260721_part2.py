import json

with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'r') as f:
    tools = json.load(f)

new_tools2 = [
    {
        "id": "clay",
        "name": "Clay",
        "description": "AI-driven databerikning och prospektering för säljteam. Skrapar data, slår upp kontakter i 50+ databaser och använder AI för att skriva hyper-personliga kalla mail i stor skala.",
        "category": "Marknadsföring",
        "price": "Freemium / Från $149/mån",
        "url": "https://www.clay.com/",
        "tags": ["sälj", "B2B", "kalla-mail", "prospektering", "CRM", "automation", "AI-agent"],
        "rating": 4.8,
        "isGDPRCompliant": True,
        "gdprNote": "Clay har DPA och inbyggda funktioner för att exkludera specifika länder och följa regionala dataregleringar."
    },
    {
        "id": "guidde",
        "name": "Guidde",
        "description": "AI-plattform för att skapa how-to-videor och dokumentation på sekunder. Spela in en process i webbläsaren, och AI genererar röst, text och visuella markeringar automatiskt.",
        "category": "Produktivitet",
        "price": "Freemium / Från $16/användare/mån",
        "url": "https://www.guidde.com/",
        "tags": ["dokumentation", "how-to", "video", "team", "onboarding", "chrome-extension"],
        "rating": 4.9,
        "isGDPRCompliant": True,
        "gdprNote": "SOC 2 Type II-certifierade och GDPR-kompatibla. Erbjuder DPA."
    },
    {
        "id": "11labs-reader",
        "name": "ElevenLabs Reader App",
        "description": "ElevenLabs officiella app för iOS/Android. Förvandlar artiklar, PDF:er, e-böcker eller e-post till högkvalitativa ljudböcker med världens bästa AI-röster.",
        "category": "Ljud",
        "price": "Gratis",
        "url": "https://elevenlabs.io/text-to-speech",
        "tags": ["ljudbok", "text-till-tal", "app", "konsument", "tillgänglighet"],
        "rating": 4.7,
        "isGDPRCompliant": True,
        "gdprNote": "Följer ElevenLabs standard för dataskydd. Konsumentinriktad, läser lokala filer och webblänkar."
    },
    {
        "id": "pika-art",
        "name": "Pika",
        "description": "Innovativ plattform för AI-genererad video. Pika låter dig skapa eller redigera videor genom enkla textprompts. Har funktioner för Lip Sync och kan modifiera specifika regioner i en video.",
        "category": "Video",
        "price": "Freemium / Från $8/mån",
        "url": "https://pika.art/",
        "tags": ["video", "text-till-video", "lip-sync", "bild-till-video", "generativ-AI", "kreativt"],
        "rating": 4.6,
        "isGDPRCompliant": False,
        "gdprNote": "Konsumentinriktad AI utan uttalad Enterprise-fokus på GDPR-compliance eller DPA. Använd ej för känslig persondata."
    },
    {
        "id": "perplexity-pro",
        "name": "Perplexity Pro",
        "description": "Premiumversionen av den populära AI-sökmotorn. Ger tillgång till GPT-4o, Claude 3 Opus och Sonnet 3.5, obegränsade sökningar och möjlighet att analysera uppladdade filer.",
        "category": "Text & Skrivande",
        "price": "$20/mån",
        "url": "https://www.perplexity.ai/pro",
        "tags": ["sökmotor", "research", "Fler-modell", "GPT-4o", "Claude-3.5", "dokumentanalys"],
        "rating": 4.9,
        "isGDPRCompliant": True,
        "gdprNote": "Perplexity Enterprise Pro är SOC2-certifierade och GDPR-kompatibla. De tränar inte modeller på Pro/Enterprise-användares data."
    }
]

tools.extend(new_tools2)

with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'w') as f:
    json.dump(tools, f, indent=4, ensure_ascii=False)
with open('/data/workspace/projects/ai-verktygskistan/tools.json', 'w') as f:
    json.dump(tools, f, indent=4, ensure_ascii=False)

import sqlite3
try:
    conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM tools")
    max_id_row = cursor.fetchone()
    max_id = max_id_row[0] if max_id_row[0] is not None else 0
    
    for tool in new_tools2:
        max_id += 1
        gdpr_status = "green" if tool["isGDPRCompliant"] else "red"
        tags_str = ", ".join(tool["tags"])
        cursor.execute('''
            INSERT INTO tools (id, name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            max_id,
            tool["name"],
            tool["category"],
            tool["description"],
            tool["price"],
            tool["rating"],
            gdpr_status,
            tags_str,
            "🚀",
            "bg-blue-100 text-blue-600"
        ))
    conn.commit()
    conn.close()
except Exception as e:
    print(f"DB Error: {e}")

print(f"Lade till {len(new_tools2)} nya verktyg. Total: {len(tools)}")
