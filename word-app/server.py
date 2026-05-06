#!/usr/bin/env python3
import os
import json
import time
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

BASE_DIR = Path(__file__).parent
PUBLIC_DIR = BASE_DIR / 'public'
IMAGES_DIR = PUBLIC_DIR / 'images'
MARKED_FILE = BASE_DIR / 'marked_images.json'

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
    """取消标记（审核通过）"""
    marked_images = load_marked_images()
    marked_images = [img for img in marked_images if img['en'] != word]
    save_marked_images(marked_images)
    
    return jsonify({
        'success': True,
        'data': marked_images
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
