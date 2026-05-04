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

def download_from_unsplash(word):
    """从多个公开图片源下载"""
    search_word = word
    
    # 使用多个备用URL
    urls_to_try = [
        # Bing图片搜索API (直接获取)
        f"https://www.bing.com/images/search?q={urllib.parse.quote(search_word + ' cartoon illustration')}&form=ANSO01",
        # 直接用图片代理服务
        f"https://source.unsplash.com/featured/400x400?{urllib.parse.quote(search_word)}",
        # Lorem Picsum
        f"https://picsum.photos/400/400",
    ]
    
    for i, url in enumerate(urls_to_try):
        try:
            print(f"  尝试 {i+1}: {url[:60]}...")
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Referer': 'https://www.google.com/'
            })
            
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
                
                if len(content) > 5000 and (content[:4] in [b'\x89PNG', b'\xff\xd8\xff', b'GIF8'] or content.startswith(b'\xff\xd8')):
                    filepath = os.path.join(save_dir, f"{word}.jpg")
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    print(f"  ✅ 成功: {word} ({len(content)} bytes)")
                    return True
                    
        except Exception as e:
            print(f"  ❌ 失败: {e}")
        
        time.sleep(1)
    
    return False

print("=" * 70)
print("从网络下载人体相关图片")
print("=" * 70)

success = 0
for word in body_words:
    print(f"\n📝 {word}:")
    if download_from_unsplash(word):
        success += 1
    time.sleep(1)

print("\n" + "=" * 70)
print(f"完成: {success}/{len(body_words)} 张图片")
print("=" * 70)
