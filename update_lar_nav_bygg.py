import re
import os

filepath = "/data/workspace/projects/ai-verktygskistan/static/lar-dig-ai.html"
with open(filepath, 'r') as f:
    content = f.read()

# Desktop nav
content = re.sub(
    r'(<a href="/lar-dig-ai\.html" class="border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">Lär dig AI</a>)',
    r'\1\n                        <a href="/bygg-med-ai.html" class="border-transparent text-gray-500 hover:text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">Bygg med AI</a>',
    content
)

# Mobile nav
content = re.sub(
    r'(<a href="/lar-dig-ai\.html" class="bg-indigo-50 border-indigo-500 text-indigo-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">Lär dig AI</a>)',
    r'\1\n                <a href="/bygg-med-ai.html" class="border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700 block pl-3 pr-4 py-2 border-l-4 text-base font-medium">Bygg med AI</a>',
    content
)

# Footer
content = re.sub(
    r'(<li><a href="/lar-dig-ai\.html" class="text-gray-500 hover:text-indigo-600">Lär dig AI</a></li>)',
    r'\1\n                        <li><a href="/bygg-med-ai.html" class="text-gray-500 hover:text-indigo-600">Bygg med AI</a></li>',
    content
)

with open(filepath, 'w') as f:
    f.write(content)
print("Updated lar-dig-ai.html")
