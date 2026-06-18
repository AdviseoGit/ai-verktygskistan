#!/bin/bash
# Check if Udio is already in tools.json
if grep -q "Udio" /data/workspace/projects/ai-verktygskistan/static/tools.json; then
  echo "Udio exists"
else
  echo "Adding Udio"
  # This requires careful json editing. Let's do it via python.
fi
