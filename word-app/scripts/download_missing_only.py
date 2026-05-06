#!/usr/bin/env python3
import os
import time
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / 'public' / 'images'

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# 缺失的图片列表
MISSING_WORDS = [
    {'word': 'purple', 'zh': '紫色', 'prompt': 'purple color swatch, solid color, minimal, white background'},
    {'word': 'white', 'zh': '白色', 'prompt': 'white color swatch, solid color, minimal, white background'},
    {'word': 'beige', 'zh': '米色', 'prompt': 'beige color swatch, solid color, minimal, white background'},
    {'word': 'thin', 'zh': '薄的', 'prompt': 'thin object, paper thin, visual representation, minimal, white background'},
    {'word': 'dark', 'zh': '黑暗的', 'prompt': 'darkness, shadow, abstract representation, minimal, white background'},
    {'word': 'clean', 'zh': '干净的', 'prompt': 'clean and tidy room, sparkling clean, minimal, white background'},
    {'word': 'fold', 'zh': '折叠', 'prompt': 'hands folding paper, origami action, instructional, white background'},
    {'word': 'release', 'zh': '释放', 'prompt': 'hand releasing object, letting go, action shot, white background'},
    {'word': 'place', 'zh': '放置', 'prompt': 'hand placing object on table, action shot, white background'},
    {'word': 'remove', 'zh': '移除', 'prompt': 'hand removing object, taking away, action shot, white background'},
    {'word': 'insert', 'zh': '插入', 'prompt': 'hand inserting object into slot, action shot, white background'},
    {'word': 'press', 'zh': '按压', 'prompt': 'finger pressing button, action shot, white background'},
    {'word': 'click', 'zh': '点击', 'prompt': 'finger clicking mouse, action shot, white background'},
    {'word': 'tap', 'zh': '轻敲', 'prompt': 'finger tapping screen, action shot, white background'},
    {'word': 'knock', 'zh': '敲击', 'prompt': 'hand knocking on door, action shot, white background'},
    {'word': 'shake', 'zh': '摇晃', 'prompt': 'hand shaking object, action shot, white background'},
    {'word': 'stir', 'zh': '搅拌', 'prompt': 'hand stirring with spoon, action shot, white background'},
    {'word': 'mix', 'zh': '混合', 'prompt': 'mixing ingredients, action shot, white background'},
    {'word': 'pour', 'zh': '倾倒', 'prompt': 'pouring liquid from container, action shot, white background'},
    {'word': 'fill', 'zh': '填充', 'prompt': 'filling glass with water, action shot, white background'},
    {'word': 'clean', 'zh': '清洁', 'prompt': 'cleaning surface with cloth, action shot, white background'},
    {'word': 'wipe', 'zh': '擦拭', 'prompt': 'wiping surface with cloth, action shot, white background'},
    {'word': 'chop', 'zh': '剁碎', 'prompt': 'chopping vegetables with knife, action shot, white background'},
    {'word': 'slice', 'zh': '切片', 'prompt': 'slicing bread with knife, action shot, white background'},
    {'word': 'tear', 'zh': '撕开', 'prompt': 'hands tearing paper, action shot, white background'},
    {'word': 'repair', 'zh': '修理', 'prompt': 'repairing with tools, action shot, white background'},
    {'word': 'destroy', 'zh': '破坏', 'prompt': 'breaking object, action shot, white background'},
    {'word': 'make', 'zh': '制作', 'prompt': 'crafting and making object, creative process, white background'},
    {'word': 'create', 'zh': '创造', 'prompt': 'creative process, making art, white background'},
    {'word': 'draw', 'zh': '绘画', 'prompt': 'hand drawing with pencil, action shot, white background'},
    {'word': 'type', 'zh': '打字', 'prompt': 'hands typing on keyboard, action shot, white background'},
    {'word': 'print', 'zh': '打印', 'prompt': 'printer printing document, white background'},
    {'word': 'copy', 'zh': '复制', 'prompt': 'copying document, photocopier, white background'},
    {'word': 'paste', 'zh': '粘贴', 'prompt': 'hand pasting sticker, action shot, white background'},
    {'word': 'save', 'zh': '保存', 'prompt': 'saving document on computer, white background'},
    {'word': 'delete', 'zh': '删除', 'prompt': 'deleting file, trash can icon concept, white background'},
    {'word': 'undo', 'zh': '撤销', 'prompt': 'undo action arrow, concept icon, white background'},
    {'word': 'redo', 'zh': '重做', 'prompt': 'redo action arrow, concept icon, white background'},
]

def download_image(word_info):
    """下载单个图片"""
    word = word_info['word']
    custom_prompt = word_info.get('prompt', f"{word}, realistic, high quality, simple background")
    image_path = IMAGES_DIR / f'{word}.jpg'
    
    if image_path.exists():
        return True, '已存在'
    
    prompt = urllib.parse.quote(custom_prompt)
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=512&height=512&nologo=true"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=120) as response:
            content = response.read()
            
            with open(image_path, 'wb') as f:
                f.write(content)
            
            if os.path.getsize(image_path) > 10240:
                return True, '下载成功'
            else:
                os.remove(image_path)
                return False, '图片太小'
            
    except Exception as e:
        if image_path.exists():
            os.remove(image_path)
        return False, f'错误: {e}'

def git_commit(message):
    """提交到git"""
    print(f"\n📦 构建 dist 目录...")
    os.chdir(BASE_DIR)
    os.system('npm run build')
    
    print(f"\n📦 提交到Git: {message}")
    os.system('git add public/images/ dist/')
    os.system(f'git commit -m "{message}"')
    os.system('git push')

def main():
    print("🚀 开始下载缺失的图片...")
    print(f"📁 图片目录: {IMAGES_DIR}")
    print(f"📋 共 {len(MISSING_WORDS)} 个缺失图片\n")
    
    total_success = 0
    total_failed = 0
    
    for i, word_info in enumerate(MISSING_WORDS):
        word = word_info['word']
        zh = word_info['zh']
        
        print(f"[{i+1}/{len(MISSING_WORDS)}] {word} ({zh}).jpg", end=" ... ", flush=True)
        
        success, msg = download_image(word_info)
        
        if success:
            total_success += 1
            print(f"✅ {msg}")
        else:
            total_failed += 1
            print(f"❌ {msg}")
        
        time.sleep(3)
    
    print("\n" + "="*60)
    print("✨ 下载完成！")
    print(f"📊 总计:")
    print(f"   ✅ 成功: {total_success}")
    print(f"   ❌ 失败: {total_failed}")
    print("="*60)
    
    if total_success > 0:
        git_commit(f"下载缺失图片 ({total_success}个)")
    else:
        print("⚠️  没有成功下载任何图片，跳过提交")

if __name__ == '__main__':
    main()
