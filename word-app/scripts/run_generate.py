#!/usr/bin/env python3
import os
import time
import json
import urllib.request
import urllib.parse
import subprocess

IMAGE_DIR = "public/images"
PROGRESS_FILE = ".image_generation_progress.json"
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_vocabulary_words():
    import re
    with open('src/data/vocabulary.js', 'r', encoding='utf-8') as f:
        content = f.read()
    en_matches = re.findall(r"en:\s*['\"]([^'\"]+)['\"]", content)
    return list(dict.fromkeys(en_matches))

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"processed": [], "failed": []}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def generate_image_url(word):
    clean_word = word.replace('_', ' ')
    prompt = f"{clean_word}, white background, simple cartoon"
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"

def download_image(word):
    filepath = os.path.join(IMAGE_DIR, f"{word}.jpg")
    
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size > 10000:
            return True, "exists", 0
    
    url = generate_image_url(word)
    start = time.time()
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=20) as response:
            data = response.read()
            elapsed = time.time() - start
            
            if len(data) > 10000:
                with open(filepath, 'wb') as f:
                    f.write(data)
                return True, f"OK {len(data)}b", elapsed
            return False, f"small {len(data)}b", elapsed
            
    except Exception as e:
        elapsed = time.time() - start
        return False, str(e)[:40], elapsed

def git_commit():
    try:
        subprocess.run(['git', 'add', 'public/images/'], capture_output=True, timeout=10)
        result = subprocess.run(['git', 'diff', '--cached', '--stat'], capture_output=True, text=True, timeout=10)
        if result.stdout.strip():
            subprocess.run(['git', 'commit', '-m', 'feat: auto image batch'], capture_output=True, timeout=30)
            return True
    except:
        pass
    return False

def batch_generate(batch_size=30):
    words = get_vocabulary_words()
    progress = load_progress()
    
    processed = set(progress["processed"])
    failed_set = set(progress["failed"])
    to_process = [w for w in words if w not in processed and w not in failed_set]
    
    total = len(words)
    completed = total - len(to_process)
    
    print(f"\n{'='*50}")
    print(f"进度: {completed}/{total} ({completed/total*100:.1f}%) 剩余:{len(to_process)}")
    print(f"{'='*50}\n")
    
    if not to_process:
        return False
    
    batch = to_process[:batch_size]
    success = 0
    fail = 0
    
    for idx, word in enumerate(batch, 1):
        print(f"[{idx}/{len(batch)}] {word}...", end=' ', flush=True)
        is_ok, status, elapsed = download_image(word)
        
        if is_ok:
            print(f"✅ {status} ({elapsed:.1f}s)")
            progress["processed"].append(word)
            success += 1
            wait = 0.2
        else:
            print(f"❌ {status}")
            progress["failed"].append(word)
            fail += 1
            wait = 2.0
            if "429" in status:
                wait = 3.0
        
        save_progress(progress)
        time.sleep(wait)
    
    total_now = len([f for f in os.listdir(IMAGE_DIR) if f.endswith('.jpg')])
    print(f"\n批次完成: ✅{success} ❌{fail} 总计:{total_now}")
    
    if git_commit():
        print("📦 已提交 Git")
    
    return len(to_process) > batch_size

if __name__ == "__main__":
    print("🚀 持续图片生成 (退让策略: 成功0.2s 失败2s 429错误3s)")
    
    for i in range(1000):
        print(f"\n📦 批次 {i+1}")
        if not batch_generate():
            print("\n🎉 全部完成!")
            break
        print("⏳ 等待 1s...\n")
        time.sleep(1)
