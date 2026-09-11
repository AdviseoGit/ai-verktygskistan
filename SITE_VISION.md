# SITE_VISION.md — aiverktygsladan.se

## Vision
Sveriges mest lättillgängliga och hjälpsamma källa för den som ska **implementera
och använda AI-agenter**. Inte en katalog till. Målet är att en svensk
beslutsfattare eller utvecklare ska kunna gå från "vi borde göra något med
agenter" till en agent i produktion med hjälp av den här sajten — och få veta
när svaret är att *inte* bygga en agent.

## Positionen
Det finns för många ramverk, för många val och för lite kunskap på svenska.
Marknaden är full av jämförelser som listar tjugo alternativ och överlåter
beslutet till läsaren. Vår position är den motsatta:

> **Vi minskar antalet val.** Varje sida ska sluta i ett svar, inte i en lista.

Tre bärande principer:
1. **Ta ställning.** Ett beslutsträd som ger ett ramverk slår en tabell med tio.
   Tabellen finns kvar, men som underlag för svaret — inte i stället för det.
2. **Var ärlig om när man ska avstå.** Sidan som säger "bygg inte agent här" är
   den som gör att någon återvänder. Den finns nästan ingen annanstans, eftersom
   de flesta som skriver om agenter säljer agenter.
3. **Skriv för svenska förhållanden.** GDPR, AI-akten, vad som går att driva
   inom EU, och vad saker kostar i praktiken. Det är det internationella
   innehållet inte skrivet för.

## Varför pivoten (september 2026)
Katalogpositionen mättes i sex månader och gav **0 klick** över fyra
mätperioder i rad, trots stigande snittposition. Slutsatsen var inte att
metoden skulle köras hårdare utan att positionen var fel: en svensk
verktygskatalog konkurrerar med internationella sajter på en fråga besökaren
redan löst med en sökmotor.

Agent-implementation är en smalare fråga med sämre svar på marknaden, högre
kommersiellt värde per besökare, och den matchar vad avsändaren faktiskt kan
leverera. Hela katalogdelen (24 sidor, `tools.json`, stack-generatorn) togs
bort och 301:ades in i agent-spåret.

## Sajtens struktur
| Spår | Sida | Roll |
|---|---|---|
| Förstå | `vad-ar-ai-agenter.html` | Pelarsida: definition, autonominivåer, när man ska avstå |
| Välj | `ai-agent-ramverk.html` | Beslutsträd + ramverksjämförelse + MCP |
| Bygg | `bygg-ai-agent.html` | Sju steg med kodexempel och de vanligaste felen |
| Tillämpa | `ai-agent-anvandningsfall.html` | Tolv fall som når produktion, fyra fällor |
| Slå upp | `ai-agent-ordlista.html` | 30 begrepp, FAQ-schema |
| Konvertera | `bygga-ai-agent-hjalp.html` | Neutralt formulär för implementationsförfrågan |
| Stöd | De fyra guiderna + kalkylator + rapport | Besluten runt omkring bygget |

## Milstolpar
- [x] Pivot till AI-agenter genomförd, katalogen retirerad med 301 (2026-09-11)
- [x] Fem nya kärnsidor med FAQ- och HowTo-schema (2026-09-11)
- [x] Konverteringsvägen samlad på en mätbar sida med källspårning (2026-09-11)
- [ ] Första indexerade klicket på en agent-term
- [ ] Topp 10 på "ai agent" eller "bygga ai agent" på svenska
- [ ] 10 kvalificerade implementationsförfrågningar

## Roadmap
- [ ] **Mät innan mer byggs.** Begär indexering av de fem nya sidorna i GSC och
      låt dem ligga i minst tre pass innan strukturen rörs igen. Pivoten är
      hypotesen som testas — bygg inte en ny ovanpå den.
- [ ] Djupsida per ramverk (`ai-agent-n8n.html`, `ai-agent-langgraph.html`) när
      huvudsidan visar vilka termer som faktiskt får visningar.
- [ ] En riktig genomgång av MCP på svenska — termen växer snabbt och har
      nästan inget svenskt innehåll.
- [ ] Kodexemplen i ett publikt repo som sidorna länkar till (länkvärde).
- [ ] Instrumentera GA4-events: `agent_lead` finns på hjälpsidan, men
      scrolldjup och klick från CTA-blocken saknas fortfarande.
- [ ] Sätt `ADMIN_TOKEN` i Railway så leadexporten går att använda.

## Gäller inte längre
Allt som rör verktygskatalogen: `tools.json`, katalogvalidatorn,
stack-generatorn, rollsidorna per yrke och featured listings. Återuppliva det
inte. Om ett verktyg ska nämnas hör det hemma inne i en agent-sida, som
underlag för ett val — inte som en post i en databas.
