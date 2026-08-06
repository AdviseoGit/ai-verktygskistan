#!/usr/bin/env python3
"""Genererar AI-stack-sidorna från stacks.json och static/tools.json.

    python3 build_stacks.py

VARNING: rollsidorna har handredigerats efter att de genererades – bland annat
med Article-schema, publicerings- och ändringsdatum för AI-citerbarhet (commit
4dc1943). Att köra det här skriptet skriver över de ändringarna. Kontrollera
med `git diff` efter körning, eller för in ändringarna i mallen nedan först.

Producerar static/ai-stackar.html (hubb) och en sida per yrkesroll. Verktygen
på varje sida hämtas från katalogens roles-fält, så en ny post i tools.json
med rätt roll dyker upp i stacken automatiskt nästa gång skriptet körs.
Kör build_sitemap.py efteråt om antalet sidor har ändrats.
"""
import html
import json

BASE = "https://aiverktygsladan.se"

GDPR_BADGE = {
    "gdpr_klar": ("bg-emerald-50 text-emerald-700 border-emerald-200", "GDPR-klar"),
    "dpa": ("bg-sky-50 text-sky-700 border-sky-200", "DPA krävs"),
    "lokal": ("bg-violet-50 text-violet-700 border-violet-200", "Kan köras lokalt"),
    "oklart": ("bg-slate-50 text-slate-600 border-slate-200", "Oklart läge"),
    "varning": ("bg-rose-50 text-rose-700 border-rose-200", "Var försiktig"),
}
SWEDISH_BADGE = {
    "bra": ("bg-blue-50 text-blue-700 border-blue-200", "Bra på svenska"),
    "delvis": ("bg-slate-50 text-slate-600 border-slate-200", "Delvis svenska"),
    "svagt": ("bg-amber-50 text-amber-700 border-amber-200", "Svagt på svenska"),
}

NAV = """    <nav class="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200/60 py-4 px-6">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <a href="/" class="text-xl font-extrabold tracking-tight">
                AI-<span class="text-indigo-600">Verktygslådan</span>
            </a>
            <div class="hidden md:flex space-x-6 items-center">
                <a href="/ai-verktyg.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Verktyg</a>
                <a href="/ai-stackar.html" class="text-sm font-medium text-indigo-600">AI-stackar</a>
                <a href="/ai-jamfor.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Jämför</a>
                <a href="/lar-dig-ai.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Lär dig AI</a>
                <a href="/ai-kalkylator.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Kalkylator</a>
            </div>
            <button id="mobile-menu-btn" class="md:hidden text-slate-600 focus:outline-none" aria-label="Meny"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg></button>
        </div>
    </nav>
    <div id="mobile-menu" class="hidden md:hidden flex-col space-y-4 py-4 px-6 bg-white border-b border-slate-200">
        <a href="/ai-verktyg.html" class="block hover:text-indigo-600 font-medium">Verktyg</a>
        <a href="/ai-stackar.html" class="block text-indigo-600 font-medium">AI-stackar</a>
        <a href="/ai-jamfor.html" class="block hover:text-indigo-600 font-medium">Jämför</a>
        <a href="/lar-dig-ai.html" class="block hover:text-indigo-600 font-medium">Lär dig AI</a>
        <a href="/ai-kalkylator.html" class="block hover:text-indigo-600 font-medium">Kalkylator</a>
    </div>
"""

FOOTER = """    <footer class="py-12 px-6 border-t border-slate-200 text-slate-500 text-sm mt-12">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
            <div>
                <div class="text-lg font-extrabold text-slate-800 mb-1">AI<span class="text-indigo-600">-Verktygslådan</span></div>
                <p class="text-xs">© 2026 Adviseo · Oberoende guide till AI för svenska företag</p>
                <p class="text-xs mt-2">Vi bedömer verktyg redaktionellt. Länkar till leverantörer kan vara affiliatelänkar och är i så fall märkta – det påverkar inte vilka verktyg vi rekommenderar.</p>
                <p class="text-xs font-semibold text-slate-600 mt-2">Denna sajt skapas och drivs helt av AI &middot; <a href="/om-sajten.html" class="underline hover:text-indigo-600">Om sajten</a></p>
            </div>
            <div class="flex gap-6 text-xs">
                <a href="/integritetspolicy.html" class="hover:text-indigo-600">Integritetspolicy</a>
                <a href="/nyhetsbrev.html" class="hover:text-indigo-600">Nyhetsbrev</a>
                <a href="/annonsera.html" class="hover:text-indigo-600">Annonsera</a>
                <a href="/om-sajten.html" class="hover:text-indigo-600">Om sajten</a>
            </div>
        </div>
    </footer>
    <script>
        document.getElementById('mobile-menu-btn').addEventListener('click', function () {
            document.getElementById('mobile-menu').classList.toggle('hidden');
        });
    </script>
"""


def head(title, description, canonical, extra_schema=""):
    return f"""<!DOCTYPE html>
<html lang="sv">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0VZV9RE3PN"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-0VZV9RE3PN');
</script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description)}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="{html.escape(title)}">
    <meta property="og:description" content="{html.escape(description)}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:locale" content="sv_SE">
    <meta name="robots" content="index, follow">
    <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
        .card-hover {{ transition: transform 0.2s ease, box-shadow 0.2s ease; }}
        .card-hover:hover {{ transform: translateY(-3px); box-shadow: 0 12px 40px rgba(99,102,241,0.12); }}
    </style>
{extra_schema}</head>
<body class="bg-slate-50 text-slate-900">
"""


def badge(cls, label):
    return (f'<span class="text-[11px] font-semibold px-2.5 py-1 rounded-full '
            f'border {cls}">{html.escape(label)}</span>')


def tool_card(tool):
    gdpr_cls, gdpr_label = GDPR_BADGE.get(tool["gdpr"], GDPR_BADGE["oklart"])
    sv_cls, sv_label = SWEDISH_BADGE.get(tool["swedish"], SWEDISH_BADGE["delvis"])
    rel = "sponsored noopener" if tool.get("affiliate") else "noopener"

    return f"""                <article class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm card-hover flex flex-col">
                    <div class="flex items-center gap-3 mb-3">
                        <span class="text-2xl" aria-hidden="true">{tool['icon_emoji']}</span>
                        <div>
                            <h3 class="font-bold text-lg">{html.escape(tool['name'])}</h3>
                            <p class="text-xs text-slate-400">{html.escape(tool['pricing'])}</p>
                        </div>
                    </div>
                    <div class="flex flex-wrap gap-1.5 mb-3">{badge(sv_cls, sv_label)}{badge(gdpr_cls, gdpr_label)}</div>
                    <p class="text-slate-500 text-sm leading-relaxed mb-4 flex-grow">{html.escape(tool['description'])}</p>
                    <p class="text-xs text-slate-400 mb-4 border-l-2 border-slate-100 pl-3">{html.escape(tool['gdpr_note'])}</p>
                    <a href="{html.escape(tool['url'])}" target="_blank" rel="{rel}" class="mt-auto text-indigo-600 text-sm font-bold hover:underline">Besök {html.escape(tool['name'])} →</a>
                </article>"""


def newsletter_block(role_slug, source):
    return f"""    <section class="bg-indigo-600 py-16 px-6 text-white">
        <div class="max-w-2xl mx-auto text-center">
            <p class="text-indigo-200 font-semibold uppercase tracking-wider text-xs mb-3">Veckans AI-verktyg</p>
            <h2 class="text-3xl font-extrabold mb-4">Ett verktyg i veckan – testat på svenska</h2>
            <p class="text-indigo-100 mb-8">Varje torsdag skickar vi ett granskat AI-verktyg med vad det kostar, hur det klarar svenska och vad GDPR-läget är. Inget annat.</p>
            <form class="newsletter-form flex flex-col sm:flex-row gap-3 max-w-md mx-auto" data-role="{role_slug}" data-source="{source}">
                <label class="sr-only" for="nl-{role_slug}">E-postadress</label>
                <input id="nl-{role_slug}" type="email" required placeholder="din@epost.se" class="flex-grow px-5 py-3.5 rounded-xl text-slate-900 outline-none focus:ring-2 focus:ring-white">
                <button type="submit" class="bg-white text-indigo-700 font-bold px-6 py-3.5 rounded-xl hover:bg-indigo-50 transition-colors whitespace-nowrap">Prenumerera</button>
            </form>
            <p class="newsletter-success hidden text-emerald-200 font-bold mt-4">✓ Tack! Du får nästa utskick på torsdag.</p>
            <p class="text-indigo-300 text-xs mt-4">Vi delar aldrig din adress. Avregistrera när du vill.</p>
        </div>
    </section>
"""


NEWSLETTER_SCRIPT = """    <script>
        document.querySelectorAll('.newsletter-form').forEach(function (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                var email = form.querySelector('input[type="email"]').value;
                fetch('/api/newsletter', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: email,
                        role: form.dataset.role || null,
                        source: form.dataset.source || null
                    })
                }).catch(function () {});
                form.classList.add('hidden');
                var ok = form.parentElement.querySelector('.newsletter-success');
                if (ok) ok.classList.remove('hidden');
                if (typeof gtag === 'function') {
                    gtag('event', 'newsletter_signup', { source: form.dataset.source });
                }
            });
        });
    </script>
"""

B2B_BLOCK = """    <section class="py-16 px-6 bg-white border-y border-slate-200" id="hjalp">
        <div class="max-w-3xl mx-auto">
            <div class="text-center mb-8">
                <h2 class="text-3xl font-extrabold mb-3">Behöver ni hjälp att komma igång?</h2>
                <p class="text-slate-600">Att välja verktyg är den enkla delen. Att få en organisation att faktiskt använda dem är den svåra. Beskriv ert läge så matchar vi er med en svensk AI-konsult som arbetat med liknande uppdrag.</p>
            </div>
            <form id="b2b-form" class="grid sm:grid-cols-2 gap-4 bg-slate-50 p-6 rounded-3xl border border-slate-200">
                <div><label class="block text-sm font-semibold mb-1" for="b2b-name">Namn</label>
                    <input id="b2b-name" required class="w-full px-4 py-3 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-indigo-500"></div>
                <div><label class="block text-sm font-semibold mb-1" for="b2b-email">E-post</label>
                    <input id="b2b-email" type="email" required class="w-full px-4 py-3 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-indigo-500"></div>
                <div><label class="block text-sm font-semibold mb-1" for="b2b-company">Företag</label>
                    <input id="b2b-company" required class="w-full px-4 py-3 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-indigo-500"></div>
                <div><label class="block text-sm font-semibold mb-1" for="b2b-employees">Antal anställda</label>
                    <select id="b2b-employees" class="w-full px-4 py-3 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-indigo-500 bg-white">
                        <option value="1-9">1–9</option><option value="10-49">10–49</option>
                        <option value="50-199">50–199</option><option value="200+">200+</option>
                    </select></div>
                <div class="sm:col-span-2"><label class="block text-sm font-semibold mb-1" for="b2b-need">Vad vill ni lösa?</label>
                    <textarea id="b2b-need" rows="3" class="w-full px-4 py-3 rounded-xl border border-slate-200 outline-none focus:ring-2 focus:ring-indigo-500"></textarea></div>
                <div class="sm:col-span-2">
                    <button type="submit" class="w-full bg-indigo-600 text-white font-bold px-8 py-4 rounded-xl hover:bg-indigo-700 transition-colors">Skicka förfrågan</button>
                    <p class="text-xs text-slate-400 mt-3">Vi förmedlar din förfrågan till en eller flera partners och kan få ersättning för det. Du binder dig inte till något.</p>
                </div>
            </form>
            <p id="b2b-success" class="hidden text-center text-emerald-600 font-bold mt-6">✓ Tack! Vi hör av oss inom ett par arbetsdagar.</p>
        </div>
    </section>
"""


def b2b_script(source):
    return """    <script>
        (function () {
            var form = document.getElementById('b2b-form');
            if (!form) return;
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                fetch('/api/lead/b2b', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: document.getElementById('b2b-name').value,
                        email: document.getElementById('b2b-email').value,
                        company: document.getElementById('b2b-company').value,
                        employees: document.getElementById('b2b-employees').value,
                        need: document.getElementById('b2b-need').value,
                        role: '%s',
                        source: '%s'
                    })
                }).catch(function () {});
                form.classList.add('hidden');
                document.getElementById('b2b-success').classList.remove('hidden');
                if (typeof gtag === 'function') gtag('event', 'b2b_lead', { source: '%s' });
            });
        })();
    </script>
""" % (source, source, source)


def partner_block(partners, role_slug):
    relevant = [p for p in partners
                if not p.get("roles") or role_slug in p.get("roles", [])]
    if not relevant:
        return ""
    cards = "".join(
        f"""                <a href="{html.escape(p['url'])}" class="block bg-white p-6 rounded-2xl border border-slate-100 card-hover">
                    <h3 class="font-bold mb-1">{html.escape(p['name'])}</h3>
                    <p class="text-sm text-slate-500">{html.escape(p.get('description', ''))}</p>
                </a>""" for p in relevant)
    return f"""    <section class="py-12 px-6 max-w-5xl mx-auto">
        <h2 class="text-2xl font-extrabold mb-6">Läs vidare</h2>
        <div class="grid sm:grid-cols-2 gap-4">
{cards}
        </div>
    </section>
"""


def faq_schema(faq):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"],
             "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faq
        ]
    }, ensure_ascii=False, indent=2)


def build_role_page(role, tools, partners):
    picks = [t for t in tools if role["role"] in t.get("roles", [])]
    picks.sort(key=lambda t: (not t["featured"], -t["rating"]))

    canonical = f"{BASE}/ai-stack-{role['slug']}.html"
    schema = (f'    <script type="application/ld+json">\n'
              f'{faq_schema(role["faq"])}\n    </script>\n')

    workflow = "".join(
        f"""                <li class="bg-white p-6 rounded-2xl border border-slate-100 flex gap-4">
                    <span class="w-8 h-8 bg-indigo-600 text-white rounded-full flex items-center justify-center font-bold text-sm shrink-0">{i}</span>
                    <div>
                        <h3 class="font-bold mb-1">{html.escape(step['step'])}</h3>
                        <p class="text-slate-500 text-sm leading-relaxed">{html.escape(step['text'])}</p>
                    </div>
                </li>""" for i, step in enumerate(role["workflow"], 1))

    faq_html = "".join(
        f"""                <details class="bg-white rounded-2xl border border-slate-100 p-6 group">
                    <summary class="font-bold cursor-pointer list-none flex justify-between items-center gap-4">
                        <span>{html.escape(item['q'])}</span>
                        <span class="text-slate-400 group-open:rotate-180 transition-transform" aria-hidden="true">▾</span>
                    </summary>
                    <p class="text-slate-600 mt-4 leading-relaxed">{html.escape(item['a'])}</p>
                </details>""" for item in role["faq"])

    others = "".join(
        f'<a href="/ai-stack-{r["slug"]}.html" class="px-4 py-2 bg-white border border-slate-200 rounded-xl text-sm font-semibold hover:border-indigo-300 transition-colors">{r["emoji"]} {html.escape(r["name"])}</a>'
        for r in ALL_ROLES if r["slug"] != role["slug"])

    return (
        head(role["title"], role["meta"], canonical, schema) + NAV +
        f"""
    <header class="py-16 px-6 max-w-4xl mx-auto text-center">
        <a href="/ai-stackar.html" class="text-sm font-semibold text-indigo-600 hover:underline">← Alla AI-stackar</a>
        <div class="text-5xl my-6" aria-hidden="true">{role['emoji']}</div>
        <h1 class="text-4xl md:text-5xl font-extrabold mb-6 tracking-tight">AI-stacken för {html.escape(role['headline'])}</h1>
        <p class="text-lg text-slate-600 leading-relaxed">{html.escape(role['intro'])}</p>
    </header>

    <section class="px-6 max-w-4xl mx-auto mb-16">
        <div class="bg-amber-50 border border-amber-200 rounded-2xl p-6">
            <h2 class="font-bold text-amber-900 mb-2">Läs det här först</h2>
            <p class="text-amber-800 text-sm leading-relaxed">{html.escape(role['warning'])}</p>
        </div>
    </section>

    <section class="px-6 max-w-4xl mx-auto mb-16">
        <h2 class="text-3xl font-extrabold mb-8">Så ser arbetsflödet ut</h2>
        <ol class="space-y-4">
{workflow}
        </ol>
    </section>

    <section class="px-6 max-w-6xl mx-auto mb-16">
        <div class="mb-8">
            <h2 class="text-3xl font-extrabold mb-3">Verktygen i stacken</h2>
            <p class="text-slate-600">{len(picks)} verktyg ur vår katalog som vi bedömer passar rollen. Varje kort visar hur det klarar svenska och vad GDPR-läget är.</p>
        </div>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
{"".join(tool_card(t) for t in picks)}
        </div>
        <div class="mt-8 text-center">
            <a href="/ai-verktyg.html" class="inline-block px-8 py-4 bg-slate-900 text-white font-bold rounded-xl hover:bg-slate-800 transition-colors">Se hela katalogen med {len(tools)} verktyg →</a>
        </div>
    </section>

{newsletter_block(role['slug'], 'stack-' + role['slug'])}
    <section class="px-6 max-w-4xl mx-auto py-16">
        <h2 class="text-3xl font-extrabold mb-8">Vanliga frågor</h2>
        <div class="space-y-4">
{faq_html}
        </div>
    </section>

{B2B_BLOCK}{partner_block(partners, role['slug'])}
    <section class="px-6 max-w-4xl mx-auto py-12 text-center">
        <h2 class="text-xl font-extrabold mb-5">Stackar för andra roller</h2>
        <div class="flex flex-wrap gap-3 justify-center">{others}</div>
    </section>

""" + FOOTER + NEWSLETTER_SCRIPT + b2b_script("stack-" + role["slug"]) +
        "</body>\n</html>\n")


def build_hub(roles, tools, partners):
    canonical = f"{BASE}/ai-stackar.html"
    title = "AI-stackar per yrkesroll 2026 – vilka AI-verktyg passar ditt jobb?"
    meta = ("Färdiga AI-stackar för mäklare, fastighetsförvaltare, HR, "
            "copywriters, ekonomi och jurister. Vilka verktyg som gäller, "
            "vad de kostar och hur de klarar svenska och GDPR.")

    cards = "".join(
        f"""            <a href="/ai-stack-{r['slug']}.html" class="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm card-hover block">
                <div class="text-4xl mb-4" aria-hidden="true">{r['emoji']}</div>
                <h2 class="text-2xl font-bold mb-3">{html.escape(r['name'])}</h2>
                <p class="text-slate-500 text-sm leading-relaxed mb-4">{html.escape(r['intro'][:170])}…</p>
                <span class="text-indigo-600 font-bold text-sm">{len([t for t in tools if r['role'] in t.get('roles', [])])} verktyg i stacken →</span>
            </a>""" for r in roles)

    return (
        head(title, meta, canonical) + NAV +
        f"""
    <header class="py-20 px-6 max-w-4xl mx-auto text-center">
        <h1 class="text-4xl md:text-6xl font-extrabold mb-6 tracking-tight">Vilka AI-verktyg passar <span class="text-indigo-600">ditt jobb</span>?</h1>
        <p class="text-xl text-slate-600 leading-relaxed">En lista med hundra AI-verktyg hjälper ingen. Det som hjälper är att veta vilka fem som är värda att lära sig i just din roll, i vilken ordning – och var GDPR sätter stopp. Här är våra stackar.</p>
    </header>

    <section class="px-6 max-w-6xl mx-auto pb-20">
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
{cards}
        </div>
    </section>

    <section class="px-6 max-w-4xl mx-auto pb-16">
        <div class="bg-white rounded-3xl border border-slate-100 p-8">
            <h2 class="text-2xl font-extrabold mb-4">Hur vi väljer verktyg till stackarna</h2>
            <p class="text-slate-600 leading-relaxed mb-4">Varje verktyg i katalogen bedöms på tre saker som spelar särskilt stor roll i Sverige: hur väl det faktiskt fungerar på svenska, vad GDPR-läget är i praktiken, och vad det kostar att komma igång. Bedömningen är redaktionell och gjord av oss – den är ingen certifiering från leverantören.</p>
            <p class="text-slate-600 leading-relaxed">Ett verktyg hamnar i en stack när vi bedömer att det löser ett återkommande problem i just den rollen. Vi rangordnar inte efter provision, och verktyg utan affiliateprogram finns med på samma villkor som de med.</p>
        </div>
    </section>

{newsletter_block('alla', 'ai-stackar')}
{B2B_BLOCK}""" + FOOTER + NEWSLETTER_SCRIPT + b2b_script("ai-stackar") +
        "</body>\n</html>\n")


ALL_ROLES = []


def main():
    global ALL_ROLES
    config = json.load(open("stacks.json", encoding="utf-8"))
    tools = json.load(open("static/tools.json", encoding="utf-8"))
    ALL_ROLES = config["roles"]
    partners = config.get("partners", [])

    for role in config["roles"]:
        path = f"static/ai-stack-{role['slug']}.html"
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_role_page(role, tools, partners))
        picks = len([t for t in tools if role["role"] in t.get("roles", [])])
        print(f"  {path} ({picks} verktyg)")

    with open("static/ai-stackar.html", "w", encoding="utf-8") as f:
        f.write(build_hub(config["roles"], tools, partners))
    print("  static/ai-stackar.html (hubb)")

    if not partners:
        print("\nOBS: partners är tom i stacks.json – partnersektionen visas inte.")
    print(f"\n✅ Byggde {len(config['roles']) + 1} sidor.")


if __name__ == "__main__":
    main()
