import sqlite3
import json

conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
cursor = conn.cursor()
cursor.execute('SELECT id, name, tags FROM tools')

updated = 0
for row in cursor.fetchall():
    tool_id = row[0]
    tags_str = row[2]
    
    if tags_str:
        try:
            json.loads(tags_str)
        except Exception:
            # It's a comma-separated string, convert it to JSON array
            tags_list = [t.strip() for t in tags_str.split(',') if t.strip()]
            new_tags_json = json.dumps(tags_list, ensure_ascii=False)
            cursor.execute('UPDATE tools SET tags = ? WHERE id = ?', (new_tags_json, tool_id))
            updated += 1

conn.commit()

# Update tools.json
cursor.execute('SELECT * FROM tools ORDER BY name ASC')
columns = [column[0] for column in cursor.description]
tools = []
for row in cursor.fetchall():
    tool = dict(zip(columns, row))
    tool['tags'] = json.loads(tool['tags']) if tool['tags'] else []
    tools.append(tool)
    
with open('/data/workspace/projects/ai-verktygskistan/static/tools.json', 'w', encoding='utf-8') as f:
    json.dump(tools, f, ensure_ascii=False, indent=2)

print(f"Fixed {updated} tools with invalid JSON tags. Wrote static JSON.")
