import urllib.request
import urllib.parse
import time
import os
import hashlib

test_words = ['bookshelf', 'apple', 'dog']

save_dir = '/workspace/word-app/test_images'
os.makedirs(save_dir, exist_ok=True)

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def test_with_wait(word):
    print(f"\n{'='*60}")
    print(f"测试单词: {word}")
    print('='*60)
    
    prompt = f"a simple cartoon {word} on white background, single object"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={word}_wait_{int(time.time()*1000)}"
    
    # 第一次请求
    print("第一次请求...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as response:
        content1 = response.read()
    
    filepath1 = os.path.join(save_dir, f"{word}_first.jpg")
    with open(filepath1, 'wb') as f:
        f.write(content1)
    print(f"  大小: {len(content1)} bytes")
    
    # 等待
    print("等待10秒...")
    time.sleep(10)
    
    # 第二次请求（相同URL）
    print("第二次请求（相同URL）...")
    req2 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req2, timeout=60) as response:
        content2 = response.read()
    
    filepath2 = os.path.join(save_dir, f"{word}_second.jpg")
    with open(filepath2, 'wb') as f:
        f.write(content2)
    print(f"  大小: {len(content2)} bytes")
    
    # 比较两次结果
    hash1 = get_file_hash(filepath1)
    hash2 = get_file_hash(filepath2)
    
    print(f"\n比较结果:")
    print(f"  第一次MD5: {hash1}")
    print(f"  第二次MD5: {hash2}")
    print(f"  文件相同: {'是' if hash1 == hash2 else '否'}")

print("测试图片生成API（带等待）...")

for word in test_words:
    test_with_wait(word)
    time.sleep(2)

print("\n" + "="*60)
print("测试完成！")
print("="*60)
