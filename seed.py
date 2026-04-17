from database import engine, SessionLocal, Base
from models import Tool

Base.metadata.create_all(bind=engine)

tools_data = [
    {
        "name": "ChatGPT Teams",
        "category": "text",
        "description": "OpenAIs GPT-4o med DPA inkluderat. Bästa valet för SME som vill ha GPT-4 med juridisk trygghet. Data tränar inte modellen.",
        "pricing": "25 USD / mån / user",
        "rating": 9.2,
        "gdpr_status": "GDPR-klar",
        "tags": "GPT-4o,Teamfunktioner,Plugins",
        "icon_emoji": "🤖",
        "icon_bg_color": "bg-indigo-100"
    },
    {
        "name": "Claude (Anthropic)",
        "category": "text",
        "description": "Stark på analys, långa dokument och juridisk text. Claude Sonnet 4.6 via AWS Bedrock EU-region – fullt GDPR-kompatibelt för enterprise.",
        "pricing": "20 USD / mån",
        "rating": 8.8,
        "gdpr_status": "GDPR-klar",
        "tags": "200K context,Dokument,AWS EU",
        "icon_emoji": "✦",
        "icon_bg_color": "bg-orange-100"
    },
    {
        "name": "Microsoft Copilot 365",
        "category": "affar",
        "description": "GPT-4o inbyggt i Word, Excel, Teams och Outlook. Perfekt om du redan betalar för M365. Datalagring i EU-region. GDPR via Microsofts DPA.",
        "pricing": "30 USD / mån / user",
        "rating": 9.0,
        "gdpr_status": "EU-data",
        "tags": "M365-integration,Teams,Excel AI",
        "icon_emoji": "🪟",
        "icon_bg_color": "bg-blue-100"
    },
    {
        "name": "Jasper AI",
        "category": "text",
        "description": "Specialiserat innehållsverktyg för marknadsföring. Mönster och templates för annonser, bloggar och e-post. DPA krävs separat – rekommenderas ej för känslig data.",
        "pricing": "49 USD / mån",
        "rating": 7.4,
        "gdpr_status": "Begränsad DPA",
        "tags": "Marketing,Templates,Brand voice",
        "icon_emoji": "✍️",
        "icon_bg_color": "bg-violet-100"
    },
    {
        "name": "GitHub Copilot",
        "category": "kod",
        "description": "AI-kodassistent inbyggd i VS Code och JetBrains. GPT-4o och Claude-modeller. Enterprise-plan med GDPR-avtal och datalagring utan träning.",
        "pricing": "10–19 USD / mån",
        "rating": 9.3,
        "gdpr_status": "GDPR-klar",
        "tags": "VS Code,Autocomplete,Chat",
        "icon_emoji": "💻",
        "icon_bg_color": "bg-gray-100"
    },
    {
        "name": "Midjourney",
        "category": "bild",
        "description": "Marknadsledande bildgenerering. Kraftfull men saknar DPA – undvik att inkludera klientdata i prompts. Bra för marknadsföringsmaterial utan personuppgifter.",
        "pricing": "10–60 USD / mån",
        "rating": 8.2,
        "gdpr_status": "Begränsad DPA",
        "tags": "Bildgenerering,Discord,Varumärke",
        "icon_emoji": "🎨",
        "icon_bg_color": "bg-pink-100"
    },
    {
        "name": "Visma Compact AI",
        "category": "juridik",
        "description": "AI-funktioner i Vismas redovisningsprogram – specifikt byggt för svenska SME. Datalagring i Sverige. Bokföring, fakturor och lönehantering med AI-stöd.",
        "pricing": "399 kr / mån",
        "rating": 8.5,
        "gdpr_status": "GDPR-klar",
        "tags": "Bokföring,Fakturaläsning,SV-data",
        "icon_emoji": "⚖️",
        "icon_bg_color": "bg-teal-100"
    },
    {
        "name": "HubSpot AI",
        "category": "affar",
        "description": "CRM med inbyggd AI för försäljning och marknadsföring. AI-mejl, lead-scoring och konversationsanalys. Serverhosting i EU. Gratis-plan tillgänglig.",
        "pricing": "0–800 USD / mån",
        "rating": 8.6,
        "gdpr_status": "GDPR-klar",
        "tags": "CRM,E-post,Lead scoring",
        "icon_emoji": "📊",
        "icon_bg_color": "bg-amber-100"
    },
    {
        "name": "Avtal24 AI",
        "category": "juridik",
        "description": "Svenskt juridikverktyg med AI-granskning av avtal. Baserat på svensk rätt. Genomgår standardavtal, NDA:er och hyreskontrakt – på svenska.",
        "pricing": "490 kr / mån",
        "rating": 8.1,
        "gdpr_status": "SE-baserat",
        "tags": "Avtalsanalys,NDA,Svensk rätt",
        "icon_emoji": "📋",
        "icon_bg_color": "bg-red-100"
    }
]

def seed_db():
    db = SessionLocal()
    # clear existing
    db.query(Tool).delete()
    for t in tools_data:
        tool = Tool(**t)
        db.add(tool)
    db.commit()
    db.close()
    print("Database seeded with {} tools.".format(len(tools_data)))

if __name__ == "__main__":
    seed_db()
