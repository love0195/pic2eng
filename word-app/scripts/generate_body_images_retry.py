import urllib.request
import urllib.parse
import time
import os

save_dir = '/workspace/word-app/public/images'
PLACEHOLDER_SIZE = 176626

body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

prompt_variations = {
    'face': ['human face cartoon', 'cartoon face illustration', 'simple face drawing'],
    'forehead': ['human forehead cartoon', 'forehead illustration', 'forehead part'],
    'eye': ['human eye cartoon', 'eye illustration', 'cartoon eye drawing'],
    'eyebrow': ['eyebrow cartoon', 'eyebrow illustration', 'eyebrow drawing'],
    'ear': ['human ear cartoon', 'ear illustration', 'cartoon ear'],
    'nose': ['human nose cartoon', 'nose illustration', 'cartoon nose'],
    'cheek': ['cheek cartoon', 'cheek illustration', 'human cheek drawing'],
    'mouth': ['human mouth cartoon', 'mouth illustration', 'cartoon mouth'],
    'lip': ['human lips cartoon', 'lips illustration', 'cartoon lips'],
    'chin': ['human chin cartoon', 'chin illustration', 'cartoon chin'],
    'head': ['human head cartoon', 'head illustration', 'cartoon head'],
    'neck': ['human neck cartoon', 'neck illustration', 'cartoon neck'],
    'shoulder': ['human shoulder cartoon', 'shoulder illustration', 'cartoon shoulder'],
    'arm': ['human arm cartoon', 'arm illustration', 'cartoon arm'],
    'elbow': ['human elbow cartoon', 'elbow illustration', 'cartoon elbow'],
    'hand': ['human hand cartoon', 'hand illustration', 'cartoon hand'],
    'finger': ['human finger cartoon', 'finger illustration', 'cartoon finger'],
    'leg': ['human leg cartoon', 'leg illustration', 'cartoon leg'],
    'knee': ['human knee cartoon', 'knee illustration', 'cartoon knee'],
    'foot': ['human foot cartoon', 'foot illustration', 'cartoon foot'],
    'skin': ['human skin cartoon', 'skin texture illustration', 'skin drawing'],
    'brain': ['human brain cartoon', 'brain illustration', 'cartoon brain anatomy'],
    'heart': ['human heart cartoon', 'heart illustration', 'cartoon heart organ'],
    'lung': ['human lung cartoon', 'lung illustration', 'cartoon lungs anatomy'],
    'liver': ['human liver cartoon', 'liver illustration', 'cartoon liver organ'],
    'stomach': ['human stomach cartoon', 'stomach illustration', 'cartoon stomach'],
    'intestine': ['human intestine cartoon', 'intestine illustration', 'cartoon intestines'],
    'kidney': ['human kidney cartoon', 'kidney illustration', 'cartoon kidney organ'],
    'muscle': ['human muscle cartoon', 'muscle illustration', 'cartoon muscle anatomy'],
}

def download_with_retries(word):
    filepath = os.path.join(save_dir, f"{word}.jpg")
    
    base_prompt = f"A simple cartoon illustration of a {word} on white background, clean design, educational style"
    variations = prompt_variations.get(word, [word])
    
    for retry in range(12):
        # 尝试不同的prompt变体，或者添加延迟
        if retry < len(variations):
            prompt = f"A simple cartoon illustration of a {variations[retry]} on white background, clean design"
        else:
            prompt = base_prompt
        
        print(f"  尝试 {retry + 1}: '{prompt[:40]}...'")
        
        params = {"prompt": prompt, "image_size": "square"}
        query_string = urllib.parse.urlencode(params)
        session_id = f"body_{word}_retry{retry}_{int(time.time()*1000)}"
        url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?{query_string}&session_id={session_id}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
        }
        
        try:
            # 第一次等待稍长一点
            wait_time = 8 if retry < 3 else 4
            print(f"    等待 {wait_time} 秒让图片生成...")
            time.sleep(wait_time)
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=90) as response:
                content = response.read()
            
            size = len(content)
            
            if size != PLACEHOLDER_SIZE and size > 10000:
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"  ✅ 成功获得真实图片 ({size} bytes)")
                return True
            else:
                print(f"  ⚠️ 占位图 ({size} bytes)")
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")
        
        time.sleep(3)
    
    return False

print("=" * 70)
print("为人体词汇生成真实图片（检测占位图并重试）")
print("=" * 70)

success = 0
total = len(body_words)

for word in body_words:
    print(f"\n📝 {word}:")
    if download_with_retries(word):
        success += 1
    time.sleep(2)

print("\n" + "=" * 70)
print(f"完成: {success}/{total} 张真实图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
