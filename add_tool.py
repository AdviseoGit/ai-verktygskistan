import sqlite3
import argparse

def add_new_tool(name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color):
    try:
        conn = sqlite3.connect('tools.db')
        cursor = conn.cursor()

        new_tool = (
            name,
            category,
            description,
            pricing,
            rating,
            gdpr_status,
            tags,
            icon_emoji,
            icon_bg_color
        )

        cursor.execute("""
            INSERT INTO tools (name, category, description, pricing, rating, gdpr_status, tags, icon_emoji, icon_bg_color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, new_tool)

        conn.commit()
        print(f"Successfully added '{name}' to the database.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a new tool to the AI Verktygskistan database.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--pricing", required=True)
    parser.add_argument("--rating", type=float, required=True)
    parser.add_argument("--gdpr_status", required=True)
    parser.add_argument("--tags", required=True)
    parser.add_argument("--icon_emoji", required=True)
    parser.add_argument("--icon_bg_color", required=True)
    
    args = parser.parse_args()
    
    add_new_tool(
        args.name,
        args.category,
        args.description,
        args.pricing,
        args.rating,
        args.gdpr_status,
        args.tags,
        args.icon_emoji,
        args.icon_bg_color
    )
