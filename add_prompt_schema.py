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
          "name": "Hur skriver man en bra prompt?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "En bra prompt är specifik, ger kontext och anger tydligt vilket format och tonläge du vill ha. Ett vanligt ramverk är 'Roll + Uppgift + Kontext + Format'."
          }
        },
        {
          "@type": "Question",
          "name": "Vad är skillnaden mellan ChatGPT och Claude när det gäller prompts?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Claude svarar ofta bättre på XML-taggar för struktur (t.ex. <instruktioner>), medan ChatGPT är stark på allmänna instruktioner och kan använda verktyg (sökning/kod) bättre."
          }
        },
        {
          "@type": "Question",
          "name": "Varför får jag dåliga svar från AI?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Oftast beror det på för vaga instruktioner (GIGO - Garbage In, Garbage Out). AI:n behöver veta din målgrupp, syftet och exakt vad du vill uppnå."
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

update_schema('/data/workspace/projects/ai-verktygskistan/static/prompt-guide.html')
