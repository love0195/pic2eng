import urllib.request
import urllib.parse
import base64
import time
import json
import os

body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

prompts = {
    'face': "A simple cartoon illustration of a human face on white background, clean design, educational style",
    'forehead': "A simple cartoon illustration of a human forehead on white background, clean design, educational style",
    'eye': "A simple cartoon illustration of a human eye on white background, clean design, educational style",
    'eyebrow': "A simple cartoon illustration of a human eyebrow on white background, clean design, educational style",
    'ear': "A simple cartoon illustration of a human ear on white background, clean design, educational style",
    'nose': "A simple cartoon illustration of a human nose on white background, clean design, educational style",
    'cheek': "A simple cartoon illustration of a human cheek on white background, clean design, educational style",
    'mouth': "A simple cartoon illustration of a human mouth on white background, clean design, educational style",
    'lip': "A simple cartoon illustration of human lips on white background, clean design, educational style",
    'chin': "A simple cartoon illustration of a human chin on white background, clean design, educational style",
    'head': "A simple cartoon illustration of a human head on white background, clean design, educational style",
    'neck': "A simple cartoon illustration of a human neck on white background, clean design, educational style",
    'shoulder': "A simple cartoon illustration of a human shoulder on white background, clean design, educational style",
    'arm': "A simple cartoon illustration of a human arm on white background, clean design, educational style",
    'elbow': "A simple cartoon illustration of a human elbow on white background, clean design, educational style",
    'hand': "A simple cartoon illustration of a human hand on white background, clean design, educational style",
    'finger': "A simple cartoon illustration of a human finger on white background, clean design, educational style",
    'leg': "A simple cartoon illustration of a human leg on white background, clean design, educational style",
    'knee': "A simple cartoon illustration of a human knee on white background, clean design, educational style",
    'foot': "A simple cartoon illustration of a human foot on white background, clean design, educational style",
    'skin': "A simple cartoon illustration of human skin on white background, clean design, educational style",
    'brain': "A simple cartoon illustration of a human brain on white background, clean design, educational style, anatomy diagram",
    'heart': "A simple cartoon illustration of a human heart on white background, clean design, educational style, anatomy diagram",
    'lung': "A simple cartoon illustration of human lungs on white background, clean design, educational style, anatomy diagram",
    'liver': "A simple cartoon illustration of a human liver on white background, clean design, educational style, anatomy diagram",
    'stomach': "A simple cartoon illustration of a human stomach on white background, clean design, educational style, anatomy diagram",
    'intestine': "A simple cartoon illustration of human intestines on white background, clean design, educational style, anatomy diagram",
    'kidney': "A simple cartoon illustration of a human kidney on white background, clean design, educational style, anatomy diagram",
    'muscle': "A simple cartoon illustration of a human muscle on white background, clean design, educational style, anatomy diagram"
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

def try_decode_as_base64(data, filename):
    try:
        decoded = base64.b64decode(data)
        if len(decoded) > 5000 and decoded[:4] in [b'\x89PNG', b'\xff\xd8\xff', b'GIF8', b'RIFF']:
            with open(filename, 'wb') as f:
                f.write(decoded)
            print(f"✅ Base64解码成功: {filename} ({len(decoded)} bytes)")
            return True
    except:
        pass
    return False

def generate_image_smart(word, max_wait=120):
    prompt = prompts.get(word, f"A simple cartoon illustration of a {word} on white background, clean design, educational style")
    encoded_prompt = urllib.parse.quote(prompt)
    
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id=body_{word}_{int(time.time())}"
    
    filename = f"{word}.jpg"
    filepath = os.path.join(save_dir, filename)
    
    print(f"\n⏳ 正在生成: {filename}")
    
    for attempt in range(10):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'image/jpeg, image/png, image/*, */*'
            })
            
            response = urllib.request.urlopen(req, timeout=90)
            content = response.read()
            
            # 首先检查是不是图片数据
            if len(content) > 100 and (content[:4] in [b'\x89PNG', b'\xff\xd8\xff', b'GIF8'] or content.startswith(b'\xff\xd8')):
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"✅ 直接保存图片成功: {filename} ({len(content)} bytes)")
                return True
            
            # 尝试base64解码
            if try_decode_as_base64(content, filepath):
                return True
            
            # 尝试JSON解析
            try:
                json_str = content.decode('utf-8', errors='ignore')
                json_data = json.loads(json_str)
                if isinstance(json_data, dict):
                    if 'image' in json_data:
                        img_data = json_data['image']
                        if isinstance(img_data, str):
                            if img_data.startswith('data:image'):
                                img_data = img_data.split(',')[1]
                            decoded = base64.b64decode(img_data)
                            with open(filepath, 'wb') as f:
                                f.write(decoded)
                            print(f"✅ JSON base64保存成功: {filename} ({len(decoded)} bytes)")
                            return True
                    elif 'url' in json_data:
                        img_url = json_data['url']
                        img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(img_req, timeout=30) as img_response:
                            img_content = img_response.read()
                            with open(filepath, 'wb') as f:
                                f.write(img_content)
                            print(f"✅ URL下载成功: {filename} ({len(img_content)} bytes)")
                            return True
                    elif 'task_id' in json_data:
                        print(f"   📝 获取到任务ID: {json_data['task_id']}, 等待生成...")
                        time.sleep(8)
                        continue
            except:
                pass
            
            print(f"   ⚠️  尝试 {attempt + 1}: 大小={len(content)}, 前10字节={content[:10] if len(content)>=10 else content}")
            time.sleep(4)
            
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            time.sleep(3)
    
    print(f"❌ 生成失败: {filename}")
    return False

total = 0
success = 0

print("=" * 70)
print("开始生成人体相关图片...")
print("=" * 70)

for word in body_words:
    total += 1
    if generate_image_smart(word):
        success += 1
    time.sleep(1.5)

print("\n" + "=" * 70)
print(f"完成: {success}/{total} 张图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
