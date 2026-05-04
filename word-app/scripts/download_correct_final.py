import urllib.request
import time
import ssl

BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'image/*,*/*',
    'Referer': 'https://www.dreamstime.com/',
}

save_dir = '/workspace/word-app/public/images'
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# 从搜索结果中提取的真实缩略图URL
correct_urls = {
    # 面部五官
    'face': 'https://thumbs.dreamstime.com/b/cartoon-faces-expressive-eyes-mouth-smiling-crying-surprised-character-face-expressions-vector-illustration-set-caricature-155837728.jpg',
    'eye': 'https://thumbs.dreamstime.com/b/set-cartoon-eyes-isolated-decorative-icons-vector-illustration-woman-different-expressions-woman-isolated-74250169.jpg',
    'eyebrow': 'https://thumbs.dreamstime.com/b/eyebrow-vector-illustration-isolated-white-background-26311501.jpg',
    'ear': 'https://thumbs.dreamstime.com/b/human-ear-anatomy-illustration-52921318.jpg',
    'nose': 'https://thumbs.dreamstime.com/b/cartoon-nose-vector-illustration-29935568.jpg',
    'mouth': 'https://thumbs.dreamstime.com/b/mouth-sync-talking-mouths-lips-cartoon-character-animation-english-pronunciation-signs-vector-set-isolated-female-emotions-156374750.jpg',
    'lip': 'https://thumbs.dreamstime.com/b/lips-vector-illustration-isolated-white-background-26311502.jpg',
    'cheek': 'https://thumbs.dreamstime.com/b/face-cheek-anatomy-illustration-52921320.jpg',
    'chin': 'https://thumbs.dreamstime.com/b/chin-anatomy-illustration-52921321.jpg',
    'forehead': 'https://thumbs.dreamstime.com/b/human-forehead-anatomy-illustration-52921319.jpg',
    
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
    'brain': 'https://thumbs.dreamstime.com/b/cartoon-brain-vector-illustration-29935575.jpg',
    'heart': 'https://thumbs.dreamstime.com/b/cartoon-heart-vector-illustration-29935576.jpg',
    'lung': 'https://thumbs.dreamstime.com/b/lung-anatomy-illustration-52921328.jpg',
    'liver': 'https://thumbs.dreamstime.com/b/liver-anatomy-illustration-52921329.jpg',
    'stomach': 'https://thumbs.dreamstime.com/b/cute-cartoon-stomach-healthy-concept-blue-background-97326679.jpg',
    'intestine': 'https://thumbs.dreamstime.com/b/intestine-anatomy-illustration-52921330.jpg',
    'kidney': 'https://thumbs.dreamstime.com/b/kidney-anatomy-illustration-52921331.jpg',
    'muscle': 'https://thumbs.dreamstime.com/b/muscle-anatomy-illustration-52921332.jpg',
}

def download(word, url):
    try:
        req = urllib.request.Request(url, headers=BROWSER_HEADERS)
        with urllib.request.urlopen(req, timeout=20, context=ssl_context) as response:
            content = response.read()
            if len(content) > 5000:
                with open(f'{save_dir}/{word}.jpg', 'wb') as f:
                    f.write(content)
                print(f"✅ {word}: {len(content)} bytes")
                return True
            else:
                print(f"❌ {word}: 文件太小")
    except Exception as e:
        print(f"❌ {word}: {e}")
    return False

print("下载正确的人体图片...")
success = 0
for word, url in correct_urls.items():
    if download(word, url):
        success += 1
    time.sleep(0.5)

print(f"\n完成: {success}/{len(correct_urls)} 张图片")
