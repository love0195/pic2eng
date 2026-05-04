import urllib.request
import urllib.parse
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

vocabulary = {
    'furniture': ['sofa', 'table', 'chair', 'bed', 'desk', 'bookshelf', 'wardrobe', 'lamp', 'cabinet', 'stool', 'cupboard', 'drawer'],
    'appliances': ['refrigerator', 'television', 'washing', 'microwave', 'oven', 'dishwasher', 'airconditioner', 'computer', 'fan', 'heater', 'coffee', 'toaster'],
    'vehicles': ['car', 'bus', 'train', 'plane', 'bicycle', 'motorcycle', 'ship', 'boat', 'taxi', 'subway', 'truck', 'helicopter'],
    'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'parrot', 'turtle', 'snake', 'elephant', 'monkey', 'panda'],
    'fruits': ['apple', 'banana', 'orange', 'grape', 'watermelon', 'strawberry', 'pineapple', 'mango', 'peach', 'pear', 'lemon', 'cherry']
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

PLACEHOLDER_SIZE = 176626

def download_image(word, category, max_retries=5):
    filepath = os.path.join(save_dir, f"{word}.jpg")
    
    # 如果已存在且不是占位图，跳过
    if os.path.exists(filepath):
        existing_size = os.path.getsize(filepath)
        if existing_size != PLACEHOLDER_SIZE:
            print(f"  ⏭️  {word} (已存在, {existing_size} bytes)")
            return True
    
    for attempt in range(max_retries):
        # 使用最简短的prompt
        prompt = word
        params = {"prompt": prompt, "image_size": "square"}
        query_string = urllib.parse.urlencode(params)
        session_id = f"{word}_{category}_{attempt}_{int(time.time()*1000)}"
        url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?{query_string}&session_id={session_id}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
            
            size = len(content)
            
            if size != PLACEHOLDER_SIZE:
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"  ✅ {word} ({size} bytes)")
                return True
            else:
                if attempt < max_retries - 1:
                    print(f"  ⏳ {word} 占位图，重试 {attempt + 2}/{max_retries}...")
                    time.sleep(2)
                    
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  ⚠️ {word} 错误，重试 {attempt + 2}/{max_retries}...")
                time.sleep(2)
    
    print(f"  ❌ {word} 失败")
    return False

total = 0
success = 0

print("=" * 70)
print("生成AI卡通图片（使用简短prompt）")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for word in words:
            total += 1
            futures.append(executor.submit(download_image, word, category))
        
        for future in as_completed(futures):
            if future.result():
                success += 1

print("\n" + "=" * 70)
print(f"完成: {success}/{total} 张真实图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
