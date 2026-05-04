import urllib.request
import urllib.parse
import ssl
import time
import os
import re
import gzip
from io import BytesIO

# 完整的浏览器请求头
BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}

body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

# 创建SSL上下文
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def decode_response(response):
    """解码响应内容"""
    content = response.read()
    encoding = response.headers.get('Content-Encoding', '')
    if 'gzip' in encoding:
        try:
            content = gzip.decompress(content)
        except:
            pass
    return content

def search_freepik(word):
    """从Freepik搜索图片"""
    query = urllib.parse.quote(f"{word} cartoon illustration")
    search_url = f"https://www.freepik.com/search?format=search&query={query}&type=photo"
    
    try:
        print(f"    Freepik搜索...")
        headers = BROWSER_HEADERS.copy()
        headers['Host'] = 'www.freepik.com'
        
        req = urllib.request.Request(search_url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=20, context=ssl_context) as response:
            html = decode_response(response).decode('utf-8', errors='ignore')
            
            # 查找图片URL
            patterns = [
                r'data-src="(https://img\.freepik\.com/[^"]+)"',
                r'src="(https://img\.freepik\.com/[^"]+\.(jpg|png))"',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, html)
                for match in matches[:3]:
                    img_url = match if isinstance(match, str) else match[0]
                    
                    # 下载图片
                    try:
                        img_headers = {
                            'User-Agent': BROWSER_HEADERS['User-Agent'],
                            'Accept': 'image/*,*/*',
                            'Referer': 'https://www.freepik.com/',
                        }
                        img_req = urllib.request.Request(img_url, headers=img_headers)
                        
                        with urllib.request.urlopen(img_req, timeout=15, context=ssl_context) as img_response:
                            content = img_response.read()
                            
                            if len(content) > 10000:
                                filepath = os.path.join(save_dir, f"{word}.jpg")
                                with open(filepath, 'wb') as f:
                                    f.write(content)
                                print(f"  ✅ Freepik成功: {word} ({len(content)} bytes)")
                                return True
                    except Exception as e:
                        print(f"      图片下载失败: {e}")
                        continue
        
    except Exception as e:
        print(f"    Freepik失败: {e}")
    
    return False

def search_pngtree(word):
    """从PNGTree搜索图片"""
    query = urllib.parse.quote(f"{word} cartoon")
    search_url = f"https://pngtree.com/so/{query}"
    
    try:
        print(f"    PNGTree搜索...")
        headers = BROWSER_HEADERS.copy()
        headers['Host'] = 'pngtree.com'
        
        req = urllib.request.Request(search_url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=20, context=ssl_context) as response:
            html = decode_response(response).decode('utf-8', errors='ignore')
            
            # 查找图片URL - 使用更简单的模式
            img_urls = re.findall(r'(https://[^"\']+\.png)', html)
            img_urls += re.findall(r'(https://[^"\']+\.jpg)', html)
            
            for img_url in img_urls[:5]:
                # 过滤掉不合适的URL
                if 'avatar' in img_url or 'logo' in img_url:
                    continue
                    
                try:
                    img_headers = {
                        'User-Agent': BROWSER_HEADERS['User-Agent'],
                        'Accept': 'image/*,*/*',
                        'Referer': 'https://pngtree.com/',
                    }
                    img_req = urllib.request.Request(img_url, headers=img_headers)
                    
                    with urllib.request.urlopen(img_req, timeout=15, context=ssl_context) as img_response:
                        content = img_response.read()
                        
                        if len(content) > 10000:
                            filepath = os.path.join(save_dir, f"{word}.jpg")
                            with open(filepath, 'wb') as f:
                                f.write(content)
                            print(f"  ✅ PNGTree成功: {word} ({len(content)} bytes)")
                            return True
                except Exception as e:
                    continue
        
    except Exception as e:
        print(f"    PNGTree失败: {e}")
    
    return False

def search_istock(word):
    """从iStock搜索图片"""
    query = urllib.parse.quote(f"{word} cartoon illustration")
    search_url = f"https://www.istockphoto.com/search/2/image?family=creative&phrase={query}"
    
    try:
        print(f"    iStock搜索...")
        headers = BROWSER_HEADERS.copy()
        headers['Host'] = 'www.istockphoto.com'
        
        req = urllib.request.Request(search_url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=20, context=ssl_context) as response:
            html = decode_response(response).decode('utf-8', errors='ignore')
            
            # 查找图片URL
            img_urls = re.findall(r'(https://media\.istockphoto\.com/[^"\']+\.jpg)', html)
            
            for img_url in img_urls[:3]:
                try:
                    img_headers = {
                        'User-Agent': BROWSER_HEADERS['User-Agent'],
                        'Accept': 'image/*,*/*',
                        'Referer': 'https://www.istockphoto.com/',
                    }
                    img_req = urllib.request.Request(img_url, headers=img_headers)
                    
                    with urllib.request.urlopen(img_req, timeout=15, context=ssl_context) as img_response:
                        content = img_response.read()
                        
                        if len(content) > 10000:
                            filepath = os.path.join(save_dir, f"{word}.jpg")
                            with open(filepath, 'wb') as f:
                                f.write(content)
                            print(f"  ✅ iStock成功: {word} ({len(content)} bytes)")
                            return True
                except Exception as e:
                    continue
        
    except Exception as e:
        print(f"    iStock失败: {e}")
    
    return False

def download_from_wikipedia(word):
    """从维基百科下载相关图片"""
    try:
        print(f"    维基百科搜索...")
        # 维基百科API
        api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={word}&prop=images&format=json"
        
        headers = BROWSER_HEADERS.copy()
        req = urllib.request.Request(api_url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
            import json
            data = json.loads(response.read().decode('utf-8'))
            
            # 获取图片信息
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_data in pages.items():
                images = page_data.get('images', [])
                for img in images[:3]:
                    img_title = img.get('title', '')
                    if 'File:' in img_title:
                        # 获取图片URL
                        img_api = f"https://en.wikipedia.org/w/api.php?action=query&titles={img_title}&prop=imageinfo&iiprop=url&format=json"
                        img_req = urllib.request.Request(img_api, headers=headers)
                        
                        with urllib.request.urlopen(img_req, timeout=15, context=ssl_context) as img_response:
                            img_data = json.loads(img_response.read().decode('utf-8'))
                            
                            for img_page in img_data.get('query', {}).get('pages', {}).values():
                                imageinfo = img_page.get('imageinfo', [])
                                if imageinfo:
                                    img_url = imageinfo[0].get('url', '')
                                    if img_url:
                                        # 下载图片
                                        download_req = urllib.request.Request(img_url, headers={'User-Agent': BROWSER_HEADERS['User-Agent']})
                                        with urllib.request.urlopen(download_req, timeout=20, context=ssl_context) as download_response:
                                            content = download_response.read()
                                            
                                            if len(content) > 10000:
                                                filepath = os.path.join(save_dir, f"{word}.jpg")
                                                with open(filepath, 'wb') as f:
                                                    f.write(content)
                                                print(f"  ✅ 维基百科成功: {word} ({len(content)} bytes)")
                                                return True
        
    except Exception as e:
        print(f"    维基百科失败: {e}")
    
    return False

def fallback_picsum(word):
    """最后的备用方案"""
    try:
        print(f"    Picsum备用...")
        url = f"https://picsum.photos/seed/{word}_body/400/400"
        
        req = urllib.request.Request(url, headers={'User-Agent': BROWSER_HEADERS['User-Agent']})
        
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
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
    
    # 1. PNGTree
    if search_pngtree(word):
        return True
    
    # 2. Freepik
    if search_freepik(word):
        return True
    
    # 3. 维基百科
    if download_from_wikipedia(word):
        return True
    
    # 4. 最后用Picsum
    if fallback_picsum(word):
        return True
    
    print(f"  ❌ {word} 所有源都失败")
    return False

print("=" * 70)
print("下载人体相关图片（多源尝试）")
print("=" * 70)

success = 0
for word in body_words:
    if download_image(word):
        success += 1
    time.sleep(2)

print("\n" + "=" * 70)
print(f"完成: {success}/{len(body_words)} 张图片")
print("=" * 70)
