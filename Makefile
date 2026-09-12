# Bygg och kontrollera sajten.
#
#   make build   – bygg allt från källorna (mallar, SEO, sitemap)
#   make check   – kontrollera utan att skriva något (samma som CI kör)
#   make css     – bygg om Tailwind-CSS:en (kräver nätverk, körs lokalt)
#   make og      – rendera om delningsbilderna (kräver playwright)
#   make serve   – kör sajten lokalt på http://127.0.0.1:8000
#
# Kör alltid `make check` innan du pushar. Den fångar det som annars
# upptäcks först i produktion: brutna länkar, saknad canonical, tom sitemap,
# ogiltig JSON, döda omdirigeringar, saknade delningsbilder och sidor som
# hamnat ur synk med mallarna eller SEO-blocket.
#
# `make css` och `make og` ingår MEDVETET inte i `make build`: de kräver
# nätverk respektive webbläsare och kan inte köras i CI. Lägger du till nya
# Tailwind-klasser måste du köra `make css` själv, annars saknas de i CSS:en.

.PHONY: build check css og serve clean

build:
	@python3 scripts/build_site.py
	@python3 scripts/seo.py
	@python3 scripts/build_sitemap.py
	@$(MAKE) --no-print-directory check

check:
	@python3 scripts/build_site.py --check
	@python3 scripts/seo.py --check
	@python3 scripts/check_site.py

css:
	@npx -y tailwindcss@3 -c tailwind.config.js -i src/input.css -o static/css/site.css --minify

og:
	@PYTHONPATH=scripts python3 scripts/build_og.py

serve:
	@uvicorn main:app --reload --host 127.0.0.1 --port 8000

clean:
	@rm -f tools.db
	@find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
