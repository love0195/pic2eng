#!/bin/bash
cd /workspace/word-app/public/images

declare -A PROMPTS=(
  ["dishwasher"]="dishwasher machine white cartoon style clean flat design simple icon"
  ["iron"]="clothes iron pressing iron cartoon style flat design simple icon"
  ["hairdryer"]="hair dryer pink purple cartoon style flat design simple icon"
  ["speaker"]="audio speaker bluetooth cartoon style flat design simple icon"
  ["charger"]="phone charger cable plug cartoon style flat design simple icon"
  ["battery"]="aa battery pack cartoon style flat design simple icon"
  ["electric_pot"]="electric pressure cooker silver cartoon style flat design simple icon"
  ["electric_blanket"]="electric blanket warm red cartoon style flat design simple icon"
  ["heater"]="room heater warming device cartoon style flat design simple icon"
)

for word in "${!PROMPTS[@]}"; do
  prompt="${PROMPTS[$word]}"
  encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$prompt'))")
  url="https://image.pollinations.ai/prompt/${encoded}?width=512&height=512&seed=42&nologo=true"

  echo "Generating: $word"
  curl -s -A "Mozilla/5.0" -o "${word}.jpg" "$url"
  sleep 5
done

echo "Done!"
