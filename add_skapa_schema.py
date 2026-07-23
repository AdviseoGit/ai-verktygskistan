import json

def update_schema(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    if "application/ld+json" not in content:
        schema = """
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Vilka är de bästa AI-verktygen för att skapa bilder?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "De mest populära AI-verktygen för bildgenerering är Midjourney (bäst kvalitet), DALL-E 3 (enklast, inbyggt i ChatGPT) och Stable Diffusion (mest kontroll, open source)."
          }
        },
        {
          "@type": "Question",
          "name": "Kan AI skapa musik?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Ja, verktyg som Suno AI och Udio kan generera kompletta låtar med sång, melodi och instrument baserat på en enkel textbeskrivning."
          }
        },
        {
          "@type": "Question",
          "name": "Vilket är det bästa verktyget för att klona röster?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "ElevenLabs anses allmänt vara det ledande verktyget för röstkloning och talsyntes, med mycket hög realism och känsla."
          }
        }
      ]
    }
    </script>
"""
        content = content.replace("</head>", f"{schema}\n</head>")
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Added schema to {filename}")
    else:
        print(f"Schema already in {filename}")

update_schema('/data/workspace/projects/ai-verktygskistan/static/skapa-med-ai.html')
