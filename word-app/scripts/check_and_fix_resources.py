#!/usr/bin/env python3
import os
import requests
import time
import json
from pathlib import Path

# 配置
BASE_DIR = Path("/workspace/word-app")
IMAGES_DIR = BASE_DIR / "public" / "images"
AUDIO_DIR = BASE_DIR / "public" / "audio"
VOCAB_FILE = BASE_DIR / "src" / "data" / "vocabulary.js"

# 有道词典API URL (用于获取音频)
YOUDAO_AUDIO_URL = "http://dict.youdao.com/dictvoice?audio={word}&type=2"

# AI图片生成API (使用您之前提到的API)
IMAGE_API_URL = "https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={prompt}"

# 备用图片API (简单的占位图)
BACKUP_IMAGE_URL = "https://via.placeholder.com/400x400/ff6b35/ffffff?text={word}"

def load_vocabulary():
    """加载词汇表"""
    with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单解析 (由于是ES6模块，我们手动提取数据)
    words = []
    lines = content.split('\n')
    in_words = False
    for line in lines:
        line = line.strip()
        if 'words: [' in line:
            in_words = True
            continue
        if in_words and ']' in line:
            in_words = False
            continue
        if in_words and 'en:' in line:
            # 提取英文单词
            parts = line.split('en:')
            if len(parts) > 1:
                word = parts[1].split(',')[0].strip('\'"')
                words.append(word)
    return list(set(words))

def check_resources(words):
    """检查资源"""
    missing_images = []
    missing_audio = []
    complete_words = []
    
    for word in words:
        has_image = (IMAGES_DIR / f"{word}.jpg").exists()
        has_audio = (AUDIO_DIR / f"{word}.mp3").exists()
        
        if has_image and has_audio:
            complete_words.append(word)
        if not has_image:
            missing_images.append(word)
        if not has_audio:
            missing_audio.append(word)
    
    return missing_images, missing_audio, complete_words

def download_audio(word):
    """下载音频"""
    audio_path = AUDIO_DIR / f"{word}.mp3"
    
    if audio_path.exists():
        print(f"  ✓ 音频已存在: {word}")
        return True
    
    print(f"  → 下载音频: {word}")
    try:
        # 尝试有道词典API
        response = requests.get(YOUDAO_AUDIO_URL.format(word=word), timeout=10)
        if response.status_code == 200 and len(response.content) > 100:
            with open(audio_path, 'wb') as f:
                f.write(response.content)
            print(f"  ✓ 音频下载成功: {word}")
            return True
    except Exception as e:
        print(f"  ✗ 音频下载失败: {word}, 错误: {e}")
    return False

def download_image(word, zh_word=None):
    """下载图片"""
    image_path = IMAGES_DIR / f"{word}.jpg"
    
    if image_path.exists():
        print(f"  ✓ 图片已存在: {word}")
        return True
    
    print(f"  → 下载图片: {word}")
    
    # 尝试使用简单的占位图API
    try:
        response = requests.get(BACKUP_IMAGE_URL.format(word=word.replace('_', '+')), timeout=15)
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"  ✓ 图片下载成功 (占位图): {word}")
            return True
    except Exception as e:
        print(f"  ✗ 图片下载失败: {word}, 错误: {e}")
    
    return False

def main():
    print("="*60)
    print("词汇资源检查与修复脚本")
    print("="*60)
    
    # 1. 加载词汇
    print("\n[步骤 1/4] 加载词汇表...")
    words = load_vocabulary()
    print(f"  ✓ 加载了 {len(words)} 个词汇")
    
    # 2. 检查现有资源
    print("\n[步骤 2/4] 检查资源状态...")
    missing_images, missing_audio, complete_words = check_resources(words)
    
    print(f"\n  完整资源: {len(complete_words)} 个")
    print(f"  缺失图片: {len(missing_images)} 个")
    print(f"  缺失音频: {len(missing_audio)} 个")
    
    if missing_images:
        print(f"  缺失图片列表: {missing_images[:10]}")
    if missing_audio:
        print(f"  缺失音频列表: {missing_audio[:10]}")
    
    # 3. 修复缺失音频
    if missing_audio:
        print(f"\n[步骤 3/4] 修复音频资源 ({len(missing_audio)}个)...")
        for word in missing_audio:
            download_audio(word)
            time.sleep(0.5)  # 避免请求过快
    
    # 4. 修复缺失图片
    if missing_images:
        print(f"\n[步骤 4/4] 修复图片资源 ({len(missing_images)}个)...")
        for word in missing_images:
            download_image(word)
            time.sleep(0.5)
    
    # 5. 最终检查
    print("\n" + "="*60)
    print("最终检查")
    print("="*60)
    missing_images, missing_audio, complete_words = check_resources(words)
    
    print(f"\n  完整资源: {len(complete_words)} 个")
    print(f"  仍缺失图片: {len(missing_images)} 个")
    print(f"  仍缺失音频: {len(missing_audio)} 个")
    
    if missing_images:
        print(f"  仍缺失图片: {missing_images}")
    if missing_audio:
        print(f"  仍缺失音频: {missing_audio}")
    
    print("\n" + "="*60)
    print("完成！")
    print("="*60)

if __name__ == "__main__":
    main()
