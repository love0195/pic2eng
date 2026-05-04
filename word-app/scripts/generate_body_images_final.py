import urllib.request
import urllib.parse
import time
import os

body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

def trigger_image_generation(word):
    prompt = f"A simple cartoon illustration of a {word} on white background, clean design, educational style"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id=body_{word}_{int(time.time()*1000)}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response = urllib.request.urlopen(req, timeout=30)
        response.read()
        print(f"  ✅ 触发成功: {word}")
        return url
    except Exception as e:
        print(f"  ❌ 触发失败: {word} - {e}")
        return None

def download_real_image(word, url):
    filepath = os.path.join(save_dir, f"{word}.jpg")
    
    for attempt in range(1, 15):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read()
                
                if len(content) > 10000 and content[:2] == b'\xff\xd8':
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    print(f"  ✅ 下载成功: {word} ({len(content)} bytes)")
                    return True
                else:
                    if attempt < 14:
                        print(f"  ⏳ 尝试 {attempt}: 大小={len(content)}, 等待...")
                        time.sleep(4)
                        
        except Exception as e:
            if attempt < 14:
                print(f"  ⏳ 尝试 {attempt}: 错误={e}, 重试...")
                time.sleep(3)
    
    print(f"  ❌ 下载失败: {word}")
    return False

word_urls = {}

print("=" * 70)
print("第一步：触发所有人体图片生成")
print("=" * 70)

for word in body_words:
    print(f"\n📝 {word}:")
    url = trigger_image_generation(word)
    if url:
        word_urls[word] = url
    time.sleep(0.5)

print("\n" + "=" * 70)
print("⏳ 等待 80 秒让AI生成图片...")
print("  请耐心等待，这需要一些时间...")
print("=" * 70)
time.sleep(80)
print("✅ 等待结束！\n")

print("=" * 70)
print("第二步：下载所有真实图片")
print("=" * 70)

success = 0
for word in body_words:
    print(f"\n📝 {word}:")
    if word in word_urls:
        if download_real_image(word, word_urls[word]):
            success += 1
    time.sleep(1)

print("\n" + "=" * 70)
print(f"最终统计: {success}/{len(body_words)} 张真实图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
