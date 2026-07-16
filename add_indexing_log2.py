import json

with open("/data/workspace/projects/ai-verktygskistan/INDEXING_LOG.md", "r") as f:
    lines = f.readlines()

new_lines = [
    "https://aiverktygsladan.se/ai-svenska-foretag-rapport.html | URL is unknown to Google | 2026-07-16 | Länkad i sitemap. Behöver indexeras manuellt av Sim.\n"
]

lines.extend(new_lines)

with open("/data/workspace/projects/ai-verktygskistan/INDEXING_LOG.md", "w") as f:
    f.writelines(lines)
