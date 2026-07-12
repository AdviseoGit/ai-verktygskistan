import json
import os

files = {
    'ai-ordlista.html': 'ai-ordlista-faq.json',
    'lar-dig-ai.html': 'lar-dig-ai-faq.json'
}

base_dir = '/data/workspace/projects/ai-verktygskistan/static/'

for html_file, json_file in files.items():
    html_path = os.path.join(base_dir, html_file)
    json_path = os.path.join(base_dir, json_file)
    
    with open(json_path, 'r', encoding='utf-8') as f:
        schema_data = f.read()
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    old_script = f'<script type="application/ld+json" src="/static/{json_file}"></script>'
    new_script = f'<script type="application/ld+json">\n{schema_data}\n</script>'
    
    if old_script in html_content:
        html_content = html_content.replace(old_script, new_script)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Updated {html_file}")
    else:
        print(f"Could not find {old_script} in {html_file}")
