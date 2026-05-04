import urllib.request
import urllib.parse
import time
import os

save_dir = '/workspace/word-app/public/images'
PLACEHOLDER_SIZE = 176626

word = 'apple'
prompt = 'red apple fruit'
filepath = os.path.join(save_dir, f"{word}.jpg")

print(f"重新生成 apple 图片（添加水果关键词）...")
print(f"Prompt: '{prompt}'")
print("="*60)

params = {"prompt": prompt, "image_size": "square"}
query_string = urllib.parse.urlencode(params)
session_id = f"{word}_fruit_{int(time.time()*1000)}"
url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?{query_string}&session_id={session_id}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': '*/*',
}

for attempt in range(5):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as response:
            content = response.read()
        
        size = len(content)
        
        if size != PLACEHOLDER_SIZE:
            with open(filepath, 'wb') as f:
                f.write(content)
            print(f"✅ 成功 ({size} bytes)")
            break
        else:
            print(f"⚠️ 占位图，重试 {attempt + 2}/5...")
            time.sleep(2)
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        time.sleep(2)

print("\nApple 图片已更新！")
