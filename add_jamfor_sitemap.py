import re

with open('static/sitemap.xml', 'r') as f:
    content = f.read()

new_url = """  <url>
    <loc>https://aiverktygsladan.se/ai-jamfor.html</loc>
    <lastmod>2026-06-29</lastmod>
    <priority>0.8</priority>
  </url>
"""

if "ai-jamfor.html" not in content:
    content = content.replace("</urlset>", new_url + "</urlset>")
    with open('static/sitemap.xml', 'w') as f:
        f.write(content)
