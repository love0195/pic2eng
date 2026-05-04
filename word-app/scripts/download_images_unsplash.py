import urllib.request
import time
import os

vocabulary = {
    'furniture': ['sofa', 'table', 'chair', 'bed', 'desk', 'bookshelf', 'wardrobe', 'lamp', 'cabinet', 'stool', 'cupboard', 'drawer'],
    'appliances': ['refrigerator', 'television', 'washing machine', 'microwave', 'oven', 'dishwasher', 'air conditioner', 'computer', 'fan', 'heater', 'coffee maker', 'toaster'],
    'vehicles': ['car', 'bus', 'train', 'airplane', 'bicycle', 'motorcycle', 'ship', 'boat', 'taxi', 'subway', 'truck', 'helicopter'],
    'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'parrot', 'turtle', 'snake', 'elephant', 'monkey', 'panda'],
    'fruits': ['apple', 'banana', 'orange', 'grape', 'watermelon', 'strawberry', 'pineapple', 'mango', 'peach', 'pear', 'lemon', 'cherry']
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

def download_image(word, category):
    search_query = word.replace(' ', '+')
    url = f"https://source.unsplash.com/400x400/?{search_query},clipart&sig={int(time.time() * 1000)}"
    
    filepath = os.path.join(save_dir, f"{word.replace(' ', '_')}.jpg")
    
    if os.path.exists(filepath):
        print(f"⏭️  Skip: {word} (already exists)")
        return True
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        print(f"⬇️  Downloading: {word}")
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            content_length = len(content)
            
            if content_length < 5000:
                print(f"❌ Failed: {word} - Image too small ({content_length} bytes)")
                return False
            
            with open(filepath, 'wb') as f:
                f.write(content)
            
            print(f"✅ Success: {word} ({content_length} bytes)")
            return True
            
    except Exception as e:
        print(f"❌ Failed: {word} - {e}")
        return False

total = 0
success = 0

print("=" * 70)
print("开始下载所有图片（使用Unsplash）...")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    for word in words:
        total += 1
        if download_image(word, category):
            success += 1
        time.sleep(0.5)

print("\n" + "=" * 70)
print(f"下载完成: {success}/{total} 张图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
