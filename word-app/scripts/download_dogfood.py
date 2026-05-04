import os

vocabulary = {
    'furniture': ['sofa', 'table', 'chair', 'bed', 'desk', 'bookshelf', 'wardrobe', 'lamp', 'cabinet', 'stool', 'cupboard', 'drawer'],
    'appliances': ['refrigerator', 'television', 'washing', 'microwave', 'oven', 'dishwasher', 'airconditioner', 'computer', 'cabinet', 'heater', 'coffee', 'toaster'],
    'vehicles': ['car', 'bus', 'train', 'plane', 'bicycle', 'motorcycle', 'ship', 'boat', 'taxi', 'subway', 'truck', 'helicopter'],
    'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'parrot', 'turtle', 'snake', 'elephant', 'monkey', 'panda'],
    'fruits': ['apple', 'banana', 'orange', 'grape', 'watermelon', 'strawberry', 'pineapple', 'mango', 'peach', 'pear', 'lemon', 'cherry']
}

emoji_map = {
    'sofa': '🛋️', 'table': '🪑', 'chair': '🪑', 'bed': '🛏️', 
    'desk': '📚', 'bookshelf': '📚', 'wardrobe': '🚪', 'lamp': '💡', 
    'cabinet': '🗄️', 'stool': '🪑', 'cupboard': '🍽️', 'drawer': '📦',
    'refrigerator': '❄️', 'television': '📺', 'washing': '🧺', 'microwave': '🔌', 
    'oven': '🔥', 'dishwasher': '🧽', 'airconditioner': '❄️', 
    'computer': '💻', 'fan': '🌀', 'heater': '🔥', 'coffee': '☕', 'toaster': '🍞',
    'car': '🚗', 'bus': '🚌', 'train': '🚂', 'plane': '✈️', 'bicycle': '🚲', 
    'motorcycle': '🏍️', 'ship': '🚢', 'boat': '🚤', 'taxi': '🚕', 'subway': '🚇', 
    'truck': '🚚', 'helicopter': '🚁',
    'dog': '🐶', 'cat': '🐱', 'bird': '🐦', 'fish': '🐟', 'rabbit': '🐰', 
    'hamster': '🐹', 'parrot': '🦜', 'turtle': '🐢', 'snake': '🐍', 
    'elephant': '🐘', 'monkey': '🐒', 'panda': '🐼',
    'apple': '🍎', 'banana': '🍌', 'orange': '🍊', 'grape': '🍇', 
    'watermelon': '🍉', 'strawberry': '🍓', 'pineapple': '🍍', 'mango': '🥭', 
    'peach': '🍑', 'pear': '🍐', 'lemon': '🍋', 'cherry': '🍒'
}

category_colors = {
    'furniture': {'bg': '#FFF5E6', 'accent': '#FF8C42', 'text': '#D35400'},
    'appliances': {'bg': '#E8F4FD', 'accent': '#3498DB', 'text': '#2471A3'},
    'vehicles': {'bg': '#E8E8E8', 'accent': '#566573', 'text': '#2C3E50'},
    'animals': {'bg': '#E8F8E8', 'accent': '#27AE60', 'text': '#1E8449'},
    'fruits': {'bg': '#FDEBD0', 'accent': '#E74C3C', 'text': '#C0392B'}
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

def create_emoji_image(word, category):
    emoji = emoji_map.get(word, '📷')
    colors = category_colors[category]

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{colors['bg']}"/>
      <stop offset="100%" style="stop-color:#FFFFFF"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#000" flood-opacity="0.15"/>
    </filter>
  </defs>
  
  <rect width="400" height="400" fill="url(#bg)"/>
  
  <g filter="url(#shadow)">
    <rect x="25" y="25" width="350" height="350" rx="30" fill="#FFFFFF" opacity="0.9"/>
  </g>
  
  <text x="200" y="200" font-family="Arial, sans-serif" font-size="120" 
        text-anchor="middle" dominant-baseline="middle">{emoji}</text>
  
  <text x="200" y="330" font-family="'Segoe UI', Arial, sans-serif" 
        font-size="36" font-weight="700" 
        fill="{colors['text']}" text-anchor="middle" 
        style="text-transform: capitalize;">{word}</text>
  
  <rect x="50" y="360" width="300" height="4" rx="2" fill="{colors['accent']}" opacity="0.5"/>
</svg>'''
    
    filename = f"{word}.svg"
    filepath = os.path.join(save_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)
    
    return filename

total = 0
success = 0

print("=" * 70)
print("生成可爱的emoji+文字图片...")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    for word in words:
        total += 1
        try:
            filename = create_emoji_image(word, category)
            success += 1
            print(f"   ✅ {word} {emoji_map.get(word, '')}")
        except Exception as e:
            print(f"   ❌ {word}")

print("\n" + "=" * 70)
print(f"生成完成: {success}/{total} 张图片")
print("=" * 70)
