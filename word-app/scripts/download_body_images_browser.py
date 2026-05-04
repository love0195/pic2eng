import urllib.request
import urllib.parse
import time
import os
import http.cookiejar

# 完整的浏览器请求头
BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}

body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

# 创建cookie处理器
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def create_request(url, headers=None):
    """创建带完整浏览器特征的请求"""
    if headers is None:
        headers = BROWSER_HEADERS.copy()
    
    req = urllib.request.Request(url, headers=headers)
    return req

def search_bing_images(word):
    """从Bing图片搜索"""
    query = urllib.parse.quote(f"{word} cartoon illustration")
    search_url = f"https://www.bing.com/images/search?q={query}&first=1&count=10"
    
    try:
        print(f"    Bing搜索...")
        req = create_request(search_url)
        
        with opener.open(req, timeout=20) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # 查找图片URL
            import re
            patterns = [
                r'mediaurl":"([^"]+)"',
                r'src="(https://[^"]+bing\.com[^"]+\.(jpg|jpeg|png))"',
                r'data-src="(https://[^"]+)"',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, html)
                for match in matches[:3]:
                    img_url = match if isinstance(match, str) else match[0]
                    
                    # 下载图片
                    try:
                        img_req = create_request(img_url, {
                            'User-Agent': BROWSER_HEADERS['User-Agent'],
                            'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
                            'Referer': 'https://www.bing.com/',
                        })
                        
                        with opener.open(img_req, timeout=15) as img_response:
                            content = img_response.read()
                            
                            if len(content) > 10000 and content[:4] in [b'\xff\xd8\xff', b'\x89PN', b'GIF8']:
                                filepath = os.path.join(save_dir, f"{word}.jpg")
                                with open(filepath, 'wb') as f:
                                    f.write(content)
                                print(f"  ✅ Bing成功: {word} ({len(content)} bytes)")
                                return True
                    except:
                        continue
        
    except Exception as e:
        print(f"    Bing失败: {e}")
    
    return False

def search_google_images(word):
    """从Google图片搜索（可能需要处理验证码）"""
    query = urllib.parse.quote(f"{word} cartoon illustration")
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"
    
    try:
        print(f"    Google搜索...")
        req = create_request(search_url)
        
        with opener.open(req, timeout=20) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            import re
            # 查找图片URL
            patterns = [
                r'"ou":"([^"]+)"',
                r'data-src="([^"]+)"',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, html)
                for img_url in matches[:5]:
                    try:
                        img_req = create_request(img_url, {
                            'User-Agent': BROWSER_HEADERS['User-Agent'],
                            'Accept': 'image/*,*/*',
                            'Referer': 'https://www.google.com/',
                        })
                        
                        with opener.open(img_req, timeout=15) as img_response:
                            content = img_response.read()
                            
                            if len(content) > 10000:
                                filepath = os.path.join(save_dir, f"{word}.jpg")
                                with open(filepath, 'wb') as f:
                                    f.write(content)
                                print(f"  ✅ Google成功: {word} ({len(content)} bytes)")
                                return True
                    except:
                        continue
        
    except Exception as e:
        print(f"    Google失败: {e}")
    
    return False

def download_from_pixabay_api(word):
    """使用Pixabay API（如果有免费密钥）"""
    # 尝试使用公开的示例密钥
    api_key = "47224900-e4a06b6f5891bc30648c10ce"  # 公开测试密钥
    
    query = urllib.parse.quote(word)
    url = f"https://pixabay.com/api/?key={api_key}&q={query}&image_type=illustration&per_page=3"
    
    try:
        print(f"    Pixabay API...")
        req = create_request(url)
        
        with opener.open(req, timeout=20) as response:
            import json
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('hits'):
                img_url = data['hits'][0]['largeImageURL']
                
                img_req = create_request(img_url, {
                    'User-Agent': BROWSER_HEADERS['User-Agent'],
                    'Accept': 'image/*,*/*',
                    'Referer': 'https://pixabay.com/',
                })
                
                with opener.open(img_req, timeout=20) as img_response:
                    content = img_response.read()
                    
                    if len(content) > 10000:
                        filepath = os.path.join(save_dir, f"{word}.jpg")
                        with open(filepath, 'wb') as f:
                            f.write(content)
                        print(f"  ✅ Pixabay成功: {word} ({len(content)} bytes)")
                        return True
        
    except Exception as e:
        print(f"    Pixabay API失败: {e}")
    
    return False

def fallback_picsum(word):
    """最后的备用方案"""
    try:
        print(f"    Picsum备用...")
        url = f"https://picsum.photos/seed/{word}/400/400"
        
        req = create_request(url, {
            'User-Agent': BROWSER_HEADERS['User-Agent'],
            'Accept': 'image/*,*/*',
        })
        
        with opener.open(req, timeout=20) as response:
            content = response.read()
            
            if len(content) > 5000:
                filepath = os.path.join(save_dir, f"{word}.jpg")
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"  ⚠️ Picsum备用: {word} ({len(content)} bytes)")
                return True
                
    except Exception as e:
        print(f"    Picsum失败: {e}")
    
    return False

def download_image(word):
    """尝试多个源下载图片"""
    print(f"\n📝 {word}:")
    
    # 1. 先试Pixabay API
    if download_from_pixabay_api(word):
        return True
    
    # 2. Bing图片搜索
    if search_bing_images(word):
        return True
    
    # 3. Google图片搜索
    if search_google_images(word):
        return True
    
    # 4. 最后用Picsum
    if fallback_picsum(word):
        return True
    
    print(f"  ❌ {word} 所有源都失败")
    return False

print("=" * 70)
print("下载人体相关图片（完整浏览器模拟）")
print("=" * 70)

success = 0
for word in body_words:
    if download_image(word):
        success += 1
    time.sleep(2)  # 避免请求太快

print("\n" + "=" * 70)
print(f"完成: {success}/{len(body_words)} 张图片")
print("=" * 70)
