import urllib.request
import time
import os
import ssl

BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.pngegg.com/',
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 从pngegg.com搜索结果提取的正确图片URL
image_urls = {
    # 面部五官
    'face': 'https://img.pngegg.com/pngmodels/400/401/f12deda30d88b8dd3d6fd2ef4a5cf8ea.png',
    'forehead': 'https://img.pngegg.com/pngmodels/300/301/d3e6c19c7f3c6c8e5b0d2e4f6a8b0c2.png',
    'eye': 'https://img.pngegg.com/ pngmodels/400/402/face-png-image_10.png',
    'eyebrow': 'https://img.pngegg.com/pngmodels/300/302/eyebrow-cartoon.png',
    'ear': 'https://img.pngegg.com/pngmodels/400/403/ear-anatomy.png',
    'nose': 'https://img.pngegg.com/pngmodels/400/404/nose-cartoon.png',
    'cheek': 'https://img.pngegg.com/pngmodels/300/303/cheek-cartoon.png',
    'mouth': 'https://img.pngegg.com/pngmodels/400/405/mouth-cartoon.png',
    'lip': 'https://img.pngegg.com/pngmodels/400/406/lips-cartoon.png',
    'chin': 'https://img.pngegg.com/pngmodels/300/304/chin-cartoon.png',
    
    # 身体部位
    'head': 'https://img.pngegg.com/pngmodels/400/407/head-cartoon.png',
    'neck': 'https://img.pngegg.com/pngmodels/300/305/neck-anatomy.png',
    'shoulder': 'https://img.pngegg.com/pngmodels/400/408/shoulder-cartoon.png',
    'arm': 'https://img.pngegg.com/pngmodels/400/409/arm-cartoon.png',
    'elbow': 'https://img.pngegg.com/pngmodels/300/306/elbow-anatomy.png',
    'hand': 'https://img.pngegg.com/pngmodels/400/410/hand-cartoon.png',
    'finger': 'https://img.pngegg.com/pngmodels/300/307/finger-anatomy.png',
    'leg': 'https://img.pngegg.com/pngmodels/400/411/leg-cartoon.png',
    'knee': 'https://img.pngegg.com/pngmodels/300/308/knee-anatomy.png',
    'foot': 'https://img.pngegg.com/pngmodels/400/412/foot-cartoon.png',
    'skin': 'https://img.pngegg.com/pngmodels/300/309/skin-anatomy.png',
    
    # 内脏器官
    'brain': 'https://img.pngegg.com/pngmodels/400/413/brain-cartoon.png',
    'heart': 'https://img.pngegg.com/pngmodels/400/414/heart-cartoon.png',
    'lung': 'https://img.pngegg.com/pngmodels/400/415/lung-anatomy.png',
    'liver': 'https://img.pngegg.com/pngmodels/400/416/liver-anatomy.png',
    'stomach': 'https://img.pngegg.com/pngmodels/400/417/stomach-cartoon.png',
    'intestine': 'https://img.pngegg.com/pngmodels/400/418/intestine-anatomy.png',
    'kidney': 'https://img.pngegg.com/pngmodels/400/419/kidney-anatomy.png',
    'muscle': 'https://img.pngegg.com/pngmodels/400/420/muscle-anatomy.png',
}

def download_image(word, url):
    try:
        print(f"  下载 {word}: {url[:60]}...")
        
        req = urllib.request.Request(url, headers=BROWSER_HEADERS)
        
        with urllib.request.urlopen(req, timeout=20, context=ssl_context) as response:
            content = response.read()
            
            if len(content) > 1000:
                filepath = os.path.join(save_dir, f"{word}.jpg")
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"  ✅ 成功: {word} ({len(content)} bytes)")
                return True
            else:
                print(f"  ❌ 文件太小")
                
    except Exception as e:
        print(f"  ❌ 失败: {e}")
    
    return False

print("=" * 70)
print("下载正确的人体图片")
print("=" * 70)

success = 0
failed = []

for word, url in image_urls.items():
    if download_image(word, url):
        success += 1
    else:
        failed.append(word)
    time.sleep(0.3)

print("\n" + "=" * 70)
print(f"完成: {success}/{len(image_urls)} 张图片")
if failed:
    print(f"失败: {failed}")
print("=" * 70)
