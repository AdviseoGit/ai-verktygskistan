#!/usr/bin/env python3
"""Lägger till ett verktyg i static/tools.json enligt det kanoniska schemat.

    python3 add_tool.py \\
        --name "Verktygsnamn" \\
        --category text \\
        --description "Vad det gör och vad det inte gör." \\
        --pricing "Freemium (från 20 USD/mån)" \\
        --price-tier freemium \\
        --rating 4.5 \\
        --gdpr dpa \\
        --gdpr-note "DPA finns för betalplaner, data behandlas i USA." \\
        --swedish bra \\
        --swedish-note "Skriver god svenska." \\
        --url https://exempel.se/ \\
        --tags Text Automation \\
        --roles hr ekonomi \\
        --icon-emoji "🤖"

Den föregående versionen av det här skriptet skrev till SQLite-tabellen `tools`
i tools.db – men sajten läser `static/tools.json`, så ett verktyg som lades till
med det gamla skriptet syntes aldrig någonstans. Skriv alltid till katalogfilen.

Efter körning: kör `validate_catalog.py`, och `build_stacks.py` om verktyget
fått roller.
"""
import argparse
import json
import re
import sys
import unicodedata

CATALOG = "static/tools.json"

CATEGORIES = ["text", "bild", "video", "ljud", "kod",
              "affar", "marknadsforing", "juridik", "produktivitet", "sok"]
GDPR = ["gdpr_klar", "dpa", "lokal", "oklart", "varning"]
SWEDISH = ["bra", "delvis", "svagt"]
PRICE_TIERS = ["gratis", "freemium", "betald"]
ROLES = ["maklare", "fastighetsforvaltare", "hr", "copywriter", "ekonomi", "juridik"]


def slugify(name):
    s = unicodedata.normalize("NFKD", name.lower())
    s = s.replace("å", "a").replace("ä", "a").replace("ö", "o")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--name", required=True)
    p.add_argument("--category", required=True, choices=CATEGORIES)
    p.add_argument("--description", required=True)
    p.add_argument("--pricing", required=True,
                   help='Visningstext, t.ex. "Freemium (från 20 USD/mån)"')
    p.add_argument("--price-tier", required=True, choices=PRICE_TIERS)
    p.add_argument("--rating", type=float, required=True, help="Skalan 0–5")
    p.add_argument("--gdpr", required=True, choices=GDPR)
    p.add_argument("--gdpr-note", required=True,
                   help="Vad som faktiskt gäller: DPA, datalagring, risker.")
    p.add_argument("--swedish", required=True, choices=SWEDISH)
    p.add_argument("--swedish-note", required=True,
                   help="Hur väl det fungerar på svenska, konkret.")
    p.add_argument("--url", required=True, help="Officiell https-URL")
    p.add_argument("--tags", nargs="*", default=[])
    p.add_argument("--roles", nargs="*", default=[], choices=ROLES)
    p.add_argument("--icon-emoji", default="🤖")
    p.add_argument("--icon-bg-color", default="bg-slate-100")
    p.add_argument("--affiliate", action="store_true",
                   help="Sätt bara om länken faktiskt är en affiliatelänk – "
                        'då renderas den med rel="sponsored".')
    p.add_argument("--featured", action="store_true",
                   help="Redaktionens val. Använd INTE för sålda placeringar; "
                        "sponsrat innehåll ska märkas som sponsrat.")
    args = p.parse_args()

    if not 0 <= args.rating <= 5:
        sys.exit(f"Betyget {args.rating} ligger utanför skalan 0–5.")
    if not args.url.startswith("https://"):
        sys.exit("URL måste börja med https://")

    tools = json.load(open(CATALOG, encoding="utf-8"))
    slug = slugify(args.name)

    if any(t["name"].lower() == args.name.lower() for t in tools):
        sys.exit(f"'{args.name}' finns redan i katalogen.")
    if any(t["slug"] == slug for t in tools):
        sys.exit(f"Sluggen '{slug}' är redan tagen.")

    tools.append({
        "id": 0,  # sätts om nedan när listan sorterats
        "slug": slug,
        "name": args.name,
        "category": args.category,
        "description": args.description,
        "pricing": args.pricing,
        "price_tier": args.price_tier,
        "rating": round(args.rating, 1),
        "gdpr": args.gdpr,
        "gdpr_note": args.gdpr_note,
        "swedish": args.swedish,
        "swedish_note": args.swedish_note,
        "tags": args.tags,
        "icon_emoji": args.icon_emoji,
        "icon_bg_color": args.icon_bg_color,
        "url": args.url,
        "affiliate": args.affiliate,
        "featured": args.featured,
        "roles": args.roles,
    })

    tools.sort(key=lambda t: t["name"].lower())
    for i, t in enumerate(tools, 1):
        t["id"] = i

    with open(CATALOG, "w", encoding="utf-8") as f:
        json.dump(tools, f, ensure_ascii=False, indent=2)

    print(f"✅ Lade till '{args.name}'. Katalogen har nu {len(tools)} verktyg.")
    print("   Kör: python3 validate_catalog.py && python3 build_stacks.py")


if __name__ == "__main__":
    main()
