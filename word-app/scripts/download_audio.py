import urllib.request
import urllib.error
import os
import time

vocabulary = {
    'furniture': ['sofa', 'table', 'chair', 'bed', 'desk', 'bookshelf', 'wardrobe', 'lamp', 'cabinet', 'stool', 'cupboard', 'drawer'],
    'appliances': ['refrigerator', 'television', 'washing', 'microwave', 'oven', 'dishwasher', 'airconditioner', 'computer', 'fan', 'heater', 'coffee', 'toaster'],
    'vehicles': ['car', 'bus', 'train', 'plane', 'bicycle', 'motorcycle', 'ship', 'boat', 'taxi', 'subway', 'truck', 'helicopter'],
    'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'parrot', 'turtle', 'snake', 'elephant', 'monkey', 'panda'],
    'fruits': ['apple', 'banana', 'orange', 'grape', 'watermelon', 'strawberry', 'pineapple', 'mango', 'peach', 'pear', 'lemon', 'cherry']
}

save_dir = '/workspace/word-app/public/audio'
os.makedirs(save_dir, exist_ok=True)

def download_audio(word):
    url = f"http://dict.youdao.com/dictvoice?audio={urllib.parse.quote(word)}&type=2"
    filename = f"{word}.mp3"
    filepath = os.path.join(save_dir, filename)
    
    if os.path.exists(filepath):
        print(f"⏭️  Skip: {filename} (already exists)")
        return True
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        print(f"⬇️  Downloading: {filename}")
        with urllib.request.urlopen(req, timeout=30) as response:
            content_type = response.headers.get('Content-Type', '')
            if 'audio' not in content_type and response.headers.get('Content-Length', 0) == '0':
                print(f"❌ Failed: {filename} - Not audio content")
                return False
            
            with open(filepath, 'wb') as f:
                f.write(response.read())
        
        if os.path.getsize(filepath) < 1000:
            print(f"❌ Failed: {filename} - File too small")
            os.remove(filepath)
            return False
        
        print(f"✅ Success: {filename}")
        time.sleep(0.3)
        return True
        
    except Exception as e:
        print(f"❌ Failed: {filename} - {e}")
        if os.path.exists(filepath):
            os.remove(filepath)
        return False

import urllib.parse

total = 0
success = 0

print("=" * 60)
print("开始下载所有语音文件...")
print("=" * 60)

for category, words in vocabulary.items():
    print(f"\n📂 分类: {category}")
    for word in words:
        total += 1
        if download_audio(word):
            success += 1

print("\n" + "=" * 60)
print(f"下载完成: {success}/{total} 个音频")
print(f"保存位置: {save_dir}")
print("=" * 60)
