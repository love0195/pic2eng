import urllib.request
import time
import os
import ssl

BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'https://www.dreamstime.com/',
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 从搜索结果中提取的真实缩略图URL
remaining_urls = {
    'mouth': 'https://thumbs.dreamstime.com/b/mouth-sync-talking-mouths-lips-cartoon-character-animation-english-pronunciation-signs-vector-set-isolated-female-emotions-156374750.jpg',
    'lip': 'https://thumbs.dreamstime.com/b/cartoon-lips-vector-illustration-image62597332.jpg',
    'arm': 'https://thumbs.dreamstime.com/b/cartoon-arm-vector-set-75336228.jpg',
}

def download_image(word, url):
    try:
        print(f"  下载: {url[:70]}...")
        
        req = urllib.request.Request(url, headers=BROWSER_HEADERS)
        
        with urllib.request.urlopen(req, timeout=20, context=ssl_context) as response:
            content = response.read()
            
            if len(content) > 5000:
                filepath = os.path.join(save_dir, f"{word}.jpg")
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"  ✅ 成功: {word} ({len(content)} bytes)")
                return True
            else:
                print(f"  ❌ 文件太小: {len(content)} bytes")
                
    except Exception as e:
        print(f"  ❌ 失败: {e}")
    
    return False

print("=" * 70)
print("下载剩余的3张图片")
print("=" * 70)

success = 0
for word, url in remaining_urls.items():
    print(f"\n📝 {word}:")
    
    if download_image(word, url):
        success += 1
    
    time.sleep(0.5)

print("\n" + "=" * 70)
print(f"完成: {success}/3 张图片")
print("=" * 70)
