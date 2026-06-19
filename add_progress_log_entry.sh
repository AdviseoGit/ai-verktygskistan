#!/bin/bash
DATE=$(date +%Y-%m-%d)
ENTRY="$DATE | SEO/TILLVÄXT | Ny artikel om GDPR-säkra AI-verktyg för HR | Fånga sökvolym på 'AI HR' | nästa: Fånga original-data/kalkylator"
TMP_FILE=$(mktemp)
echo "$ENTRY" > "$TMP_FILE"
cat /data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md >> "$TMP_FILE"
mv "$TMP_FILE" /data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md
