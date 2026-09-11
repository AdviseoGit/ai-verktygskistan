# Agent Mission: AI-Verktygslådan — AI-agenter

## 1. Mål (Goal)
- Vara Sveriges mest lättillgängliga källa för den som ska implementera och
  använda AI-agenter.
- Omvandla den trafiken till kvalificerade implementationsförfrågningar.

**Sajten pivoterade i september 2026** från verktygskatalog till AI-agenter.
Läs `SITE_VISION.md` innan du gör något strukturellt — särskilt avsnittet
"Gäller inte längre". Katalogen ska inte återuppstå.

## 2. Mätbara KPI:er
- Första klicket på en agent-relaterad sökterm (baslinjen är 0).
- Topp 10 på svenska agent-termer ("ai agent", "bygga ai agent", "ai agent
  ramverk") inom sex månader.
- 10 kvalificerade förfrågningar via `/bygga-ai-agent-hjalp.html`.

## 3. Strategi & Taktik
- **Innehåll:** djup före bredd. En sida som faktiskt besvarar en fråga slår
  fem som nuddar den. Varje ny sida ska sluta i ett svar, inte i en lista.
- **Ta ställning.** Rekommendera ett alternativ och motivera. Jämförelser utan
  rekommendation är det marknaden redan har för mycket av.
- **Var ärlig om när man ska avstå.** Avsnitten om när man *inte* ska bygga en
  agent är en tillgång, inte en brist. De är också det enda i innehållet som
  konkurrenterna inte kopierar.
- **SEO/GEO:** FAQ- och HowTo-schema på allt, hårda siffror med källa, svenska
  termer. Sidorna ska gå att citera av en språkmodell utan omskrivning.
- **Rapportering:** `SCOREBOARD.md` skrivs av scoreboard.py och är passens enda
  minne av vad siffrorna gjorde. Ändra den aldrig för hand.

## 4. Gränser & Ramverk
- Bedömningar ska vara ärliga. Nackdelar väger lika tungt som fördelar, och
  rekommendationen "bygg inte det här" ska ges när den är riktig.
- Konverteringsvägen är neutralt formulerad och behovsdriven. Inga
  säljargument i det redaktionella innehållet.
- Ändra inte den visuella profilen utan manuellt godkännande.
- Påstå aldrig siffror utan källa. De statistikuppgifter som används i dag
  (Gartners 40 %, 89 % av piloter, MCP-adoption) har källor listade på
  `/ai-agent-ramverk.html` — utöka den listan när nya siffror tillkommer.

## 5. Aktualitet – KRITISK REGEL

### 5.0 Regeln gäller inte bara modeller
Den här regeln skrevs för modellversioner. Den missade därför OpenClaw helt:
ett projekt som släpptes i slutet av 2025, passerade 350 000 GitHub-stjärnor
och blev den mest omskrivna agentprodukten – utan att nämnas på sajten, för att
ingen letade efter *produkter*, bara efter modellnamn.

**Sök därför varje pass även efter nya agentprodukter och ramverk**, inte bara
nya modellversioner. Sökfrågor som fungerar: "new AI agent framework [månad
år]", "fastest growing open source AI agent", "AI agent launch [år]". En
produkt som saknas på sajten är en lucka; en produkt som beskrivs inaktuellt är
en bugg.

Gäller särskilt: plattformsnamn byts ofta (Azure AI Foundry → Microsoft
Foundry, Agentspace → Gemini Enterprise Agent Platform). Kontrollera dem vid
varje större uppdatering av `ai-agent-microsoft-365.html`,
`ai-agent-google-workspace.html` och `ai-agent-ramverk.html`.

## 5a. Modellaktualitet
AI-modeller uppdateras ofta. Gammal modellinformation skadar credibiliteten.

### 5b. Verifiera ALLTID aktuell modell innan publicering
Innan du nämner en specifik modellversion på en sida – särskilt i kodexemplet
på `bygg-ai-agent.html` eller i ramverkstabellen på `ai-agent-ramverk.html`:

1. **Sök på leverantörens officiella sida**:
   - OpenAI: https://openai.com/blog och https://platform.openai.com/docs/models
   - Anthropic: https://www.anthropic.com/news och https://docs.anthropic.com/en/docs/models-overview
   - Google: https://blog.google/technology/ai/ och https://ai.google.dev/gemini-api/docs/models/gemini
   - Microsoft: https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/
   - GitHub Copilot: https://docs.github.com/en/copilot/about-github-copilot/github-copilot-features

2. **Kontrollera att modellen fortfarande är default/flagship** – inte superseded av nyare version.

3. **Uppdatera sidan** om du hittar en nyare version, och notera det i
   `MAINTENANCE_LOG.md`.

### 5c. Checklist vid modelluppdatering
- [ ] Vilken modell är nuvarande default på webbplatsen (inte bara API)?
- [ ] Har pricing förändrats?
- [ ] Finns ny GDPR/DPA-information?
- [ ] Uppdatera varje sida där modellnamnet nämns (`grep -rn` i `static/`).
- [ ] Uppdatera "Uppdaterad [månad] [år]"-märket i berörda sidors hero.

### 5d. Modeller att bevaka (verifierat 25 juli 2026)
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

### 5e. Söktermer att använda vid verifiering
- "[Modelnamn] latest model [innevarande år]"
- "[Leverantör] new model release [innevarande månad och år]"
- "what is the current [GPT/Claude/Gemini] model [innevarande år]"

## 6. Teknisk Info
- Railway-deploy: Automatisk deploy vid push till main branch.
- **Katalogen är borttagen.** `static/tools.json`, `static/js/tools.js`,
  `stacks.json`, `validate_catalog.py`, `build_stacks.py`, `add_tool.py` och
  `seed.py` togs bort vid pivoten i september 2026 tillsammans med de 24 sidor
  som läste dem. Skapa dem inte igen.
- **De borttagna sidorna lever som 301.** `REDIRECTS` i `main.py` pekar varje
  gammal URL till sin närmaste efterföljare. `check_site.py` kontrollerar att
  målen finns, så en omdirigering kan inte tyst börja peka på en 404. Lägg till
  en rad där när en sida tas bort — ta aldrig bort en rad.
- Sidorna nämner modellnamn sparsamt och medvetet: innehållet är byggt kring
  mönster som håller över modellgenerationer, inte kring vilken modell som är
  bäst i veckan. Kodexemplet på `bygg-ai-agent.html` anger dock en modell och
  måste hållas aktuellt enligt regel 5 ovan.

### 6a. Bygga sajten – ETT kommando

```bash
make check    # kontrollera utan att skriva något (samma som CI kör)
make build    # bygg allt från källorna och kontrollera
make serve    # kör lokalt på http://127.0.0.1:8000
```

**Kör `make check` innan du pushar.** Den fångar det som annars upptäcks först
i produktion: brutna länkar, saknad canonical, dubblerade titlar, tom sitemap,
ogiltig JSON, obalanserad markup och sidor som hamnat ur synk med mallarna.

#### Nav och sidfot ligger i templates/, inte i sidorna

`templates/nav.html` och `templates/footer.html` är enda källan. Sidorna har
markörer som `scripts/build_site.py` fyller på:

```html
<!-- @nav -->   …genereras…   <!-- /@nav -->
<!-- @footer --> …genereras… <!-- /@footer -->
```

**Redigera aldrig innehållet mellan markörerna** – det skrivs över vid nästa
bygge. Ändra i `templates/` och kör `make build`.

Bakgrunden: varje sida bar tidigare sin egen kopia. Med 27 sidor blev det 27
ställen att ändra, och resultatet var fyra olika navigationer, nio olika
sidfötter och överblivna `</div>` i menyn på 14 av 27 sidor.

### 6b. Databasen – läs detta innan du rör datalagret

Appen läser **`DATABASE_URL`** från miljön. Sätts den inte faller den tillbaka
på en lokal SQLite-fil, vilket är fint lokalt men **förstör data i produktion**.

Bakgrunden: `database.py` hårdkodade tidigare `sqlite:///./tools.db`, en relativ
sökväg på containerdisken. Railway-tjänsten har ingen volym monterad och
redeployar dagligen via driver-cronen, så databasfilen återskapades tom ungefär
var 24:e timme. Alla leads, nyhetsbrevsprenumeranter och kalkylatorsvar
försvann, utan att något syntes i loggarna – exporterna returnerade bara en tom
lista. Det som räddade leadflödet var att `_deliver_aiv` mejlar ägaren vid varje
inskick; kalkylatordatan hade ingen sådan kopia och gick förlorad helt.

**Två uppsättningar duger i produktion:** `sqlite:////data/tools.db` på en
monterad Railway-volym, eller `postgresql://…` mot en hostad instans. Postgres
ger automatiska säkerhetskopior, volymen gör det inte – väg in det.

Det som *inte* duger är en relativ sökväg (`sqlite:///./tools.db`), som hamnar
på containerdisken. Startloggen varnar då. Dyker varningen upp i Railway-loggen
skriver tjänsten till en disk som snart raderas.

Skriv aldrig verksamhetsdata till filsystemet. `capture_calc_data` gjorde det
via `data_moat_calc.csv`; den filen är borta och datan går till tabellen
`calc_data`.

Tabellerna skapas av `Base.metadata.create_all` vid uppstart. Det hanterar
**nya tabeller men inte ändringar i befintliga** – lägger ni till en kolumn i en
tabell som redan finns i produktion måste den läggas till manuellt eller med
Alembic.

### 6c. Skript i scripts/ – hela listan
Roten innehöll tidigare ~100 engångsskript (`add_tools_20260719k.py`,
`update_nav_lar_v4.py` och liknande), många med hårdkodade sökvägar till
`/data/workspace`. De är borttagna. **Skapa inte nya engångsskript i roten** –
ändra filerna direkt eller lägg till en flagga i ett befintligt byggskript.

Aktiva filer, och inget annat:

| Fil | Roll |
|-----|------|
| `main.py` | FastAPI-appen: routing, lead- och nyhetsbrevs-API |
| `models.py` / `database.py` | SQLAlchemy-modeller och session |
| `mailer.py` / `scripts/report_aiv.py` | E-postutskick och PDF-generering |
| `scripts/build_site.py` | Injicerar nav och sidfot från templates/ |
| `scripts/check_site.py` | Kontrollerar länkar, canonical, sitemap, markup, omdirigeringar |
| `scripts/build_sitemap.py` | Genererar sitemapen från static/*.html |

`/api/tools` och `scripts/seed.py` är borttagna tillsammans med katalogen.
Tabellen `tools` finns kvar i `models.py` men används inte av något – lämna den
eller migrera bort den, men lita inte på den som datakälla.

### 6d. Obligatoriskt före commit

```bash
make build
```

`make check` körs av CI och fångar det som annars upptäcks först i produktion:
brutna interna länkar, saknad canonical, dubblerade titlar, tom sitemap, ogiltig
JSON-LD, obalanserad markup, sidor ur synk med `templates/`, och omdirigeringar
som pekar på sidor som inte finns.

Sidor med description över 160 tecken ger en varning, inte ett fel – men kapas i
sökresultatet, så åtgärda den.

### 6e. Att lägga till en ny sida

1. Skriv sidan i `static/` med `<!-- @nav --><!-- /@nav -->` och
   `<!-- @footer --><!-- /@footer -->` som tomma markörer – `build_site.py`
   fyller dem.
2. Sätt `<title>`, `meta description` (högst 160 tecken) och `canonical`
   (`https://aiverktygsladan.se/<filnamn>.html`). Titlar måste vara unika.
3. Lägg till FAQ- eller HowTo-schema om sidan besvarar frågor.
4. Länka in sidan från minst en befintlig sida – annars är den föräldralös.
5. Sätt prioritet i `PRIORITY` i `scripts/build_sitemap.py`.
6. Kör `make build`.

## 7. Monetarisering – implementerat
Sajten har en konverteringsväg, inte flera:

- **Implementationsförfrågningar:** `/bygga-ai-agent-hjalp.html` postar till
  `POST /api/lead/b2b` → tabellen `b2b_leads`. CTA-blocken på innehållssidorna
  länkar dit med `?fran=<sida>`, vilket sparas som
  `source="agent_hjalp:<sida>"`. Det är så vi ser vilken sida som faktiskt
  konverterar – ändra inte det formatet utan att uppdatera rapporteringen.
- **Nyhetsbrev:** `POST /api/newsletter` → `newsletter_subscribers`.
- **Export:** `/api/admin/leads`, `/api/admin/newsletter`,
  `/api/admin/b2b-leads` kräver headern `X-Admin-Token` som matchar
  miljövariabeln `ADMIN_TOKEN`. Saknas variabeln svarar de 404. Sätt den i
  Railway innan export används – endpointsen lämnar ut personuppgifter.

Annonsförsäljning och affiliate-märkning i katalogen är borttaget tillsammans
med katalogen. Det redaktionella innehållet är inte till salu.
