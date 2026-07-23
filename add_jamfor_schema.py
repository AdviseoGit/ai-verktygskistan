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
          "name": "Vad är skillnaden mellan ChatGPT och Claude?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Claude är ofta bättre på att skriva naturlig text och hantera stora dokument (upp till 200K tokens), medan ChatGPT (GPT-4) är bättre på kodning, webbsökning och dataanalys med inbyggda verktyg."
          }
        },
        {
          "@type": "Question",
          "name": "Vilket är bäst av Midjourney och DALL-E 3?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Midjourney ger överlägsen konstnärlig kvalitet och fotorealism, men kräver Discord. DALL-E 3 är mycket lättare att använda (inbyggt i ChatGPT) och följer instruktioner bättre för att skapa exakta scener."
          }
        },
        {
          "@type": "Question",
          "name": "Vilka AI-verktyg är bäst för företag?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "För företag rekommenderas ofta Enterprise-versioner (som ChatGPT Enterprise eller Claude for Work) eftersom dessa vanligtvis inte tränar sina modeller på företagets data."
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

update_schema('/data/workspace/projects/ai-verktygskistan/static/ai-jamfor.html')
