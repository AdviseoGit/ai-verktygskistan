#!/bin/bash
FILES=(
  "static/ai-verktyg.html"
  "static/gratis-ai-verktyg.html"
  "static/vad-ar-ai-verktyg.html"
  "static/claude-fable-5-vs-gpt-5.5.html"
  "static/ai-kalkylator.html"
  "static/ai-for-hr.html"
  "static/ai-svenska-foretag-rapport.html"
  "static/ai-program.html"
  "static/om-sajten.html"
  "static/integritetspolicy.html"
  "static/lar-dig-ai.html"
  "static/index.html"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        if grep -q "Denna sajt skapas och drivs helt av AI" "$file"; then
           echo "$file OK"
        else
           echo "$file MISSING"
        fi
    fi
done
