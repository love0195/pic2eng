#!/usr/bin/env python3
import os
import sys
import time
import json
import urllib.request
import urllib.parse
from pathlib import Path

# 配置路径
BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / 'public' / 'images'
MISSING_FILE = BASE_DIR / '.missing_images.json'

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def load_missing_list():
    """加载缺失列表"""
    if MISSING_FILE.exists():
        with open(MISSING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def download_image(word):
    """下载单个图片 - 使用Pollinations AI"""
    image_path = IMAGES_DIR / f'{word}.jpg'
    
    # 检查是否已存在
    if image_path.exists() and os.path.getsize(image_path) > 10240:
        return True, '已存在'
    
    # Pollinations AI
    prompt = urllib.parse.quote(f"{word}, realistic, high quality, simple background")
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
    """提交到git - 先构建再提交"""
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
    print(f"🖼️  使用服务: Pollinations AI")
    print(f"📋 API: https://image.pollinations.ai/\n")
    
    missing_words = load_missing_list()
    
    if not missing_words:
        print("❌ 没有找到缺失列表文件")
        return
    
    print(f"📋 共有 {len(missing_words)} 个缺失的图片文件\n")
    
    # 分成批次处理，每30个单词提交一次
    batch_size = 30
    total_batches = (len(missing_words) + batch_size - 1) // batch_size
    
    print(f"📊 总共 {len(missing_words)} 个单词，分为 {total_batches} 个批次\n")
    
    total_success = 0
    total_failed = 0
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, len(missing_words))
        batch_words = missing_words[start_idx:end_idx]
        
        print(f"{'='*60}")
        print(f"📦 第 {batch_num + 1}/{total_batches} 批处理 ({len(batch_words)} 个单词)")
        print(f"{'='*60}\n")
        
        batch_success = 0
        batch_failed = 0
        
        for i, word in enumerate(batch_words):
            word = word.strip()
            if not word:
                continue
                
            print(f"[{i+1}/{len(batch_words)}] {word}.jpg", end=" ... ", flush=True)
            
            success, msg = download_image(word)
            
            if success:
                batch_success += 1
                print(f"✅ {msg}")
            else:
                batch_failed += 1
                print(f"❌ {msg}")
            
            # 间隔2秒
            time.sleep(2)
        
        total_success += batch_success
        total_failed += batch_failed
        
        print(f"\n{'='*60}")
        print(f"📊 第 {batch_num + 1} 批完成:")
        print(f"   ✅ 成功: {batch_success}/{len(batch_words)}")
        print(f"   ❌ 失败: {batch_failed}/{len(batch_words)}")
        print(f"{'='*60}\n")
        
        # 提交这一批
        if batch_success > 0:
            git_commit(f"下载图片 - 第 {batch_num + 1}/{total_batches} 批 (成功: {total_success}/{len(missing_words)})")
        else:
            print("⚠️  这一批没有下载成功任何资源，继续下一批\n")
    
    print("✨ 所有批次处理完成！")
    print(f"📊 总计:")
    print(f"   ✅ 成功: {total_success}")
    print(f"   ❌ 失败: {total_failed}")
    print(f"   📁 总计下载: {total_success} 个图片文件")

if __name__ == '__main__':
    main()
