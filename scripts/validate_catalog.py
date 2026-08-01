#!/usr/bin/env python3
"""Validerar static/tools.json mot det kanoniska schemat.

Kör detta efter varje ändring i katalogen:

    python3 validate_catalog.py

Bakgrund: i juli 2026 hade katalogen 23 kategorivarianter, 16 olika
GDPR-statussträngar och två olika betygsskalor samtidigt. Renderingen i
tools.js kraschade dessutom tyst på poster där `tags` var en lista i stället
för en sträng, vilket gjorde att hela verktygsgriden försvann från sajten
utan att något syntes i logg eller sitemap. Den här validatorn finns för att
det inte ska hända igen.
"""
import json
import sys

CATEGORIES = {
    "text", "bild", "video", "ljud", "kod",
    "affar", "marknadsforing", "juridik", "produktivitet", "sok",
}
GDPR = {"gdpr_klar", "dpa", "lokal", "oklart", "varning"}
SWEDISH = {"bra", "delvis", "svagt"}
PRICE_TIERS = {"gratis", "freemium", "betald"}
ROLES = {"maklare", "fastighetsforvaltare", "hr", "copywriter", "ekonomi", "juridik"}

REQUIRED = [
    ("id", int), ("slug", str), ("name", str), ("category", str),
    ("description", str), ("pricing", str), ("price_tier", str),
    ("rating", float), ("gdpr", str), ("gdpr_note", str),
    ("swedish", str), ("swedish_note", str), ("tags", list),
    ("icon_emoji", str), ("icon_bg_color", str), ("url", str),
    ("affiliate", bool), ("featured", bool), ("roles", list),
]


def validate(path="static/tools.json"):
    errors = []
    tools = json.load(open(path, encoding="utf-8"))

    if not isinstance(tools, list):
        return [f"{path} måste innehålla en lista."]

    seen_names, seen_slugs, seen_ids = set(), set(), set()

    for t in tools:
        name = t.get("name", "<utan namn>")

        for field, ftype in REQUIRED:
            if field not in t:
                errors.append(f"{name}: saknar fältet '{field}'")
            elif ftype is float:
                if not isinstance(t[field], (int, float)):
                    errors.append(f"{name}: '{field}' måste vara ett tal")
            elif not isinstance(t[field], ftype):
                errors.append(
                    f"{name}: '{field}' är {type(t[field]).__name__}, "
                    f"förväntade {ftype.__name__}")

        if t.get("category") not in CATEGORIES:
            errors.append(f"{name}: okänd kategori '{t.get('category')}' "
                          f"(tillåtna: {sorted(CATEGORIES)})")
        if t.get("gdpr") not in GDPR:
            errors.append(f"{name}: okänd gdpr '{t.get('gdpr')}'")
        if t.get("swedish") not in SWEDISH:
            errors.append(f"{name}: okänt swedish '{t.get('swedish')}'")
        if t.get("price_tier") not in PRICE_TIERS:
            errors.append(f"{name}: okänd price_tier '{t.get('price_tier')}'")

        rating = t.get("rating")
        if isinstance(rating, (int, float)) and not 0 <= rating <= 5:
            errors.append(f"{name}: rating {rating} ligger utanför skalan 0–5")

        for role in t.get("roles", []):
            if role not in ROLES:
                errors.append(f"{name}: okänd roll '{role}'")

        url = t.get("url", "")
        if not url.startswith("https://"):
            errors.append(f"{name}: url saknas eller är inte https")

        for key, bucket, label in (("name", seen_names, "namn"),
                                   ("slug", seen_slugs, "slug"),
                                   ("id", seen_ids, "id")):
            value = t.get(key)
            if value in bucket:
                errors.append(f"{name}: dubblerat {label} '{value}'")
            bucket.add(value)

    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print(f"❌ {len(problems)} fel i katalogen:\n")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    count = len(json.load(open("static/tools.json", encoding="utf-8")))
    print(f"✅ Katalogen är giltig ({count} verktyg).")
