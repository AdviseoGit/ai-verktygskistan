import json
import sqlite3

def main():
    conn = sqlite3.connect("tools.db")
    c = conn.cursor()
    
    # Let's inspect the database
    c.execute("SELECT id, name FROM tools")
    tools = c.fetchall()
    print(f"Total tools in db: {len(tools)}")
    
    # See what exists around ID 50-70
    c.execute("SELECT id, name FROM tools WHERE id > 45 ORDER BY id")
    print("Recent tools:", c.fetchall())

if __name__ == "__main__":
    main()
