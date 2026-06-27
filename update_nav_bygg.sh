#!/bin/bash
cd /data/workspace/projects/ai-verktygskistan/static

# We need to add 'Bygg med AI' to the navigation in key files
for file in index.html ai-verktyg.html gratis-ai-verktyg.html vad-ar-ai-verktyg.html ai-kalkylator.html ai-svenska-foretag-rapport.html claude-fable-5-vs-gpt-5.5.html ai-for-hr.html om-sajten.html integritetspolicy.html; do
    if [ -f "$file" ]; then
        # Add to desktop nav
        sed -i 's|<a href="/lar-dig-ai.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Lär dig AI</a>|<a href="/lar-dig-ai.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Lär dig AI</a>\n                    <a href="/bygg-med-ai.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Bygg med AI</a>|g' "$file"
        
        # Note: some files might have text-gray-500 instead of indigo-600 (like lar-dig-ai.html which has a different nav structure)
        
        # Add to mobile nav
        sed -i 's|<a href="/lar-dig-ai.html" class="hover:text-indigo-600 transition-colors font-medium py-2">Lär dig AI</a>|<a href="/lar-dig-ai.html" class="hover:text-indigo-600 transition-colors font-medium py-2">Lär dig AI</a>\n             <a href="/bygg-med-ai.html" class="hover:text-indigo-600 transition-colors font-medium py-2">Bygg med AI</a>|g' "$file"
        
        # Add to footer
        sed -i 's|<a href="/lar-dig-ai.html" class="hover:text-indigo-400 transition-colors">Lär dig AI</a>|<a href="/lar-dig-ai.html" class="hover:text-indigo-400 transition-colors">Lär dig AI</a>\n                    <a href="/bygg-med-ai.html" class="hover:text-indigo-400 transition-colors">Bygg med AI</a>|g' "$file"
        
        echo "Updated $file"
    fi
done
