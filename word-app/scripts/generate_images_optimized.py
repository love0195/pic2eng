#!/usr/bin/env python3
import os
import time
import json
import urllib.request
import urllib.parse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

IMAGE_DIR = "public/images"
PROGRESS_FILE = ".image_generation_progress.json"
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_vocabulary_words():
    words = []
    with open('src/data/vocabulary.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    import re
    en_matches = re.findall(r"en:\s*['\"]([^'\"]+)['\"]", content)
    unique_words = list(dict.fromkeys(en_matches))
    return unique_words

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "processed": [],
        "failed": []
    }

def save_progress(progress):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def generate_image_url(word, style="simple cartoon illustration", background="white"):
    clean_word = word.replace('_', ' ')
    prompt = f"{clean_word}, {background} background, {style}"
    encoded_prompt = urllib.parse.quote(prompt)
    seed = str(hash(word) % 1000000)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed={seed}&nologo=true"

def download_image(word):
    filepath = os.path.join(IMAGE_DIR, f"{word}.jpg")
    
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size > 10000:
            return word, True, "exists"
    
    url = generate_image_url(word)
    
    for attempt in range(2):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                
                if len(data) > 10000:
                    with open(filepath, 'wb') as f:
                        f.write(data)
                    return word, True, f"downloaded ({len(data)} bytes)"
                else:
                    if attempt == 1:
                        return word, False, f"too small ({len(data)} bytes)"
                    time.sleep(1)
                    
        except Exception as e:
            if "429" in str(e):
                time.sleep(0.5 + attempt * 0.5)
            elif attempt == 1:
                return word, False, str(e)
            else:
                time.sleep(0.5)
    
    return word, False, "max retries"

def batch_generate(batch_size=60, max_workers=8):
    words = get_vocabulary_words()
    progress = load_progress()
    
    processed = set(progress["processed"])
    failed = set(progress["failed"])
    to_process = [w for w in words if w not in processed and w not in failed]
    
    total = len(words)
    remaining = len(to_process)
    completed = total - remaining
    
    print(f"{'='*60}")
    print(f"📊 进度: {completed}/{total} 完成 ({completed/total*100:.1f}%)")
    print(f"剩余: {remaining} 张图片")
    print(f"批量大小: {batch_size} 张/批")
    print(f"并行: {max_workers} 个线程")
    print(f"{'='*60}")
    
    batch_words = to_process[:batch_size]
    success_count = 0
    fail_count = 0
    lock = threading.Lock()
    
    print(f"\n开始处理批次 ({len(batch_words)} 张)...\n")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_image, word): word for word in batch_words}
        
        for idx, future in enumerate(as_completed(futures), 1):
            word, ok, status = future.result()
            
            with lock:
                if ok:
                    print(f"[{idx}/{len(batch_words)}] {word}... ✅ {status}")
                    progress["processed"].append(word)
                    success_count += 1
                else:
                    print(f"[{idx}/{len(batch_words)}] {word}... ❌ {status}")
                    progress["failed"].append(word)
                    fail_count += 1
                
                save_progress(progress)
    
    print(f"\n{'='*60}")
    print(f"📦 批次完成!")
    print(f"成功: {success_count} 张")
    print(f"失败: {fail_count} 张")
    print(f"已生成图片总数: {len([f for f in os.listdir(IMAGE_DIR) if f.endswith('.jpg')])} 张")
    print(f"{'='*60}")

if __name__ == "__main__":
    import sys
    batch_size = 60
    max_workers = 8
    if len(sys.argv) > 1:
        try:
            batch_size = int(sys.argv[1])
        except ValueError:
            pass
        if len(sys.argv) > 2:
            try:
                max_workers = int(sys.argv[2])
            except ValueError:
                pass
    batch_generate(batch_size=batch_size, max_workers=max_workers)
