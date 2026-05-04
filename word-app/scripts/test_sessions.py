import urllib.request
import urllib.parse
import time
import os
import hashlib

save_dir = '/workspace/word-app/test_images'
os.makedirs(save_dir, exist_ok=True)

def get_file_hash(content):
    return hashlib.md5(content).hexdigest()

def test_different_sessions(word, count=5):
    print(f"\n{'='*60}")
    print(f"测试单词: {word} - 使用不同session_id")
    print('='*60)
    
    prompt = f"a simple cartoon {word} on white background, single object"
    encoded_prompt = urllib.parse.quote(prompt)
    
    hashes = []
    
    for i in range(count):
        session_id = f"{word}_unique_{i}_{int(time.time()*1000)}_{i}"
        url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={session_id}"
        
        print(f"\n请求 {i+1}: session_id={session_id[:30]}...")
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
            
            file_hash = get_file_hash(content)
            hashes.append(file_hash)
            
            filepath = os.path.join(save_dir, f"{word}_session{i}.jpg")
            with open(filepath, 'wb') as f:
                f.write(content)
            
            print(f"  大小: {len(content)} bytes")
            print(f"  MD5: {file_hash}")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"  错误: {e}")
    
    # 检查是否有不同的图片
    unique_hashes = set(hashes)
    print(f"\n结果分析:")
    print(f"  总请求数: {count}")
    print(f"  不同图片数: {len(unique_hashes)}")
    print(f"  所有图片相同: {'是' if len(unique_hashes) == 1 else '否'}")

print("测试不同session_id的效果...")

test_words = ['bookshelf', 'apple']
for word in test_words:
    test_different_sessions(word, 5)
    time.sleep(2)

print("\n" + "="*60)
print("测试完成！")
print("="*60)
