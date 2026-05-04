import urllib.request
import urllib.parse
import os
import json
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

def download_image_with_retry(word, max_retries=5):
    prompt = f"A simple cartoon illustration of a {word} on white background, clean design, single object"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square"
    
    filename = f"{word}.png"
    filepath = os.path.join(save_dir, filename)
    
    print(f"⏳ Processing: {filename}")
    
    for attempt in range(max_retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
                content_length = len(content)
                
                if content_length < 5000:
                    print(f"   ⚠️  Attempt {attempt + 1}: File too small ({content_length} bytes), waiting...")
                    time.sleep(3)
                    continue
                
                with open(filepath, 'wb') as f:
                    f.write(content)
                
                print(f"✅ Success: {filename} ({content_length} bytes)")
                return True
                
        except Exception as e:
            print(f"   ⚠️  Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(3)
    
    print(f"❌ Failed after {max_retries} attempts: {filename}")
    return False

total = 0
success = 0

print("=" * 70)
print("开始下载所有图片（带重试机制）...")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    for word in words:
        total += 1
        if download_image_with_retry(word):
            success += 1
        time.sleep(1)

print("\n" + "=" * 70)
print(f"下载完成: {success}/{total} 张图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
