#!/usr/bin/env python3
import os
import sys
import time
import json
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / 'public' / 'images'

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# 增强提示词映射表 - 根据分类优化提示词
ENHANCED_PROMPTS = {
    '内脏器官': {
        'prefix': 'human organ, anatomical illustration, medical diagram, realistic, white background',
        'words': {}
    },
    '颜色形状': {
        'prefix': 'color swatch, solid color, minimal, white background',
        'words': {
            'purple': 'purple color, solid purple background, color sample',
            'white': 'white color sample, clean white background',
            'beige': 'beige tan color, warm neutral tone, color sample'
        }
    },
    '动作单词': {
        'prefix': 'human hand action, instructional, white background',
        'words': {
            'fold': 'hands folding paper, origami action',
            'release': 'hand releasing object, letting go',
            'press': 'finger pressing button',
            'click': 'finger clicking mouse button',
            'tap': 'finger tapping touch screen',
            'shake': 'hand shaking object',
            'stir': 'hand stirring with spoon',
            'mix': 'mixing ingredients in bowl',
            'pour': 'pouring liquid from container',
            'fill': 'filling glass with water',
            'clean': 'cleaning surface with cloth',
            'wipe': 'wiping surface with cloth',
            'chop': 'chopping vegetables with knife',
            'slice': 'slicing bread with knife',
            'tear': 'hands tearing paper',
            'draw': 'hand drawing with pencil',
            'type': 'hands typing on keyboard'
        }
    },
    '动作词组': {
        'prefix': 'human action, two hands interaction, instructional, white background',
        'words': {}
    },
    '日常用品': {
        'prefix': 'everyday object, product photography, clean white background',
        'words': {}
    },
    '食物': {
        'prefix': 'food photography, fresh ingredients, white background',
        'words': {}
    },
    '动物': {
        'prefix': 'animal portrait, wildlife photography, white background',
        'words': {}
    },
    '植物': {
        'prefix': 'plant, botanical illustration, white background',
        'words': {}
    },
    '交通工具': {
        'prefix': 'vehicle, transportation, clean white background',
        'words': {}
    },
    '衣物': {
        'prefix': 'clothing fashion, product photography, white background',
        'words': {}
    },
    '身体部位': {
        'prefix': 'human body part, anatomical, white background',
        'words': {}
    },
    '抽象概念': {
        'prefix': 'abstract concept, minimal icon, white background',
        'words': {
            'thin': 'thin object, slim, visual representation',
            'dark': 'darkness shadow, abstract representation',
            'clean': 'clean and tidy room, sparkling clean'
        }
    }
}

def get_enhanced_prompt(word, category):
    """根据分类和单词获取增强提示词"""
    # 优先使用单词特定的提示词
    if category in ENHANCED_PROMPTS:
        if word in ENHANCED_PROMPTS[category]['words']:
            return ENHANCED_PROMPTS[category]['words'][word]
        # 使用分类前缀
        return f"{word}, {ENHANCED_PROMPTS[category]['prefix']}"
    
    # 默认提示词
    return f"{word}, realistic, high quality, simple white background"

def download_image(word, prompt):
    """下载单个图片"""
    image_path = IMAGES_DIR / f'{word}.jpg'
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"
    
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

def load_marked_images():
    """从JSON文件加载标记的图片列表"""
    marked_file = BASE_DIR / 'marked_images.json'
    if marked_file.exists():
        with open(marked_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def export_marked_images():
    """导出标记的图片列表到文件"""
    print("📥 导出标记的图片列表...")
    
    # 从localStorage导出的示例数据格式
    # 用户需要手动从浏览器控制台执行: localStorage.getItem('badImages')
    # 然后保存到 marked_images.json
    
    print("提示: 从浏览器导出标记列表的方法:")
    print("1. 打开浏览器开发者工具 (F12)")
    print("2. 在控制台输入: localStorage.getItem('badImages')")
    print("3. 复制输出内容")
    print("4. 粘贴到 marked_images.json 文件中")
    print()
    
    # 检查是否有标记文件
    marked_file = BASE_DIR / 'marked_images.json'
    if marked_file.exists():
        with open(marked_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 已找到标记文件，共 {len(data)} 个标记")
        return data
    else:
        print("❌ 未找到 marked_images.json 文件")
        print("请按照上述步骤导出标记列表")
        return []

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
    print("🚀 重新生成标记的图片")
    print(f"📁 图片目录: {IMAGES_DIR}")
    print("📋 使用服务: Pollinations AI\n")
    
    # 导出标记列表
    marked_images = export_marked_images()
    
    if not marked_images:
        print("⚠️  没有需要重新生成的图片")
        return
    
    print(f"📋 共有 {len(marked_images)} 个标记的图片需要重新生成\n")
    
    total_success = 0
    total_failed = 0
    regenerated_list = []
    
    for i, item in enumerate(marked_images):
        word = item['en']
        zh = item.get('zh', '')
        category = item.get('category', '')
        
        # 获取增强提示词
        prompt = get_enhanced_prompt(word, category)
        
        print(f"[{i+1}/{len(marked_images)}] {word} ({zh})")
        print(f"   分类: {category}")
        print(f"   提示词: {prompt}")
        
        success, msg = download_image(word, prompt)
        
        if success:
            total_success += 1
            regenerated_list.append(word)
            print(f"   ✅ {msg}\n")
        else:
            total_failed += 1
            print(f"   ❌ {msg}\n")
        
        time.sleep(3)
    
    print("\n" + "="*60)
    print("✨ 重新生成完成！")
    print(f"📊 总计:")
    print(f"   ✅ 成功: {total_success}")
    print(f"   ❌ 失败: {total_failed}")
    
    if regenerated_list:
        print(f"\n🔄 重新生成的图片:")
        for word in regenerated_list:
            print(f"   - {word}.jpg")
    
    print("="*60)
    
    if total_success > 0:
        git_commit(f"重新生成标记图片 ({total_success}个)")
    else:
        print("⚠️  没有成功重新生成任何图片，跳过提交")

if __name__ == '__main__':
    main()
