import urllib.request
import urllib.parse
import time
import os
import hashlib

save_dir = '/workspace/word-app/test_images'
os.makedirs(save_dir, exist_ok=True)

def get_file_hash(content):
    return hashlib.md5(content).hexdigest()

def test_short_prompts():
    print("测试简短prompt的效果...")
    print("="*60)
    
    test_words = ['bookshelf', 'desk', 'dog', 'car', 'apple']
    
    for word in test_words:
        print(f"\n单词: {word}")
        
        # 使用简短prompt
        prompt = f"cartoon {word}"
        params = {"prompt": prompt, "image_size": "square"}
        query_string = urllib.parse.urlencode(params)
        url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?{query_string}&session_id={word}_short_{int(time.time()*1000)}"
        
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
            
            filepath = os.path.join(save_dir, f"{word}_short.jpg")
            with open(filepath, 'wb') as f:
                f.write(content)
            
            status = "✅ 真实图片" if size != 176626 else "⚠️ 占位图"
            print(f"  大小: {size} bytes")
            print(f"  MD5: {file_hash[:16]}...")
            print(f"  状态: {status}")
            print(f"  保存: {filepath}")
            
        except Exception as e:
            print(f"  错误: {e}")
        
        time.sleep(2)

test_short_prompts()

print("\n" + "="*60)
print("测试完成！检查图片是否不同。")
print("="*60)
