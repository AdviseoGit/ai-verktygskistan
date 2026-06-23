import xml.etree.ElementTree as ET
from xml.dom import minidom
import datetime

sitemap_path = "/data/workspace/projects/ai-verktygskistan/static/sitemap.xml"
tree = ET.parse(sitemap_path)
root = tree.getroot()

namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace('', namespace)

new_url = ET.Element(f"{{{namespace}}}url")
loc = ET.SubElement(new_url, f"{{{namespace}}}loc")
loc.text = "https://aiverktygsladan.se/ai-program.html"
lastmod = ET.SubElement(new_url, f"{{{namespace}}}lastmod")
lastmod.text = datetime.datetime.now().strftime("%Y-%m-%d")
priority = ET.SubElement(new_url, f"{{{namespace}}}priority")
priority.text = "0.9"

root.append(new_url)

xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
with open(sitemap_path, "w") as f:
    f.write(xmlstr)

print("Added ai-program.html to sitemap")
