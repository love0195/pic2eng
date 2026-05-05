#!/usr/bin/env python3
import os
import sys
import time
import json
import re
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# 配置路径
BASE_DIR = Path(__file__).parent.parent
AUDIO_DIR = BASE_DIR / 'public' / 'audio'
VOCAB_FILE = BASE_DIR / 'src' / 'data' / 'vocabulary.js'

AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def get_all_words():
    """从vocabulary.js获取所有单词"""
    content = VOCAB_FILE.read_text(encoding='utf-8')
    
    # 匹配单词
    pattern = r'\{\s*en:\s*[\'"]([^\'"]+)[\'"]\s*,\s*zh:\s*[\'"]([^\'"]+)[\'"]\s*\}'
    matches = re.findall(pattern, content)
    
    # 收集所有单词
    all_words = set()
    compound_words = []
    
    for en, zh in matches:
        all_words.add(en)
        if '_' in en:
            compound_words.append(en)
    
    return all_words, compound_words

def get_existing_audio():
    """获取已有的音频文件"""
    existing = set()
    if AUDIO_DIR.exists():
        for f in AUDIO_DIR.glob('*.mp3'):
            existing.add(f.stem)
    return existing

def download_audio(word):
    """下载单个音频 - 使用有道词典API"""
    word = word.strip()
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
            
            if 'audio' not in content_type and int(content_length) == 0:
                return False, '非音频内容'
            
            content = response.read()
            
            with open(audio_path, 'wb') as f:
                f.write(content)
            
            if os.path.getsize(audio_path) < 1000:
                os.remove(audio_path)
                return False, '文件太小'
            
            return True, '下载成功'
            
    except urllib.error.HTTPError as e:
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
    print("🚀 拆分复合词并下载音频...")
    print(f"📁 音频目录: {AUDIO_DIR}")
    print(f"🔊 使用服务: 有道词典TTS API\n")
    
    # 获取所有单词
    all_words, compound_words = get_all_words()
    print(f"📊 词汇统计：")
    print(f"   - 总单词数: {len(all_words)}")
    print(f"   - 复合词数: {len(compound_words)}")
    
    # 拆分复合词
    split_words = set()
    for word in compound_words:
        parts = word.split('_')
        for part in parts:
            part = part.strip()
            if part and len(part) > 1:  # 过滤空字符串和单字符
                split_words.add(part)
    
    print(f"   - 拆分后的单词数: {len(split_words)}\n")
    
    # 获取已有的音频
    existing_audio = get_existing_audio()
    print(f"🎵 已有音频文件: {len(existing_audio)} 个\n")
    
    # 找出需要下载的单词
    words_to_download = []
    for word in sorted(split_words):
        if word not in existing_audio:
            words_to_download.append(word)
    
    if not words_to_download:
        print("✅ 所有拆分后的单词音频都已存在！")
        return
    
    print(f"📋 需要下载的音频: {len(words_to_download)} 个\n")
    print(f"缺失的单词列表（前30个）：")
    for word in words_to_download[:30]:
        print(f"  - {word}.mp3")
    if len(words_to_download) > 30:
        print(f"  ... 还有 {len(words_to_download) - 30} 个\n")
    
    # 分批下载
    batch_size = 30
    total_batches = (len(words_to_download) + batch_size - 1) // batch_size
    
    print(f"\n📊 开始下载，分为 {total_batches} 个批次\n")
    
    total_success = 0
    total_failed = 0
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, len(words_to_download))
        batch_words = words_to_download[start_idx:end_idx]
        
        print(f"{'='*60}")
        print(f"📦 第 {batch_num + 1}/{total_batches} 批处理 ({len(batch_words)} 个单词)")
        print(f"{'='*60}\n")
        
        batch_success = 0
        batch_failed = 0
        
        for i, word in enumerate(batch_words):
            print(f"[{i+1}/{len(batch_words)}] {word}.mp3", end=" ... ", flush=True)
            
            success, msg = download_audio(word)
            
            if success:
                batch_success += 1
                print(f"✅ {msg}")
            else:
                batch_failed += 1
                print(f"❌ {msg}")
            
            time.sleep(0.5)
        
        total_success += batch_success
        total_failed += batch_failed
        
        print(f"\n{'='*60}")
        print(f"📊 第 {batch_num + 1} 批完成:")
        print(f"   ✅ 成功: {batch_success}/{len(batch_words)}")
        print(f"   ❌ 失败: {batch_failed}/{len(batch_words)}")
        print(f"{'='*60}\n")
        
        if batch_success > 0:
            git_commit(f"下载复合词拆分音频 - 第 {batch_num + 1}/{total_batches} 批 (成功: {total_success}/{len(words_to_download)})")
        else:
            print("⚠️  这一批没有下载成功任何资源，继续下一批\n")
    
    print("✨ 所有批次处理完成！")
    print(f"📊 总计:")
    print(f"   ✅ 成功: {total_success}")
    print(f"   ❌ 失败: {total_failed}")
    
    # 最终统计
    final_existing = get_existing_audio()
    print(f"\n🎵 最终音频文件数: {len(final_existing)} 个")

if __name__ == '__main__':
    main()
