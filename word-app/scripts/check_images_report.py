#!/usr/bin/env python3
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
IMAGES_DIR = BASE_DIR / 'public' / 'images'
DATA_FILE = BASE_DIR / 'src' / 'data' / 'vocabulary.js'

def extract_words_from_js():
    """从JS文件中提取单词数据"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则提取所有单词条目
    # 匹配 { en: 'xxx', zh: 'xxx' } 格式
    pattern = r"\{\s*en:\s*['\"]([^'\"]+)['\"]\s*,\s*zh:\s*['\"]([^'\"]+)['\"]\s*\}"
    matches = re.findall(pattern, content)
    
    # 提取分组和分类信息
    groups = []
    # 匹配 groupName 和 categories
    group_pattern = r"(\w+)\s*:\s*\{\s*groupName:\s*['\"]([^'\"]+)['\"]"
    group_matches = re.findall(group_pattern, content)
    
    for group_key, group_name in group_matches:
        # 找到该组的categories
        group_start = content.find(f"{group_key}: {{")
        if group_start == -1:
            continue
        
        # 找到categories
        categories_start = content.find("categories:", group_start)
        if categories_start == -1:
            continue
        
        # 找到下一个组开始
        next_group_start = content.find("\n  },\n\n  ", categories_start)
        if next_group_start == -1:
            next_group_start = content.find("\n}\n};", categories_start)
        
        category_content = content[categories_start:next_group_start]
        
        # 提取分类
        cat_pattern = r"(\w+)\s*:\s*\{\s*name:\s*['\"]([^'\"]+)['\"]"
        cat_matches = re.findall(cat_pattern, category_content)
        
        for cat_key, cat_name in cat_matches:
            # 在该分类内找单词
            cat_start = category_content.find(f"{cat_key}: {{")
            words_start = category_content.find("words:", cat_start)
            next_cat_start = category_content.find("\n      },", words_start)
            
            if words_start == -1 or next_cat_start == -1:
                continue
            
            words_str = category_content[words_start:next_cat_start]
            word_matches = re.findall(pattern, words_str)
            
            for en_word, zh_word in word_matches:
                groups.append({
                    'group': group_name,
                    'category': cat_name,
                    'en': en_word,
                    'zh': zh_word
                })
    
    return groups

def generate_report():
    """生成图片检查报告"""
    words_data = extract_words_from_js()
    
    all_words = []
    missing_words = []
    small_words = []
    
    for item in words_data:
        en_word = item['en']
        zh_word = item['zh']
        image_path = IMAGES_DIR / f'{en_word}.jpg'
        
        status = '存在'
        size = 0
        
        if image_path.exists():
            size = os.path.getsize(image_path)
            if size < 10240:
                status = '太小'
                small_words.append({'en': en_word, 'zh': zh_word, 'group': item['group'], 'category': item['category'], 'size': size})
        else:
            status = '缺失'
            missing_words.append({'en': en_word, 'zh': zh_word, 'group': item['group'], 'category': item['category']})
        
        all_words.append({
            'en': en_word,
            'zh': zh_word,
            'group': item['group'],
            'category': item['category'],
            'status': status,
            'size': size
        })
    
    # 生成报告
    report = []
    report.append("# 图片检查报告")
    report.append(f"生成时间: {os.popen('date').read().strip()}")
    report.append(f"总单词数: {len(all_words)}")
    report.append(f"图片存在: {len([w for w in all_words if w['status'] == '存在'])}")
    report.append(f"图片缺失: {len(missing_words)}")
    report.append(f"图片太小: {len(small_words)}")
    report.append("")
    
    # 按分组统计
    report.append("## 按分组统计")
    groups_summary = {}
    for word in all_words:
        group = word['group']
        if group not in groups_summary:
            groups_summary[group] = {'total': 0, 'exists': 0, 'missing': 0, 'small': 0}
        groups_summary[group]['total'] += 1
        if word['status'] == '存在':
            groups_summary[group]['exists'] += 1
        elif word['status'] == '缺失':
            groups_summary[group]['missing'] += 1
        elif word['status'] == '太小':
            groups_summary[group]['small'] += 1
    
    for group, stats in groups_summary.items():
        report.append(f"- **{group}**: 总计 {stats['total']} | 存在 {stats['exists']} | 缺失 {stats['missing']} | 太小 {stats['small']}")
    
    # 缺失列表
    if missing_words:
        report.append("")
        report.append("## 缺失图片列表")
        for item in missing_words:
            report.append(f"- `{item['en']}.jpg` - {item['zh']} ({item['group']} / {item['category']})")
    
    # 太小列表
    if small_words:
        report.append("")
        report.append("## 图片太小列表 (< 10KB)")
        for item in small_words:
            report.append(f"- `{item['en']}.jpg` - {item['zh']} ({item['group']} / {item['category']}) - {item['size']} bytes")
    
    # 保存报告
    report_path = BASE_DIR / 'images_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"📄 报告已生成: {report_path}")
    print(f"📊 统计: 总单词 {len(all_words)}, 存在 {len([w for w in all_words if w['status'] == '存在'])}, 缺失 {len(missing_words)}, 太小 {len(small_words)}")
    
    # 返回数据供后续使用
    return {
        'all': all_words,
        'missing': missing_words,
        'small': small_words
    }

if __name__ == '__main__':
    generate_report()
