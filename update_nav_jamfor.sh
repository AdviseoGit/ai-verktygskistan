#!/bin/bash
find /data/workspace/projects/ai-verktygskistan/static -name "*.html" -print0 | while IFS= read -r -d '' file; do
  # Leta efter "Alla Verktyg" och "AI Program" och lägg till Jämför-länken om den inte finns
  if ! grep -q "ai-jamfor.html" "$file"; then
    sed -i 's|<a href="/ai-program.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">AI Program</a>|<a href="/ai-program.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">AI Program</a>\n                <a href="/ai-jamfor.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Jämför Verktyg</a>|g' "$file"
    
    sed -i 's|<a href="/ai-program.html" class="hover:text-indigo-600 transition-colors font-medium">AI Program</a>|<a href="/ai-program.html" class="hover:text-indigo-600 transition-colors font-medium">AI Program</a>\n             <a href="/ai-jamfor.html" class="hover:text-indigo-600 transition-colors font-medium">Jämför Verktyg</a>|g' "$file"

    sed -i 's|<li><a href="/ai-program.html" class="hover:text-white transition-colors">AI Program</a></li>|<li><a href="/ai-program.html" class="hover:text-white transition-colors">AI Program</a></li>\n                            <li><a href="/ai-jamfor.html" class="hover:text-white transition-colors">Jämför Verktyg</a></li>|g' "$file"
  fi
done
