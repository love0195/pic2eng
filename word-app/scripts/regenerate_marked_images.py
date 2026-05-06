#!/usr/bin/env python3
"""
重新生成标记的图片
根据分类优化提示词，生成更准确的图片
"""

import json
import os
import time
import requests
import urllib.parse

MARKED_FILE = "marked_images.json"
IMAGES_DIR = "public/images"
VOCABULARY_FILE = "src/data/vocabulary.js"

def get_prompt_for_word(word_en, word_zh, category):
    """根据单词和分类生成优化的提示词"""
    
    word_clean = word_en.replace("_", " ")
    
    # 身体部位 - 使用卡通/简笔画风格
    if category == "身体部位" or category == "body_parts":
        # 特殊处理手指/脚趾
        if word_en == "finger":
            return "simple cartoon illustration of human hand with 5 fingers, palm up, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "toe":
            return "simple cartoon illustration of human foot with 5 toes, top view, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "hand":
            return "simple cartoon illustration of human hand, palm up, 5 fingers, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "foot":
            return "simple cartoon illustration of human foot, top view, 5 toes, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "elbow":
            return "simple cartoon illustration of human elbow, arm bent, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "knee":
            return "simple cartoon illustration of human knee, leg slightly bent, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "skin":
            return "simple cartoon illustration of human skin texture, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "thumb":
            return "simple cartoon illustration of human thumb, part of hand, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "index_finger":
            return "simple cartoon illustration of human index finger pointing, part of hand, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "middle_finger":
            return "simple cartoon illustration of human middle finger, part of hand, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "ring_finger":
            return "simple cartoon illustration of human ring finger, part of hand, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "little_finger":
            return "simple cartoon illustration of human little finger (pinky), part of hand, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "palm":
            return "simple cartoon illustration of human palm, hand open, 5 fingers, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "wrist":
            return "simple cartoon illustration of human wrist, part of forearm and hand, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "ankle":
            return "simple cartoon illustration of human ankle, part of leg and foot, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "heel":
            return "simple cartoon illustration of human heel, bottom view of foot, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "arch":
            return "simple cartoon illustration of human foot arch, side view of foot, clean lines, flat design, white background, cute cartoon style"
        elif word_en == "knuckle":
            return "simple cartoon illustration of human knuckles, closed fist, clean lines, flat design, white background, cute cartoon style"
        else:
            return f"simple cartoon illustration of human {word_clean}, clean lines, flat design, white background, cute cartoon style"
    
    # 内脏器官 - 使用医学解剖风格
    if category == "内脏器官" or category == "internal_organs":
        return f"human {word_clean} organ, anatomical illustration, medical diagram, realistic, white background, educational"
    
    # 动作单词 - 使用动作演示风格
    if category == "动作单词" or category == "action_words":
        return f"person {word_clean} action, demonstration, instructional, clear motion, white background"
    
    # 动作词组 - 使用动作演示风格
    if category == "动作词组" or category == "action_phrases":
        action = word_clean.replace("_", " ")
        return f"hands {action}, action demonstration, instructional, step by step, white background"
    
    # 颜色 - 使用纯色背景
    if category == "颜色" or category == "colors":
        return f"{word_clean} color, solid {word_clean} background, color sample, pure color"
    
    # 形状 - 使用几何形状
    if category == "形状" or category == "shapes":
        return f"{word_clean} shape, geometric figure, clean lines, white background, educational"
    
    # 动物 - 使用真实动物照片
    if category == "动物" or category == "animals":
        return f"{word_clean}, real animal, nature photography, white background, clear view"
    
    # 水果 - 使用真实水果照片
    if category == "水果" or category == "fruits":
        return f"{word_clean}, fresh fruit, real photography, white background, appetizing"
    
    # 蔬菜 - 使用真实蔬菜照片
    if category == "蔬菜" or category == "vegetables":
        return f"{word_clean}, fresh vegetable, real photography, white background, healthy"
    
    # 默认提示词
    return f"{word_clean}, {word_zh}, clear illustration, white background, educational"


def download_image(word_en, prompt, max_retries=3):
    """从 Pollinations API 下载图片"""
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                content = response.content
                if len(content) > 10240:  # 大于10KB
                    return content
                else:
                    print(f"  ⚠️  图片太小 ({len(content)} bytes)，重试...")
            else:
                print(f"  ⚠️  HTTP {response.status_code}，重试...")
        except Exception as e:
            print(f"  ⚠️  错误: {e}，重试...")
        
        time.sleep(2)
    
    return None


def main():
    print("=" * 50)
    print("  🔄 重新生成标记的图片")
    print("=" * 50)
    print()
    
    # 读取标记的图片
    if not os.path.exists(MARKED_FILE):
        print("❌ 没有找到标记文件")
        return
    
    with open(MARKED_FILE, "r", encoding="utf-8") as f:
        marked_images = json.load(f)
    
    if not marked_images:
        print("✅ 没有需要重新生成的图片")
        return
    
    print(f"📋 共有 {len(marked_images)} 个图片需要重新生成")
    print()
    
    success_count = 0
    fail_count = 0
    
    for i, item in enumerate(marked_images, 1):
        word_en = item["en"]
        word_zh = item["zh"]
        category = item.get("category", "")
        
        print(f"[{i}/{len(marked_images)}] {word_en} ({word_zh})")
        
        # 生成优化的提示词
        prompt = get_prompt_for_word(word_en, word_zh, category)
        print(f"  📝 提示词: {prompt[:60]}...")
        
        # 下载图片
        image_data = download_image(word_en, prompt)
        
        if image_data:
            # 保存图片
            image_path = os.path.join(IMAGES_DIR, f"{word_en}.jpg")
            with open(image_path, "wb") as f:
                f.write(image_data)
            print(f"  ✅ 已保存: {image_path}")
            success_count += 1
        else:
            print(f"  ❌ 下载失败")
            fail_count += 1
        
        print()
        time.sleep(1)  # 避免请求过快
    
    print("=" * 50)
    print(f"  ✅ 成功: {success_count}")
    print(f"  ❌ 失败: {fail_count}")
    print("=" * 50)


if __name__ == "__main__":
    main()
