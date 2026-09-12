#!/usr/bin/env python3
"""Injicerar den SEO-teknik som ska vara identisk på varje sida.

    python3 scripts/seo.py [--check]

Sidorna bär sin egen titel, description, canonical och sitt eget FAQ- eller
HowTo-schema. Allt *annat* som sökmotorer och svarsmotorer läser var tidigare
antingen inkonsekvent eller helt frånvarande:

* **og:image och Twitter-kort** saknades på samtliga 31 sidor, vilket gjorde
  varje delning på LinkedIn och i Slack till en tom grå ruta.
* **datePublished och dateModified** saknades helt. Det är den tyngsta enskilda
  signalen både för Googles färskhetsbedömning och för svarsmotorer som väljer
  vilken källa de citerar. Datumen hämtas ur git, så de kan inte ljuga.
* **Organization** fanns på två sidor av 31, vilket gjorde att sajten inte var
  en entitet i sökmotorernas kunskapsgraf utan bara löst kopplade dokument.
* **BreadcrumbList** och synliga brödsmulor saknades, så hierarkin syntes inte.

Skriptet äger regionerna

    <!-- @seo -->        …genereras…   <!-- /@seo -->
    <!-- @breadcrumbs --> …genereras…  <!-- /@breadcrumbs -->

och byter dessutom cdn.tailwindcss.com mot den lokalt byggda CSS-filen.
Saknas markörerna läggs de till vid första körningen.

`--check` skriver ingenting och returnerar 1 om någon sida är ur synk.
"""
import argparse
import datetime
import json
import pathlib
import re
import subprocess
import sys

STATIC = pathlib.Path("static")
DOMAIN = "https://aiverktygsladan.se"
ORG = "Adviseo"

CDN = '<script src="https://cdn.tailwindcss.com"></script>'
LOCAL_CSS = '<link rel="stylesheet" href="/static/css/site.css">'

# Brödsmulans mellannivå per sida. Sidor som saknas här hamnar direkt under Hem.
PARENT = {
    "vad-ar-ai-agenter": ("Lär dig AI-agenter", "/lar-dig-ai-agenter.html"),
    "ai-agent-ramverk": ("Lär dig AI-agenter", "/lar-dig-ai-agenter.html"),
    "bygg-ai-agent": ("Lär dig AI-agenter", "/lar-dig-ai-agenter.html"),
    "ai-agent-n8n": ("Lär dig AI-agenter", "/lar-dig-ai-agenter.html"),
    "ai-agent-mcp": ("Lär dig AI-agenter", "/lar-dig-ai-agenter.html"),
    "ai-agent-sakerhet": ("Lär dig AI-agenter", "/lar-dig-ai-agenter.html"),
    "multiagent-system": ("Lär dig AI-agenter", "/lar-dig-ai-agenter.html"),
    "ai-agent-exempel": ("Lär dig AI-agenter", "/lar-dig-ai-agenter.html"),
    "ai-agent-anvandningsfall": ("Lär dig AI-agenter", "/lar-dig-ai-agenter.html"),
    "ai-agent-ordlista": ("Lär dig AI-agenter", "/lar-dig-ai-agenter.html"),
    "ai-agent-openclaw": ("Lär dig AI-agenter", "/lar-dig-ai-agenter.html"),
    "ai-agent-microsoft-365": ("Vad passar oss?", "/ai-agent-vagval.html"),
    "ai-agent-google-workspace": ("Vad passar oss?", "/ai-agent-vagval.html"),
    "ai-agent-litet-foretag": ("Vad passar oss?", "/ai-agent-vagval.html"),
    "ai-agent-reglerad-bransch": ("Vad passar oss?", "/ai-agent-vagval.html"),
    "ai-agent-kostnad": ("Guider", "/ai-guider-foretag.html"),
    "ai-agent-gdpr": ("Guider", "/ai-guider-foretag.html"),
    "ai-arkitektur-foretag": ("Guider", "/ai-guider-foretag.html"),
    "ai-kostnader-tco": ("Guider", "/ai-guider-foretag.html"),
    "ai-sakerhet-gdpr": ("Guider", "/ai-guider-foretag.html"),
    "implementera-ai-guide": ("Guider", "/ai-guider-foretag.html"),
    "ai-kalkylator": ("Guider", "/ai-guider-foretag.html"),
}

# Sidor som är verktyg eller formella dokument, inte artiklar.
WEBPAGE_ONLY = {"index", "bygga-ai-agent-hjalp", "integritetspolicy",
                "om-sajten", "nyhetsbrev", "ai-kalkylator", "ai-agent-vagval"}

# Sidor med teknisk instruktion snarare än resonemang.
TECH = {"bygg-ai-agent", "ai-agent-mcp", "ai-agent-n8n", "ai-agent-ramverk",
        "ai-agent-sakerhet", "multiagent-system", "ai-agent-exempel"}

KNOWS_ABOUT = [
    "AI-agenter", "Agentic AI", "Model Context Protocol",
    "LangGraph", "n8n", "OpenClaw", "Microsoft Copilot Studio",
    "Retrieval-Augmented Generation", "Promptinjektion",
    "EU AI Act", "GDPR", "AI-implementation",
]


def kor_git(*args):
    try:
        ut = subprocess.run(["git", *args], capture_output=True, text=True,
                            timeout=15)
        return ut.stdout.strip() if ut.returncode == 0 else ""
    except Exception:
        return ""


def datum(path):
    """(publicerat, ändrat) ur git. Faller tillbaka på filens mtime."""
    idag = datetime.date.today().isoformat()
    skapad = kor_git("log", "--diff-filter=A", "--follow", "--format=%ad",
                     "--date=short", "--", str(path)).splitlines()
    andrad = kor_git("log", "-1", "--format=%ad", "--date=short", "--", str(path))
    smutsig = bool(kor_git("status", "--porcelain", "--", str(path)))
    if not skapad or not andrad:
        m = datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()
        return m, m
    return skapad[-1], (idag if smutsig else andrad)


def falt(html, monster):
    m = re.search(monster, html, re.S)
    return m.group(1).strip() if m else ""


def brodsmulor(namn, titel):
    steg = [("Hem", "/")]
    if namn in PARENT:
        steg.append(PARENT[namn])
    if namn != "index":
        steg.append((titel, f"/{namn}.html"))
    return steg


def graf(namn, html, publicerad, andrad):
    titel = falt(html, r"<title>(.*?)</title>").split(" | ")[0]
    beskrivning = falt(html, r'<meta name="description" content="([^"]*)"')
    url = f"{DOMAIN}/" if namn == "index" else f"{DOMAIN}/{namn}.html"
    steg = brodsmulor(namn, titel)

    org = {
        "@type": "Organization",
        "@id": f"{DOMAIN}/#organization",
        "name": ORG,
        "url": DOMAIN,
        "description": "Driver AI-Verktygslådan, en svensk kunskapsbank om att "
                       "bygga och driftsätta AI-agenter.",
        "knowsAbout": KNOWS_ABOUT,
    }
    webbplats = {
        "@type": "WebSite",
        "@id": f"{DOMAIN}/#website",
        "url": DOMAIN,
        "name": "AI-Verktygslådan",
        "description": "Sveriges mest lättillgängliga guide till att bygga och "
                       "använda AI-agenter.",
        "inLanguage": "sv-SE",
        "publisher": {"@id": f"{DOMAIN}/#organization"},
    }
    sida = {
        "@type": "WebPage",
        "@id": f"{url}#webpage",
        "url": url,
        "name": titel,
        "description": beskrivning,
        "inLanguage": "sv-SE",
        "isPartOf": {"@id": f"{DOMAIN}/#website"},
        "datePublished": publicerad,
        "dateModified": andrad,
        "breadcrumb": {"@id": f"{url}#breadcrumb"},
    }
    smula = {
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n,
             **({"item": DOMAIN + h} if i < len(steg) - 1 else {})}
            for i, (n, h) in enumerate(steg)
        ],
    }
    noder = [org, webbplats, sida, smula]

    if namn not in WEBPAGE_ONLY:
        text = re.sub(r"<[^>]+>", " ", html)
        noder.append({
            "@type": "TechArticle" if namn in TECH else "Article",
            "@id": f"{url}#article",
            "isPartOf": {"@id": f"{url}#webpage"},
            "mainEntityOfPage": {"@id": f"{url}#webpage"},
            "headline": titel,
            "description": beskrivning,
            "inLanguage": "sv-SE",
            "datePublished": publicerad,
            "dateModified": andrad,
            "wordCount": len(text.split()),
            "author": {"@id": f"{DOMAIN}/#organization"},
            "publisher": {"@id": f"{DOMAIN}/#organization"},
            "image": f"{DOMAIN}/static/og/{namn}.jpg",
        })

    return {"@context": "https://schema.org", "@graph": noder}


def seo_block(namn, html, publicerad, andrad):
    titel = falt(html, r"<title>(.*?)</title>").split(" | ")[0]
    beskrivning = falt(html, r'<meta name="description" content="([^"]*)"')
    url = f"{DOMAIN}/" if namn == "index" else f"{DOMAIN}/{namn}.html"
    bild = f"{DOMAIN}/static/og/{namn}.jpg"
    data = json.dumps(graf(namn, html, publicerad, andrad),
                      ensure_ascii=False, indent=2)
    rader = [
        f'<meta property="og:site_name" content="AI-Verktygslådan">',
        f'<meta property="og:image" content="{bild}">',
        f'<meta property="og:image:width" content="1200">',
        f'<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{titel}">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{titel}">',
        f'<meta name="twitter:description" content="{beskrivning}">',
        f'<meta name="twitter:image" content="{bild}">',
        f'<link rel="alternate" hreflang="sv-SE" href="{url}">',
        f'<link rel="alternate" hreflang="x-default" href="{url}">',
        f'<meta name="article:published_time" content="{publicerad}">',
        f'<meta name="article:modified_time" content="{andrad}">',
    ]
    meta = "\n".join("    " + r for r in rader)
    return (meta + '\n    <script type="application/ld+json">\n'
            + data + "\n    </script>")


def smul_html(namn, html):
    if namn == "index":
        return ""
    titel = falt(html, r"<title>(.*?)</title>").split(" | ")[0]
    steg = brodsmulor(namn, titel)
    delar = []
    for i, (n, h) in enumerate(steg):
        if i < len(steg) - 1:
            delar.append(f'<a href="{h}" class="hover:text-indigo-600 transition-colors">{n}</a>')
            delar.append('<span class="text-slate-300" aria-hidden="true">/</span>')
        else:
            delar.append(f'<span class="text-slate-700">{n}</span>')
    return ('    <nav aria-label="Brödsmulor" class="max-w-7xl mx-auto px-6 pt-6 '
            'text-sm text-slate-500 flex flex-wrap gap-2 items-center">\n        '
            + "\n        ".join(delar) + "\n    </nav>")


def ersatt(html, namn, kropp):
    """Ersätter mellan markörer, eller lägger till dem på rätt ställe."""
    monster = re.compile(rf"[ \t]*<!-- @{namn} -->.*?<!-- /@{namn} -->", re.S)
    ny = f"    <!-- @{namn} -->\n{kropp}\n    <!-- /@{namn} -->" if kropp else \
         f"    <!-- @{namn} -->\n    <!-- /@{namn} -->"
    if monster.search(html):
        return monster.sub(lambda _: ny, html, count=1)
    if namn == "seo":
        return html.replace("</head>", ny + "\n</head>", 1)
    # Brödsmulorna hamnar direkt efter navigationen.
    if "<!-- /@nav -->" in html:
        return html.replace("<!-- /@nav -->", "<!-- /@nav -->\n" + ny, 1)
    return html


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="Skriv inget, returnera 1 om någon sida är ur synk.")
    args = ap.parse_args()

    andrade, osynk = [], []
    for sida in sorted(STATIC.glob("*.html")):
        namn = sida.stem
        original = sida.read_text(encoding="utf-8")
        html = original.replace(CDN, LOCAL_CSS)
        publicerad, andrad = datum(sida)
        html = ersatt(html, "seo", seo_block(namn, html, publicerad, andrad))
        html = ersatt(html, "breadcrumbs", smul_html(namn, html))

        if html != original:
            if args.check:
                osynk.append(sida.name)
            else:
                sida.write_text(html, encoding="utf-8")
                andrade.append(sida.name)

    if args.check:
        if osynk:
            print(f"❌ {len(osynk)} sidor saknar aktuell SEO-injektion:")
            for n in osynk:
                print(f"   - {n}")
            print("\nKör: python3 scripts/seo.py")
            return 1
        print(f"✅ SEO-blocket är aktuellt på alla "
              f"{len(list(STATIC.glob('*.html')))} sidor.")
        return 0

    print(f"✅ SEO injicerat på {len(andrade)} sidor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
