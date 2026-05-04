#!/usr/bin/env python3
"""
使用 Pollinations AI 生成卡通插图风格的图片
API: https://image.pollinations.ai/
"""
import urllib.request
import urllib.parse
import time
import json
from pathlib import Path

# 配置
BASE_DIR = Path('/workspace/word-app')
IMAGES_DIR = BASE_DIR / 'public' / 'images'
LINKS_FILE = BASE_DIR / 'docs' / 'pollinations_results.json'

# 人体相关词汇 - Pollinations AI 提示词
POLLINATIONS_PROMPTS = {
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
    'brain': 'cute cartoon human brain, simple flat design, white background, kawaii style, clean lines, anatomy diagram',
    'heart': 'cute cartoon human heart, simple flat design, white background, kawaii style, clean lines, anatomy diagram',
    'lung': 'cute cartoon human lungs, simple flat design, white background, kawaii style, clean lines, anatomy diagram',
    'liver': 'cute cartoon human liver, simple flat design, white background, kawaii style, clean lines, anatomy diagram',
    'stomach': 'cute cartoon human stomach, simple flat design, white background, kawaii style, clean lines, anatomy diagram',
    'intestine': 'cute cartoon human intestine, simple flat design, white background, kawaii style, clean lines, anatomy diagram',
    'kidney': 'cute cartoon human kidney, simple flat design, white background, kawaii style, clean lines, anatomy diagram',
    'muscle': 'cute cartoon human muscle, simple flat design, white background, kawaii style, clean lines, anatomy diagram'
}

def generate_image_url(word, prompt):
    """生成 Pollinations AI 图片 URL"""
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"
    return url

def download_image(url, timeout=120):
    """下载图片"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()
            return content
    except Exception as e:
        print(f"    ❌ 下载失败: {e}")
        return None

def is_valid_image(content):
    """验证是否是有效图片"""
    if not content or len(content) < 10000:
        return False
    valid_headers = [b'\xff\xd8\xff', b'\x89PNG', b'GIF87a', b'GIF89a']
    return any(content[:len(h)] == h for h in valid_headers if len(h) <= len(content))

def main():
    print("=" * 70)
    print("🎯 使用 Pollinations AI 生成卡通插图")
    print("=" * 70)
    print(f"API: https://image.pollinations.ai/")
    print(f"目标: {len(POLLINATIONS_PROMPTS)} 个人体相关词汇")
    print("=" * 70)
    
    links_data = {}
    if Path(LINKS_FILE).exists():
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            links_data = json.load(f)
    
    success_count = 0
    for i, (word, prompt) in enumerate(POLLINATIONS_PROMPTS.items(), 1):
        print(f"\n\n{'#'*70}")
        print(f"# [{i}/{len(POLLINATIONS_PROMPTS)}] 生成: {word}")
        print('#'*70)
        
        url = generate_image_url(word, prompt)
        print(f"  🔗 URL: {url[:80]}...")
        
        if word not in links_data:
            links_data[word] = []
        links_data[word].append({
            'prompt': prompt,
            'url': url,
            'timestamp': time.time(),
            'attempt': len(links_data[word]) + 1
        })
        
        print(f"  📥 下载中...")
        content = download_image(url)
        
        if content and is_valid_image(content):
            img_path = IMAGES_DIR / f"{word}.jpg"
            if img_path.exists():
                backup_path = IMAGES_DIR / f"{word}_pollinations_bak.jpg"
                img_path.rename(backup_path)
            with open(img_path, 'wb') as f:
                f.write(content)
            print(f"  ✅ 已保存: {img_path.name} ({len(content)} bytes)")
            success_count += 1
        else:
            print(f"  ❌ 下载失败或图片无效")
        
        with open(LINKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(links_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 当前进度: {success_count}/{i} 成功")
        
        time.sleep(3)
    
    print("\n" + "=" * 70)
    print("🎉 处理完成!")
    print("=" * 70)
    print(f"成功: {success_count}/{len(POLLINATIONS_PROMPTS)}")
    print(f"链接已保存到: {LINKS_FILE}")
    print("=" * 70)

if __name__ == "__main__":
    main()
