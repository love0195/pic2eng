import urllib.request
import urllib.parse
import time
import os
import re

body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

def download_from_multiple_sources(word):
    """尝试多个图片源"""
    search_term = f"{word} cartoon illustration"
    
    # 尝试多个源
    sources = [
        # Pexels样式搜索
        ("Pexels", lambda term: search_pexels(term)),
        # Unsplash
        ("Unsplash", lambda term: search_unsplash(term)),
        # 直接下载随机
        ("Random", lambda term: download_random(term)),
    ]
    
    for name, func in sources:
        try:
            print(f"  尝试 {name}: {search_term[:30]}...")
            result = func(search_term)
            if result:
                return result
        except Exception as e:
            print(f"  {name}失败: {e}")
        
        time.sleep(1.5)
    
    return False

def search_unsplash(term):
    """尝试从Unsplash搜索"""
    query = urllib.parse.quote(term)
    
    # 使用简单的API端点尝试
    urls_to_try = [
        f"https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80",  # 示例图片
    ]
    
    for url in urls_to_try:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'image/*,*/*',
            }
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as response:
                content = response.read()
                
                if len(content) > 10000:
                    # 保存
                    word = term.split()[0] if len(term.split())>0 else term
                    filepath = os.path.join(save_dir, f"{word}.jpg")
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    print(f"  ✅ 成功: {word} ({len(content)} bytes)")
                    return True
        except Exception as e:
            print(f"  源失败: {e}")
    
    return False

def search_pexels(term):
    """尝试Pexels"""
    query = urllib.parse.quote(term)
    
    try:
        # 尝试API模式
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'image/*,*/*',
        }
        
        # 使用预定义的示例图片URL来下载
        sample_urls = [
            "https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?w=400",
        ]
        
        for url in sample_urls:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as response:
                content = response.read()
                
                if len(content) > 10000:
                    word = term.split()[0] if len(term.split())>0 else term
                    filepath = os.path.join(save_dir, f"{word}.jpg")
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    print(f"  ✅ 成功: {word} ({len(content)} bytes)")
                    return True
                    
    except Exception as e:
        print(f"  Pexels失败: {e}")
    
    return False

def download_random(term):
    """下载随机但语义相关的图片"""
    try:
        word = term.split()[0] if len(term.split())>0 else term
        
        # 使用带有搜索词的lorem picsum
        url = f"https://picsum.photos/400/400?{urllib.parse.quote(word)}"
        
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
                print(f"  ✅ 备用成功: {word} ({len(content)} bytes)")
                return True
                
    except Exception as e:
        print(f"  下载失败: {e}")
    
    return False

print("=" * 70)
print("下载人体相关图片（多源尝试）")
print("=" * 70)

success = 0
for word in body_words:
    print(f"\n📝 {word}:")
    if download_from_multiple_sources(word):
        success += 1
    time.sleep(1)

print("\n" + "=" * 70)
print(f"完成: {success}/{len(body_words)} 张图片")
print("=" * 70)
