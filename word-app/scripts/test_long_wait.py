import urllib.request
import urllib.parse
import time
import os
import hashlib

save_dir = '/workspace/word-app/test_images'
os.makedirs(save_dir, exist_ok=True)

def get_file_hash(content):
    return hashlib.md5(content).hexdigest()

def test_long_wait(word):
    print(f"\n{'='*60}")
    print(f"测试单词: {word} - 长时间等待测试")
    print('='*60)
    
    prompt = f"a simple cartoon {word} on white background, single object"
    encoded_prompt = urllib.parse.quote(prompt)
    session_id = f"{word}_longwait_{int(time.time()*1000)}"
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={session_id}"
    
    # 第一次请求
    print("\n第1次请求（触发）...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as response:
        content1 = response.read()
    hash1 = get_file_hash(content1)
    print(f"  大小: {len(content1)} bytes, MD5: {hash1[:16]}...")
    
    # 等待30秒
    print("\n等待30秒...")
    for i in range(30):
        print(f"  {i+1}/30 秒...", end='\r')
        time.sleep(1)
    print()
    
    # 第二次请求
    print("\n第2次请求（检查）...")
    req2 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req2, timeout=60) as response:
        content2 = response.read()
    hash2 = get_file_hash(content2)
    print(f"  大小: {len(content2)} bytes, MD5: {hash2[:16]}...")
    
    # 再等待30秒
    print("\n再等待30秒...")
    for i in range(30):
        print(f"  {i+1}/30 秒...", end='\r')
        time.sleep(1)
    print()
    
    # 第三次请求
    print("\n第3次请求（检查）...")
    req3 = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req3, timeout=60) as response:
        content3 = response.read()
    hash3 = get_file_hash(content3)
    print(f"  大小: {len(content3)} bytes, MD5: {hash3[:16]}...")
    
    # 保存图片
    filepath = os.path.join(save_dir, f"{word}_longwait.jpg")
    with open(filepath, 'wb') as f:
        f.write(content3)
    
    # 比较
    print(f"\n结果分析:")
    print(f"  第1次和第2次相同: {'是' if hash1 == hash2 else '否'}")
    print(f"  第2次和第3次相同: {'是' if hash2 == hash3 else '否'}")
    print(f"  所有图片相同: {'是' if hash1 == hash2 == hash3 else '否'}")

print("测试长时间等待的效果...")

test_long_wait('apple')

print("\n" + "="*60)
print("测试完成！")
print("="*60)
