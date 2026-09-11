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
    "index": (1.0, "weekly"),
    "vad-ar-ai-agenter": (0.9, "monthly"),
    "ai-agent-ramverk": (0.9, "weekly"),
    "bygg-ai-agent": (0.9, "monthly"),
    "ai-agent-anvandningsfall": (0.9, "monthly"),
    "ai-agent-ordlista": (0.8, "monthly"),
    "bygga-ai-agent-hjalp": (0.8, "monthly"),
    "ai-guider-foretag": (0.7, "monthly"),
    "ai-arkitektur-foretag": (0.7, "monthly"),
    "ai-kostnader-tco": (0.7, "monthly"),
    "ai-sakerhet-gdpr": (0.7, "monthly"),
    "implementera-ai-guide": (0.7, "monthly"),
    "ai-kalkylator": (0.7, "monthly"),
    "ai-svenska-foretag-rapport": (0.6, "monthly"),
    "nyhetsbrev": (0.5, "monthly"),
    "om-sajten": (0.4, "yearly"),
    "integritetspolicy": (0.3, "yearly"),
}
DEFAULT = (0.7, "monthly")


def rank(page):
    return PRIORITY.get(page, DEFAULT)


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
