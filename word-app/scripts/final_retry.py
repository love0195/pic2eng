import urllib.request
import urllib.parse
import time
import os

images_dir = '/workspace/word-app/public/images'
PLACEHOLDER_SIZE = 176626

# 更简单的变体
failed_words = [
    ('seahorse', ['seahorse', 'horse fish', 'small sea creature']),
    ('seal', ['seal animal', 'arctic seal', 'pinniped']),
    ('bear', ['bear animal', 'teddy', 'grizzly']),
    ('wolf', ['wolf animal', 'gray wolf', 'wild dog']),
    ('deer', ['deer animal', 'wild deer', 'elk']),
    ('daisy', ['daisy flower', 'white flower', 'garden daisy']),
    ('leaf', ['leaf plant', 'green plant', 'foliage']),
    ('bamboo', ['bamboo stick', 'green bamboo', 'bamboo plant']),
]

def download_image(word, prompts):
    filepath = os.path.join(images_dir, f"{word}.jpg")
    
    for i, prompt in enumerate(prompts):
        print(f"  尝试: '{prompt}'")
        
        params = {"prompt": prompt, "image_size": "square"}
        query_string = urllib.parse.urlencode(params)
        session_id = f"{word}_var{i}_{int(time.time()*1000)}"
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
                print(f"  ⚠️ 占位图")
        except Exception as e:
            print(f"  ⚠️ {e}")
        
        time.sleep(2)
    
    print(f"  ❌ {word} 失败")
    return False

print("="*70)
print("最后尝试...")
print("="*70)

for word, prompts in failed_words:
    print(f"\n📝 {word}:")
    download_image(word, prompts)

print("\n" + "="*70)
print("完成！")
print("="*70)
