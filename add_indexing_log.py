import os

log_path = '/data/workspace/projects/ai-verktygskistan/INDEXING_LOG.md'
new_entry = "https://aiverktygsladan.se/hitta-ratt-ai.html | URL is unknown to Google | 2026-07-12 | Länkad i topnav + sitemap\n"

with open(log_path, 'a', encoding='utf-8') as f:
    f.write(new_entry)
print("Updated INDEXING_LOG.md")
