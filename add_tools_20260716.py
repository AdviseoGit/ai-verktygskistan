import sqlite3

new_tools = [
    (
        "Perplexity AI",
        "Sök & Research",
        "En AI-driven sökmotor som ger direkta svar med källhänvisningar. Perfekt för research och faktagranskning istället för traditionell sökning.",
        "🔍",
        "bg-blue-100",
        "Freemium ($20/mån)",
        "Oklart",
        "Sökmotor, Research, Chatbot",
        4.8
    ),
    (
        "GitHub Copilot",
        "Kod & Dev",
        "En AI-parprogrammerare inbyggd i din kodredigerare. Föreslår kodrader och hela funktioner i realtid baserat på din kontext.",
        "💻",
        "bg-slate-100",
        "$10/mån",
        "GDPR-klar",
        "Programmering, Kodning, Developer Tool",
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
        else:
            print(f"Tool {t[0]} already exists.")
    except Exception as e:
        print(f"Error adding {t[0]}: {e}")

conn.commit()
print("Total tools:", cur.execute("SELECT count(*) FROM tools").fetchone()[0])
conn.close()
