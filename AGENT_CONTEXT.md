# Agent Mission: AI-verktygslådan Growth

## 1. Mål (Goal)
- Etablera AI-verktygslådan som en go-to resurs för svenska användare som vill hitta och jämföra AI-verktyg.
- Driva organisk trafik och generera affiliatintäkter.

## 2. Mätbara KPI:er (Key Performance Indicators)
- Nå topp 5 på Google för minst 20 olika söktermer relaterade till specifika AI-verktyg (t.ex. "bästa ai bildgenerator", "chatgpt alternativ") inom 6 månader.
- Öka organisk trafik med 25% per månad.
- Generera 100 affiliate-klick per vecka.

## 3. Strategi & Taktik (Execution)
- **Content:** Varje torsdag, lägg till och recensera 3-5 nya, relevanta AI-verktyg. Uppdatera befintliga recensioner om verktygen har fått stora uppdateringar.
- **SEO:** Fokusera på "long-tail"-sökord och recensions-schema (structured data) för att få rika resultat i Google.
- **Monetization:** Identifiera och implementera nya affiliate-program. A/B-testa placering och utformning av affiliate-länkar för att maximera klickfrekvens (CTR).
- **Rapportering:** Varje fredag, sammanställ en rapport med veckans åtgärder, trafik- och klickdata.

## 4. Gränser & Ramverk (Boundaries)
- Alla recensioner måste vara ärliga och transparenta. Nackdelar med ett verktyg ska belysas lika väl som fördelar.
- Markera tydligt ut affiliatelänkar.
- Ändra inte den visuella profilen utan manuellt godkännande.

## 5. Modellaktualitet – KRITISK REGEL
AI-modeller uppdateras ofta. Gammal modellinformation skadar credibiliteten.

### 5a. Verifiera ALLTID aktuell modell innan publicering
Innan du nämner en specifik modellversion (t.ex. "GPT-4o", "Claude 3.5") i tools.json, index.html eller artiklar:

1. **Sök på leverantörens officiella sida**:
   - OpenAI: https://openai.com/blog och https://platform.openai.com/docs/models
   - Anthropic: https://www.anthropic.com/news och https://docs.anthropic.com/en/docs/models-overview
   - Google: https://blog.google/technology/ai/ och https://ai.google.dev/gemini-api/docs/models/gemini
   - Microsoft: https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/
   - GitHub Copilot: https://docs.github.com/en/copilot/about-github-copilot/github-copilot-features

2. **Kontrollera att modellen fortfarande är default/flagship** – inte superseded av nyare version.

3. **Uppdatera tools.json** om du hittar en nyare version. Ändra description, tags och rating vid behov.

### 5b. Checklist vid modelluppdatering
- [ ] Vilken modell är nuvarande default på webbplatsen (inte bara API)?
- [ ] Har pricing förändrats?
- [ ] Finns ny GDPR/DPA-information?
- [ ] Är betyget (rating) fortfarande rimligt jämfört med konkurrenter?
- [ ] Uppdatera **både** tools.json OCH index.html om modellnamnet nämns där.
- [ ] Uppdatera "Uppdaterad [månad] [år]"-märket i index.html hero-sektionen.

### 5c. Modeller att bevaka (verifierat 25 juli 2026)
| Leverantör | Aktuell flagship | Senaste uppdatering |
|-----------|-----------------|---------------------|
| OpenAI    | GPT-5.6 (Luna / Terra / Sol) | 9 juli 2026 – GA efter gated preview 26 juni |
| Anthropic | Claude Fable 5 (mest kapabel), Claude Opus 5 | 24 juli 2026 – Opus 5 ersätter Opus 4.8, halva priset |
| Google    | Gemini 3.1 Pro, Gemini 3.6 Flash | 21 juli 2026 – 3.6 Flash, 3.5 Flash-Lite, 3.5 Flash Cyber |
| Microsoft | Copilot (GPT-5.6)| Juli 2026          |
| Meta      | Llama 4 (Scout / Maverick / Behemoth) | April 2026 |
| Midjourney| V8.1            | Standard sedan 10 juni 2026 |
| Runway    | Gen-4.5         | 2026                |
| Kling     | Kling 3.0       | 2026                |

### 5d. Söktermer att använda vid verifiering
- "[Modelnamn] latest model [innevarande år]"
- "[Leverantör] new model release [innevarande månad och år]"
- "what is the current [GPT/Claude/Gemini] model [innevarande år]"

## 6. Teknisk Info
- Railway-deploy: Automatisk deploy vid push till main branch.
- **`static/tools.json` är enda källan för katalogen.** Den läses av tools.js,
  ai-jamfor.html, hitta-ratt-ai.html och build_stacks.py. Roten hade tidigare en
  andra `tools.json` som låg ur synk – den är borttagen, skapa den inte igen.
- index.html innehåller hårdkodade modellnamn i hero-sektionen och
  jämförelsetabellen – dessa måste uppdateras manuellt vid stora modellsläpp.

### 6a. Skript i repo-roten – hela listan
Roten innehöll tidigare ~100 engångsskript (`add_tools_20260719k.py`,
`update_nav_lar_v4.py` och liknande), många med hårdkodade sökvägar till
`/data/workspace`. De är borttagna. **Skapa inte nya engångsskript i roten** –
ändra filerna direkt eller lägg till en flagga i ett befintligt byggskript.

Aktiva filer, och inget annat:

| Fil | Roll |
|-----|------|
| `main.py` | FastAPI-appen: routing, lead- och nyhetsbrevs-API |
| `models.py` / `database.py` | SQLAlchemy-modeller och session |
| `mailer.py` / `report_aiv.py` | E-postutskick och PDF-generering |
| `add_tool.py` | Lägg till ett verktyg i katalogen enligt schemat |
| `validate_catalog.py` | Spärr mot att katalogschemat spretar |
| `build_stacks.py` | Genererar rollsidorna från stacks.json |
| `build_sitemap.py` | Genererar sitemapen från static/*.html |
| `seed.py` | Seedar SQLite-tabellen `tools` – se varningen nedan |

**Varning om seed.py och /api/tools:** tabellen `tools` och endpointen
`/api/tools` läses inte av någon sida. Frontend hämtar `static/tools.json`.
Innehållet i `seed.py` är dessutom utdaterat (nämner GPT-4o). Antingen ta bort
tabellen, endpointen och seed.py, eller koppla dem till katalogen – men lita
inte på dem som datakälla i nuläget.

### 6b. Obligatoriskt efter ändring i katalogen
Kör alltid dessa tre i ordning innan commit:

```bash
python3 validate_catalog.py   # schemat måste hålla, annars kraschar renderingen
python3 build_stacks.py       # rollsidorna hämtar sina verktyg ur katalogen
python3 build_sitemap.py      # sitemapen genereras från static/*.html
```

`validate_catalog.py` finns av en anledning: i juli 2026 hade katalogen 23
kategorivarianter, 16 GDPR-statussträngar och två betygsskalor samtidigt, och
`tools.js` kraschade tyst på poster där `tags` var en lista i stället för en
sträng. Effekten var att hela verktygsgriden var borta från index.html,
ai-verktyg.html och ai-program.html – utan att något syntes i loggarna.
Redigera aldrig katalogen utan att köra validatorn.

### 6c. Kanoniskt schema för ett verktyg
Kategorier: `text, bild, video, ljud, kod, affar, marknadsforing, juridik,
produktivitet, sok`. GDPR: `gdpr_klar, dpa, lokal, oklart, varning`.
Svenska: `bra, delvis, svagt`. Pris: `gratis, freemium, betald`.
Roller: `maklare, fastighetsforvaltare, hr, copywriter, ekonomi, juridik`.
Betyg alltid på skalan 0–5. Alla poster måste ha `url` (https).

`affiliate: true` sätter `rel="sponsored"` på länken och ska bara användas när
länken faktiskt är kommersiell. `featured: true` ger märkningen
"Redaktionens val" – den är redaktionell, inte såld. Sponsrade placeringar ska
märkas som sponsrade, inte som redaktionens val.

## 7. Monetarisering – implementerat
- **Affiliate:** `url` + `affiliate`-flagga per verktyg. Ingen post är i dag
  markerad som affiliate; lägg in riktiga affiliatelänkar i `url` och sätt
  flaggan när programmen är på plats.
- **Featured listings:** säljs via `/annonsera.html`, renderas via `featured`.
- **Nyhetsbrev:** `POST /api/newsletter` (e-post, roll, källa) →
  tabellen `newsletter_subscribers`. Rollen används för segmenterade utskick.
- **B2B-leads:** `POST /api/lead/b2b` → tabellen `b2b_leads`. Annonsörer landar
  i samma tabell med `source="annonsera"`.
- **Export:** `/api/admin/leads`, `/api/admin/newsletter`, `/api/admin/b2b-leads`
  kräver headern `X-Admin-Token` som matchar miljövariabeln `ADMIN_TOKEN`.
  Saknas variabeln svarar de 404. Sätt `ADMIN_TOKEN` i Railway innan export
  används – endpointsen lämnar ut personuppgifter.
