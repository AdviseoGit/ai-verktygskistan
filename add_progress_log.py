with open("/data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md", "r") as f:
    lines = f.readlines()

new_line = "2026-07-19 | TILLVÄXT/DATA | Lade till 16 nya AI-verktyg och fixade 40 JSON-fel | Katalog 54->70, massivt lyft för sökintent | nästa: Optimera leads-flöde\n"
lines.insert(1, new_line)

with open("/data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md", "w") as f:
    f.writelines(lines)
