import xml.etree.ElementTree as ET
import os

sitemap_path = "/data/workspace/projects/ai-verktygskistan/static/sitemap.xml"

ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")
tree = ET.parse(sitemap_path)
root = tree.getroot()

namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
url_exists = False

for url in root.findall(f"{namespace}url"):
    loc = url.find(f"{namespace}loc")
    if loc is not None and loc.text == "https://aiverktygsladan.se/bygg-med-ai.html":
        url_exists = True
        break

if not url_exists:
    url_el = ET.SubElement(root, "url")
    loc_el = ET.SubElement(url_el, "loc")
    loc_el.text = "https://aiverktygsladan.se/bygg-med-ai.html"
    
    lastmod_el = ET.SubElement(url_el, "lastmod")
    lastmod_el.text = "2026-06-27"
    
    priority_el = ET.SubElement(url_el, "priority")
    priority_el.text = "0.9"

    ET.indent(tree, space="  ", level=0)
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)
    print("Added bygg-med-ai.html to sitemap.")
else:
    print("bygg-med-ai.html already in sitemap.")
