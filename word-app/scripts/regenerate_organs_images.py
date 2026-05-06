#!/usr/bin/env python3
import os
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path

# 配置路径
BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / 'public' / 'images'

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# 内脏器官词汇及其增强提示词
ORGANS_WORDS = [
    {'en': 'brain', 'zh': '大脑', 'prompt': 'human brain organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'heart', 'zh': '心脏', 'prompt': 'human heart organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'lung', 'zh': '肺', 'prompt': 'human lungs organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'liver', 'zh': '肝脏', 'prompt': 'human liver organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'stomach', 'zh': '胃', 'prompt': 'human stomach organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'intestine', 'zh': '肠', 'prompt': 'human intestines organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'kidney', 'zh': '肾脏', 'prompt': 'human kidneys organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'muscle', 'zh': '肌肉', 'prompt': 'human muscle tissue, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'bone', 'zh': '骨头', 'prompt': 'human bone, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'blood', 'zh': '血液', 'prompt': 'human blood cells, medical illustration, realistic, scientific, white background'},
    {'en': 'vein', 'zh': '静脉', 'prompt': 'human vein blood vessel, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'artery', 'zh': '动脉', 'prompt': 'human artery blood vessel, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'nerve', 'zh': '神经', 'prompt': 'human nerve cells, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'spine', 'zh': '脊柱', 'prompt': 'human spine vertebrae, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'rib', 'zh': '肋骨', 'prompt': 'human rib bone, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'skull', 'zh': '颅骨', 'prompt': 'human skull bone, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'pancreas', 'zh': '胰腺', 'prompt': 'human pancreas organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'gallbladder', 'zh': '胆囊', 'prompt': 'human gallbladder organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'spleen', 'zh': '脾脏', 'prompt': 'human spleen organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'bladder', 'zh': '膀胱', 'prompt': 'human bladder organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'thyroid', 'zh': '甲状腺', 'prompt': 'human thyroid gland, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'tonsil', 'zh': '扁桃体', 'prompt': 'human tonsils, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'appendix', 'zh': '阑尾', 'prompt': 'human appendix organ, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'diaphragm', 'zh': '横膈膜', 'prompt': 'human diaphragm muscle, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'esophagus', 'zh': '食道', 'prompt': 'human esophagus, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'trachea', 'zh': '气管', 'prompt': 'human trachea windpipe, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'bronchus', 'zh': '支气管', 'prompt': 'human bronchus, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'windpipe', 'zh': '气管', 'prompt': 'human windpipe trachea, anatomical illustration, medical diagram, realistic, white background'},
    {'en': 'gullet', 'zh': '食管', 'prompt': 'human gullet esophagus, anatomical illustration, medical diagram, realistic, white background'},
]

def download_image(word_info):
    """下载单个图片 - 使用Pollinations AI，带增强提示词"""
    word = word_info['en']
    custom_prompt = word_info['prompt']
    image_path = IMAGES_DIR / f'{word}.jpg'
    
    # Pollinations AI - 使用增强提示词
    prompt = urllib.parse.quote(custom_prompt)
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=512&height=512&nologo=true"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=120) as response:
            content = response.read()
            
            # 保存图片
            with open(image_path, 'wb') as f:
                f.write(content)
            
            # 验证大小
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
    print("🚀 开始重新生成内脏器官分类的图片...")
    print(f"📁 图片目录: {IMAGES_DIR}")
    print(f"🖼️  使用服务: Pollinations AI")
    print(f"📋 API: https://image.pollinations.ai/\n")
    
    print(f"📋 共有 {len(ORGANS_WORDS)} 个内脏器官单词\n")
    
    total_success = 0
    total_failed = 0
    
    for i, word_info in enumerate(ORGANS_WORDS):
        word = word_info['en']
        zh = word_info['zh']
        
        print(f"[{i+1}/{len(ORGANS_WORDS)}] {word} ({zh}).jpg", end=" ... ", flush=True)
        
        success, msg = download_image(word_info)
        
        if success:
            total_success += 1
            print(f"✅ {msg}")
        else:
            total_failed += 1
            print(f"❌ {msg}")
        
        # 间隔3秒，避免请求过快
        time.sleep(3)
    
    print("\n" + "="*60)
    print("✨ 所有内脏器官图片重新生成完成！")
    print(f"📊 总计:")
    print(f"   ✅ 成功: {total_success}")
    print(f"   ❌ 失败: {total_failed}")
    print("="*60)
    
    # 提交到git
    if total_success > 0:
        git_commit(f"重新生成内脏器官图片 ({total_success}个)")
    else:
        print("⚠️  没有成功下载任何图片，跳过提交")

if __name__ == '__main__':
    main()
