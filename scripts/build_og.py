#!/usr/bin/env python3
"""Renderar en delningsbild (og:image) per sida.

    python3 scripts/build_og.py [--bara sida1,sida2]

Varje sida delad i LinkedIn, Slack eller Teams visade tidigare en tom grå
ruta, eftersom og:image saknades på samtliga sidor. En bild med sidans egen
rubrik höjer klickfrekvensen på delningar markant och kostar ingenting i
löpande drift – bilderna är statiska filer som checkas in.

Kräver playwright med chromium. Kör lokalt vid behov, inte i CI:

    pip install playwright && playwright install chromium

Bilderna hamnar i static/og/<sida>.jpg i formatet 1200x630. JPEG, inte
PNG: en PNG av den har gradienten blev ~140 kB per bild och 4,4 MB totalt,
mot ~45 kB som JPEG utan synlig skillnad.
"""
import argparse
import pathlib
import re
import sys

STATIC = pathlib.Path("static")
UT = STATIC / "og"

MALL = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { width:1200px; height:630px; display:flex; flex-direction:column;
         justify-content:space-between; padding:72px 80px;
         background:#0f172a; color:#fff;
         font-family:'DejaVu Sans','Liberation Sans',system-ui,sans-serif; }
  .glow { position:absolute; top:-220px; right:-180px; width:680px; height:680px;
          border-radius:50%; background:radial-gradient(circle,#6366f1 0%,rgba(99,102,241,0) 68%);
          opacity:.55; }
  .top { position:relative; z-index:1; display:flex; align-items:center; gap:18px; }
  .dot { width:14px; height:14px; border-radius:50%; background:#818cf8; }
  .brand { font-size:26px; font-weight:700; letter-spacing:-.3px; }
  .brand span { color:#818cf8; }
  .mid { position:relative; z-index:1; }
  .kicker { display:inline-block; font-size:20px; font-weight:700; color:#a5b4fc;
            text-transform:uppercase; letter-spacing:1.6px; margin-bottom:26px; }
  h1 { font-size:__STORLEK__px; line-height:1.12; font-weight:800;
       letter-spacing:-1.4px; max-width:1010px; }
  .bot { position:relative; z-index:1; display:flex; justify-content:space-between;
         align-items:flex-end; font-size:21px; color:#94a3b8; }
  .bot strong { color:#e2e8f0; font-weight:600; }
</style></head><body>
  <div class="glow"></div>
  <div class="top"><div class="dot"></div><div class="brand">AI-<span>Verktygslådan</span></div></div>
  <div class="mid"><div class="kicker">__KICKER__</div><h1>__TITEL__</h1></div>
  <div class="bot"><div><strong>aiverktygsladan.se</strong></div><div>__FOT__</div></div>
</body></html>"""

# Samma indelning som brödsmulorna, men kortare för bildens skull.
from seo import PARENT  # noqa: E402


def kicker(namn):
    if namn == "index":
        return "AI-agenter på svenska"
    return PARENT.get(namn, ("Guide", ""))[0].replace("Lär dig AI-agenter", "Lär dig")


def rensa(text):
    text = re.sub(r"&ndash;", "–", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&[a-z]+;", "", text)
    return text.strip()


def bygg(sidor):
    from playwright.sync_api import sync_playwright
    UT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        webblasare = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        flik = webblasare.new_page(viewport={"width": 1200, "height": 630})
        for sida in sidor:
            html = sida.read_text(encoding="utf-8")
            m = re.search(r"<title>(.*?)</title>", html, re.S)
            titel = rensa(m.group(1).split(" | ")[0]) if m else sida.stem
            # Rubriken får krympa så att långa titlar fortfarande ryms.
            storlek = 66 if len(titel) < 48 else (56 if len(titel) < 72 else 46)
            markup = (MALL.replace("__TITEL__", titel)
                          .replace("__KICKER__", kicker(sida.stem))
                          .replace("__STORLEK__", str(storlek))
                          .replace("__FOT__", "Uppdaterad september 2026"))
            flik.set_content(markup, wait_until="load")
            flik.screenshot(path=str(UT / f"{sida.stem}.jpg"),
                            type="jpeg", quality=86)
            print(f"  {sida.stem}.jpg  ({titel[:56]})")
        webblasare.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bara", help="Kommaseparerade sidnamn utan .html")
    args = ap.parse_args()
    sidor = sorted(STATIC.glob("*.html"))
    if args.bara:
        vald = set(args.bara.split(","))
        sidor = [s for s in sidor if s.stem in vald]
    bygg(sidor)
    print(f"\n✅ {len(sidor)} delningsbilder i {UT}/")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    sys.exit(main())
