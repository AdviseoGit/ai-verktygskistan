import json
import sqlite3

# Load json
with open('tools.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Clear json duplicates based on name
seen = set()
new_data = []
for tool in data:
    if tool['name'] not in seen:
        seen.add(tool['name'])
        new_data.append(tool)

with open('tools.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)

# Rebuild DB from json to ensure consistency
conn = sqlite3.connect('tools.db')
c = conn.cursor()

c.execute('DELETE FROM tools')

for i, tool in enumerate(new_data):
    # Ensure all required fields exist
    tags_str = json.dumps(tool.get('tags', []))
    c.execute('''
        INSERT INTO tools (id, name, category, description, pricing, tags, icon_emoji, icon_bg_color, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        i + 1,
        tool.get('name'), 
        tool.get('category'), 
        tool.get('description'),
        tool.get('pricing', 'Freemium'), 
        tags_str,
        tool.get('icon_emoji', '🔧'), 
        tool.get('icon_bg_color', 'bg-slate-100'), 
        tool.get('rating', 4.5)
    ))

conn.commit()
conn.close()

print(f"Rebuilt DB with {len(new_data)} tools.")
