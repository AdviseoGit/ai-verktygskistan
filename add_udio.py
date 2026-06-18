import json

with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# data is a list
exists = any(t['name'] == 'Udio' for t in data)

if not exists:
    new_id = max((t.get('id', 0) for t in data if isinstance(t.get('id'), int)), default=0) + 1
    new_tool = {
        "id": new_id,
        "name": "Udio",
        "category": "ljud",
        "description": "Revolutionerande AI-musikgenerator som skapar högkvalitativa låtar med sång och instrument från textbeskrivningar. Ett fantastiskt gratisalternativ för kreativt ljudskapande.",
        "pricing": "Freemium (gratis för 10 låtar/dag)",
        "rating": 8.8,
        "gdpr_status": "Varning",
        "tags": "Musik,Sång,Gratis",
        "icon_emoji": "🎵",
        "icon_bg_color": "bg-yellow-100"
    }
    data.append(new_tool)
    with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Added Udio to tools.json")
else:
    print("Udio already exists in tools.json")
