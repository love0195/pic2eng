import urllib.request
import urllib.parse
import time
import os
import hashlib

save_dir = '/workspace/word-app/test_images'
os.makedirs(save_dir, exist_ok=True)

def get_file_hash(content):
    return hashlib.md5(content).hexdigest()

def test_with_headers_and_wait(word):
    print(f"\n{'='*60}")
    print(f"测试单词: {word}")
    print('='*60)
    
    prompt = f"a simple cartoon {word} on white background, single object"
    encoded_prompt = urllib.parse.quote(prompt)
    session_id = f"{word}_browser_{int(time.time()*1000)}"
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={session_id}"
    
    # 记录链接
    print(f"\n生成的URL:")
    print(f"  {url}")
    
    # 完整的浏览器头部
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
    }
    
    # 第一次请求
    print("\n第1次请求...")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as response:
        content1 = response.read()
        response_headers = dict(response.headers)
    
    hash1 = get_file_hash(content1)
    print(f"  大小: {len(content1)} bytes")
    print(f"  MD5: {hash1}")
    print(f"  响应头: Content-Type={response_headers.get('Content-Type', 'N/A')}")
    
    # 等待
    wait_time = 60
    print(f"\n等待 {wait_time} 秒后再次请求...")
    for i in range(wait_time):
        if i % 10 == 0:
            print(f"  已等待 {i}/{wait_time} 秒...")
        time.sleep(1)
    
    # 第二次请求（相同URL）
    print(f"\n第2次请求（相同URL）...")
    req2 = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req2, timeout=60) as response:
        content2 = response.read()
    
    hash2 = get_file_hash(content2)
    print(f"  大小: {len(content2)} bytes")
    print(f"  MD5: {hash2}")
    
    # 保存图片
    filepath1 = os.path.join(save_dir, f"{word}_browser_1.jpg")
    filepath2 = os.path.join(save_dir, f"{word}_browser_2.jpg")
    with open(filepath1, 'wb') as f:
        f.write(content1)
    with open(filepath2, 'wb') as f:
        f.write(content2)
    
    # 比较
    print(f"\n结果分析:")
    print(f"  两次图片相同: {'是' if hash1 == hash2 else '否 ✅'}")
    print(f"  保存位置:")
    print(f"    {filepath1}")
    print(f"    {filepath2}")
    
    return url, hash1, hash2

print("测试带完整浏览器头部的请求...")
print("记录链接，等待后再次获取\n")

urls = []
test_words = ['apple', 'bookshelf']

for word in test_words:
    url, h1, h2 = test_with_headers_and_wait(word)
    urls.append((word, url, h1, h2))
    time.sleep(5)

print("\n" + "="*60)
print("汇总结果:")
print("="*60)
for word, url, h1, h2 in urls:
    print(f"\n{word}:")
    print(f"  URL: {url[:60]}...")
    print(f"  第1次MD5: {h1}")
    print(f"  第2次MD5: {h2}")
    print(f"  相同: {'是' if h1 == h2 else '否'}")
