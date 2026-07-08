#!/bin/bash
FILES=(
    "ai-verktyg.html"
    "ai-program.html"
    "ai-jamfor.html"
    "ai-kalkylator.html"
    "lar-dig-ai.html"
    "bygg-med-ai.html"
    "gratis-ai-verktyg.html"
    "index.html"
)
cd /data/workspace/projects/ai-verktygskistan/static
for file in "${FILES[@]}"; do
    if ! grep -q "/ai-ordlista.html" "$file"; then
        # Add to footer "Lär dig AI" context
        sed -i 's|<li><a href="/lar-dig-ai.html" class="hover:text-indigo-400 transition-colors">Lär dig AI</a></li>|<li><a href="/lar-dig-ai.html" class="hover:text-indigo-400 transition-colors">Lär dig AI</a></li>\n                    <li><a href="/ai-ordlista.html" class="hover:text-indigo-400 transition-colors">AI Ordlista</a></li>|g' "$file"
        echo "Updated $file"
    fi
done
