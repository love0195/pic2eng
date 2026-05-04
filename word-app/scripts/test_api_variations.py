import urllib.request
import urllib.parse
import time
import os
import base64
import json

save_dir = '/workspace/word-app/test_images'
os.makedirs(save_dir, exist_ok=True)

# 尝试不同的API参数组合
def test_api_variations(word):
    print(f"\n{'='*60}")
    print(f"测试单词: {word}")
    print('='*60)
    
    base_url = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image"
    
    variations = [
        # 不同的参数组合
        {"prompt": f"cartoon {word}", "image_size": "square"},
        {"prompt": f"a {word} clipart", "image_size": "square"},
        {"prompt": f"{word} illustration", "image_size": "square_hd"},
        {"prompt": f"simple {word} drawing", "image_size": "square"},
    ]
    
    for i, params in enumerate(variations):
        print(f"\n变体 {i+1}: {params['prompt'][:30]}... (size={params['image_size']})")
        
        query_string = urllib.parse.urlencode(params)
        url = f"{base_url}?{query_string}&session_id={word}_var{i}_{int(time.time()*1000)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
                content_type = response.headers.get('Content-Type', '')
            
            print(f"  大小: {len(content)} bytes")
            print(f"  类型: {content_type}")
            
            # 检查是否是不同的图片
            if len(content) != 176626:
                print(f"  ✅ 图片大小不同！可能是真实图片")
            
            filepath = os.path.join(save_dir, f"{word}_var{i}.jpg")
            with open(filepath, 'wb') as f:
                f.write(content)
            
        except Exception as e:
            print(f"  错误: {e}")
        
        time.sleep(2)

# 测试
test_api_variations('apple')

# 尝试检查返回的图片内容
print("\n" + "="*60)
print("检查占位图片内容...")
print("="*60)

placeholder_path = '/workspace/word-app/test_images/apple_browser_1.jpg'
with open(placeholder_path, 'rb') as f:
    content = f.read()

# 检查JPEG注释或EXIF数据
print(f"文件大小: {len(content)} bytes")
print(f"文件头: {content[:20].hex()}")

# 尝试找到JPEG中的文本信息
try:
    # JPEG EOI 标记是 FF D9
    eoi_pos = content.rfind(b'\xff\xd9')
    print(f"JPEG结束位置: {eoi_pos}")
except:
    pass
