# SITE_VISION.md — aiverktygsladan.se

## Vision
Sveriges största och mest AKTUELLA AI-verktygskatalog och AI-nyhetskälla. När något händer inom AI ska det synas här SAMMA DAG — färskhet är vår konkurrensfördel. Katalogen växer varje dag tills den är nischens självklara go-to.

## Milstolpar
- [x] Daglig nyhetspipeline etablerad: varje pass börjar med nyhetssvep (web_search) → viktiga lanseringar publiceras/uppdateras samma pass
- [x] Katalogen växer med 1–3 kvalitetsposter per pass
- [x] gratis-ai-verktyg.html rebuilt to full on-brand design system (juni 2026)
- [x] Hela sajten håller design-nordstjärnan (sammanhållet designsystem, mobil-först) (2026-06-20)
- [x] Katalogen normaliserad till ett kanoniskt schema med validator (2026-07-25)
- [x] Directory-filter för svenskt språkstöd, GDPR-status och pris (2026-07-25)
- [x] AI-stackar per yrkesroll: 6 rollsidor + hubb (2026-07-25)
- [x] "Veckans AI-verktyg"-nyhetsbrev med segmentering på roll (2026-07-25)
- [ ] #1 på Google för "AI verktyg"

## AKUT INNEHÅLLSSKULD
- [x] Artikeln om Claude Opus 4.7 vs GPT-5.5 är UTDATERAD: Anthropic har lanserat Claude Opus 4.8 och den nya modellen Claude Fable 5. Uppdaterad.
- [x] Granska övriga artiklar/poster för gamla modellnamn och versionsnummer — utdaterat är en bugg. Uppdaterat i verktygsdatabasen.
- [x] index.html hero badge uppdaterad: "maj 2026" → "juni 2026"

## ROADMAP (nästa prioriteringar)
- [x] Bygga en "Skapa med AI" sida för att fånga utbildnings-intent inom bild/video
- [x] Konvertera "AI verktyg" och "AI program" från statiska artiklar till dynamiska katalogsidor (tools.js integration för att matcha sökintentionen)
- [x] Utöka katalogen till 35+ verktyg (särskilt inom 'juridik & HR' och 'kod & dev')
- [x] Skapa en "Jämför"-funktion för verktyg så man kan se skillnaden mellan t.ex. ChatGPT och Claude side-by-side
- [x] Fånga fler leads: en "GDPR-checklista för AI" lead magnet i PDF-format som skickas vid sign-up (klar på index, ai-jamfor)
- [x] Implementera databas-lagring för leads i main.py (och admin route för export)
- [x] Publicera en stor rapport baserad på vår AI-kalkylator (skapa länkvärdighet)
- [x] Implementera en AI Ordlista (Sökmotorer älskar definitioner)
- [x] Implementera schema.org FAQ-markup på Lär dig AI och AI-ordlistan för att synas som utvald snippet i Google.
- [x] Implementera schema.org för övriga guider (Prompt, Skapa, Jämför) och AI-kalkylator (SoftwareApplication)

## STRATEGISK INRIKTNING (juli 2026)
Positionen är inte "ännu en AI-verktygslista" utan **den svenska filtret**: av
alla verktyg som finns, vilka fungerar faktiskt på svenska och vilka får ett
svenskt bolag använda enligt GDPR. Det är den frågan besökarna har och den som
de internationella katalogerna inte besvarar.

Tre bärande delar:
1. **Katalogen som filter** – varje verktyg har svenskt språkstöd, GDPR-läge och
   prisnivå som strukturerade fält, filtrerbara i gränssnittet.
2. **AI-stackar per yrkesroll** – en katalog konverterar inte, en färdig
   uppsättning för "mäklare" gör det. Rollsidorna är också den naturliga
   ingången för internlänkning mot portföljens övriga sajter.
3. **Nyhetsbrevet som tillgång** – e-postlistan är den enda kanalen som inte kan
   tas ifrån oss av en algoritmändring. Roll fångas vid anmälan för segmentering.

### Nästa steg
- [ ] Ansöka till affiliateprogram och fylla `url` + `affiliate: true` för de
      verktyg som har program. Plumbingen finns, avtalen saknas.
- [ ] Fylla `partners` i stacks.json med portföljsajterna när domänerna är spikade.
- [ ] Sätta `ADMIN_TOKEN` i Railway så leadexporten går att använda.
- [x] Bygga faktiskt utskicksflöde för nyhetsbrevet (i dag lagras prenumeranter,
      utskicket är manuellt). [Fixade inline-formulär 2026-07-27 för att öka signups]
- [ ] Rensa de ~120 engångsskripten i repo-roten – de gör det svårt att se
      vilka skript som faktiskt används (validate_catalog, build_stacks,
      build_sitemap, seed, mailer, report_aiv).
