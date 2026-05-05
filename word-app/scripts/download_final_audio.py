#!/usr/bin/env python3
import os
import sys
import time
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# 配置路径
BASE_DIR = Path(__file__).parent.parent
AUDIO_DIR = BASE_DIR / 'public' / 'audio'

AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def download_audio(word):
    """下载单个音频 - 使用有道词典API"""
    word = word.strip()  # 清理空格
    if not word:
        return False, '空单词'
    
    audio_path = AUDIO_DIR / f'{word}.mp3'
    
    # 检查是否已存在
    if audio_path.exists() and os.path.getsize(audio_path) > 1000:
        return True, '已存在'
    
    # 有道词典TTS API
    url = f"http://dict.youdao.com/dictvoice?audio={urllib.parse.quote(word)}&type=2"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            content_type = response.headers.get('Content-Type', '')
            content_length = response.headers.get('Content-Length', '0')
            
            # 验证响应是音频
            if 'audio' not in content_type and int(content_length) == 0:
                return False, '非音频内容'
            
            content = response.read()
            
            # 保存音频
            with open(audio_path, 'wb') as f:
                f.write(content)
            
            # 验证大小
            if os.path.getsize(audio_path) < 1000:
                os.remove(audio_path)
                return False, '文件太小'
            
            return True, '下载成功'
            
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print("⚠️  触发429，等待10秒...")
            time.sleep(10)
        return False, f'HTTP错误: {e.code}'
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
    print("🚀 继续下载缺失的音频文件...")
    print(f"📁 音频目录: {AUDIO_DIR}")
    print(f"🔊 使用服务: 有道词典TTS API\n")
    
    # 加载缺失列表
    missing_file = BASE_DIR / '.remaining_missing_audio.json'
    if missing_file.exists():
        with open(missing_file, 'r', encoding='utf-8') as f:
            missing_words = json.load(f)
    else:
        print("❌ 没有找到缺失列表文件")
        return
    
    print(f"📋 缺失列表: {len(missing_words)} 个单词\n")
    
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
                
            print(f"[{i+1}/{len(batch_words)}] {word}.mp3", end=" ... ", flush=True)
            
            success, msg = download_audio(word)
            
            if success:
                batch_success += 1
                print(f"✅ {msg}")
            else:
                batch_failed += 1
                print(f"❌ {msg}")
            
            # 间隔0.5秒
            time.sleep(0.5)
        
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
