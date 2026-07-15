import re
with open("/data/workspace/projects/ai-verktygskistan/INDEXING_LOG.md", "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(
    r'https://aiverktygsladan\.se/skapa-med-ai\.html.*?(\n|$)',
    r'https://aiverktygsladan.se/skapa-med-ai.html | URL is unknown to Google | 2026-07-13 | Länkad i nav + sitemap (2026-07-09). Behöver indexeras manuellt av Sim.\n',
    content
)
content = re.sub(
    r'https://aiverktygsladan\.se/prompt-guide\.html.*?(\n|$)',
    r'https://aiverktygsladan.se/prompt-guide.html | URL is unknown to Google | 2026-07-13 | Länkad i nav + sitemap (2026-07-08). Behöver indexeras manuellt av Sim.\n',
    content
)
content = re.sub(
    r'https://aiverktygsladan\.se/ai-ordlista\.html.*?(\n|$)',
    r'https://aiverktygsladan.se/ai-ordlista.html | URL is unknown to Google | 2026-07-13 | Länkad i nav + sitemap (2026-07-04). Behöver indexeras manuellt av Sim.\n',
    content
)
content = re.sub(
    r'https://aiverktygsladan\.se/ai-kalkylator\.html.*?(\n|$)',
    r'https://aiverktygsladan.se/ai-kalkylator.html | URL is unknown to Google | 2026-07-13 | Länkad i nav + sitemap (2026-06-21). Behöver indexeras manuellt av Sim.\n',
    content
)
content = re.sub(
    r'https://aiverktygsladan\.se/ai-jamfor\.html.*?(\n|$)',
    r'https://aiverktygsladan.se/ai-jamfor.html | URL is unknown to Google | 2026-07-13 | Länkad i nav + sitemap (2026-06-29). Behöver indexeras manuellt av Sim.\n',
    content
)
content = re.sub(
    r'https://aiverktygsladan\.se/ai-verktyg\.html.*?(\n|$)',
    r'',
    content
)
content += "https://aiverktygsladan.se/ai-verktyg.html | URL is unknown to Google | 2026-07-13 | Länkad i nav + sitemap (2026-06-15). Behöver indexeras manuellt av Sim.\n"

content = re.sub(
    r'https://aiverktygsladan\.se/ai-program\.html.*?(\n|$)',
    r'',
    content
)
content += "https://aiverktygsladan.se/ai-program.html | URL is unknown to Google | 2026-07-13 | Länkad i nav + sitemap (2026-06-23). Behöver indexeras manuellt av Sim.\n"

content = re.sub(
    r'https://aiverktygsladan\.se/lar-dig-ai\.html.*?(\n|$)',
    r'',
    content
)
content += "https://aiverktygsladan.se/lar-dig-ai.html | URL is unknown to Google | 2026-07-13 | Länkad i nav + sitemap (2026-06-24). Behöver indexeras manuellt av Sim.\n"

with open("/data/workspace/projects/ai-verktygskistan/INDEXING_LOG.md", "w", encoding="utf-8") as f:
    f.write(content)
