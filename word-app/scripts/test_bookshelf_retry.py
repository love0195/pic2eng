import urllib.request
import urllib.parse
import time
import os
import hashlib

save_dir = '/workspace/word-app/test_images'
os.makedirs(save_dir, exist_ok=True)

def get_file_hash(content):
    return hashlib.md5(content).hexdigest()

def test_bookshelf_retry():
    print("测试 bookshelf 多次重试...")
    print("="*60)
    
    word = "bookshelf"
    
    # 尝试不同的prompt变体
    prompts = [
        f"cartoon {word}",
        f"{word} cartoon",
        f"a {word}",
        f"{word}",
        f"cartoon empty {word}",
        f"simple {word}",
    ]
    
    for i, prompt in enumerate(prompts):
        print(f"\n尝试 {i+1}: '{prompt}'")
        
        params = {"prompt": prompt, "image_size": "square"}
        query_string = urllib.parse.urlencode(params)
        url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?{query_string}&session_id={word}_retry{i}_{int(time.time()*1000)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
            
            size = len(content)
            file_hash = get_file_hash(content)
            
            filepath = os.path.join(save_dir, f"{word}_retry{i}.jpg")
            with open(filepath, 'wb') as f:
                f.write(content)
            
            status = "✅ 真实图片" if size != 176626 else "⚠️ 占位图"
            print(f"  大小: {size} bytes")
            print(f"  状态: {status}")
            
        except Exception as e:
            print(f"  错误: {e}")
        
        time.sleep(3)

test_bookshelf_retry()

print("\n" + "="*60)
print("测试完成！")
print("="*60)
