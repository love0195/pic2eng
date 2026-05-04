import urllib.request
import json
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

def download_with_pexels(word):
    safe_word = word.replace(' ', '_')
    filepath = os.path.join(save_dir, f"{safe_word}.jpg")
    
    if os.path.exists(filepath):
        print(f"⏭️  Skip: {word} (already exists)")
        return True
    
    try:
        search_url = f"https://api.pexels.com/v1/search?query={word.replace(' ', '+')}+clipart&per_page=1"
        
        headers = {
            'Authorization': 'YOUR_PEXELS_API_KEY',
            'User-Agent': 'Mozilla/5.0'
        }
        
        req = urllib.request.Request(search_url, headers=headers)
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode())
        
        if data['photos']:
            photo = data['photos'][0]
            img_url = photo['src']['large']
            
            img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(img_req, timeout=30) as img_response:
                content = img_response.read()
                
                with open(filepath, 'wb') as f:
                    f.write(content)
                
                print(f"✅ Downloaded: {word} from Pexels")
                return True
        
    except Exception as e:
        print(f"⚠️  Pexels failed for {word}: {e}")
    
    return False

def create_colored_placeholder(word):
    safe_word = word.replace(' ', '_')
    filepath = os.path.join(save_dir, f"{safe_word}.jpg")
    
    colors = {
        'furniture': ('#8B4513', '#DEB887'),
        'appliances': ('#4682B4', '#87CEEB'),
        'vehicles': ('#2F4F4F', '#708090'),
        'animals': ('#228B22', '#90EE90'),
        'fruits': ('#FF6347', '#FFA07A')
    }
    
    category = None
    for cat in vocabulary:
        if word in vocabulary[cat]:
            category = cat
            break
    
    bg_color, fg_color = colors.get(category, ('#9370DB', '#E6E6FA'))
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="{bg_color}" rx="20"/>
  <circle cx="200" cy="180" r="90" fill="white" opacity="0.9"/>
  <text x="200" y="175" font-family="Arial Black, sans-serif" font-size="32" fill="{fg_color}" text-anchor="middle" font-weight="bold">{word.capitalize()}</text>
  <text x="200" y="300" font-family="Arial, sans-serif" font-size="20" fill="white" text-anchor="middle">📷 Image</text>
</svg>'''
    
    with open(filepath.replace('.jpg', '.svg'), 'w', encoding='utf-8') as f:
        f.write(svg)
    
    print(f"✅ Created placeholder: {word} ({category or 'default'} style)")
    return True

total = 0
success = 0

print("=" * 70)
print("开始处理图片...")
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
        
        if download_with_pexels(word):
            success += 1
        else:
            if create_colored_placeholder(word):
                success += 1
        
        time.sleep(0.3)

print("\n" + "=" * 70)
print(f"完成: {success}/{total} 个图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
