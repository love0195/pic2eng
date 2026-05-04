#!/usr/bin/env python3
"""
生成卡通插图风格的图片
使用AI图片生成API，专门的提示词
"""
import urllib.request
import urllib.parse
import time
import json
from pathlib import Path

# 配置
BASE_DIR = Path('/workspace/word-app')
IMAGES_DIR = BASE_DIR / 'public' / 'images'
LINKS_FILE = BASE_DIR / 'docs' / 'cartoon_image_results.json'

# 人体相关词汇 - 专门的卡通插图提示词
CARTOON_PROMPTS = {
    'face': 'cute cartoon human face, simple flat design, white background, kawaii style, clean lines, educational illustration',
    'forehead': 'cute cartoon human forehead, simple flat design, white background, kawaii style, clean lines',
    'eye': 'cute cartoon human eye, simple flat design, white background, kawaii style, clean lines, big eye',
    'eyebrow': 'cute cartoon human eyebrow, simple flat design, white background, kawaii style, clean lines',
    'ear': 'cute cartoon human ear, simple flat design, white background, kawaii style, clean lines',
    'nose': 'cute cartoon human nose, simple flat design, white background, kawaii style, clean lines',
    'cheek': 'cute cartoon human cheek, simple flat design, white background, kawaii style, clean lines, pink blush',
    'mouth': 'cute cartoon human mouth smiling, simple flat design, white background, kawaii style, clean lines',
    'lip': 'cute cartoon human lips, simple flat design, white background, kawaii style, clean lines',
    'chin': 'cute cartoon human chin, simple flat design, white background, kawaii style, clean lines',
    'head': 'cute cartoon human head, simple flat design, white background, kawaii style, clean lines',
    'neck': 'cute cartoon human neck, simple flat design, white background, kawaii style, clean lines',
    'shoulder': 'cute cartoon human shoulder, simple flat design, white background, kawaii style, clean lines',
    'arm': 'cute cartoon human arm, simple flat design, white background, kawaii style, clean lines',
    'elbow': 'cute cartoon human elbow, simple flat design, white background, kawaii style, clean lines',
    'hand': 'cute cartoon human hand, simple flat design, white background, kawaii style, clean lines, five fingers',
    'finger': 'cute cartoon human finger, simple flat design, white background, kawaii style, clean lines',
    'leg': 'cute cartoon human leg, simple flat design, white background, kawaii style, clean lines',
    'knee': 'cute cartoon human knee, simple flat design, white background, kawaii style, clean lines',
    'foot': 'cute cartoon human foot, simple flat design, white background, kawaii style, clean lines',
    'skin': 'cute cartoon human skin texture, simple flat design, white background, kawaii style, clean lines',
    'brain': 'cute cartoon human brain, simple flat design, white background, kawaii style, clean lines, anatomy',
    'heart': 'cute cartoon human heart, simple flat design, white background, kawaii style, clean lines, anatomy',
    'lung': 'cute cartoon human lungs, simple flat design, white background, kawaii style, clean lines, anatomy',
    'liver': 'cute cartoon human liver, simple flat design, white background, kawaii style, clean lines, anatomy',
    'stomach': 'cute cartoon human stomach, simple flat design, white background, kawaii style, clean lines, anatomy',
    'intestine': 'cute cartoon human intestine, simple flat design, white background, kawaii style, clean lines, anatomy',
    'kidney': 'cute cartoon human kidney, simple flat design, white background, kawaii style, clean lines, anatomy',
    'muscle': 'cute cartoon human muscle, simple flat design, white background, kawaii style, clean lines, anatomy'
}

PLACEHOLDER_SIZE = 176626
MIN_IMAGE_SIZE = 100000  # AI生成的图片通常较大

def generate_image_url(word, prompt):
    """生成AI图片API URL"""
    encoded_prompt = urllib.parse.quote(prompt)
    # 添加时间戳确保每次请求都是新的
    timestamp = int(time.time() * 1000)
    session_id = f"cartoon_{word}_{timestamp}"
    
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={session_id}"
    return url

def download_and_check(word, url, max_retries=5, retry_delay=60):
    """下载并检查图片"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        print(f"\n  📥 尝试 {attempt + 1}/{max_retries}...")
        
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as response:
                content = response.read()
                size = len(content)
                
            print(f"    响应大小: {size} bytes")
            
            # 检查是否是占位图
            if size == PLACEHOLDER_SIZE:
                print(f"    ⏳ 占位图，等待 {retry_delay} 秒...")
                time.sleep(retry_delay)
                continue
            
            # 检查是否是有效图片
            if size < 5000:
                print(f"    ⚠️ 图片太小，等待 {retry_delay} 秒...")
                time.sleep(retry_delay)
                continue
            
            # 检查文件头
            valid_headers = [b'\xff\xd8\xff', b'\x89PNG', b'GIF87a', b'GIF89a']
            is_valid = any(content.startswith(h) for h in valid_headers)
            
            if is_valid:
                print(f"    ✅ 真实图片! ({size} bytes)")
                return True, content
            
            print(f"    ⚠️ 无效图片，等待 {retry_delay} 秒...")
            time.sleep(retry_delay)
            
        except Exception as e:
            print(f"    ❌ 错误: {e}")
            time.sleep(retry_delay)
    
    return False, None

def main():
    print("=" * 70)
    print("🎯 卡通插图风格图片生成")
    print("=" * 70)
    print(f"策略: 使用专门的卡通提示词，生成高质量卡通插图")
    print(f"目标: {len(CARTOON_PROMPTS)} 个人体相关词汇")
    print("=" * 70)
    
    # 加载已有链接
    links_data = {}
    if Path(LINKS_FILE).exists():
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            links_data = json.load(f)
    
    success_count = 0
    
    for i, (word, prompt) in enumerate(CARTOON_PROMPTS.items(), 1):
        print(f"\n\n{'#'*70}")
        print(f"# [{i}/{len(CARTOON_PROMPTS)}] 生成: {word}")
        print('#'*70)
        print(f"提示词: {prompt}")
        
        # 生成新链接
        url = generate_image_url(word, prompt)
        
        # 保存链接
        if word not in links_data:
            links_data[word] = []
        links_data[word].append({
            'prompt': prompt,
            'url': url,
            'timestamp': time.time(),
            'attempt': len(links_data[word]) + 1
        })
        
        # 立即尝试下载
        success, content = download_and_check(word, url)
        
        if success:
            # 保存图片
            img_path = IMAGES_DIR / f"{word}.jpg"
            
            # 备份原图
            if img_path.exists():
                backup_path = IMAGES_DIR / f"{word}_cartoon_bak.jpg"
                img_path.rename(backup_path)
            
            with open(img_path, 'wb') as f:
                f.write(content)
            
            print(f"  💾 已保存: {img_path.name}")
            success_count += 1
        
        # 保存进度
        with open(LINKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(links_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 当前进度: {success_count}/{i} 成功")
        
        # 避免请求过快
        time.sleep(5)
    
    # 最终统计
    print("\n" + "=" * 70)
    print("🎉 处理完成!")
    print("=" * 70)
    print(f"成功: {success_count}/{len(CARTOON_PROMPTS)}")
    print(f"链接已保存到: {LINKS_FILE}")
    print("=" * 70)

if __name__ == "__main__":
    main()
