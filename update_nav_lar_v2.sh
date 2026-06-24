#!/bin/bash
# Länka "Lär dig AI" från navigeringsmenyerna i befintliga filer

FILES=(
  "static/index.html"
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
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        if ! grep -q "lar-dig-ai.html" "$file"; then
           # Header nav items
           sed -i 's|<a href="/vad-ar-ai-verktyg.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Vad är AI-verktyg?</a>|<a href="/lar-dig-ai.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Lär dig AI</a>\n                <a href="/vad-ar-ai-verktyg.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Vad är AI-verktyg?</a>|g' "$file"
           
           # Mobile nav items
           sed -i 's|<a href="/vad-ar-ai-verktyg.html" class="hover:text-indigo-600 transition-colors font-medium">Vad är AI-verktyg?</a>|<a href="/lar-dig-ai.html" class="hover:text-indigo-600 transition-colors font-medium">Lär dig AI</a>\n             <a href="/vad-ar-ai-verktyg.html" class="hover:text-indigo-600 transition-colors font-medium">Vad är AI-verktyg?</a>|g' "$file"

           # Footer nav items
           sed -i 's|<li><a href="/vad-ar-ai-verktyg.html" class="text-slate-500 hover:text-indigo-600">Vad är AI-verktyg?</a></li>|<li><a href="/lar-dig-ai.html" class="text-slate-500 hover:text-indigo-600">Lär dig AI</a></li>\n                        <li><a href="/vad-ar-ai-verktyg.html" class="text-slate-500 hover:text-indigo-600">Vad är AI-verktyg?</a></li>|g' "$file"
           
           # For files using other nav classes
           sed -i 's|<a href="/vad-ar-ai-verktyg.html" class="border-transparent text-gray-500 hover:text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">Guider</a>|<a href="/lar-dig-ai.html" class="border-transparent text-gray-500 hover:text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">Lär dig AI</a>\n                        <a href="/vad-ar-ai-verktyg.html" class="border-transparent text-gray-500 hover:text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">Guider</a>|g' "$file"
           
           sed -i 's|<a href="/vad-ar-ai-verktyg.html" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">Guider</a>|<a href="/lar-dig-ai.html" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">Lär dig AI</a>\n                <a href="/vad-ar-ai-verktyg.html" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">Guider</a>|g' "$file"

           echo "Updated $file"
        fi
    fi
done
