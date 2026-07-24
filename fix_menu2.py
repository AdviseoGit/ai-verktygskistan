import os
import glob
import re

html_files = glob.glob('/data/workspace/projects/ai-verktygskistan/static/*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove cdn-cgi email protection link which causes 404
    content = content.replace('href="/cdn-cgi/l/email-protection#"', 'href="mailto:simon@adviseo.se"')
    content = content.replace('href="/cdn-cgi/l/email-protection"', 'href="mailto:simon@adviseo.se"')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {file}")
