#!/usr/bin/env python3
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / 'public' / 'images'
VUE_DATA = BASE_DIR / 'src' / 'data' / 'vocabulary.js'

# 加载现有图片
existing_images = set()
if IMAGES_DIR.exists():
    for f in IMAGES_DIR.glob('*.jpg'):
        existing_images.add(f.stem)

# 从 vocabulary.js 中提取所有单词（简单的字符串解析）
missing_words = []

with open(VUE_DATA, 'r', encoding='utf-8') as f:
    content = f.read()

# 简单的解析方法：查找 "en": "xxx" 格式
import re
matches = re.findall(r'"en":\s*"([^"]+)"', content)

for word in matches:
    if word not in existing_images:
        missing_words.append(word)

# 保存缺失列表
with open(BASE_DIR / '.missing_images.json', 'w', encoding='utf-8') as f:
    json.dump(missing_words, f, indent=2, ensure_ascii=False)

print(f"✅ 总单词数: {len(matches)}")
print(f"✅ 已下载: {len(matches) - len(missing_words)}")
print(f"❌ 缺失: {len(missing_words)}")
print(f"📝 已保存到 .missing_images.json")
