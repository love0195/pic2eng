import urllib.request
import urllib.parse
import json
import time
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

def generate_image(word, max_wait=60):
    prompt = f"A simple cartoon illustration of a {word} on white background, clean design, single object"
    encoded_prompt = urllib.parse.quote(prompt)
    
    init_url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id=unique_session_{int(time.time() * 1000)}"
    
    filename = f"{word}.png"
    filepath = os.path.join(save_dir, filename)
    
    print(f"⏳ Generating: {filename}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        req = urllib.request.Request(init_url, headers=headers)
        response = urllib.request.urlopen(req, timeout=30)
        result = json.loads(response.read().decode())
        
        if 'task_id' in result:
            task_id = result['task_id']
            print(f"   📝 Task ID: {task_id}")
            
            for i in range(max_wait // 3):
                time.sleep(3)
                
                status_url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image/status?task_id={task_id}"
                status_req = urllib.request.Request(status_url, headers=headers)
                
                try:
                    status_response = urllib.request.urlopen(status_req, timeout=10)
                    status_data = json.loads(status_response.read().decode())
                    
                    if status_data.get('status') == 'completed' and 'image_url' in status_data:
                        img_url = status_data['image_url']
                        
                        img_req = urllib.request.Request(img_url, headers=headers)
                        with urllib.request.urlopen(img_req, timeout=30) as img_response:
                            content = img_response.read()
                            content_length = len(content)
                            
                            if content_length > 10000:
                                with open(filepath, 'wb') as f:
                                    f.write(content)
                                print(f"✅ Success: {filename} ({content_length} bytes)")
                                return True
                            else:
                                print(f"   ⚠️  Image too small, waiting...")
                    elif status_data.get('status') == 'failed':
                        print(f"❌ Generation failed")
                        return False
                    else:
                        print(f"   ⏱️  Still generating... ({i * 3}s)")
                        
                except Exception as e:
                    print(f"   ⚠️  Status check failed: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

total = 0
success = 0

print("=" * 70)
print("开始生成图片（智能等待）...")
print("=" * 70)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    for word in words:
        total += 1
        if generate_image(word):
            success += 1
        else:
            print(f"   ❌ Failed: {word}")

print("\n" + "=" * 70)
print(f"完成: {success}/{total} 张图片")
print(f"保存位置: {save_dir}")
print("=" * 70)
