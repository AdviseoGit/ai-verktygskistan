import xml.etree.ElementTree as ET
from datetime import datetime

tree = ET.parse('/data/workspace/projects/ai-verktygskistan/static/sitemap.xml')
root = tree.getroot()

namespaces = {'': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')

today = datetime.now().strftime('%Y-%m-%d')

for url in root.findall('url', namespaces):
    loc = url.find('loc', namespaces).text
    if 'gratis-ai-verktyg.html' in loc or loc.endswith('se/'):
        lastmod = url.find('lastmod', namespaces)
        if lastmod is not None:
            lastmod.text = today
        else:
            new_lastmod = ET.SubElement(url, 'lastmod')
            new_lastmod.text = today

tree.write('/data/workspace/projects/ai-verktygskistan/static/sitemap.xml', encoding='utf-8', xml_declaration=True)
print("Sitemap updated.")
