import urllib.request
import urllib.parse
import time
import os

vocabulary = {
    'furniture': ['sofa', 'table', 'chair', 'bed', 'desk', 'bookshelf', 'wardrobe', 'lamp', 'cabinet', 'stool', 'cupboard', 'drawer'],
    'appliances': ['refrigerator', 'television', 'washing', 'microwave', 'oven', 'dishwasher', 'airconditioner', 'computer', 'fan', 'heater', 'coffee', 'toaster'],
    'vehicles': ['car', 'bus', 'train', 'plane', 'bicycle', 'motorcycle', 'ship', 'boat', 'taxi', 'subway', 'truck', 'helicopter'],
    'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'parrot', 'turtle', 'snake', 'elephant', 'monkey', 'panda'],
    'fruits': ['apple', 'banana', 'orange', 'grape', 'watermelon', 'strawberry', 'pineapple', 'mango', 'peach', 'pear', 'lemon', 'cherry']
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

def download_from_placeholder(word, i):
    # 使用Placeholder.com的图片生成服务，它们有简单的占位图和卡通图
    url = f"https://via.placeholder.com/400/FFF8E1/FF5722?text={urllib.parse.quote(word)}"
    
    filepath = os.path.join(save_dir, f"{word}.jpg")
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            
            with open(filepath, 'wb') as f:
                f.write(content)
            
            print(f"  ✅ {word}")
            return True
    except Exception as e:
        print(f"  ❌ {word}: {e}")
        return False

total = 0
success = 0

print("=" * 70)
print("下载高质量占位图...")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    for i, word in enumerate(words):
        total += 1
        if download_from_placeholder(word, i):
            success += 1
        time.sleep(0.3)

print("\n" + "=" * 70)
print(f"最终统计: {success}/{total} 张图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
