# Maintenance Log

## 2026-04-14
- Verified existing structured data (Schema.org JSON-LD and FAQPage schema) in `static/index.html` and `static/schema.json`.
- Added `static/llms.txt` to provide clean, structured markdown for AI scrapers (Claude, ChatGPT, Perplexity) to improve Generative Engine indexing (RAG).
- Pushed changes to `main`.


## 2026-04-17
- Added Privacy Policy (Integritetspolicy) at `/static/privacy.html` to ensure AdSense Readiness.
- Implemented GDPR-compliant Cookie Banner in `index.html` with accept/decline functionality.
- Updated footer links to point to the new privacy policy and cookie settings.
- Verified generative engine readiness (Markdown & Schema).
-e 
## 2026-04-17 (Weekly Friday Maintenance)
- Cleaned up duplicate cookie banners in `index.html`.
- Corrected links from `/static/privacy.html` to `/static/integritetspolicy.html`.
- Expanded `integritetspolicy.html` with comprehensive AdSense requirements (third-party vendors, Google AdSense opt-outs).
- Ensured schema.json and llms.txt remain highly optimized for Generative Engine Indexing (GEI).
- Committed and pushed to origin main.

## 2026-04-17 (Database Upgrade)
- Transitioned AI-verktygskistan from a static SEO page to a real dynamic directory.
- Built an SQLite database and SQLAlchemy models (`database.py`, `models.py`).
- Seeded the database with 9 verified AI tools (GPT-4, Claude, Copilot, etc.).
- Added `/api/tools` endpoint to `main.py`.
- Implemented frontend `tools.js` to dynamically fetch and render database entries, effectively replacing hardcoded HTML.
- Fulfills the roadmap goal of "Directory and educational hub. Build real database entries, not just SEO landing pages."


## 2026-09-11 — Pivot till AI-agenter
Sajten smalnades av från verktygskatalog till AI-agent-implementation efter
0 klick över fyra mätperioder. 24 sidor borttagna och 301:ade via `REDIRECTS`
i main.py; katalogmaskineriet (tools.json, tools.js, stacks.json,
validate_catalog.py, build_stacks.py, add_tool.py, seed.py, /api/tools) borttaget.
Fem nya kärnsidor plus en konverteringssida tillagda. `check_site.py` fick
`check_redirects()` så att en omdirigering inte tyst kan börja peka på en 404.
Affärsmodellstexterna på om-sajten och nyhetsbrev stämde inte längre med
verkligheten (påstod affiliate och annonser) och är omskrivna.

## 2026-09-11 — Klustret utbyggt till 25 sidor
Åtta nya sidor med kursen `lar-dig-ai-agenter.html` som ryggrad. Nav och sidfot
omstrukturerade, sitemap-prioriteter och llms.txt uppdaterade. `check_site.py`
fick en spärr mot dubblettnycklar i REDIRECTS — literal_eval sväljer dem tyst
och låter sista raden vinna, vilket hittades genom att själv råka införa en.

## 2026-09-11 — Situationsspår (30 sidor)
Fem sidor som svarar utifrån företagets eget läge i stället för generellt:
vägvalsguide (interaktiv, räknas i webbläsaren, inget sparas) plus profilsidor
för Microsoft 365, Google Workspace, små bolag och reglerad verksamhet.
Fakta om Microsofts och Googles agentplattformar verifierade mot källor från
2026 och listade på sidorna — produktnamnen har bytts flera gånger och blir
snabbt inaktuella, kontrollera vid varje större uppdatering.
Vägvalsguidens JS skrevs först utan å/ä/ö; rättat. Notera att optionsvärdena
(`lasa`, `kansligt` m.fl.) medvetet är ASCII eftersom de jämförs mot
HTML-attribut — rätta aldrig dem.

## 2026-09-11 — OpenClaw (31 sidor)
OpenClaw saknades helt trots att det är ett av de snabbast växande öppna
projekten någonsin (350 000+ GitHub-stjärnor, släppt sent 2025). Orsaken var
att aktualitetsregeln i AGENT_CONTEXT bara täckte modellversioner, inte
produkter. Regeln är utvidgad — se avsnitt 5.0.
Sidan tar ställning: bra som personligt verktyg, villkorat som intern
operationsbot, nej som produktionsagent i verksamheten. Säkerhetsavsnittet
bygger på publicerade CVE:er och exponeringsmätningar från 2026 med källor.
Siffrorna är ögonblicksbilder från början av 2026 och 2.0 kom i augusti —
det står i texten, men kontrollera vid uppdatering.
