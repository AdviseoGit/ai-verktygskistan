#!/bin/bash
# Lägg till AI-Kompassen i navigeringen för HTML-filer som saknar det

find /data/workspace/projects/ai-verktygskistan/static/ -name "*.html" -type f | while read file; do
    if ! grep -q "hitta-ratt-ai.html" "$file"; then
        # Desktop
        sed -i 's|<a href="/ai-jamfor.html" class="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors">Jämför</a>|<a href="/ai-jamfor.html" class="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors">Jämför</a>\n                    <a href="/hitta-ratt-ai.html" class="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors">Hitta rätt AI</a>|g' "$file"
        sed -i 's|<a href="/ai-jamfor.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Jämför Verktyg</a>|<a href="/ai-jamfor.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Jämför Verktyg</a>\n                <a href="/hitta-ratt-ai.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Hitta rätt AI</a>|g' "$file"
        
        # Mobile
        sed -i 's|<a href="/ai-jamfor.html" class="block px-3 py-2 text-base font-medium text-slate-600 hover:text-indigo-600 hover:bg-slate-50 rounded-md">Jämför Verktyg</a>|<a href="/ai-jamfor.html" class="block px-3 py-2 text-base font-medium text-slate-600 hover:text-indigo-600 hover:bg-slate-50 rounded-md">Jämför Verktyg</a>\n                <a href="/hitta-ratt-ai.html" class="block px-3 py-2 text-base font-medium text-slate-600 hover:text-indigo-600 hover:bg-slate-50 rounded-md">Hitta rätt AI</a>|g' "$file"
        
        # Footer
        sed -i 's|<a href="/om-sajten.html" class="hover:text-white transition-colors">Om sajten</a>|<a href="/om-sajten.html" class="hover:text-white transition-colors">Om sajten</a>\n                <a href="/hitta-ratt-ai.html" class="hover:text-white transition-colors">Hitta rätt AI</a>|g' "$file"
        
        echo "Updated $file"
    fi
done
