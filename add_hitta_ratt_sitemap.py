import os

sitemap_path = '/data/workspace/projects/ai-verktygskistan/static/sitemap.xml'

with open(sitemap_path, 'r', encoding='utf-8') as f:
    content = f.read()

if '<loc>https://aiverktygsladan.se/hitta-ratt-ai.html</loc>' not in content:
    new_url = """    <url>
        <loc>https://aiverktygsladan.se/hitta-ratt-ai.html</loc>
        <lastmod>2026-07-12</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
</urlset>"""
    content = content.replace('</urlset>', new_url)
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added to sitemap")
else:
    print("Already in sitemap")
