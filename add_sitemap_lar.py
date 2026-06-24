import xml.etree.ElementTree as ET
from datetime import datetime

sitemap_path = "/data/workspace/projects/ai-verktygskistan/static/sitemap.xml"

# Parse the existing sitemap
ET.register_namespace('', "http://www.sitemaps.org/schemas/sitemap/0.9")
tree = ET.parse(sitemap_path)
root = tree.getroot()

# Check if URL already exists
namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
exists = False
for url in root.findall('ns:url', namespace):
    loc = url.find('ns:loc', namespace)
    if loc is not None and loc.text == "https://aiverktygsladan.se/lar-dig-ai.html":
        exists = True
        break

if not exists:
    # Create new url element
    url_element = ET.Element("url")
    
    loc = ET.SubElement(url_element, "loc")
    loc.text = "https://aiverktygsladan.se/lar-dig-ai.html"
    
    lastmod = ET.SubElement(url_element, "lastmod")
    lastmod.text = datetime.now().strftime("%Y-%m-%d")
    
    priority = ET.SubElement(url_element, "priority")
    priority.text = "0.9"
    
    root.append(url_element)
    
    # Write back to file
    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
    print("Added lar-dig-ai.html to sitemap.")
else:
    print("URL already in sitemap.")
