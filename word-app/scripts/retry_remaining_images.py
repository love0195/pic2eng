import urllib.request
import urllib.parse
import time
import os

save_dir = '/workspace/word-app/public/images'
PLACEHOLDER_SIZE = 176626

# 剩余失败的单词
remaining_words = [
    ('stool', 'furniture'),
    ('cupboard', 'furniture'),
    ('dishwasher', 'appliances'),
    ('heater', 'appliances'),
    ('subway', 'vehicles'),
]

# 更多prompt变体
more_variations = {
    'stool': ['chair stool', 'bar stool', 'seat', 'step stool'],
    'cupboard': ['closet', 'wardrobe cabinet', 'storage closet', 'pantry'],
    'dishwasher': ['dish washer', 'dishwashing machine', 'kitchen appliance'],
    'heater': ['radiator', 'space heater', 'warm air blower', 'heating radiator'],
    'subway': ['metro', 'train station', 'underground railway', 'metro car'],
}

def download_with_more_variations(word, category):
    filepath = os.path.join(save_dir, f"{word}.jpg")
    
    variations = more_variations.get(word, [word])
    
    for i, prompt in enumerate(variations):
        print(f"  尝试: '{prompt}'")
        
        params = {"prompt": prompt, "image_size": "square"}
        query_string = urllib.parse.urlencode(params)
        session_id = f"{word}_more{i}_{int(time.time()*1000)}"
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
                print(f"  ✅ 成功 ({size} bytes)")
                return True
            else:
                print(f"  ⚠️ 占位图")
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")
        
        time.sleep(2)
    
    return False

print("=" * 70)
print("为剩余5个单词重试")
print("=" * 70)

success = 0

for word, category in remaining_words:
    print(f"\n📝 {word} ({category}):")
    if download_with_more_variations(word, category):
        success += 1

print("\n" + "=" * 70)
print(f"本轮成功: {success}/5 张")
print("=" * 70)

# 统计总数
total_images = 0
real_images = 0
for f in os.listdir(save_dir):
    if f.endswith('.jpg'):
        total_images += 1
        filepath = os.path.join(save_dir, f)
        if os.path.getsize(filepath) != PLACEHOLDER_SIZE:
            real_images += 1

print(f"\n总计: {real_images}/{total_images} 张真实图片")
