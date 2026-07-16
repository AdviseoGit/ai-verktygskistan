import sqlite3

new_tools = [
    (
        "Cursor",
        "Kod & Dev",
        "En AI-first kodredigerare byggd på VS Code. Ger dig kontextmedveten kodgenerering och kan refaktorera hela filer baserat på ditt repo.",
        "⚡",
        "bg-slate-100",
        "Freemium ($20/mån)",
        "Oklart",
        "Programmering, Kodning, Developer Tool",
        4.9
    ),
    (
        "Suno AI",
        "Ljud & Video",
        "Skapa fullständiga låtar med sång och musik på sekunder utifrån textprompter. Perfekt för marknadsföring eller prototyper.",
        "🎵",
        "bg-purple-100",
        "Freemium",
        "Oklart",
        "Musik, Audio, Musikgenerering",
        4.8
    )
]

conn = sqlite3.connect("/data/workspace/projects/ai-verktygskistan/tools.db")
cur = conn.cursor()

for t in new_tools:
    try:
        cur.execute("SELECT id FROM tools WHERE name = ?", (t[0],))
        if cur.fetchone() is None:
            cur.execute("""
                INSERT INTO tools (name, category, description, icon_emoji, icon_bg_color, pricing, gdpr_status, tags, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, t)
            print(f"Added {t[0]}")
        else:
            print(f"Tool {t[0]} already exists.")
    except Exception as e:
        print(f"Error adding {t[0]}: {e}")

conn.commit()
print("Total tools:", cur.execute("SELECT count(*) FROM tools").fetchone()[0])
conn.close()
