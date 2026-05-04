import urllib.request
import urllib.parse
import time
import os

test_words = ['bookshelf', 'desk', 'apple', 'dog', 'car']

save_dir = '/workspace/word-app/test_images'
os.makedirs(save_dir, exist_ok=True)

def test_image_generation(word):
    print(f"\n{'='*60}")
    print(f"测试单词: {word}")
    print('='*60)
    
    prompts = [
        f"a simple cartoon {word} on white background, single object, clean design",
        f"a cute cartoon illustration of a {word}, isolated on white background, simple style",
        f"clipart style {word}, white background, single object, no other objects"
    ]
    
    for i, prompt in enumerate(prompts):
        print(f"\nPrompt {i+1}: {prompt[:50]}...")
        
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={word}_{i}_{int(time.time()*1000)}"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            start = time.time()
            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
                elapsed = time.time() - start
            
            filepath = os.path.join(save_dir, f"{word}_prompt{i+1}.jpg")
            with open(filepath, 'wb') as f:
                f.write(content)
            
            print(f"  大小: {len(content)} bytes")
            print(f"  耗时: {elapsed:.2f}s")
            print(f"  保存: {filepath}")
            
            time.sleep(2)
            
        except Exception as e:
            print(f"  错误: {e}")

print("开始测试图片生成API...")
print("测试目录:", save_dir)

for word in test_words:
    test_image_generation(word)
    time.sleep(3)

print("\n" + "="*60)
print("测试完成！请查看图片效果")
print("="*60)
