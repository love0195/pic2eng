#!/usr/bin/env python3
import os
import json
import time
import threading
import urllib.request
import urllib.parse
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

BASE_DIR = Path(__file__).parent
PUBLIC_DIR = BASE_DIR / 'public'
IMAGES_DIR = PUBLIC_DIR / 'images'
MARKED_FILE = BASE_DIR / 'marked_images.json'

# 增强提示词映射表 - 根据分类优化提示词
ENHANCED_PROMPTS = {
    '内脏器官': {
        'prefix': 'human organ, anatomical illustration, medical diagram, realistic, white background',
        'words': {}
    },
    '颜色形状': {
        'prefix': 'color swatch, solid color, minimal, white background',
        'words': {
            'purple': 'purple color, solid purple background, color sample',
            'white': 'white color sample, clean white background',
            'beige': 'beige tan color, warm neutral tone, color sample'
        }
    },
    '动作单词': {
        'prefix': 'human hand action, instructional, white background',
        'words': {
            'fold': 'hands folding paper, origami action',
            'release': 'hand releasing object, letting go',
            'press': 'finger pressing button',
            'click': 'finger clicking mouse button',
            'tap': 'finger tapping touch screen',
            'shake': 'hand shaking object',
            'stir': 'hand stirring with spoon',
            'mix': 'mixing ingredients in bowl',
            'pour': 'pouring liquid from container',
            'fill': 'filling glass with water',
            'clean': 'cleaning surface with cloth',
            'wipe': 'wiping surface with cloth',
            'chop': 'chopping vegetables with knife',
            'slice': 'slicing bread with knife',
            'tear': 'hands tearing paper',
            'draw': 'hand drawing with pencil',
            'type': 'hands typing on keyboard'
        }
    },
    '动作词组': {
        'prefix': 'human action, two hands interaction, instructional, white background',
        'words': {}
    },
    '日常用品': {
        'prefix': 'everyday object, product photography, clean white background',
        'words': {}
    },
    '食物': {
        'prefix': 'food photography, fresh ingredients, white background',
        'words': {}
    },
    '动物': {
        'prefix': 'animal portrait, wildlife photography, white background',
        'words': {}
    },
    '植物': {
        'prefix': 'plant, botanical illustration, white background',
        'words': {}
    },
    '交通工具': {
        'prefix': 'vehicle, transportation, clean white background',
        'words': {}
    },
    '衣物': {
        'prefix': 'clothing fashion, product photography, white background',
        'words': {}
    },
    '身体部位': {
        'prefix': 'human body part, anatomical, white background',
        'words': {}
    },
    '抽象概念': {
        'prefix': 'abstract concept, minimal icon, white background',
        'words': {
            'thin': 'thin object, slim, visual representation',
            'dark': 'darkness shadow, abstract representation',
            'clean': 'clean and tidy room, sparkling clean'
        }
    }
}

# 重新生成任务状态
regeneration_status = {
    'running': False,
    'progress': 0,
    'total': 0,
    'success': 0,
    'failed': 0,
    'current': '',
    'log': []
}

def load_marked_images():
    """加载标记的图片列表"""
    if MARKED_FILE.exists():
        with open(MARKED_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_marked_images(data):
    """保存标记的图片列表"""
    with open(MARKED_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_enhanced_prompt(word, category):
    """根据分类和单词获取增强提示词"""
    if category in ENHANCED_PROMPTS:
        if word in ENHANCED_PROMPTS[category]['words']:
            return ENHANCED_PROMPTS[category]['words'][word]
        return f"{word}, {ENHANCED_PROMPTS[category]['prefix']}"
    return f"{word}, realistic, high quality, simple white background"

def download_image(word, prompt):
    """下载单个图片"""
    image_path = IMAGES_DIR / f'{word}.jpg'
    
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=120) as response:
            content = response.read()
            
            with open(image_path, 'wb') as f:
                f.write(content)
            
            if os.path.getsize(image_path) > 10240:
                return True, '下载成功'
            else:
                os.remove(image_path)
                return False, '图片太小'
            
    except Exception as e:
        if image_path.exists():
            os.remove(image_path)
        return False, f'错误: {e}'

def regenerate_images_async():
    """异步重新生成图片"""
    global regeneration_status
    
    marked_images = load_marked_images()
    regeneration_status['total'] = len(marked_images)
    regeneration_status['progress'] = 0
    regeneration_status['success'] = 0
    regeneration_status['failed'] = 0
    regeneration_status['log'] = []
    
    for i, item in enumerate(marked_images):
        word = item['en']
        zh = item.get('zh', '')
        category = item.get('category', '')
        
        regeneration_status['current'] = f"{word} ({zh})"
        prompt = get_enhanced_prompt(word, category)
        
        regeneration_status['log'].append(f"🔄 正在处理: {word}")
        regeneration_status['log'].append(f"   提示词: {prompt}")
        
        success, msg = download_image(word, prompt)
        
        if success:
            regeneration_status['success'] += 1
            regeneration_status['log'].append(f"   ✅ {msg}")
        else:
            regeneration_status['failed'] += 1
            regeneration_status['log'].append(f"   ❌ {msg}")
        
        regeneration_status['progress'] = i + 1
        time.sleep(3)
    
    # 完成后更新状态
    regeneration_status['running'] = False
    regeneration_status['log'].append("✨ 重新生成完成！")

@app.route('/')
def index():
    return send_from_directory('dist', 'index.html')

@app.route('/api/marked-images', methods=['GET'])
def get_marked_images():
    """获取标记的图片列表"""
    return jsonify({
        'success': True,
        'data': load_marked_images()
    })

@app.route('/api/marked-images', methods=['POST'])
def mark_image():
    """标记图片为不合适"""
    data = request.json
    word = data.get('en')
    
    marked_images = load_marked_images()
    
    # 检查是否已存在
    if not any(img['en'] == word for img in marked_images):
        marked_images.append({
            'en': word,
            'zh': data.get('zh', ''),
            'group': data.get('group', ''),
            'category': data.get('category', ''),
            'markedAt': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        })
        save_marked_images(marked_images)
    
    return jsonify({
        'success': True,
        'data': marked_images
    })

@app.route('/api/marked-images/<word>', methods=['DELETE'])
def unmark_image(word):
    """取消标记"""
    marked_images = load_marked_images()
    marked_images = [img for img in marked_images if img['en'] != word]
    save_marked_images(marked_images)
    
    return jsonify({
        'success': True,
        'data': marked_images
    })

@app.route('/api/regenerate', methods=['POST'])
def start_regenerate():
    """开始重新生成图片"""
    global regeneration_status
    
    if regeneration_status['running']:
        return jsonify({
            'success': False,
            'message': '正在生成中，请稍后'
        })
    
    regeneration_status['running'] = True
    regeneration_status['log'] = ['🚀 开始重新生成图片...']
    
    # 在后台线程中运行
    thread = threading.Thread(target=regenerate_images_async)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': '已开始重新生成'
    })

@app.route('/api/regenerate/status', methods=['GET'])
def get_regenerate_status():
    """获取重新生成状态"""
    return jsonify({
        'success': True,
        'data': regeneration_status
    })

if __name__ == '__main__':
    print("🚀 启动服务器...")
    print(f"📁 图片目录: {IMAGES_DIR}")
    print(f"📝 标记文件: {MARKED_FILE}")
    print("🌐 访问地址: http://localhost:28765/")
    print()
    
    # 创建必要的目录
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    app.run(host='0.0.0.0', port=28765, debug=True)
