import json

with open('tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

new_tools = [
    {
        "id": "perplexity-ai",
        "name": "Perplexity AI",
        "category": "Sök & Research",
        "description": "En AI-driven sökmotor som ger direkta svar med källhänvisningar. Perfekt för research och faktagranskning istället för traditionell sökning.",
        "icon_emoji": "🔍",
        "url": "https://www.perplexity.ai/",
        "pricing": "Freemium ($20/mån)",
        "gdpr_status": "Oklart",
        "tags": "Sökmotor, Research, Chatbot",
        "rating": "4.8"
    },
    {
        "id": "github-copilot",
        "name": "GitHub Copilot",
        "category": "Kod & Dev",
        "description": "En AI-parprogrammerare inbyggd i din kodredigerare. Suggererar kodrader och hela funktioner i realtid baserat på din kontext.",
        "icon_emoji": "💻",
        "url": "https://github.com/features/copilot",
        "pricing": "$10/mån",
        "gdpr_status": "GDPR-klar",
        "tags": "Programmering, Kodning, Developer Tool",
        "rating": "4.9"
    }
]

# Ensure we don't duplicate
existing_ids = {t.get("id") for t in tools}

for tool in new_tools:
    if tool["id"] not in existing_ids:
        tools.append(tool)

with open('tools.json', 'w', encoding='utf-8') as f:
    json.dump(tools, f, indent=4, ensure_ascii=False)

print("Added new tools.")
