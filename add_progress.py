import sys
with open("/data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md", "r") as f:
    content = f.read()

new_entry = "2026-07-06 | TILLVÄXT/DATA | Utökade katalogen med 4 tunga AI-verktyg (Gemini 3.1, Sora, Sonnet 4.5, Krea) | Katalog 34->38, starkare sökordsintent för flaggskeppsmodeller | nästa: Fånga fler leads eller ny intent-sida\n"

with open("/data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md", "w") as f:
    f.write(new_entry + content)
