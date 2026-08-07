# Bygg och kontrollera sajten.
#
#   make build   – bygg allt från källorna (mallar, katalog, stackar, sitemap)
#   make check   – kontrollera utan att skriva något (samma som CI kör)
#   make serve   – kör sajten lokalt på http://127.0.0.1:8000
#
# Kör alltid `make check` innan du pushar. Den fångar det som annars
# upptäcks först i produktion: brutna länkar, saknad canonical, tom sitemap,
# ogiltig JSON och sidor som hamnat ur synk med mallarna.

.PHONY: build check serve clean

build:
	@python3 scripts/build_site.py
	@python3 scripts/build_stacks.py
	@python3 scripts/build_sitemap.py
	@$(MAKE) --no-print-directory check

check:
	@python3 scripts/validate_catalog.py
	@python3 scripts/build_site.py --check
	@python3 scripts/check_site.py

serve:
	@uvicorn main:app --reload --host 127.0.0.1 --port 8000

clean:
	@rm -f tools.db
	@find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
