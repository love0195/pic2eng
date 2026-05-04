#!/usr/bin/env python3
import urllib.request
import urllib.parse
import time
import json
import os
from pathlib import Path

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

def check_image_status(word):
    """检查图片当前状态"""
    img_path = IMAGES_DIR / f"{word}.jpg"
    if img_path.exists():
        size = img_path.stat().st_size
        is_placeholder = (size == PLACEHOLDER_SIZE)
        return {
            'exists': True,
            'size': size,
            'is_placeholder': is_placeholder,
            'status': 'placeholder' if is_placeholder else 'real_image'
        }
    return {
        'exists': False,
        'size': 0,
        'is_placeholder': False,
        'status': 'missing'
    }

def generate_link(word, prompt):
    """生成图片API链接"""
    encoded_prompt = urllib.parse.quote(prompt)
    session_id = f"body_{word}_{int(time.time()*1000)}"
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={session_id}"
    return url

def main():
    print("="*70)
    print("检查29张人体相关图片状态并记录链接")
    print("="*70)
    
    # 加载或初始化链接记录
    links_data = {}
    if LINKS_FILE.exists():
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            links_data = json.load(f)
    
    results = {}
    placeholder_count = 0
    real_count = 0
    missing_count = 0
    
    print("\n检查图片状态...")
    print("-"*70)
    
    for word in body_words:
        status = check_image_status(word)
        results[word] = status
        
        # 统计
        if status['status'] == 'placeholder':
            placeholder_count += 1
            status_icon = "❌"
        elif status['status'] == 'real_image':
            real_count += 1
            status_icon = "✅"
        else:
            missing_count += 1
            status_icon = "⚠️"
        
        # 如果是占位图或缺失，生成新链接
        if status['status'] != 'real_image':
            prompt = prompts.get(word, f"A simple cartoon illustration of a {word}")
            link = generate_link(word, prompt)
            results[word]['link'] = link
            results[word]['timestamp'] = time.time()
            
            # 保存到链接数据
            if word not in links_data:
                links_data[word] = []
            links_data[word].append({
                'link': link,
                'timestamp': time.time(),
                'attempt': len(links_data[word]) + 1
            })
        
        print(f"{status_icon} {word:15} - {status['status']:15} (size: {status['size']} bytes)")
    
    # 保存链接数据
    with open(LINKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(links_data, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*70)
    print("检查结果统计:")
    print(f"  真实图片: {real_count}/{len(body_words)}")
    print(f"  占位图: {placeholder_count}/{len(body_words)}")
    print(f"  缺失: {missing_count}/{len(body_words)}")
    print(f"\n链接已保存到: {LINKS_FILE}")
    print("="*70)

if __name__ == "__main__":
    main()
