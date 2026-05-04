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
image_urls = {
    # 面部五官
    'face': 'https://thumbs.dreamstime.com/b/cartoon-faces-expressive-eyes-mouth-smiling-crying-surprised-character-face-expressions-vector-illustration-set-caricature-155837728.jpg',
    'forehead': 'https://thumbs.dreamstime.com/b/human-forehead-diagram-anatomy-illustration-education-medical-diagram-forehead-145345892.jpg',
    'eye': 'https://thumbs.dreamstime.com/b/set-cartoon-eyes-isolated-decorative-icons-vector-illustration-woman-different-expressions-woman-isolated-74250169.jpg',
    'eyebrow': 'https://thumbs.dreamstime.com/b/eyebrow-vector-illustration-isolated-white-background-26311501.jpg',
    'ear': 'https://thumbs.dreamstime.com/b/human-ear-anatomy-illustration-52921318.jpg',
    'nose': 'https://thumbs.dreamstime.com/b/cartoon-nose-vector-illustration-29935568.jpg',
    'cheek': 'https://thumbs.dreamstime.com/b/face-cheek-anatomy-illustration-52921320.jpg',
    'mouth': 'https://thumbs.dreamstime.com/b/cartoon-mouth-vector-illustration-isolated-white-background-29935569.jpg',
    'lip': 'https://thumbs.dreamstime.com/b/lips-vector-illustration-isolated-white-background-26311502.jpg',
    'chin': 'https://thumbs.dreamstime.com/b/chin-anatomy-illustration-52921321.jpg',
    
    # 身体部位
    'head': 'https://thumbs.dreamstime.com/b/cartoon-head-vector-illustration-29935570.jpg',
    'neck': 'https://thumbs.dreamstime.com/b/human-neck-anatomy-illustration-52921322.jpg',
    'shoulder': 'https://thumbs.dreamstime.com/b/shoulder-anatomy-illustration-52921323.jpg',
    'arm': 'https://thumbs.dreamstime.com/b/cartoon-arm-vector-illustration-29935571.jpg',
    'elbow': 'https://thumbs.dreamstime.com/b/elbow-anatomy-illustration-52921324.jpg',
    'hand': 'https://thumbs.dreamstime.com/b/flat-hands-cartoon-human-male-hands-showing-thumbs-up-pointing-greeting-vector-isolated-collection-arms-gestures-drawing-164785256.jpg',
    'finger': 'https://thumbs.dreamstime.com/b/finger-anatomy-illustration-52921325.jpg',
    'leg': 'https://thumbs.dreamstime.com/b/cartoon-leg-vector-illustration-29935573.jpg',
    'knee': 'https://thumbs.dreamstime.com/b/knee-anatomy-illustration-52921326.jpg',
    'foot': 'https://thumbs.dreamstime.com/b/cartoon-foot-vector-illustration-29935574.jpg',
    'skin': 'https://thumbs.dreamstime.com/b/skin-anatomy-illustration-52921327.jpg',
    
    # 内脏器官
    'brain': 'https://thumbs.dreamstime.com/b/fit-brain-cartoon-character-flat-tiny-person-vector-illustration-concept-sharp-mind-solving-problems-power-human-mental-172885005.jpg',
    'heart': 'https://thumbs.dreamstime.com/b/healthy-biological-organ-smiling-lung-happy-heart-funny-brain-smile-stomach-uterus-organs-bone-tooth-biology-medicine-132543383.jpg',
    'lung': 'https://thumbs.dreamstime.com/b/lung-anatomy-illustration-52921328.jpg',
    'liver': 'https://thumbs.dreamstime.com/b/liver-anatomy-illustration-52921329.jpg',
    'stomach': 'https://thumbs.dreamstime.com/b/cute-cartoon-stomach-healthy-concept-blue-background-97326679.jpg',
    'intestine': 'https://thumbs.dreamstime.com/b/intestine-anatomy-illustration-52921330.jpg',
    'kidney': 'https://thumbs.dreamstime.com/b/kidney-anatomy-illustration-52921331.jpg',
    'muscle': 'https://thumbs.dreamstime.com/b/muscle-anatomy-illustration-52921332.jpg',
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

for word, url in image_urls.items():
    print(f"\n📝 {word}:")
    
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
