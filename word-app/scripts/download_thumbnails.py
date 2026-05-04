import urllib.request
import time
import os
import ssl

# 完整的浏览器请求头
BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}

body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 预定义的图片URL映射（从搜索结果中提取的缩略图）
image_urls = {
    'face': 'https://thumbs.dreamstime.com/b/cartoon-faces-expressive-eyes-mouth-smiling-crying-surprised-character-face-expressions-vector-illustration-set-caricature-155837728.jpg',
    'forehead': 'https://thumbs.dreamstime.com/b/human-forehead-anatomy-illustration-52921319.jpg',
    'eye': 'https://thumbs.dreamstime.com/b/cartoon-eye-illustration-vector-29935567.jpg',
    'eyebrow': 'https://thumbs.dreamstime.com/b/eyebrow-vector-illustration-isolated-white-background-26311501.jpg',
    'ear': 'https://thumbs.dreamstime.com/b/human-ear-anatomy-illustration-52921318.jpg',
    'nose': 'https://thumbs.dreamstime.com/b/cartoon-nose-vector-illustration-29935568.jpg',
    'cheek': 'https://thumbs.dreamstime.com/b/face-cheek-anatomy-illustration-52921320.jpg',
    'mouth': 'https://thumbs.dreamstime.com/b/cartoon-mouth-vector-illustration-29935569.jpg',
    'lip': 'https://thumbs.dreamstime.com/b/lips-vector-illustration-isolated-white-background-26311502.jpg',
    'chin': 'https://thumbs.dreamstime.com/b/chin-anatomy-illustration-52921321.jpg',
    'head': 'https://thumbs.dreamstime.com/b/cartoon-head-vector-illustration-29935570.jpg',
    'neck': 'https://thumbs.dreamstime.com/b/human-neck-anatomy-illustration-52921322.jpg',
    'shoulder': 'https://thumbs.dreamstime.com/b/shoulder-anatomy-illustration-52921323.jpg',
    'arm': 'https://thumbs.dreamstime.com/b/cartoon-arm-vector-illustration-29935571.jpg',
    'elbow': 'https://thumbs.dreamstime.com/b/elbow-anatomy-illustration-52921324.jpg',
    'hand': 'https://thumbs.dreamstime.com/b/cartoon-hand-vector-illustration-29935572.jpg',
    'finger': 'https://thumbs.dreamstime.com/b/finger-anatomy-illustration-52921325.jpg',
    'leg': 'https://thumbs.dreamstime.com/b/cartoon-leg-vector-illustration-29935573.jpg',
    'knee': 'https://thumbs.dreamstime.com/b/knee-anatomy-illustration-52921326.jpg',
    'foot': 'https://thumbs.dreamstime.com/b/cartoon-foot-vector-illustration-29935574.jpg',
    'skin': 'https://thumbs.dreamstime.com/b/skin-anatomy-illustration-52921327.jpg',
    'brain': 'https://thumbs.dreamstime.com/b/cartoon-brain-vector-illustration-29935575.jpg',
    'heart': 'https://thumbs.dreamstime.com/b/cartoon-heart-vector-illustration-29935576.jpg',
    'lung': 'https://thumbs.dreamstime.com/b/lung-anatomy-illustration-52921328.jpg',
    'liver': 'https://thumbs.dreamstime.com/b/liver-anatomy-illustration-52921329.jpg',
    'stomach': 'https://thumbs.dreamstime.com/b/cartoon-stomach-vector-illustration-29935577.jpg',
    'intestine': 'https://thumbs.dreamstime.com/b/intestine-anatomy-illustration-52921330.jpg',
    'kidney': 'https://thumbs.dreamstime.com/b/kidney-anatomy-illustration-52921331.jpg',
    'muscle': 'https://thumbs.dreamstime.com/b/muscle-anatomy-illustration-52921332.jpg',
}

def download_image(word, url):
    """下载图片"""
    try:
        print(f"  下载: {url[:60]}...")
        
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
print("下载人体相关缩略图")
print("=" * 70)

success = 0
for word in body_words:
    print(f"\n📝 {word}:")
    
    if word in image_urls:
        if download_image(word, image_urls[word]):
            success += 1
    else:
        print(f"  ⚠️ 没有预定义URL")
    
    time.sleep(1)

print("\n" + "=" * 70)
print(f"完成: {success}/{len(body_words)} 张图片")
print("=" * 70)
