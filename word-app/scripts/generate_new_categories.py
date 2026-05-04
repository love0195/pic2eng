import urllib.request
import urllib.parse
import time
import os

images_dir = '/workspace/word-app/public/images'
audio_dir = '/workspace/word-app/public/audio'
os.makedirs(images_dir, exist_ok=True)
os.makedirs(audio_dir, exist_ok=True)

PLACEHOLDER_SIZE = 176626

new_words = [
    # 海洋动物
    'whale', 'dolphin', 'shark', 'octopus', 'jellyfish', 'seahorse', 'crab', 'lobster', 'starfish', 'seal',
    # 哺乳动物
    'lion', 'tiger', 'bear', 'wolf', 'fox', 'deer', 'giraffe', 'zebra', 'kangaroo', 'koala',
    # 植物
    'rose', 'sunflower', 'tulip', 'daisy', 'tree', 'flower', 'grass', 'leaf', 'mushroom', 'bamboo',
]

def download_image(word):
    filepath = os.path.join(images_dir, f"{word}.jpg")
    
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size != PLACEHOLDER_SIZE:
            print(f"  ⏭️  {word} (已存在)")
            return True
    
    for attempt in range(5):
        params = {"prompt": word, "image_size": "square"}
        query_string = urllib.parse.urlencode(params)
        session_id = f"{word}_new_{attempt}_{int(time.time()*1000)}"
        url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?{query_string}&session_id={session_id}"
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'Accept': '*/*'}
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
            
            size = len(content)
            if size != PLACEHOLDER_SIZE:
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"  ✅ {word} ({size} bytes)")
                return True
            else:
                print(f"  ⏳ {word} 占位图，重试 {attempt + 2}/5...")
                time.sleep(2)
        except Exception as e:
            print(f"  ⚠️ {word} 错误: {e}")
            time.sleep(2)
    
    print(f"  ❌ {word} 失败")
    return False

def download_audio(word):
    filepath = os.path.join(audio_dir, f"{word}.mp3")
    
    if os.path.exists(filepath):
        print(f"  ⏭️  {word} 音频 (已存在)")
        return True
    
    url = f"http://dict.youdao.com/dictvoice?audio={urllib.parse.quote(word)}&type=2"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            
            if len(content) > 1000:
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"  ✅ {word} 音频")
                return True
    except Exception as e:
        print(f"  ⚠️ {word} 音频错误: {e}")
    
    return False

print("="*70)
print("生成新分类的图片和语音")
print("="*70)

# 海洋动物
print("\n📂 海洋动物:")
for word in new_words[:10]:
    download_image(word)
    download_audio(word)
    time.sleep(0.5)

# 哺乳动物
print("\n📂 哺乳动物:")
for word in new_words[10:20]:
    download_image(word)
    download_audio(word)
    time.sleep(0.5)

# 植物
print("\n📂 植物:")
for word in new_words[20:]:
    download_image(word)
    download_audio(word)
    time.sleep(0.5)

print("\n" + "="*70)
print("完成！")
print("="*70)
