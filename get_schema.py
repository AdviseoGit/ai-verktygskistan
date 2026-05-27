
import sqlite3

try:
    conn = sqlite3.connect('tools.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(tools);")
    columns = cursor.fetchall()
    if columns:
        print("Columns in the 'tools' table:")
        for column in columns:
            print(f"- {column[1]} ({column[2]})")
    else:
        print("No columns found for the 'tools' table.")
except sqlite3.Error as e:
    print(f"Database error: {e}")
finally:
    if conn:
        conn.close()
