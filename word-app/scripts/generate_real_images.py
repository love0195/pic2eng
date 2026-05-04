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

def trigger_image_generation(word, category):
    prompt = f"A simple cartoon illustration of a {word} on white background, clean design, single object"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={word}_{category}_{int(time.time()*1000)}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        
        # 第一次触发：只请求，不保存
        response = urllib.request.urlopen(req, timeout=30)
        response.read()
        return url
    except Exception as e:
        print(f"❌ Trigger failed for {word}: {e}")
        return None

def download_real_image(word, url):
    filepath = os.path.join(save_dir, f"{word}.jpg")
    
    for attempt in range(1, 15):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0'
            })
            
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read()
                
                if len(content) > 5000:
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    print(f"  ✅ {word} ({len(content)} bytes)")
                    return True
                else:
                    if attempt < 14:
                        time.sleep(3)
                        
        except Exception as e:
            if attempt < 14:
                time.sleep(2)
    
    print(f"  ❌ {word} failed after 14 attempts")
    return False

total = 0
success = 0
word_urls = {}

print("=" * 70)
print("第一步：触发所有图片生成")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    for word in words:
        total += 1
        print(f"  📝 触发: {word}...")
        url = trigger_image_generation(word, category)
        if url:
            word_urls[word] = url
        time.sleep(0.5)

print(f"\n⏳ 等待图片生成中...")
print("  请耐心等待，这需要60-90秒...")
time.sleep(80)
print("  ✓ 等待结束！\n")

print("=" * 70)
print("第二步：下载所有真实图片")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for word in words:
            if word in word_urls:
                futures.append(executor.submit(download_real_image, word, word_urls[word]))
        
        for future in as_completed(futures):
            if future.result():
                success += 1

print("\n" + "=" * 70)
print(f"最终统计: {success}/{total} 张真实图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
