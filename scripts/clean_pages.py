import glob
import os

files = glob.glob("/data/workspace/projects/ai-verktygskistan/static/*.html")
for f in files:
    with open(f, 'r') as file:
        content = file.read()
    if 'extern[snabel-a]exempel.se' in content:
        content = content.replace('extern[snabel-a]exempel.se', 'extern@exempel.se')
        with open(f, 'w') as file:
            file.write(content)
