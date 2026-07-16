import sqlite3

new_tools = [
    (
        "Luma Dream Machine",
        "Ljud & Video",
        "AI-videogenerator av högsta klass som kan skapa realistiska scener och animera stillbilder med extremt hög kvalitet och hastighet.",
        "🎥",
        "bg-blue-100",
        "Freemium",
        "Oklart",
        "Video, Animation, Videogenerering",
        4.8
    ),
    (
        "Runway Gen-3",
        "Ljud & Video",
        "Nästa generations AI för videoregistrering och skapande. Möjliggör text-till-video, bild-till-video och avancerad videokontroll.",
        "🎬",
        "bg-purple-100",
        "Freemium",
        "Oklart",
        "Video, Animation, Videogenerering, Kreativt",
        4.9
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
