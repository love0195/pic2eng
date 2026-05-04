import urllib.request
import urllib.parse
import time
import ssl
import os

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

MAX_RETRIES = 10
WAIT_INTERVAL = 30
PLACEHOLDER_SIZE = 176626

def generate_image_with_retry(word):
    """尝试生成图片，等待最多10次，每次30秒"""
    
    prompt = f"A simple cartoon illustration of a human {word} on white background, clean design, educational style, flat illustration"
    encoded_prompt = urllib.parse.quote(prompt)
    session_id = f"body_{word}_{int(time.time()*1000)}"
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={session_id}"
    
    print(f"\n📝 生成: {word}")
    print(f"   Prompt: {prompt}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'image/jpeg, image/*, */*',
    }
    
    try:
        # 发送请求触发生成
        print(f"   发送请求...")
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=60) as response:
            initial_content = response.read()
            print(f"   初始响应: {len(initial_content)} bytes")
        
        # 等待并重复检测
        for attempt in range(1, MAX_RETRIES + 1):
            print(f"\n   第 {attempt}/{MAX_RETRIES} 次检测...")
            print(f"   等待 {WAIT_INTERVAL} 秒...")
            time.sleep(WAIT_INTERVAL)
            
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=60) as response:
                    content = response.read()
                    
                    print(f"   响应大小: {len(content)} bytes")
                    
                    # 检查是否是真实图片
                    if len(content) > PLACEHOLDER_SIZE or (len(content) > 10000 and content[:2] == b'\xff\xd8'):
                        if len(content) != PLACEHOLDER_SIZE:
                            print(f"   ✅ 成功获得真实图片!")
                            
                            filepath = os.path.join(save_dir, f"{word}.jpg")
                            with open(filepath, 'wb') as f:
                                f.write(content)
                            print(f"   ✅ 已保存: {filepath} ({len(content)} bytes)")
                            return True
                        else:
                            print(f"   ⚠️ 仍是占位图")
                    else:
                        print(f"   ⚠️ 内容异常: {len(content)} bytes")
                        
            except Exception as e:
                print(f"   ❌ 检测失败: {e}")
        
        print(f"   ❌ {MAX_RETRIES}次检测后仍未获得真实图片")
        return False
        
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
        return False

# 测试生成 face 图片
if __name__ == '__main__':
    word = 'face'
    success = generate_image_with_retry(word)
    
    if success:
        print(f"\n✅ {word} 生成成功!")
    else:
        print(f"\n❌ {word} 生成失败")
