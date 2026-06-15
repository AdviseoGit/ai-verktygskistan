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

### 5c. Modeller att bevaka (juni 2026)
| Leverantör | Aktuell flagship | Senaste uppdatering |
|-----------|-----------------|---------------------|
| OpenAI    | GPT-5.5         | April 23, 2026      |
| Anthropic | Claude Fable 5 / Opus 4.8 | Juni 2026  |
| Google    | Gemini 3.1 Ultra| Maj 2026            |
| Microsoft | Copilot (GPT-5.5)| April 2026         |
| Meta      | Llama 4         | April 2026          |

### 5d. Söktermer att använda vid verifiering
- "[Modelnamn] latest model [innevarande år]"
- "[Leverantör] new model release [innevarande månad och år]"
- "what is the current [GPT/Claude/Gemini] model [innevarande år]"

## 6. Teknisk Info
- Railway-deploy: Automatisk deploy vid push till main branch.
- tools.json styr verktygslistan på webbplatsen – ändringar syns direkt efter deploy.
- index.html innehåller hårdkodade modellnamn i hero-sektionen och jämförelsetabellen – dessa måste uppdateras manuellt vid stora modellsläpp.
