#!/usr/bin/env python3
"""Injicerar de gemensamma delarna (nav, sidfot) i alla sidor.

    python3 scripts/build_site.py [--check]

Varje sida har tidigare burit sin egen kopia av navigation och sidfot. Med 27
sidor innebar det 27 ställen att ändra vid varje justering, och resultatet blev
därefter: fyra olika navigationer, nio olika sidfötter, och överblivna
</div>-taggar i menyn på 14 av 27 sidor.

Nu ligger de i `templates/nav.html` och `templates/footer.html`. Det här
skriptet ersätter innehållet mellan markörerna

    <!-- @nav -->   ...   <!-- /@nav -->
    <!-- @footer --> ... <!-- /@footer -->

Saknas markörerna hittar skriptet den befintliga regionen och lägger dit dem,
så första körningen migrerar sidan automatiskt. Sidunikt innehåll rörs aldrig.

`--check` skriver ingenting utan returnerar exit 1 om någon sida har hamnat ur
synk med mallarna. Det är den varianten CI kör.
"""
import argparse
import pathlib
import re
import sys

STATIC = pathlib.Path("static")
TEMPLATES = pathlib.Path("templates")

# Sidor som medvetet saknar den gemensamma ramen.
SKIP = set()

# Där huvudinnehållet börjar – används för att hitta slutet på nav-regionen
# första gången, innan markörerna finns.
CONTENT_START = re.compile(
    r"<header\b|<main\b|<!--\s*Hero\b|<!--\s*Main Content\b|<!--\s*Ingångar\b|<section\b")


def load(name):
    return TEMPLATES.joinpath(f"{name}.html").read_text(encoding="utf-8").rstrip("\n")


def wrap(name, body):
    return f"    <!-- @{name} -->\n{body}\n    <!-- /@{name} -->"


def replace_marked(html, name, body):
    """Ersätter mellan befintliga markörer. Returnerar None om de saknas."""
    pattern = re.compile(
        rf"[ \t]*<!-- @{name} -->.*?<!-- /@{name} -->", re.S)
    if not pattern.search(html):
        return None
    return pattern.sub(lambda _: wrap(name, body), html, count=1)


def find_nav_region(html):
    """Hittar nav + mobilmeny i en sida som ännu inte har markörer."""
    start = html.find("<nav ")
    if start < 0:
        return None
    m = CONTENT_START.search(html, start + 5)
    if not m:
        return None
    end = m.start()
    # Backa till radbrytningen före innehållet så indraget inte slits sönder.
    while end > start and html[end - 1] in " \t":
        end -= 1
    return start, end


def find_footer_region(html):
    start = html.find("<footer")
    if start < 0:
        return None
    end = html.find("</footer>", start)
    if end < 0:
        return None
    end += len("</footer>")
    return start, end


def apply(html, name, body, finder):
    marked = replace_marked(html, name, body)
    if marked is not None:
        return marked, False
    region = finder(html)
    if region is None:
        return html, None
    start, end = region
    return html[:start] + wrap(name, body).lstrip() + html[end:], True


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="Skriv inget, returnera 1 om någon sida är ur synk.")
    args = ap.parse_args()

    nav, footer = load("nav"), load("footer")
    changed, migrated, missing, stale = [], [], [], []

    for page in sorted(STATIC.glob("*.html")):
        if page.name in SKIP:
            continue
        original = page.read_text(encoding="utf-8")
        html = original

        for name, body, finder in (("nav", nav, find_nav_region),
                                   ("footer", footer, find_footer_region)):
            html, did_migrate = apply(html, name, body, finder)
            if did_migrate is None:
                missing.append(f"{page.name}: hittade ingen {name}-region")
            elif did_migrate:
                migrated.append(f"{page.name} ({name})")

        if html != original:
            if args.check:
                stale.append(page.name)
            else:
                page.write_text(html, encoding="utf-8")
                changed.append(page.name)

    if args.check:
        for m in missing:
            print(f"  ⚠ {m}")
        if stale:
            print(f"❌ {len(stale)} sidor är ur synk med templates/:")
            for name in stale:
                print(f"   - {name}")
            print("\nKör: python3 scripts/build_site.py")
            return 1
        print(f"✅ Alla {len(list(STATIC.glob('*.html')))} sidor följer mallarna.")
        return 0

    for m in migrated:
        print(f"  migrerade {m}")
    for m in missing:
        print(f"  ⚠ {m}")
    print(f"\n✅ Uppdaterade {len(changed)} sidor från templates/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
