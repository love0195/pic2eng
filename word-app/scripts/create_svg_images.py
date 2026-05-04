import urllib.request
import time
import os

vocabulary = {
    'furniture': ['sofa', 'table', 'chair', 'bed', 'desk', 'bookshelf', 'wardrobe', 'lamp', 'cabinet', 'stool', 'cupboard', 'drawer'],
    'appliances': ['refrigerator', 'television', 'washing machine', 'microwave oven', 'oven', 'dishwasher', 'air conditioner', 'computer', 'fan', 'heater', 'coffee maker', 'toaster'],
    'vehicles': ['car', 'bus', 'train', 'airplane', 'bicycle', 'motorcycle', 'ship', 'boat', 'taxi', 'subway', 'truck', 'helicopter'],
    'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'parrot', 'turtle', 'snake', 'elephant', 'monkey', 'panda'],
    'fruits': ['apple', 'banana', 'orange', 'grape', 'watermelon', 'strawberry', 'pineapple', 'mango', 'peach', 'pear', 'lemon', 'cherry']
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

def create_simple_svg_image(word, filepath):
    svg_template = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#f9fafc"/>
  <circle cx="200" cy="160" r="100" fill="#e5e7eb" stroke="#d1d5db" stroke-width="3"/>
  <text x="200" y="320" font-family="Arial, sans-serif" font-size="24" fill="#6b7280" text-anchor="middle">{word.capitalize()}</text>
  <text x="200" y="360" font-family="Arial, sans-serif" font-size="16" fill="#9ca3af" text-anchor="middle">Image</text>
</svg>'''
    
    with open(filepath.replace('.jpg', '.svg'), 'w', encoding='utf-8') as f:
        f.write(svg_template)
    
    print(f"✅ Created SVG: {word}")
    return True

total = 0
success = 0

print("=" * 70)
print("创建SVG占位图片...")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    for word in words:
        total += 1
        safe_word = word.replace(' ', '_')
        filepath = os.path.join(save_dir, f"{safe_word}.jpg")
        
        if os.path.exists(filepath):
            print(f"⏭️  Skip: {word} (already exists)")
            success += 1
            continue
        
        if create_simple_svg_image(word, filepath):
            success += 1

print("\n" + "=" * 70)
print(f"创建完成: {success}/{total} 个SVG图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
