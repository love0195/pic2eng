import urllib.request
import urllib.parse
import time
import os

save_dir = '/workspace/word-app/public/images'
PLACEHOLDER_SIZE = 176626

# 失败的单词列表
failed_words = [
    ('stool', 'furniture'),
    ('cupboard', 'furniture'),
    ('cabinet', 'furniture'),
    ('drawer', 'furniture'),
    ('washing', 'appliances'),
    ('microwave', 'appliances'),
    ('oven', 'appliances'),
    ('dishwasher', 'appliances'),
    ('airconditioner', 'appliances'),
    ('fan', 'appliances'),
    ('heater', 'appliances'),
    ('plane', 'vehicles'),
    ('ship', 'vehicles'),
    ('subway', 'vehicles'),
    ('parrot', 'animals'),
    ('turtle', 'animals'),
]

# 为每个单词尝试不同的prompt变体
prompt_variations = {
    'stool': ['stool seat', 'small stool', 'wooden stool'],
    'cupboard': ['kitchen cupboard', 'storage cupboard', 'cupboard furniture'],
    'cabinet': ['storage cabinet', 'wooden cabinet', 'cabinet furniture'],
    'drawer': ['drawer box', 'wooden drawer', 'storage drawer'],
    'washing': ['washing machine', 'laundry machine', 'washer'],
    'microwave': ['microwave oven', 'microwave appliance', 'kitchen microwave'],
    'oven': ['kitchen oven', 'baking oven', 'cooking oven'],
    'dishwasher': ['dishwasher machine', 'kitchen dishwasher', 'dish cleaning machine'],
    'airconditioner': ['air conditioner', 'ac unit', 'cooling unit'],
    'fan': ['electric fan', 'cooling fan', 'desk fan'],
    'heater': ['electric heater', 'room heater', 'heating device'],
    'plane': ['airplane', 'aircraft', 'passenger plane'],
    'ship': ['large ship', 'ocean ship', 'cargo ship'],
    'subway': ['metro train', 'underground train', 'subway train'],
    'parrot': ['colorful parrot', 'bird parrot', 'talking parrot'],
    'turtle': ['sea turtle', 'tortoise', 'green turtle'],
}

def download_with_variations(word, category):
    filepath = os.path.join(save_dir, f"{word}.jpg")
    
    variations = prompt_variations.get(word, [word])
    
    for i, prompt in enumerate(variations):
        print(f"  尝试: '{prompt}'")
        
        params = {"prompt": prompt, "image_size": "square"}
        query_string = urllib.parse.urlencode(params)
        session_id = f"{word}_var{i}_{int(time.time()*1000)}"
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
print("为失败的单词重试（使用不同的prompt）")
print("=" * 70)

success = 0
total = len(failed_words)

for word, category in failed_words:
    print(f"\n📝 {word} ({category}):")
    if download_with_variations(word, category):
        success += 1
    time.sleep(1)

print("\n" + "=" * 70)
print(f"完成: {success}/{total} 张新图片")
print("=" * 70)
