import urllib.request
import urllib.parse
import time
import os

save_dir = '/workspace/word-app/public/images'
PLACEHOLDER_SIZE = 176626

# 使用替代词
word = 'heater'
alt_prompts = ['fireplace', 'stove', 'furnace', 'boiler']

filepath = os.path.join(save_dir, f"{word}.jpg")

print(f"为 '{word}' 使用替代词...")
print("="*60)

for prompt in alt_prompts:
    print(f"尝试替代词: '{prompt}'")
    
    params = {"prompt": prompt, "image_size": "square"}
    query_string = urllib.parse.urlencode(params)
    session_id = f"{word}_alt_{int(time.time()*1000)}"
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
            print(f"✅ 成功 ({size} bytes) - 使用 '{prompt}' 作为 '{word}' 的图片")
            break
        else:
            print(f"⚠️ 占位图")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    time.sleep(2)

# 最终统计
print("\n" + "="*60)
real_images = 0
for f in os.listdir(save_dir):
    if f.endswith('.jpg'):
        filepath = os.path.join(save_dir, f)
        if os.path.getsize(filepath) != PLACEHOLDER_SIZE:
            real_images += 1

print(f"🎉 最终统计: {real_images}/60 张真实AI图片")
print("="*60)
