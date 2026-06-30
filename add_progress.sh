#!/bin/bash
DATE=$(date +%Y-%m-%d)
ENTRY="$DATE | LEADFLOW | Lade till GDPR-checklista PDF-lead capture i ai-jamfor.html | Ökar leads konvertering på verktygssida | nästa: Fånga fler leads (PDF) från index"
echo -e "$ENTRY\n$(cat /data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md)" > /data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md
