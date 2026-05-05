#!/usr/bin/env python3
import os
import time
import urllib.request
import urllib.parse
from pathlib import Path

# 配置路径
BASE_DIR = Path(__file__).parent.parent
AUDIO_DIR = BASE_DIR / 'public' / 'audio'

AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def download_audio(word):
    """下载单个音频 - 使用有道词典API"""
    audio_path = AUDIO_DIR / f'{word}.mp3'
    
    if audio_path.exists() and os.path.getsize(audio_path) > 1000:
        return True, '已存在'
    
    # 有道词典TTS API
    url = f"http://dict.youdao.com/dictvoice?audio={urllib.parse.quote(word)}&type=2"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            
            # 保存音频
            with open(audio_path, 'wb') as f:
                f.write(content)
            
            # 验证大小
            if os.path.getsize(audio_path) < 1000:
                os.remove(audio_path)
                return False, '文件太小'
            
            return True, '下载成功'
            
    except Exception as e:
        return False, f'错误: {e}'

words = ["clothespin"]

print("🔊 尝试下载 clothespin 的单数形式...")
print(f"目标: {words}\n")

for word in words:
    print(f"{word}.mp3 ... ", end="", flush=True)
    success, msg = download_audio(word)
    if success:
        print(f"✅ {msg}")
        # 如果单数成功，复制一份给复数
        src = AUDIO_DIR / f'{word}.mp3'
        dst = AUDIO_DIR / 'clothespins.mp3'
        import shutil
        shutil.copy(src, dst)
        print(f"   ✅ 已复制为 clothespins.mp3")
    else:
        print(f"❌ {msg}")
    time.sleep(0.5)

print("\n✅ 完成！")
