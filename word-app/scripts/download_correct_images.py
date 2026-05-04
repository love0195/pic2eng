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

def download_single_image(word, category):
    prompt = f"A simple cartoon illustration of a {word} on white background, clean design, single object"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={word}_{category}_{int(time.time()*1000)}"
    
    filepath = os.path.join(save_dir, f"{word}.jpg")
    
    try:
        # 第一次请求：触发生成
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        urllib.request.urlopen(req, timeout=30)
        
        # 等待一会儿
        time.sleep(5)
        
        # 第二次请求：获取真正的图片
        req2 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req2, timeout=30) as response2:
            content = response2.read()
            
            with open(filepath, 'wb') as f:
                f.write(content)
            
            print(f"✅ {word} ({len(content)} bytes)")
            return True
            
    except Exception as e:
        print(f"❌ {word}: {e}")
        return False

total = 0
success = 0

print("=" * 70)
print("下载真正的AI生成图片")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for word in words:
            total += 1
            futures.append(executor.submit(download_single_image, word, category))
        
        for future in as_completed(futures):
            if future.result():
                success += 1

print("\n" + "=" * 70)
print(f"最终统计: {success}/{total} 张图片")
print("=" * 70)
