#!/usr/bin/env python3
"""
为身体部位生成SVG替代图片
包含中英文文字的简洁SVG设计
"""

import json
import os

IMAGES_DIR = "public/images"

# 身体部位的SVG定义
BODY_PART_SVGS = {
    "hand": {
        "emoji": "👋",
        "zh": "手",
        "en": "Hand",
        "color": "#FFB6C1"
    },
    "elbow": {
        "emoji": "💪",
        "zh": "肘",
        "en": "Elbow",
        "color": "#FFA07A"
    },
    "arm": {
        "emoji": "💪",
        "zh": "手臂",
        "en": "Arm",
        "color": "#FFA07A"
    },
    "finger": {
        "emoji": "🖐️",
        "zh": "手指",
        "en": "Finger",
        "color": "#FFB6C1"
    },
    "knee": {
        "emoji": "🦵",
        "zh": "膝盖",
        "en": "Knee",
        "color": "#FFA07A"
    },
    "foot": {
        "emoji": "🦶",
        "zh": "脚",
        "en": "Foot",
        "color": "#FFA07A"
    },
    "skin": {
        "emoji": "🫧",
        "zh": "皮肤",
        "en": "Skin",
        "color": "#FFE4C4"
    },
    "waist": {
        "emoji": "👖",
        "zh": "腰部",
        "en": "Waist",
        "color": "#87CEEB"
    },
    "hip": {
        "emoji": "🩳",
        "zh": "臀部",
        "en": "Hip",
        "color": "#87CEEB"
    },
    "calf": {
        "emoji": "🦵",
        "zh": "小腿",
        "en": "Calf",
        "color": "#FFA07A"
    },
    "ankle": {
        "emoji": "🦶",
        "zh": "脚踝",
        "en": "Ankle",
        "color": "#FFA07A"
    },
    "wrist": {
        "emoji": "⌚",
        "zh": "手腕",
        "en": "Wrist",
        "color": "#FFB6C1"
    },
    "knuckle": {
        "emoji": "✊",
        "zh": "指节",
        "en": "Knuckle",
        "color": "#FFB6C1"
    },
    "palm": {
        "emoji": "✋",
        "zh": "手掌",
        "en": "Palm",
        "color": "#FFB6C1"
    },
    "thumb": {
        "emoji": "👍",
        "zh": "拇指",
        "en": "Thumb",
        "color": "#FFB6C1"
    },
    "index_finger": {
        "emoji": "👈",
        "zh": "食指",
        "en": "Index Finger",
        "color": "#FFB6C1"
    },
    "middle_finger": {
        "emoji": "☝️",
        "zh": "中指",
        "en": "Middle Finger",
        "color": "#FFB6C1"
    },
    "ring_finger": {
        "emoji": "💍",
        "zh": "无名指",
        "en": "Ring Finger",
        "color": "#FFB6C1"
    },
    "toe": {
        "emoji": "🦶",
        "zh": "脚趾",
        "en": "Toe",
        "color": "#FFA07A"
    },
    "little_finger": {
        "emoji": "👎",
        "zh": "小指",
        "en": "Little Finger",
        "color": "#FFB6C1"
    },
    "heel": {
        "emoji": "🦶",
        "zh": "脚后跟",
        "en": "Heel",
        "color": "#FFA07A"
    },
    "arch": {
        "emoji": "🦶",
        "zh": "脚弓",
        "en": "Arch",
        "color": "#FFA07A"
    }
}

def create_svg(word_en, info):
    """创建SVG图片"""
    emoji = info["emoji"]
    zh = info["zh"]
    en = info["en"]
    color = info["color"]
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <!-- 背景 -->
  <rect width="200" height="200" fill="#FFFFFF" rx="20" ry="20"/>
  
  <!-- 装饰圆形 -->
  <circle cx="100" cy="100" r="80" fill="{color}" opacity="0.3"/>
  
  <!-- Emoji -->
  <text x="100" y="85" font-size="64" text-anchor="middle" dominant-baseline="middle">{emoji}</text>
  
  <!-- 中文 -->
  <text x="100" y="130" font-size="28" font-weight="bold" fill="#333333" text-anchor="middle" font-family="Arial, sans-serif">{zh}</text>
  
  <!-- 英文 -->
  <text x="100" y="160" font-size="16" fill="#666666" text-anchor="middle" font-family="Arial, sans-serif">{en}</text>
</svg>'''
    
    return svg

def main():
    print("=" * 50)
    print("  🎨 生成身体部位SVG图片")
    print("=" * 50)
    print()
    
    # 读取标记的图片
    if not os.path.exists("marked_images.json"):
        print("❌ 没有找到标记文件")
        return
    
    with open("marked_images.json", "r", encoding="utf-8") as f:
        marked_images = json.load(f)
    
    if not marked_images:
        print("✅ 没有需要处理的图片")
        return
    
    print(f"📋 共有 {len(marked_images)} 个图片需要生成SVG")
    print()
    
    success_count = 0
    
    for item in marked_images:
        word_en = item["en"]
        
        if word_en in BODY_PART_SVGS:
            info = BODY_PART_SVGS[word_en]
            svg_content = create_svg(word_en, info)
            
            # 保存SVG
            svg_path = os.path.join(IMAGES_DIR, f"{word_en}.svg")
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
            
            # 同时保存为PNG占位（删除旧的jpg）
            jpg_path = os.path.join(IMAGES_DIR, f"{word_en}.jpg")
            if os.path.exists(jpg_path):
                os.remove(jpg_path)
            
            # 复制到dist目录
            dist_svg_path = os.path.join("dist/images", f"{word_en}.svg")
            dist_jpg_path = os.path.join("dist/images", f"{word_en}.jpg")
            
            with open(dist_svg_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
            
            if os.path.exists(dist_jpg_path):
                os.remove(dist_jpg_path)
            
            print(f"✅ 已生成: {word_en} ({info['zh']}) - {info['emoji']}")
            success_count += 1
        else:
            print(f"⚠️  未找到定义: {word_en}")
    
    print()
    print("=" * 50)
    print(f"  ✅ 成功: {success_count} 个SVG图片")
    print("=" * 50)

if __name__ == "__main__":
    main()
