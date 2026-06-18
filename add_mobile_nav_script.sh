#!/bin/bash
# Adding JS for mobile nav to index.html
sed -i 's/<\/body>/<script>\n        document.getElementById("mobile-menu-btn").addEventListener("click", function() {\n            document.getElementById("mobile-menu").classList.toggle("hidden");\n        });\n        document.querySelectorAll(".mobile-nav-link").forEach(link => {\n            link.addEventListener("click", () => {\n                document.getElementById("mobile-menu").classList.add("hidden");\n            });\n        });\n    <\/script>\n<\/body>/g' /data/workspace/projects/ai-verktygskistan/static/index.html
