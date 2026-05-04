import urllib.request
import urllib.parse
import time
import os

images_dir = '/workspace/word-app/public/images'
audio_dir = '/workspace/word-app/public/audio'
os.makedirs(images_dir, exist_ok=True)
os.makedirs(audio_dir, exist_ok=True)

PLACEHOLDER_SIZE = 176626

new_categories = {
    'body': {
        'name': '人体',
        'icon': '🧍',
        'words': [
            { 'en': 'head', 'zh': '头' },
            { 'en': 'hand', 'zh': '手' },
            { 'en': 'foot', 'zh': '脚' },
            { 'en': 'arm', 'zh': '手臂' },
            { 'en': 'leg', 'zh': '腿' },
            { 'en': 'neck', 'zh': '脖子' },
            { 'en': 'shoulder', 'zh': '肩膀' },
            { 'en': 'finger', 'zh': '手指' },
            { 'en': 'knee', 'zh': '膝盖' },
            { 'en': 'elbow', 'zh': '手肘' },
        ]
    },
    'face': {
        'name': '面部',
        'icon': '😊',
        'words': [
            { 'en': 'eye', 'zh': '眼睛' },
            { 'en': 'nose', 'zh': '鼻子' },
            { 'en': 'mouth', 'zh': '嘴巴' },
            { 'en': 'ear', 'zh': '耳朵' },
            { 'en': 'tooth', 'zh': '牙齿' },
            { 'en': 'lip', 'zh': '嘴唇' },
            { 'en': 'eyebrow', 'zh': '眉毛' },
            { 'en': 'cheek', 'zh': '脸颊' },
            { 'en': 'chin', 'zh': '下巴' },
            { 'en': 'forehead', 'zh': '额头' },
        ]
    },
    'organs': {
        'name': '内脏',
        'icon': '❤️',
        'words': [
            { 'en': 'heart', 'zh': '心脏' },
            { 'en': 'brain', 'zh': '大脑' },
            { 'en': 'lung', 'zh': '肺' },
            { 'en': 'liver', 'zh': '肝脏' },
            { 'en': 'stomach', 'zh': '胃' },
            { 'en': 'kidney', 'zh': '肾脏' },
            { 'en': 'intestine', 'zh': '肠' },
            { 'en': 'bone', 'zh': '骨头' },
            { 'en': 'muscle', 'zh': '肌肉' },
            { 'en': 'skin', 'zh': '皮肤' },
        ]
    },
    'indoor': {
        'name': '室内空间',
        'icon': '🏠',
        'words': [
            { 'en': 'kitchen', 'zh': '厨房' },
            { 'en': 'bedroom', 'zh': '卧室' },
            { 'en': 'bathroom', 'zh': '浴室' },
            { 'en': 'living room', 'zh': '客厅' },
            { 'en': 'door', 'zh': '门' },
            { 'en': 'window', 'zh': '窗户' },
            { 'en': 'floor', 'zh': '地板' },
            { 'en': 'wall', 'zh': '墙壁' },
            { 'en': 'ceiling', 'zh': '天花板' },
            { 'en': 'stairs', 'zh': '楼梯' },
        ]
    },
    'buildings': {
        'name': '公共建筑',
        'icon': '🏛️',
        'words': [
            { 'en': 'school', 'zh': '学校' },
            { 'en': 'hospital', 'zh': '医院' },
            { 'en': 'church', 'zh': '教堂' },
            { 'en': 'library', 'zh': '图书馆' },
            { 'en': 'museum', 'zh': '博物馆' },
            { 'en': 'theater', 'zh': '剧院' },
            { 'en': 'stadium', 'zh': '体育场' },
            { 'en': 'tower', 'zh': '塔' },
            { 'en': 'castle', 'zh': '城堡' },
            { 'en': 'palace', 'zh': '宫殿' },
        ]
    }
}

with open('/workspace/word-app/src/data/vocabulary.js', 'r', encoding='utf-8') as f:
    content = f.read()

last_bracket_pos = content.rfind('}')
insert_pos = content.rfind('}', 0, last_bracket_pos) + 1

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

with open('/workspace/word-app/src/data/vocabulary.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ 新分类已添加:")
for key, category in new_categories.items():
    print(f"  - {category['name']} ({len(category['words'])} 个单词)")

print(f"\n总计: 13 个分类")
