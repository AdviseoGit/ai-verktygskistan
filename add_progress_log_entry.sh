#!/bin/bash
cd /data/workspace/projects/ai-verktygskistan
DATE=$(date +%Y-%m-%d)
ENTRY="$DATE | SEO/TILLVÄXT | Ny dedikerad landningssida för 'AI Program' | Fånga sökintention & volym | nästa: Bygg SEO-sidor för 'Lär dig AI' & 'Bygg med AI'"
echo "$ENTRY" > temp_log.md
cat PROGRESS_LOG.md >> temp_log.md
mv temp_log.md PROGRESS_LOG.md
