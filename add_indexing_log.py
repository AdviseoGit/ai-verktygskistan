with open("/data/workspace/projects/ai-verktygskistan/INDEXING_LOG.md", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "URL is unknown to Google" in line:
        parts = line.split("|")
        if len(parts) >= 3:
            parts[2] = " 2026-07-19 "
            lines[i] = "|".join(parts)

with open("/data/workspace/projects/ai-verktygskistan/INDEXING_LOG.md", "w") as f:
    f.writelines(lines)
