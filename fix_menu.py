import os
import glob
import re

html_files = glob.glob('/data/workspace/projects/ai-verktygskistan/static/*.html')

new_nav_desktop = '''            <div class="hidden md:flex space-x-6 items-center">
                <a href="/ai-verktyg.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Verktyg</a>
                <div class="relative group">
                    <button class="text-sm font-medium hover:text-indigo-600 transition-colors inline-flex items-center">
                        Guider & Info
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </button>
                    <div class="absolute left-0 mt-2 w-48 bg-white border border-slate-200 rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                        <a href="/lar-dig-ai.html" class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 hover:text-indigo-600">Lär dig AI</a>
                        <a href="/bygg-med-ai.html" class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 hover:text-indigo-600">Bygg med AI</a>
                        <a href="/skapa-med-ai.html" class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 hover:text-indigo-600">Skapa med AI</a>
                        <a href="/prompt-guide.html" class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 hover:text-indigo-600">Prompt Guide</a>
                        <a href="/vad-ar-ai-verktyg.html" class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 hover:text-indigo-600">Vad är AI-verktyg?</a>
                        <a href="/ai-ordlista.html" class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 hover:text-indigo-600">AI-ordlista</a>
                    </div>
                </div>
                <a href="/ai-jamfor.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Jämför</a>
                <a href="/hitta-ratt-ai.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Hitta rätt AI</a>
                <div class="relative group">
                    <button class="text-sm font-medium hover:text-indigo-600 transition-colors inline-flex items-center">
                        Data & ROI
                        <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </button>
                    <div class="absolute left-0 mt-2 w-48 bg-white border border-slate-200 rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                        <a href="/ai-kalkylator.html" class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 hover:text-indigo-600">AI-Kalkylatorn</a>
                        <a href="/ai-svenska-foretag-rapport.html" class="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 hover:text-indigo-600">Rapport 2026</a>
                    </div>
                </div>
            </div>'''

new_nav_mobile = '''        <div id="mobile-menu" class="hidden md:hidden mt-4 pb-4 border-t border-slate-100 flex flex-col space-y-4 pt-4 px-6 bg-white absolute w-full left-0 shadow-lg z-50">
            <a href="/ai-verktyg.html" class="hover:text-indigo-600 transition-colors font-medium">Verktyg</a>
            <a href="/ai-jamfor.html" class="hover:text-indigo-600 transition-colors font-medium">Jämför Verktyg</a>
            <a href="/hitta-ratt-ai.html" class="hover:text-indigo-600 transition-colors font-medium">Hitta rätt AI</a>
            <div class="border-t border-slate-100 pt-2 mt-2">
                <span class="text-xs text-slate-500 uppercase tracking-wider font-semibold">Guider</span>
                <a href="/lar-dig-ai.html" class="block mt-2 hover:text-indigo-600 transition-colors">Lär dig AI</a>
                <a href="/bygg-med-ai.html" class="block mt-2 hover:text-indigo-600 transition-colors">Bygg med AI</a>
                <a href="/skapa-med-ai.html" class="block mt-2 hover:text-indigo-600 transition-colors">Skapa med AI</a>
                <a href="/prompt-guide.html" class="block mt-2 hover:text-indigo-600 transition-colors">Prompt Guide</a>
            </div>
            <div class="border-t border-slate-100 pt-2 mt-2">
                <span class="text-xs text-slate-500 uppercase tracking-wider font-semibold">Data & ROI</span>
                <a href="/ai-kalkylator.html" class="block mt-2 hover:text-indigo-600 transition-colors">AI-Kalkylatorn</a>
                <a href="/ai-svenska-foretag-rapport.html" class="block mt-2 hover:text-indigo-600 transition-colors">Rapport 2026</a>
            </div>
        </div>'''

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace desktop nav
    content = re.sub(r'<div class="hidden md:flex space-x-6 items-center">.*?</div>\s*<button id="mobile-menu-btn"', 
                     new_nav_desktop + '\n            <button id="mobile-menu-btn"', 
                     content, flags=re.DOTALL)
    
    # Replace mobile nav
    content = re.sub(r'<div id="mobile-menu" class="hidden md:hidden[^>]*>.*?</div>', 
                     new_nav_mobile, 
                     content, flags=re.DOTALL)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {file}")
