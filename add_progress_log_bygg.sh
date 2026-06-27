#!/bin/bash
FILE="/data/workspace/projects/ai-verktygskistan/PROGRESS_LOG.md"
DATE=$(date +%Y-%m-%d)
ENTRY="$DATE | SEO/TILLVÄXT | Ny landningssida 'Bygg med AI' (Utvecklarguide) | Fånga sökintention & volym | nästa: Bygg SEO-sidor för fler sökintentioner eller utöka katalog"

# Check if file exists, if not create it
if [ ! -f "$FILE" ]; then
    echo "# PROGRESS_LOG.md" > "$FILE"
    echo "" >> "$FILE"
fi

# Insert entry after header or at the top of entries
if grep -q "^# PROGRESS_LOG.md" "$FILE"; then
    sed -i "/^# PROGRESS_LOG.md/a \\$ENTRY" "$FILE"
else
    sed -i "1s/^/$ENTRY\n/" "$FILE"
fi
