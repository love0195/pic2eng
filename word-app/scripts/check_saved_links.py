#!/usr/bin/env python3
import urllib.request
import urllib.parse
import time
import json
import os
from pathlib import Path

# 配置
BASE_DIR = Path('/workspace/word-app')
IMAGES_DIR = BASE_DIR / 'public' / 'images'
LINKS_FILE = BASE_DIR / 'docs' / 'image_generation_links.json'
PLACEHOLDER_SIZE = 176626

def check_link(link):
    """检查链接是否返回真实图片"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(link, headers=headers)
        
        print(f"  检查链接: {link[:80]}...")
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            size = len(content)
            
        is_placeholder = (size == PLACEHOLDER_SIZE)
        return {
            'success': True,
            'size': size,
            'is_placeholder': is_placeholder,
            'content': content if not is_placeholder else None
        }
    except Exception as e:
        print(f"  ❌ 错误: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def check_and_save(word, link_data):
    """检查链接并保存图片"""
    word = link_data.get('word', word)
    link = link_data.get('link')
    attempt = link_data.get('attempt', 1)
    
    print(f"\n📝 {word} (第 {attempt} 次尝试):")
    result = check_link(link)
    
    if result['success'] and not result['is_placeholder']:
        print(f"  ✅ 找到真实图片! ({result['size']} bytes)")
        
        # 保存图片
        img_path = IMAGES_DIR / f"{word}.jpg"
        with open(img_path, 'wb') as f:
            f.write(result['content'])
        
        print(f"  💾 已保存到: {img_path}")
        return True
    elif result['success']:
        print(f"  ⏳ 仍是占位图 ({result['size']} bytes)")
    else:
        print(f"  ❌ 检查失败")
    
    return False

def main():
    print("="*70)
    print("检查保存的图片生成链接")
    print("="*70)
    
    if not LINKS_FILE.exists():
        print(f"\n❌ 链接文件不存在: {LINKS_FILE}")
        return
    
    with open(LINKS_FILE, 'r', encoding='utf-8') as f:
        links_data = json.load(f)
    
    if not links_data:
        print("\nℹ️ 链接文件为空")
        return
    
    print(f"\n发现 {len(links_data)} 个词汇的链接记录")
    print("\n是否检查所有词汇的最新链接? (y/n)")
    
    # 这里直接执行检查
    success_count = 0
    total_count = 0
    
    for word, attempts in links_data.items():
        if not attempts:
            continue
        
        # 检查最新的链接
        latest_attempt = attempts[-1]
        total_count += 1
        
        if check_and_save(word, latest_attempt):
            success_count += 1
        
        # 防止请求过快
        time.sleep(1)
    
    print("\n" + "="*70)
    print(f"检查完成: {success_count}/{total_count} 成功")
    print("="*70)

if __name__ == "__main__":
    main()
