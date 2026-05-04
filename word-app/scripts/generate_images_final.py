import urllib.request
import urllib.parse
import base64
import time
import json
import os

vocabulary = {
    'furniture': ['sofa', 'table', 'chair', 'bed', 'desk', 'bookshelf', 'wardrobe', 'lamp', 'cabinet', 'stool', 'cupboard', 'drawer'],
    'appliances': ['refrigerator', 'television', 'washing', 'microwave', 'oven', 'dishwasher', 'airconditioner', 'computer', 'fan', 'heater', 'coffee', 'toaster'],
    'vehicles': ['car', 'bus', 'train', 'plane', 'bicycle', 'motorcycle', 'ship', 'boat', 'taxi', 'subway', 'truck', 'helicopter'],
    'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'parrot', 'turtle', 'snake', 'elephant', 'monkey', 'panda'],
    'fruits': ['apple', 'banana', 'orange', 'grape', 'watermelon', 'strawberry', 'pineapple', 'mango', 'peach', 'pear', 'lemon', 'cherry']
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
    prompt = f"A simple cartoon illustration of a {word} on white background, clean design, single object"
    encoded_prompt = urllib.parse.quote(prompt)
    
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id=img_{word}_{int(time.time())}"
    
    filename = f"{word}.png"
    filepath = os.path.join(save_dir, filename)
    
    print(f"\n⏳ 正在生成: {filename}")
    
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, image/png, image/*, */*'
            })
            
            response = urllib.request.urlopen(req, timeout=60)
            content = response.read()
            
            content_type = response.headers.get('Content-Type', '')
            
            if try_decode_as_base64(content, filepath):
                return True
            
            if content[:4] in [b'\x89PNG', b'\xff\xd8\xff', b'GIF8']:
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"✅ 直接保存成功: {filename} ({len(content)} bytes)")
                return True
            
            try:
                json_data = json.loads(content.decode('utf-8'))
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
                        time.sleep(5)
                        continue
            except json.JSONDecodeError:
                pass
            
            print(f"   ⚠️  尝试 {attempt + 1}: 内容类型={content_type}, 大小={len(content)}")
            time.sleep(3)
            
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            time.sleep(3)
    
    print(f"❌ 生成失败: {filename}")
    return False

total = 0
success = 0

print("=" * 70)
print("开始生成图片（智能检测格式）...")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    for word in words:
        total += 1
        if generate_image_smart(word):
            success += 1
        time.sleep(0.5)

print("\n" + "=" * 70)
print(f"完成: {success}/{total} 张图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
