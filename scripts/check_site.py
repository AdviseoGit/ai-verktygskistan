#!/usr/bin/env python3
"""Kontrollerar hela sajten innan den går live.

    python3 scripts/check_site.py

Returnerar exit 1 om något är fel. Kontrollerna finns för att varje punkt här
en gång har gått sönder i produktion utan att någon märkte det:

* **Interna länkar** – sitemapen pekade en period på borttagna sidor.
* **Sitemap mot filsystem** – sitemap.xml var 0 bytes i ett dygn.
* **Titel och beskrivning** – nya sidor har publicerats utan.
* **Canonical** – sex sidor saknade den, och startsidans pekade på en domän
  som inte ens resolvar.
* **Dubblerade titlar** – två sidor med samma titel konkurrerar i sök.
* **Balanserad markup** – 14 sidor hade överblivna </div> i menyn.
* **JSON-validitet** – schema.json och sidornas JSON-LD läses av sökmotorer.
* **Varumärkesnamn** – sajten hette fel namn i förhållande till domänen.
* **Omdirigeringar** – REDIRECTS i main.py pekade på sidor som tagits bort.
* **Tillgångar** – delningsbilder som saknades på disk, och CSS som inte byggts.
"""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

STATIC = pathlib.Path("static")
DOMAIN = "https://aiverktygsladan.se"
OLD_BRAND = "Verktygskistan"

# Sidor som avsiktligt inte ska ligga i sitemapen.
SITEMAP_EXEMPT: set[str] = set()


def pages():
    return sorted(STATIC.glob("*.html"))


def check_meta(errors, warnings):
    titles, descriptions = {}, {}
    for p in pages():
        s = p.read_text(encoding="utf-8")
        name = p.name

        t = re.search(r"<title>(.*?)</title>", s, re.S)
        if not t or not t.group(1).strip():
            errors.append(f"{name}: saknar <title>")
        else:
            titles.setdefault(t.group(1).strip(), []).append(name)

        d = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', s)
        if not d or not d.group(1).strip():
            errors.append(f"{name}: saknar meta description")
        else:
            text = d.group(1).strip()
            descriptions.setdefault(text, []).append(name)
            if len(text) > 160:
                warnings.append(f"{name}: description är {len(text)} tecken (>160 kapas i sök)")

        c = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', s)
        if not c:
            errors.append(f"{name}: saknar canonical")
        else:
            url = c.group(1)
            expected = f"{DOMAIN}/" if name == "index.html" else f"{DOMAIN}/{name}"
            if url != expected:
                errors.append(f"{name}: canonical är {url}, förväntade {expected}")

    for text, names in titles.items():
        if len(names) > 1:
            errors.append(f"dubblerad titel på {', '.join(names)}: {text[:60]!r}")
    for text, names in descriptions.items():
        if len(names) > 1:
            warnings.append(f"dubblerad description på {', '.join(names)}")


def check_links(errors):
    existing = {p.name for p in pages()}
    for p in pages():
        s = p.read_text(encoding="utf-8")
        for href in set(re.findall(r'href="(/[^"]*)"', s)):
            target = href.split("#")[0].split("?")[0]
            if target in ("/", ""):
                continue
            if target.startswith("/static/"):
                if not pathlib.Path(target.lstrip("/")).exists():
                    errors.append(f"{p.name}: bruten länk till {target}")
                continue
            if target.lstrip("/") not in existing:
                errors.append(f"{p.name}: bruten länk till {target}")


def check_sitemap(errors):
    path = STATIC / "sitemap.xml"
    if not path.exists() or path.stat().st_size == 0:
        errors.append("sitemap.xml saknas eller är tom")
        return
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        errors.append(f"sitemap.xml går inte att parsa: {e}")
        return

    urls = [u.find(f"{ns}loc").text for u in root]
    listed = {u.replace(f"{DOMAIN}/", "") or "index.html" for u in urls}
    on_disk = {p.name for p in pages()} - SITEMAP_EXEMPT

    for missing in sorted(on_disk - listed):
        errors.append(f"sitemap: {missing} finns på disk men saknas i sitemapen")
    for extra in sorted(listed - on_disk):
        errors.append(f"sitemap: {extra} ligger i sitemapen men finns inte på disk")
    if len(urls) != len(set(urls)):
        errors.append("sitemap: innehåller dubblerade URL:er")


def check_markup(errors):
    for p in pages():
        s = p.read_text(encoding="utf-8")
        for region in ("nav", "footer"):
            i = s.find(f"<!-- @{region} -->")
            j = s.find(f"<!-- /@{region} -->")
            if i < 0 or j < 0:
                errors.append(f"{p.name}: saknar {region}-markörer "
                              f"(kör scripts/build_site.py)")
                continue
            block = s[i:j]
            if block.count("<div") != block.count("</div>"):
                errors.append(f"{p.name}: obalanserade div i {region}")
        if s.count("<div") != s.count("</div>"):
            errors.append(f"{p.name}: obalanserade div i hela sidan "
                          f"({s.count('<div')} öppnande, {s.count('</div>')} stängande)")


def check_json(errors):
    for path in (STATIC / "schema.json",):
        if not path.exists():
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{path}: ogiltig JSON – {e}")

    for p in pages():
        s = p.read_text(encoding="utf-8")
        for block in re.findall(
                r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
            if not block.strip():
                continue
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                errors.append(f"{p.name}: ogiltig JSON-LD – {e}")


def check_brand(errors):
    for p in list(pages()) + [STATIC / "llms.txt", STATIC / "schema.json"]:
        if not p.exists():
            continue
        if OLD_BRAND in p.read_text(encoding="utf-8"):
            errors.append(f"{p.name}: innehåller gamla varumärkesnamnet "
                          f"'{OLD_BRAND}'")


def check_redirects(errors):
    """REDIRECTS i main.py ska peka på sidor som faktiskt finns.

    De gamla katalogsidorna togs bort när sajten smalnade av till AI-agenter.
    Omdirigeringarna är det enda som håller deras länkvärde vid liv, så en
    omdirigering till en sida som i sin tur tagits bort är värre än ingen
    alls: den skickar besökaren till en 404 via en 301.
    """
    import ast

    source = pathlib.Path("main.py")
    if not source.exists():
        return
    tree = ast.parse(source.read_text(encoding="utf-8"))
    mapping = None
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign)
                and any(getattr(t, "id", None) == "REDIRECTS" for t in node.targets)):
            mapping = ast.literal_eval(node.value)
            break
    if mapping is None:
        errors.append("main.py: hittar ingen REDIRECTS-tabell")
        return

    # literal_eval sväljer dubblettnycklar – sista vinner, tyst. Räkna dem i
    # källan i stället, annars kan två rader för samma sida peka olika håll
    # utan att någon märker vilken som gäller.
    seen, keys = set(), [k.value for k in node.value.keys]
    for key in keys:
        if key in seen:
            errors.append(f"REDIRECTS: {key} förekommer flera gånger")
        seen.add(key)

    existing = {p.name for p in pages()}
    for source_page, target in sorted(mapping.items()):
        if f"{source_page}.html" in existing:
            errors.append(f"REDIRECTS: {source_page} omdirigeras men finns "
                          f"kvar som sida – ta bort det ena")
        if target == "/":
            continue
        if target.lstrip("/") not in existing:
            errors.append(f"REDIRECTS: {source_page} pekar på {target} "
                          f"som inte finns")


def check_assets(errors, warnings):
    """Kontrollerar att det SEO-blocket pekar på faktiskt finns.

    og:image byggs av scripts/build_og.py och CSS:en av `make css`. Inget av
    dem körs i CI, så utan den här kontrollen kan en delning peka på en 404
    eller en sida sakna sina stilar utan att något syns förrän i produktion.
    """
    css = STATIC / "css" / "site.css"
    if not css.exists():
        errors.append("static/css/site.css saknas – kör `make css`")
    elif css.stat().st_size < 10_000:
        errors.append(f"static/css/site.css är bara {css.stat().st_size} byte "
                      f"– byggdes den mot rätt sidor? Kör `make css`")

    for p in pages():
        s = p.read_text(encoding="utf-8")
        if "cdn.tailwindcss.com" in s:
            errors.append(f"{p.name}: laddar fortfarande Tailwind från CDN "
                          f"(render-blockerande) – kör `python3 scripts/seo.py`")
        m = re.search(r'<meta property="og:image" content="[^"]*?(/static/og/[^"]+)"', s)
        if not m:
            errors.append(f"{p.name}: saknar og:image")
        elif not pathlib.Path(m.group(1).lstrip("/")).exists():
            errors.append(f"{p.name}: og:image pekar på {m.group(1)} "
                          f"som inte finns – kör `make og`")
        if "dateModified" not in s:
            errors.append(f"{p.name}: saknar dateModified i schemat")


def check_robots(errors):
    path = STATIC / "robots.txt"
    if not path.exists():
        errors.append("robots.txt saknas")
        return
    s = path.read_text(encoding="utf-8")
    if "Sitemap:" not in s:
        errors.append("robots.txt saknar Sitemap-rad")
    if re.search(r"^Disallow:\s*/\s*$", s, re.M):
        errors.append("robots.txt blockerar hela sajten")
    for p in pages():
        if re.search(r'<meta[^>]+name="robots"[^>]+noindex', p.read_text(encoding="utf-8")):
            errors.append(f"{p.name}: har noindex")


def main():
    errors, warnings = [], []
    check_meta(errors, warnings)
    check_links(errors)
    check_sitemap(errors)
    check_markup(errors)
    check_json(errors)
    check_brand(errors)
    check_redirects(errors)
    check_assets(errors, warnings)
    check_robots(errors)

    for w in warnings:
        print(f"  ⚠  {w}")
    if warnings:
        print()

    if errors:
        print(f"❌ {len(errors)} fel:\n")
        for e in errors:
            print(f"   {e}")
        return 1

    print(f"✅ Sajten är hel: {len(pages())} sidor, "
          f"{len(warnings)} varningar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
