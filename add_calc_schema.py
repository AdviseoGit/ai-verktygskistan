import json

def update_schema(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    if "application/ld+json" not in content:
        schema = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "AI Kalkylator - Beräkna ROI för AI-investering",
      "applicationCategory": "BusinessApplication",
      "operatingSystem": "Web",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "SEK"
      },
      "description": "Gratis AI-kalkylator för att beräkna potentiell tidsbesparing och avkastning (ROI) för ditt företag vid implementering av AI-verktyg."
    }
    </script>
"""
        content = content.replace("</head>", f"{schema}\n</head>")
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Added schema to {filename}")
    else:
        print(f"Schema already in {filename}")

update_schema('/data/workspace/projects/ai-verktygskistan/static/ai-kalkylator.html')
