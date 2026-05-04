import urllib.request
import urllib.parse
import time
import os

save_dir = '/workspace/word-app/public/images'
PLACEHOLDER_SIZE = 176626

# 最后3个单词
final_words = [
    ('cupboard', 'furniture', ['kitchen cabinet', 'food storage', 'pantry cabinet', 'storage unit']),
    ('heater', 'appliances', ['heat source', 'warming device', 'portable heater', 'wall heater']),
    ('subway', 'vehicles', ['train', 'railway train', 'electric train', 'passenger train']),
]

def download_final(word, category, prompts):
    filepath = os.path.join(save_dir, f"{word}.jpg")
    
    for i, prompt in enumerate(prompts):
        print(f"  尝试: '{prompt}'")
        
        params = {"prompt": prompt, "image_size": "square"}
        query_string = urllib.parse.urlencode(params)
        session_id = f"{word}_final{i}_{int(time.time()*1000)}"
        url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?{query_string}&session_id={session_id}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
        }
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
            
            size = len(content)
            
            if size != PLACEHOLDER_SIZE:
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"  ✅ 成功 ({size} bytes)")
                return True
            else:
                print(f"  ⚠️ 占位图")
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")
        
        time.sleep(2)
    
    return False

print("=" * 70)
print("最后3个单词重试")
print("=" * 70)

success = 0

for word, category, prompts in final_words:
    print(f"\n📝 {word} ({category}):")
    if download_final(word, category, prompts):
        success += 1

print("\n" + "=" * 70)
print(f"本轮成功: {success}/3 张")
print("=" * 70)
