#!/bin/bash
DATE=$(date +%Y-%m-%d)
sed -i "1s/^/$DATE | KONVERTERING \& LEADS | Kopplat in db-mätning via api\/stats\/leads | mätning | nästa: Identifiera top leads-källor\n/" /data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md
