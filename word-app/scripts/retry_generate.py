#!/usr/bin/env python3
import urllib.request
import urllib.parse
import time
import json
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# 人体相关词汇列表
body_words = [
    # 面部五官
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    # 身体部位
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    # 内脏器官
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

# 图片描述提示词
prompts = {
    'face': "A simple cartoon illustration of a human face on white background, clean design, educational style",
    'forehead': "A simple cartoon illustration of a human forehead on white background, clean design, educational style",
    'eye': "A simple cartoon illustration of a human eye on white background, clean design, educational style",
    'eyebrow': "A simple cartoon illustration of a human eyebrow on white background, clean design, educational style",
    'ear': "A simple cartoon illustration of a human ear on white background, clean design, educational style",
    'nose': "A simple cartoon illustration of a human nose on white background, clean design, educational style",
    'cheek': "A simple cartoon illustration of a human cheek on white background, clean design, educational style",
    'mouth': "A simple cartoon illustration of a human mouth on white background, clean design, educational style",
    'lip': "A simple cartoon illustration of human lips on white background, clean design, educational style",
    'chin': "A simple cartoon illustration of a human chin on white background, clean design, educational style",
    'head': "A simple cartoon illustration of a human head on white background, clean design, educational style",
    'neck': "A simple cartoon illustration of a human neck on white background, clean design, educational style",
    'shoulder': "A simple cartoon illustration of a human shoulder on white background, clean design, educational style",
    'arm': "A simple cartoon illustration of a human arm on white background, clean design, educational style",
    'elbow': "A simple cartoon illustration of a human elbow on white background, clean design, educational style",
    'hand': "A simple cartoon illustration of a human hand on white background, clean design, educational style",
    'finger': "A simple cartoon illustration of a human finger on white background, clean design, educational style",
    'leg': "A simple cartoon illustration of a human leg on white background, clean design, educational style",
    'knee': "A simple cartoon illustration of a human knee on white background, clean design, educational style",
    'foot': "A simple cartoon illustration of a human foot on white background, clean design, educational style",
    'skin': "A simple cartoon illustration of human skin on white background, clean design, educational style",
    'brain': "A simple cartoon illustration of a human brain on white background, clean design, educational style, anatomy diagram",
    'heart': "A simple cartoon illustration of a human heart on white background, clean design, educational style, anatomy diagram",
    'lung': "A simple cartoon illustration of human lungs on white background, clean design, educational style, anatomy diagram",
    'liver': "A simple cartoon illustration of a human liver on white background, clean design, educational style, anatomy diagram",
    'stomach': "A simple cartoon illustration of a human stomach on white background, clean design, educational style, anatomy diagram",
    'intestine': "A simple cartoon illustration of human intestines on white background, clean design, educational style, anatomy diagram",
    'kidney': "A simple cartoon illustration of a human kidney on white background, clean design, educational style, anatomy diagram",
    'muscle': "A simple cartoon illustration of a human muscle on white background, clean design, educational style, anatomy diagram"
}

# 配置
BASE_DIR = Path('/workspace/word-app')
IMAGES_DIR = BASE_DIR / 'public' / 'images'
LINKS_FILE = BASE_DIR / 'docs' / 'image_generation_links.json'
PLACEHOLDER_SIZE = 176626
MIN_REAL_SIZE = 50000

def load_links():
    """加载已保存的链接"""
    if LINKS_FILE.exists():
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_links(links_data):
    """保存链接数据"""
    with open(LINKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(links_data, f, indent=2, ensure_ascii=False)

def generate_link(word, prompt):
    """生成图片API链接"""
    encoded_prompt = urllib.parse.quote(prompt)
    session_id = f"body_{word}_{int(time.time()*1000)}"
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={session_id}"
    return url

def download_image(task):
    """下载图片"""
    word = task['word']
    url = task['link']
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=60) as response:
            content = response.read()
            size = len(content)
        
        if size != PLACEHOLDER_SIZE and size >= MIN_REAL_SIZE:
            img_path = IMAGES_DIR / f"{word}.jpg"
            with open(img_path, 'wb') as f:
                f.write(content)
            return {
                'word': word,
                'success': True,
                'size': size,
                'link': url
            }
        else:
            return {
                'word': word,
                'success': False,
                'size': size,
                'link': url,
                'is_placeholder': size == PLACEHOLDER_SIZE
            }
    except Exception as e:
        return {
            'word': word,
            'success': False,
            'error': str(e),
            'link': url
        }

def main():
    print("="*70)
    print("重新尝试生成人体相关图片")
    print("="*70)
    
    # 加载已有链接
    links_data = load_links()
    
    # 第一步：触发所有生成请求
    print("\n📋 第一步：触发所有图片生成请求...")
    tasks = []
    for word in body_words:
        prompt = prompts.get(word, f"A simple cartoon illustration of a {word}")
        link = generate_link(word, prompt)
        
        if word not in links_data:
            links_data[word] = []
        
        links_data[word].append({
            'link': link,
            'timestamp': time.time(),
            'attempt': len(links_data[word]) + 1
        })
        
        tasks.append({
            'word': word,
            'link': link,
            'prompt': prompt
        })
        
        print(f"  ✅ {word}: 生成请求已触发")
        time.sleep(0.2)
    
    # 保存链接
    save_links(links_data)
    print(f"\n💾 链接已保存到: {LINKS_FILE}")
    
    # 等待一段时间让AI生成
    wait_time = 120
    print(f"\n⏳ 等待 {wait_time} 秒让AI生成图片...")
    for i in range(wait_time, 0, -10):
        print(f"  剩余 {i} 秒...")
        time.sleep(10)
    
    # 第二步：尝试下载图片
    print("\n📥 第二步：尝试下载生成的图片...")
    print("-"*70)
    
    success_count = 0
    placeholder_count = 0
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_image, task) for task in tasks]
        
        for future in as_completed(futures):
            result = future.result()
            word = result['word']
            
            if result.get('success'):
                success_count += 1
                print(f"  ✅ {word:15} - 下载成功! ({result['size']} bytes)")
            else:
                is_placeholder = result.get('is_placeholder', False)
                if is_placeholder:
                    placeholder_count += 1
                    print(f"  ⏳ {word:15} - 占位图 ({result['size']} bytes)")
                else:
                    print(f"  ❌ {word:15} - 失败 - {result.get('error', 'unknown')}")
    
    print("\n" + "="*70)
    print(f"最终结果: {success_count}/{len(body_words)} 成功")
    print(f"占位图: {placeholder_count}/{len(body_words)}")
    print(f"链接已保存，下次可以继续尝试")
    print("="*70)

if __name__ == "__main__":
    main()
