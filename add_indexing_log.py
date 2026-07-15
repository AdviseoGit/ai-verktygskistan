import re

with open('/data/workspace/projects/ai-verktygskistan/INDEXING_LOG.md', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "hitta-ratt-ai.html" in line:
        new_lines.append(line.replace("2026-07-12", "2026-07-15").replace("Länkad i topnav + sitemap", "Länkad i topnav + sitemap. Behöver indexeras manuellt av Sim."))
    else:
        new_lines.append(line)

with open('/data/workspace/projects/ai-verktygskistan/INDEXING_LOG.md', 'w') as f:
    f.writelines(new_lines)
