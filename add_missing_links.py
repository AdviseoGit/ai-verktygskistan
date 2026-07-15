import os
import re

STATIC_DIR = "/data/workspace/projects/ai-verktygskistan/static"

def link_in_file(filepath, url):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return url in content

def add_link_to_nav(filepath, url, label):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Desktop nav
    desktop_pattern = r'(<a href="/lar-dig-ai\.html" class="text-sm font-medium hover:text-indigo-600 transition-colors">Lär dig AI</a>)'
    desktop_replacement = f'\\1\n                <a href="{url}" class="text-sm font-medium hover:text-indigo-600 transition-colors">{label}</a>'
    content = re.sub(desktop_pattern, desktop_replacement, content)

    # Mobile nav
    mobile_pattern = r'(<a href="/lar-dig-ai\.html" class="hover:text-indigo-600 transition-colors font-medium">Lär dig AI</a>)'
    mobile_replacement = f'\\1\n             <a href="{url}" class="hover:text-indigo-600 transition-colors font-medium">{label}</a>'
    content = re.sub(mobile_pattern, mobile_replacement, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for filename in os.listdir(STATIC_DIR):
    if filename.endswith(".html"):
        filepath = os.path.join(STATIC_DIR, filename)
        
        if not link_in_file(filepath, "/skapa-med-ai.html"):
            add_link_to_nav(filepath, "/skapa-med-ai.html", "Skapa med AI")
        if not link_in_file(filepath, "/prompt-guide.html"):
            add_link_to_nav(filepath, "/prompt-guide.html", "Prompt Guide")
        if not link_in_file(filepath, "/ai-ordlista.html"):
            add_link_to_nav(filepath, "/ai-ordlista.html", "AI Ordlista")
            
print("Done adding links.")
