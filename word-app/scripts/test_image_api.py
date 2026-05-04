import urllib.request
import urllib.parse
import time
import os

def test_api_timing():
    word = "apple"
    prompt = f"A simple cartoon illustration of a {word} on white background"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square"
    
    print("测试图片生成时间...")
    print("=" * 60)
    
    for i in range(5):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0'
            })
            
            start = time.time()
            response = urllib.request.urlopen(req, timeout=30)
            content = response.read()
            elapsed = time.time() - start
            
            size = len(content)
            print(f"第 {i+1} 次请求: 大小={size} bytes, 耗时={elapsed:.2f}s")
            
            if i == 0:
                first_size = size
            
            if size != first_size:
                print(f"✅ 图片已更新！")
                break
                
            if i < 4:
                print(f"   等待 5 秒...")
                time.sleep(5)
                
        except Exception as e:
            print(f"错误: {e}")
            break
    
    print("=" * 60)

test_api_timing()
