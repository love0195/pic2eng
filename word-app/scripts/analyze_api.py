import urllib.request
import urllib.parse
import json
import base64

def analyze_api_response():
    word = "apple"
    prompt = f"A simple cartoon illustration of a {word} on white background"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square"
    
    print("分析API响应...")
    print("=" * 70)
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, */*'
        })
        
        response = urllib.request.urlopen(req, timeout=30)
        content = response.read()
        content_type = response.headers.get('Content-Type', '')
        
        print(f"Content-Type: {content_type}")
        print(f"Content-Length: {len(content)} bytes")
        print(f"")
        
        print("检查是否为PNG图片:")
        if content[:4] == b'\x89PNG':
            print("  ✅ 是PNG图片")
        else:
            print("  ❌ 不是PNG图片")
        
        print("\n检查是否为Base64编码:")
        try:
            decoded = base64.b64decode(content)
            if decoded[:4] == b'\x89PNG':
                print(f"  ✅ Base64解码成功，解码后大小: {len(decoded)} bytes")
            else:
                print("  ❌ Base64解码后不是PNG")
        except:
            print("  ❌ 不是有效的Base64")
        
        print("\n检查是否为JSON:")
        try:
            json_data = json.loads(content.decode('utf-8'))
            print(f"  ✅ 是JSON: {type(json_data)}")
            if isinstance(json_data, dict):
                print(f"  JSON字段: {list(json_data.keys())}")
                for key, value in json_data.items():
                    if isinstance(value, str) and len(value) > 100:
                        print(f"    {key}: (长度 {len(value)} 字符串)")
                    elif isinstance(value, str) and value.startswith('data:'):
                        print(f"    {key}: (base64 data URI)")
                    else:
                        print(f"    {key}: {value}")
        except json.JSONDecodeError:
            print("  ❌ 不是JSON")
        
        print("\n原始内容前100字节:")
        print(content[:100])
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

analyze_api_response()
