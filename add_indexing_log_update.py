import re
import datetime

log_file = "/data/workspace/projects/ai-verktygskistan/INDEXING_LOG.md"

with open(log_file, "r") as f:
    content = f.read()

# ai-svenska-foretag-rapport.html still unknown
today = datetime.datetime.now().strftime("%Y-%m-%d")

# content = re.sub(
#     r'(https://aiverktygsladan.se/ai-svenska-foretag-rapport.html \| URL is unknown to Google \|) \d{4}-\d{2}-\d{2} (\| Länkad i sitemap\. Behöver indexeras manuellt av Sim\.)',
#     rf'\1 {today} \2',
#     content
# )

with open(log_file, "w") as f:
    f.write(content)

