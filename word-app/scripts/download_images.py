import urllib.request
import urllib.error
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

def download_image(word, category):
    prompt = f"A simple cartoon illustration of a {word} on white background, clean design, single object, white background"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square"
    
    filename = f"{category}_{word}.png"
    filepath = os.path.join(save_dir, filename)
    
    if os.path.exists(filepath):
        print(f"⏭️  Skip: {filename} (already exists)")
        return True
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        print(f"⬇️  Downloading: {filename}")
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        
        print(f"✅ Success: {filename}")
        time.sleep(0.5)
        return True
        
    except Exception as e:
        print(f"❌ Failed: {filename} - {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False

import urllib.parse

total = 0
success = 0

print("=" * 60)
print("开始下载所有图片...")
print("=" * 60)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    for word in words:
        total += 1
        if download_image(word, category):
            success += 1
        else:
            print(f"   ⚠️  Will retry: {word}")

print("\n" + "=" * 60)
print(f"下载完成: {success}/{total} 张图片")
print(f"保存位置: {save_dir}")
print("=" * 60)
