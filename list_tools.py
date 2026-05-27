
import sqlite3

try:
    conn = sqlite3.connect('tools.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, category FROM tools;")
    tools = cursor.fetchall()
    if tools:
        print("Existing tools and categories:")
        for tool in tools:
            print(f"- {tool[0]} ({tool[1]})")
    else:
        print("No tools found in the database.")
except sqlite3.Error as e:
    print(f"Database error: {e}")
finally:
    if conn:
        conn.close()
