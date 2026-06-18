#!/bin/bash
TODAY=$(date +%Y-%m-%d)
ENTRY="$TODAY | DESIGN/TILLVÄXT | Fixat mobilmeny, lagt till Udio + 5 nya verktyg | UX-lyft + katalog 20->26 | nästa: Ny artikel HR-avdelningen GDPR"
sed -i "1i$ENTRY" /data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md
