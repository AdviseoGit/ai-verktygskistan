import json

with open('tools.json', 'r', encoding='utf-8') as f:
    tools = json.load(f)

# Update Perplexity pricing/description if needed to be perfectly aligned with vision
for tool in tools:
    if tool['id'] == 'perplexity-ai':
        tool['pricing'] = 'Freemium ($20/mån)'
        tool['gdpr_status'] = 'Oklar'

with open('tools.json', 'w', encoding='utf-8') as f:
    json.dump(tools, f, indent=4, ensure_ascii=False)
