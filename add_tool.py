
import sqlite3

def add_new_tool():
    try:
        conn = sqlite3.connect('tools.db')
        cursor = conn.cursor()

        new_tool = (
            "Suno AI",
            "musik",
            "Suno AI är en banbrytande AI-tjänst som kan skapa realistisk musik, kompletta med sång och instrument, baserat på en enkel textprompt. Användare kan specificera genre, stil och text för att generera unika låtar på sekunder.",
            "Freemium",
            4.7,
            "Oklart",
            "musikgenerering, AI-låtar, text-till-musik",
            "🎵",
            "#FFD700"  # Gold
        )

        cursor.execute("""
            INSERT INTO tools (name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, new_tool)

        conn.commit()
        print("Successfully added 'Suno AI' to the database.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_new_tool()
