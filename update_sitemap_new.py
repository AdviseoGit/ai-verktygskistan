import os
from datetime import datetime
import xml.etree.ElementTree as ET

sitemap_path = "/data/workspace/projects/ai-verktygskistan/static/sitemap.xml"
tree = ET.parse(sitemap_path)
root = tree.getroot()

namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
ET.register_namespace('', namespace['ns'])

urls = [
    ("https://aiverktygsladan.se/ai-kalkylator.html", "0.9"),
    ("https://aiverktygsladan.se/ai-for-hr.html", "0.8"),
    ("https://aiverktygsladan.se/om-sajten.html", "0.5")
]

today = datetime.now().strftime("%Y-%m-%d")

existing_urls = []
for url in root.findall('ns:url', namespace):
    loc = url.find('ns:loc', namespace).text
    existing_urls.append(loc)

for loc, priority in urls:
    if loc not in existing_urls:
        url_elem = ET.SubElement(root, "url")
        loc_elem = ET.SubElement(url_elem, "loc")
        loc_elem.text = loc
        lastmod_elem = ET.SubElement(url_elem, "lastmod")
        lastmod_elem.text = today
        priority_elem = ET.SubElement(url_elem, "priority")
        priority_elem.text = priority

tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
print("Added new URLs to sitemap.")
