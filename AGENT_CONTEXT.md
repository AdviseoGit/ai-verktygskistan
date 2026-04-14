# AI-Verktygskistan – Agent Context

## Project identity
- **Name:** AI-Verktygskistan
- **URL (target):** ai-verktygskistan.se
- **Brand parent:** Adviseo
- **Created:** 2026-04-09
- **Stack:** FastAPI + static HTML (Tailwind CDN) — same pattern as proptech-guide-se

## Mission
Swedish-language AI tools directory and compliance portal. Information arbitrage: bridge the gap between English-only AI resources and Swedish business users who need GDPR/AI Act guidance.

## Primary SEO target
- **Keyword:** gpt 4 (Vol 2400 SE)
- **Cluster:** gpt-4 svenska, gpt 4 pris, chatgpt gdpr, ai verktyg företag, ai act sverige

## Content pillars
1. **Tool directory** – 40+ AI tools, each with GDPR status, price in SEK, use case
2. **GDPR guide** – IMY-focused checklist for using AI legally in Sweden
3. **EU AI Act explainer** – 4 risk levels, what applies to Swedish SME
4. **Pricing calculator** – total cost for soloföretagare / SME / enterprise

## Information arbitrage angles
- Most AI GDPR content is in English → Swedish translation of key concepts
- Confusing regulation → clear checklist format
- USD pricing → converted to SEK with context
- Generic AI hype → "what's actually legal here"

## Deployment
- Same Railway/Fly.io pattern as other Adviseo projects
- PORT env var for dynamic port binding
- Static files served from /static

## Next features (backlog)
- [ ] Tool comparison wizard (2-3 tools side by side)
- [ ] GDPR self-assessment quiz → email lead capture
- [ ] Weekly newsletter ("AI i Sverige den här veckan")
- [ ] Swedish-specific tools section (Visma, Fortnox AI, etc.)
- [ ] Sitemap.xml generation
