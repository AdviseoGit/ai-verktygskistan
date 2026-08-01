#!/usr/bin/env python3
"""Genererar static/sitemap.xml från de HTML-sidor som faktiskt finns.

Kör efter att sidor lagts till eller tagits bort:

    python3 build_sitemap.py

Sitemapen har historiskt underhållits för hand med ett tiotal engångsskript,
vilket ledde till att den både pekade på borttagna sidor och vid ett tillfälle
skrevs till noll bytes. Genom att alltid generera den från filsystemet kan den
varken bli tom eller innehålla döda länkar.
"""
import datetime
import os
import xml.etree.ElementTree as ET

BASE = "https://aiverktygsladan.se"
STATIC = "static"

# Sidor som inte hör hemma i sitemapen (tack-sidor, dubbletter osv).
EXCLUDE = set()

# Prioritet och uppdateringsfrekvens per sida. Sidor som saknas här får
# standardvärdena längst ned.
PRIORITY = {
    "index": (1.0, "daily"),
    "ai-verktyg": (0.9, "daily"),
    "ai-stackar": (0.9, "weekly"),
    "gratis-ai-verktyg": (0.9, "weekly"),
    "hitta-ratt-ai": (0.8, "weekly"),
    "ai-jamfor": (0.8, "weekly"),
    "ai-kalkylator": (0.9, "monthly"),
    "ai-program": (0.9, "weekly"),
    "lar-dig-ai": (0.9, "monthly"),
    "bygg-med-ai": (0.9, "monthly"),
    "skapa-med-ai": (0.9, "monthly"),
    "prompt-guide": (0.8, "monthly"),
    "ai-ordlista": (0.8, "monthly"),
    "claude-fable-5-vs-gpt-5.5": (0.9, "weekly"),
    "ai-svenska-foretag-rapport": (0.8, "monthly"),
    "ai-for-hr": (0.8, "monthly"),
    "vad-ar-ai-verktyg": (0.7, "monthly"),
    "nyhetsbrev": (0.7, "monthly"),
    "annonsera": (0.6, "monthly"),
    "om-sajten": (0.4, "yearly"),
    "integritetspolicy": (0.3, "yearly"),
}
DEFAULT = (0.7, "monthly")

# Sidor som genereras av build_stacks.py delar prioritet via prefix.
PREFIX_PRIORITY = {"ai-stack-": (0.9, "weekly")}


def rank(page):
    if page in PRIORITY:
        return PRIORITY[page]
    for prefix, value in PREFIX_PRIORITY.items():
        if page.startswith(prefix):
            return value
    return DEFAULT


def build():
    today = datetime.date.today().isoformat()
    pages = sorted(
        f[:-5] for f in os.listdir(STATIC)
        if f.endswith(".html") and f[:-5] not in EXCLUDE
    )

    urlset = ET.Element("urlset",
                        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # Startsidan först och som "/" snarare än "/index.html".
    ordered = ["index"] + [p for p in pages if p != "index"]

    for page in ordered:
        if page not in pages:
            continue
        priority, changefreq = rank(page)
        url = ET.SubElement(urlset, "url")
        loc = f"{BASE}/" if page == "index" else f"{BASE}/{page}.html"
        ET.SubElement(url, "loc").text = loc
        ET.SubElement(url, "lastmod").text = today
        ET.SubElement(url, "changefreq").text = changefreq
        ET.SubElement(url, "priority").text = f"{priority:.1f}"

    ET.indent(urlset, space="  ")
    xml = ET.tostring(urlset, encoding="unicode")
    output = f'<?xml version="1.0" encoding="UTF-8"?>\n{xml}\n'

    path = os.path.join(STATIC, "sitemap.xml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"✅ Skrev {path} med {len(ordered)} sidor (lastmod {today}).")


if __name__ == "__main__":
    build()
