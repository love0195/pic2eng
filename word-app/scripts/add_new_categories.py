import urllib.request
import urllib.parse
import time
import os

# 新增分类和单词
new_categories = {
    'sea_animals': {
        'name': '海洋动物',
        'icon': '🐙',
        'words': [
            { 'en': 'whale', 'zh': '鲸鱼' },
            { 'en': 'dolphin', 'zh': '海豚' },
            { 'en': 'shark', 'zh': '鲨鱼' },
            { 'en': 'octopus', 'zh': '章鱼' },
            { 'en': 'jellyfish', 'zh': '水母' },
            { 'en': 'seahorse', 'zh': '海马' },
            { 'en': 'crab', 'zh': '螃蟹' },
            { 'en': 'lobster', 'zh': '龙虾' },
            { 'en': 'starfish', 'zh': '海星' },
            { 'en': 'seal', 'zh': '海豹' },
        ]
    },
    'mammals': {
        'name': '哺乳动物',
        'icon': '🦁',
        'words': [
            { 'en': 'lion', 'zh': '狮子' },
            { 'en': 'tiger', 'zh': '老虎' },
            { 'en': 'bear', 'zh': '熊' },
            { 'en': 'wolf', 'zh': '狼' },
            { 'en': 'fox', 'zh': '狐狸' },
            { 'en': 'deer', 'zh': '鹿' },
            { 'en': 'giraffe', 'zh': '长颈鹿' },
            { 'en': 'zebra', 'zh': '斑马' },
            { 'en': 'kangaroo', 'zh': '袋鼠' },
            { 'en': 'koala', 'zh': '考拉' },
        ]
    },
    'plants': {
        'name': '植物篇',
        'icon': '🌸',
        'words': [
            { 'en': 'rose', 'zh': '玫瑰' },
            { 'en': 'sunflower', 'zh': '向日葵' },
            { 'en': 'tulip', 'zh': '郁金香' },
            { 'en': 'daisy', 'zh': '雏菊' },
            { 'en': 'tree', 'zh': '树' },
            { 'en': 'flower', 'zh': '花' },
            { 'en': 'grass', 'zh': '草' },
            { 'en': 'leaf', 'zh': '叶子' },
            { 'en': 'mushroom', 'zh': '蘑菇' },
            { 'en': 'bamboo', 'zh': '竹子' },
        ]
    }
}

# 读取现有vocabulary.js
with open('/workspace/word-app/src/data/vocabulary.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到最后一个分类的位置（fruits的结束）
last_bracket_pos = content.rfind('}')
insert_pos = content.rfind('}', 0, last_bracket_pos) + 1

# 添加新分类
new_content = content[:insert_pos] + ',\n\n'

for key, category in new_categories.items():
    new_content += f"  {key}: {{\n"
    new_content += f"    name: '{category['name']}',\n"
    new_content += f"    icon: '{category['icon']}',\n"
    new_content += f"    words: [\n"
    for word in category['words']:
        new_content += f"      {{ en: '{word['en']}', zh: '{word['zh']}' }},\n"
    new_content += f"    ]\n"
    new_content += f"  }}\n"

new_content += content[insert_pos:]

# 写回文件
with open('/workspace/word-app/src/data/vocabulary.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ 新分类已添加到 vocabulary.js:")
for key, category in new_categories.items():
    print(f"  - {category['name']} ({len(category['words'])} 个单词)")

print(f"\n总计: 8 个分类")
