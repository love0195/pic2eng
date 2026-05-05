#!/usr/bin/env python3
import os
import sys
import time
import json
import requests
import urllib.parse
from pathlib import Path

# 配置路径
BASE_DIR = Path(__file__).parent.parent
AUDIO_DIR = BASE_DIR / 'public' / 'audio'
MISSING_FILE = BASE_DIR / '.missing_audio.json'

AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def load_missing_list():
    """加载缺失列表"""
    if MISSING_FILE.exists():
        with open(MISSING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def download_audio(word):
    """下载单个音频"""
    audio_path = AUDIO_DIR / f'{word}.mp3'
    
    if audio_path.exists() and os.path.getsize(audio_path) > 1024:
        return True, '已存在'
    
    # Google Text-to-Speech
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={urllib.parse.quote(word)}&tl=en"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(tts_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 保存音频
        with open(audio_path, 'wb') as f:
            f.write(response.content)
        
        # 验证大小
        if os.path.getsize(audio_path) > 1024:
            return True, '下载成功'
        else:
            os.remove(audio_path)
            return False, '音频太小'
            
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 429:
            print("⚠️  触发429，等待10秒...")
            time.sleep(10)
        return False, f'HTTP错误: {e}'
    except Exception as e:
        return False, f'错误: {e}'

def git_commit(message):
    """提交到git"""
    print(f"\n📦 提交到Git: {message}")
    os.chdir(BASE_DIR)
    os.system('git add public/audio/')
    os.system(f'git commit -m "{message}"')
    os.system('git push')

def main():
    print("🚀 开始下载缺失的音频文件...")
    print(f"📁 音频目录: {AUDIO_DIR}\n")
    
    missing_words = load_missing_list()
    
    if not missing_words:
        print("❌ 没有找到缺失列表文件")
        return
    
    print(f"📋 共有 {len(missing_words)} 个缺失的音频文件\n")
    
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
            print(f"[{i+1}/{len(batch_words)}] 下载: {word}.mp3", end=" ... ", flush=True)
            
            success, msg = download_audio(word)
            
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
            git_commit(f"下载音频 - 第 {batch_num + 1}/{total_batches} 批 (成功: {total_success}/{len(missing_words)})")
        else:
            print("⚠️  这一批没有下载成功任何资源，继续下一批\n")
    
    print("✨ 所有批次处理完成！")
    print(f"📊 总计:")
    print(f"   ✅ 成功: {total_success}")
    print(f"   ❌ 失败: {total_failed}")
    print(f"   📁 总计下载: {total_success} 个音频文件")

if __name__ == '__main__':
    main()
