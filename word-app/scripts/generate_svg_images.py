import os
import time

vocabulary = {
    'furniture': ['sofa', 'table', 'chair', 'bed', 'desk', 'bookshelf', 'wardrobe', 'lamp', 'cabinet', 'stool', 'cupboard', 'drawer'],
    'appliances': ['refrigerator', 'television', 'washing', 'microwave', 'oven', 'dishwasher', 'airconditioner', 'computer', 'fan', 'heater', 'coffee', 'toaster'],
    'vehicles': ['car', 'bus', 'train', 'plane', 'bicycle', 'motorcycle', 'ship', 'boat', 'taxi', 'subway', 'truck', 'helicopter'],
    'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'parrot', 'turtle', 'snake', 'elephant', 'monkey', 'panda'],
    'fruits': ['apple', 'banana', 'orange', 'grape', 'watermelon', 'strawberry', 'pineapple', 'mango', 'peach', 'pear', 'lemon', 'cherry']
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

category_colors = {
    'furniture': {'bg': '#FFF5E6', 'accent': '#FF8C42', 'text': '#D35400'},
    'appliances': {'bg': '#E8F4FD', 'accent': '#3498DB', 'text': '#2471A3'},
    'vehicles': {'bg': '#E8E8E8', 'accent': '#566573', 'text': '#2C3E50'},
    'animals': {'bg': '#E8F8E8', 'accent': '#27AE60', 'text': '#1E8449'},
    'fruits': {'bg': '#FDEBD0', 'accent': '#E74C3C', 'text': '#C0392B'}
}

def create_svg_image(word, category):
    colors = category_colors.get(category, category_colors['furniture'])
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="400" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors['bg']};stop-opacity:1" />
      <stop offset="100%" style="stop-color:white;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000" flood-opacity="0.1"/>
    </filter>
  </defs>
  
  <rect width="400" height="400" fill="url(#bgGrad)"/>
  
  <g filter="url(#shadow)" transform="translate(200, 160)">
    <circle cx="0" cy="0" r="90" fill="white" opacity="0.95"/>
    <circle cx="0" cy="0" r="85" fill="{colors['bg']}" stroke="{colors['accent']}" stroke-width="2"/>
  </g>
  
  <text x="200" y="160" font-family="'Segoe UI', Arial, sans-serif" font-size="56" 
        font-weight="bold" fill="{colors['accent']}" text-anchor="middle" 
        dominant-baseline="middle" style="text-transform: capitalize;">
    {word[0].upper()}
  </text>
  
  <text x="200" y="310" font-family="'Segoe UI', Arial, sans-serif" font-size="24" 
        font-weight="600" fill="{colors['text']}" text-anchor="middle"
        style="text-transform: capitalize;">
    {word}
  </text>
  
  <rect x="50" y="350" width="300" height="4" rx="2" fill="{colors['accent']}" opacity="0.3"/>
</svg>'''
    
    filename = f"{word}.svg"
    filepath = os.path.join(save_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    
    return filename

total = 0
success = 0

print("=" * 70)
print("生成SVG词汇图片...")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    colors = category_colors[category]
    print(f"   配色: 背景={colors['bg']}, 主色={colors['accent']}")
    
    for word in words:
        total += 1
        try:
            filename = create_svg_image(word, category)
            success += 1
            print(f"   ✅ {word}")
        except Exception as e:
            print(f"   ❌ {word}: {e}")

print("\n" + "=" * 70)
print(f"生成完成: {success}/{total} 个SVG图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
