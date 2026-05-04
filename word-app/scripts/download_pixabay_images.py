import urllib.request
import urllib.parse
import re
import time
import os

body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

def search_and_download_from_pixabay(word):
    """尝试从Pixabay搜索并下载图片"""
    # 搜索关键词，加上"cartoon"或"illustration"
    search_terms = [
        f"{word} cartoon illustration",
        f"{word} cartoon",
        f"{word} illustration",
        word
    ]
    
    for search_term in search_terms:
        try:
            # Pixabay搜索URL
            query = urllib.parse.quote(search_term)
            url = f"https://pixabay.com/images/search/{query}/?order=latest"
            
            print(f"  搜索: {search_term}")
            
            # 获取搜索页面
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=20) as response:
                html = response.read().decode('utf-8')
                
                # 查找图片链接 - 查找 img src或 data-src
                img_patterns = [
                    r'src="(https://cdn\.pixabay\.com/photo/[^"]+\.(jpg|png))"',
                    r'data-src="(https://cdn\.pixabay\.com/photo/[^"]+\.(jpg|png))"',
                    r'srcset="(https://cdn\.pixabay\.com/photo/[^"]+\.(jpg|png))',
                ]
                
                for pattern in img_patterns:
                    matches = re.findall(pattern, html)
                    if matches:
                        img_url = matches[0][0]
                        
                        # 下载图片
                        print(f"    找到图片: {img_url[:60]}...")
                        img_req = urllib.request.Request(img_url, headers=headers)
                        
                        with urllib.request.urlopen(img_req, timeout=20) as img_response:
                            content = img_response.read()
                            
                            if len(content) > 10000:
                                filepath = os.path.join(save_dir, f"{word}.jpg")
                                with open(filepath, 'wb') as f:
                                    f.write(content)
                                print(f"  ✅ 成功: {word} ({len(content)} bytes)")
                                return True
                
                print(f"    未找到图片，尝试下一个搜索词")
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")
        
        time.sleep(2)
    
    return False

def download_with_fallback(word):
    """先试Pixabay，不成功再试其他源"""
    print(f"\n📝 {word}:")
    
    # 1. 尝试Pixabay
    if search_and_download_from_pixabay(word):
        return True
    
    # 2. 如果Pixabay失败，用我们的备用方案
    print(f"  Pixabay失败，尝试其他源...")
    
    fallback_urls = [
        f"https://picsum.photos/400/400?random={word}",
        f"https://picsum.photos/400/400?random={word}2",
    ]
    
    for url in fallback_urls:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'image/*,*/*',
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read()
                
                if len(content) > 5000:
                    filepath = os.path.join(save_dir, f"{word}.jpg")
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    print(f"  ✅ 备用方案成功: {word} ({len(content)} bytes)")
                    return True
        except Exception as e:
            print(f"  备用失败: {e}")
        
        time.sleep(1)
    
    return False

print("=" * 70)
print("从Pixabay下载人体相关图片")
print("=" * 70)

success = 0
for word in body_words:
    if download_with_fallback(word):
        success += 1
    time.sleep(1)

print("\n" + "=" * 70)
print(f"完成: {success}/{len(body_words)} 张图片")
print("=" * 70)
