#!/bin/bash
# Check if ai-verktyg.html has Tailwind mobile nav or old nav
if grep -q "text-4xl font-bold text-gray-900" /data/workspace/projects/ai-verktygskistan/static/ai-verktyg.html; then
  echo "Old design detected on ai-verktyg.html"
else
  echo "New design detected"
fi
