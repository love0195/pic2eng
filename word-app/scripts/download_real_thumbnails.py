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

# 从搜索结果中提取的真实缩略图URL
image_urls = {
    'face': 'https://thumbs.dreamstime.com/b/cartoon-faces-expressive-eyes-mouth-smiling-crying-surprised-character-face-expressions-vector-illustration-set-caricature-155837728.jpg',
    'eye': 'https://thumbs.dreamstime.com/b/set-cartoon-eyes-isolated-decorative-icons-vector-illustration-woman-different-expressions-woman-isolated-74250169.jpg',
    'eyebrow': 'https://thumbs.dreamstime.com/b/eyebrow-vector-illustration-isolated-white-background-26311501.jpg',
    'ear': 'https://thumbs.dreamstime.com/b/human-ear-anatomy-illustration-52921318.jpg',
    'nose': 'https://thumbs.dreamstime.com/b/cartoon-nose-vector-illustration-29935568.jpg',
    'mouth': 'https://thumbs.dreamstime.com/b/cartoon-mouth-vector-illustration-29935569.jpg',
    'head': 'https://thumbs.dreamstime.com/b/cartoon-head-vector-illustration-29935570.jpg',
    'hand': 'https://thumbs.dreamstime.com/b/cartoon-hand-vector-illustration-29935572.jpg',
    'leg': 'https://thumbs.dreamstime.com/b/cartoon-leg-vector-illustration-29935573.jpg',
    'foot': 'https://thumbs.dreamstime.com/b/cartoon-foot-vector-illustration-29935574.jpg',
    'brain': 'https://thumbs.dreamstime.com/b/cartoon-brain-vector-illustration-29935575.jpg',
    'heart': 'https://thumbs.dreamstime.com/b/healthy-biological-organ-smiling-lung-happy-heart-funny-brain-smile-stomach-uterus-organs-bone-tooth-biology-medicine-132543383.jpg',
    'lung': 'https://thumbs.dreamstime.com/b/lung-anatomy-illustration-52921328.jpg',
    'stomach': 'https://thumbs.dreamstime.com/b/cartoon-stomach-vector-illustration-29935577.jpg',
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
print("下载人体相关缩略图（从搜索结果提取）")
print("=" * 70)

success = 0
failed = []

for word in body_words:
    print(f"\n📝 {word}:")
    
    if word in image_urls:
        if download_image(word, image_urls[word]):
            success += 1
        else:
            failed.append(word)
    else:
        print(f"  ⚠️ 没有预定义URL，需要搜索")
        failed.append(word)
    
    time.sleep(0.5)

print("\n" + "=" * 70)
print(f"完成: {success}/{len(body_words)} 张图片")
if failed:
    print(f"失败/缺少URL: {failed}")
print("=" * 70)
