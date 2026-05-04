import urllib.request
import urllib.parse
import json

word = "apple"
prompt = f"a simple cartoon {word} on white background"
encoded_prompt = urllib.parse.quote(prompt)
url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square"

print(f"请求URL: {url[:80]}...")
print()

try:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json, image/*'
    })
    
    with urllib.request.urlopen(req, timeout=60) as response:
        content_type = response.headers.get('Content-Type', '')
        content = response.read()
        
        print(f"Content-Type: {content_type}")
        print(f"Content-Length: {len(content)} bytes")
        print()
        
        # 尝试解析为JSON
        try:
            json_data = json.loads(content.decode('utf-8'))
            print("✅ 响应是JSON格式:")
            print(json.dumps(json_data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print("❌ 响应不是JSON格式")
            print()
            print("响应前200字节:")
            print(content[:200])
            
            # 检查是否是图片
            if content[:3] == b'\xff\xd8\xff':
                print("\n✅ 这是JPEG图片数据")
            elif content[:4] == b'\x89PNG':
                print("\n✅ 这是PNG图片数据")
                
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
