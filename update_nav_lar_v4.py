import os
import glob

files = glob.glob('/data/workspace/projects/ai-verktygskistan/static/*.html')

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    if 'lar-dig-ai.html' not in content:
        # Header
        old_header = '<a href="/vad-ar-ai-verktyg.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Vad är AI-verktyg?</a>'
        new_header = '<a href="/lar-dig-ai.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Lär dig AI</a>\n                <a href="/vad-ar-ai-verktyg.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Vad är AI-verktyg?</a>'
        
        # Mobile
        old_mobile = '<a href="/vad-ar-ai-verktyg.html" class="hover:text-indigo-600 transition-colors font-medium">Vad är AI-verktyg?</a>'
        new_mobile = '<a href="/lar-dig-ai.html" class="hover:text-indigo-600 transition-colors font-medium">Lär dig AI</a>\n             <a href="/vad-ar-ai-verktyg.html" class="hover:text-indigo-600 transition-colors font-medium">Vad är AI-verktyg?</a>'

        # Desktop alternative
        old_desk_alt = '<a href="/vad-ar-ai-verktyg.html" class="border-transparent text-gray-500 hover:text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">Guider</a>'
        new_desk_alt = '<a href="/lar-dig-ai.html" class="border-transparent text-gray-500 hover:text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">Lär dig AI</a>\n                        <a href="/vad-ar-ai-verktyg.html" class="border-transparent text-gray-500 hover:text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">Guider</a>'

        # Mobile alternative
        old_mob_alt = '<a href="/vad-ar-ai-verktyg.html" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">Guider</a>'
        new_mob_alt = '<a href="/lar-dig-ai.html" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">Lär dig AI</a>\n                <a href="/vad-ar-ai-verktyg.html" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">Guider</a>'

        # Footer 1
        old_foot1 = '<li><a href="/vad-ar-ai-verktyg.html" class="text-slate-500 hover:text-indigo-600">Vad är AI-verktyg?</a></li>'
        new_foot1 = '<li><a href="/lar-dig-ai.html" class="text-slate-500 hover:text-indigo-600">Lär dig AI</a></li>\n                        <li><a href="/vad-ar-ai-verktyg.html" class="text-slate-500 hover:text-indigo-600">Vad är AI-verktyg?</a></li>'

        # Footer 2
        old_foot2 = '<li><a href="/vad-ar-ai-verktyg.html" class="text-gray-500 hover:text-indigo-600">Vad är AI-verktyg?</a></li>'
        new_foot2 = '<li><a href="/lar-dig-ai.html" class="text-gray-500 hover:text-indigo-600">Lär dig AI</a></li>\n                        <li><a href="/vad-ar-ai-verktyg.html" class="text-gray-500 hover:text-indigo-600">Vad är AI-verktyg?</a></li>'


        content = content.replace(old_header, new_header)
        content = content.replace(old_mobile, new_mobile)
        content = content.replace(old_desk_alt, new_desk_alt)
        content = content.replace(old_mob_alt, new_mob_alt)
        content = content.replace(old_foot1, new_foot1)
        content = content.replace(old_foot2, new_foot2)

        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")
