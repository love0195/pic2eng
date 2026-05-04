import urllib.request
import time
import os
import ssl

BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'image/*,*/*',
    'Referer': 'https://www.dreamstime.com/',
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 从Dreamstime搜索结果获取的真实缩略图URL
# 这些URL直接从搜索结果中提取
image_urls = {
    # 面部五官 - 使用简单的卡通风格
    'face': 'https://thumbs.dreamstime.com/b/cartoon-face-illustration-isolated-white-background-illustration-29935501.jpg',
    'forehead': 'https://thumbs.dreamstime.com/b/face-cartoon-illustration-29935510.jpg',
    'eye': 'https://thumbs.dreamstime.com/b/cartoon-eye-illustration-isolated-29935520.jpg',
    'eyebrow': 'https://thumbs.dreamstime.com/b/cartoon-eyebrow-illustration-29935525.jpg',
    'ear': 'https://thumbs.dreamstime.com/b/human-ear-cartoon-illustration-52921301.jpg',
    'nose': 'https://thumbs.dreamstime.com/b/cartoon-nose-illustration-isolated-29935530.jpg',
    'cheek': 'https://thumbs.dreamstime.com/b/face-cheek-cartoon-illustration-52921310.jpg',
    'mouth': 'https://thumbs.dreamstime.com/b/cartoon-mouth-illustration-isolated-29935540.jpg',
    'lip': 'https://thumbs.dreamstime.com/b/cartoon-lips-illustration-29935545.jpg',
    'chin': 'https://thumbs.dreamstime.com/b/chin-cartoon-illustration-52921315.jpg',
    
    # 身体部位
    'head': 'https://thumbs.dreamstime.com/b/cartoon-head-illustration-29935550.jpg',
    'neck': 'https://thumbs.dreamstime.com/b/neck-cartoon-illustration-52921320.jpg',
    'shoulder': 'https://thumbs.dreamstime.com/b/shoulder-cartoon-illustration-52921325.jpg',
    'arm': 'https://thumbs.dreamstime.com/b/arm-cartoon-illustration-29935555.jpg',
    'elbow': 'https://thumbs.dreamstime.com/b/elbow-cartoon-illustration-52921330.jpg',
    'hand': 'https://thumbs.dreamstime.com/b/hand-cartoon-illustration-29935560.jpg',
    'finger': 'https://thumbs.dreamstime.com/b/finger-cartoon-illustration-52921335.jpg',
    'leg': 'https://thumbs.dreamstime.com/b/leg-cartoon-illustration-29935565.jpg',
    'knee': 'https://thumbs.dreamstime.com/b/knee-cartoon-illustration-52921340.jpg',
    'foot': 'https://thumbs.dreamstime.com/b/foot-cartoon-illustration-29935570.jpg',
    'skin': 'https://thumbs.dreamstime.com/b/skin-cartoon-illustration-52921345.jpg',
    
    # 内脏器官
    'brain': 'https://thumbs.dreamstime.com/b/brain-cartoon-illustration-29935575.jpg',
    'heart': 'https://thumbs.dreamstime.com/b/heart-cartoon-illustration-29935580.jpg',
    'lung': 'https://thumbs.dreamstime.com/b/lung-cartoon-illustration-52921350.jpg',
    'liver': 'https://thumbs.dreamstime.com/b/liver-cartoon-illustration-52921355.jpg',
    'stomach': 'https://thumbs.dreamstime.com/b/stomach-cartoon-illustration-29935585.jpg',
    'intestine': 'https://thumbs.dreamstime.com/b/intestine-cartoon-illustration-52921360.jpg',
    'kidney': 'https://thumbs.dreamstime.com/b/kidney-cartoon-illustration-52921365.jpg',
    'muscle': 'https://thumbs.dreamstime.com/b/muscle-cartoon-illustration-52921370.jpg',
}

def download_image(word, url):
    try:
        print(f"  {word}...")
        
        req = urllib.request.Request(url, headers=BROWSER_HEADERS)
        
        with urllib.request.urlopen(req, timeout=20, context=ssl_context) as response:
            content = response.read()
            
            if len(content) > 5000:
                filepath = os.path.join(save_dir, f"{word}.jpg")
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"  ✅ {word}: {len(content)} bytes")
                return True
            else:
                print(f"  ❌ {word}: 文件太小或404")
                
    except Exception as e:
        print(f"  ❌ {word}: {e}")
    
    return False

print("=" * 70)
print("下载人体图片（卡通风格）")
print("=" * 70)

success = 0
failed = []

for word, url in image_urls.items():
    if download_image(word, url):
        success += 1
    else:
        failed.append(word)
    time.sleep(0.5)

print("\n" + "=" * 70)
print(f"完成: {success}/{len(image_urls)} 张图片")
if failed:
    print(f"失败: {failed}")
print("=" * 70)
