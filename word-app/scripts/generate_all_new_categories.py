import urllib.request
import urllib.parse
import time
import os

images_dir = '/workspace/word-app/public/images'
audio_dir = '/workspace/word-app/public/audio'
os.makedirs(images_dir, exist_ok=True)
os.makedirs(audio_dir, exist_ok=True)

PLACEHOLDER_SIZE = 176626

all_new_words = [
    # 人体
    'head', 'hand', 'foot', 'arm', 'leg', 'neck', 'shoulder', 'finger', 'knee', 'elbow',
    # 面部
    'eye', 'nose', 'mouth', 'ear', 'tooth', 'lip', 'eyebrow', 'cheek', 'chin', 'forehead',
    # 内脏
    'heart', 'brain', 'lung', 'liver', 'stomach', 'kidney', 'intestine', 'bone', 'muscle', 'skin',
    # 室内空间
    'kitchen', 'bedroom', 'bathroom', 'living room', 'door', 'window', 'floor', 'wall', 'ceiling', 'stairs',
    # 公共建筑
    'school', 'hospital', 'church', 'library', 'museum', 'theater', 'stadium', 'tower', 'castle', 'palace',
]

prompt_map = {
    'living room': 'living room interior',
    'living room': 'living room',
}

def download_image(word):
    filepath = os.path.join(images_dir, f"{word.replace(' ', '_')}.jpg")
    
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size != PLACEHOLDER_SIZE:
            print(f"  ⏭️  {word} (已存在)")
            return True
    
    prompt = prompt_map.get(word, word)
    
    for attempt in range(5):
        params = {"prompt": prompt, "image_size": "square"}
        query_string = urllib.parse.urlencode(params)
        session_id = f"{word.replace(' ', '_')}_{attempt}_{int(time.time()*1000)}"
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
    filepath = os.path.join(audio_dir, f"{word.replace(' ', '_')}.mp3")
    
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

categories = [
    ("人体", all_new_words[:10]),
    ("面部", all_new_words[10:20]),
    ("内脏", all_new_words[20:30]),
    ("室内空间", all_new_words[30:40]),
    ("公共建筑", all_new_words[40:50]),
]

for cat_name, words in categories:
    print(f"\n📂 {cat_name}:")
    for word in words:
        download_image(word)
        download_audio(word)
        time.sleep(0.3)

print("\n" + "="*70)
print("完成！")
print("="*70)
