import urllib.request
import urllib.parse
import time
import os

images_dir = '/workspace/word-app/public/images'
PLACEHOLDER_SIZE = 176626

failed_words = [
    ('seahorse', 'sea horse'),
    ('seal', 'marine seal'),
    ('bear', 'teddy bear'),
    ('wolf', 'wild wolf'),
    ('deer', 'forest deer'),
    ('daisy', 'white daisy'),
    ('leaf', 'green leaf'),
    ('bamboo', 'bamboo plant'),
]

def download_image(word, prompt):
    filepath = os.path.join(images_dir, f"{word}.jpg")
    
    for attempt in range(5):
        params = {"prompt": prompt, "image_size": "square"}
        query_string = urllib.parse.urlencode(params)
        session_id = f"{word}_fix_{attempt}_{int(time.time()*1000)}"
        url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?{query_string}&session_id={session_id}"
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Accept': '*/*'}
        
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
                print(f"  ⏳ {word} 占位图，重试 {attempt + 2}/5...")
                time.sleep(2)
        except Exception as e:
            print(f"  ⚠️ {word} 错误: {e}")
            time.sleep(2)
    
    print(f"  ❌ {word} 失败")
    return False

print("="*70)
print("重试失败的图片...")
print("="*70)

for word, prompt in failed_words:
    print(f"\n📝 {word}:")
    download_image(word, prompt)

print("\n" + "="*70)
print("完成！")
print("="*70)
