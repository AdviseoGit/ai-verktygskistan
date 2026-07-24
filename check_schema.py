import sqlite3

conn = sqlite3.connect('/data/workspace/projects/ai-verktygskistan/tools.db')
c = conn.cursor()
c.execute("PRAGMA table_info(tools);")
for row in c.fetchall():
    print(row)
