#!/bin/bash
DATE=$(date +%Y-%m-%d)
ENTRY="$DATE | TILLVÄXT/DATA | Byggt interaktiv AI-Kalkylator för ROI | Fångar unik företagsdata (Data Moat) | nästa: Publicera original-data-rapport"
TEMP_FILE=$(mktemp)
echo "$ENTRY" > "$TEMP_FILE"
cat /data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md >> "$TEMP_FILE"
mv "$TEMP_FILE" /data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md
