#!/usr/bin/env python3
import os
import json
from pathlib import Path

# 配置
BASE_DIR = Path("/workspace/word-app")
IMAGES_DIR = BASE_DIR / "public" / "images"
AUDIO_DIR = BASE_DIR / "public" / "audio"

# 列出所有现有资源
existing_images = set([f.stem for f in IMAGES_DIR.glob("*.jpg")])
existing_audio = set([f.stem for f in AUDIO_DIR.glob("*.mp3")])

# 完整资源单词
complete_words = existing_images & existing_audio

print("="*60)
print("资源检查报告")
print("="*60)
print(f"\n现有图片数: {len(existing_images)}")
print(f"现有音频数: {len(existing_audio)}")
print(f"完整资源数: {len(complete_words)}")

print(f"\n完整资源单词列表:")
for word in sorted(complete_words):
    print(f"  ✓ {word}")

print("\n" + "="*60)
print("修复建议")
print("="*60)
print("\n为了确保所有单词都有完整资源，我们可以:")
print("1. 只保留有完整资源的单词")
print("2. 或者用现有资源重新生成词汇表")
