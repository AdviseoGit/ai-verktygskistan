import xml.etree.ElementTree as ET
from datetime import datetime

sitemap_path = "/data/workspace/projects/ai-verktygskistan/static/sitemap.xml"
tree = ET.parse(sitemap_path)
root = tree.getroot()
namespace = {"": "http://www.sitemaps.org/schemas/sitemap/0.9"}
ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")

# Check if ai-ordlista.html is already in the sitemap
ordlista_url = "https://aiverktygsladan.se/ai-ordlista.html"
found = False
for url in root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
    loc = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    if loc is not None and loc.text == ordlista_url:
        found = True
        break

if not found:
    new_url = ET.Element("url")
    loc = ET.SubElement(new_url, "loc")
    loc.text = ordlista_url
    lastmod = ET.SubElement(new_url, "lastmod")
    lastmod.text = "2026-07-04"
    priority = ET.SubElement(new_url, "priority")
    priority.text = "0.8"
    root.append(new_url)
    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
    print("Added ai-ordlista.html to sitemap")
else:
    print("ai-ordlista.html already in sitemap")
