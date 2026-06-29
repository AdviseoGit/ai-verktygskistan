#!/bin/bash
DATE=$(date +%Y-%m-%d)
ENTRY="$DATE | SEO/TILLVÄXT | Ny interaktiv Jämför-funktion för AI-verktyg | Stärker 'AI Verktyg' intent & UX | nästa: Fånga fler leads (PDF)"

if ! grep -q "$DATE | SEO/TILLVÄXT | Ny interaktiv Jämför-funktion" /data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md; then
  sed -i "1i$ENTRY" /data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md
fi
