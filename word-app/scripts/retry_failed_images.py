#!/usr/bin/env python3
import os
import time
import json
import urllib.request
import urllib.parse

IMAGE_DIR = "public/images"
PROGRESS_FILE = ".image_generation_progress.json"
os.makedirs(IMAGE_DIR, exist_ok=True)


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
    
    # Check if image already exists
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        if size > 10000:
            return True, "already exists"
    
    url = generate_image_url(word)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/512.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
            
            if len(data) > 10000:
                with open(filepath, 'wb') as f:
                    f.write(data)
                return True, f"downloaded ({len(data)} bytes)"
            else:
                return False, f"too small ({len(data)} bytes)"
                
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(" ⚠️ 429 error - waiting 10 seconds...", end='', flush=True)
            time.sleep(10)
        return False, str(e)
    except Exception as e:
        return False, str(e)


def retry_failed(batch_size=100):
    progress = load_progress()
    failed_words = list(progress["failed"])
    processed = set(progress["processed"])
    failed_set = set(progress["failed"])
    
    if not failed_words:
        print("✅ No failed words to retry!")
        return
    
    # Remove words already in processed
    to_retry = [w for w in failed_words if w not in processed]
    # Also check if file already exists
    to_retry = [w for w in to_retry if not os.path.exists(os.path.join(IMAGE_DIR, f"{w}.jpg")) or os.path.getsize(os.path.join(IMAGE_DIR, f"{w}.jpg")) <= 10000]
    
    total_to_retry = len(to_retry)
    total_failed = len(failed_words)
    total_processed = len(processed)
    
    print(f"{ '='*60}")
    print(f"📊 Status:")
    print(f"   - Total processed: {total_processed}")
    print(f"   - Total failed: {total_failed}")
    print(f"   - To retry now: {total_to_retry}")
    print(f"   - Batch size: {batch_size}")
    print(f"{ '='*60}")
    
    if total_to_retry == 0:
        print("✅ All failed words either already processed or files exist!")
        return
    
    # Take first batch
    batch_words = to_retry[:batch_size]
    success_count = 0
    fail_count = 0
    
    print(f"\n🔄 Retrying {len(batch_words)} words...\n")
    
    for idx, word in enumerate(batch_words, 1):
        print(f"[{idx}/{len(batch_words)}] {word}... ", end='', flush=True)
        
        ok, status = download_image(word)
        
        if ok:
            print(f"✅ {status}")
            progress["processed"].append(word)
            # Remove from failed
            if word in progress["failed"]:
                progress["failed"].remove(word)
            success_count += 1
        else:
            print(f"❌ {status}")
            # Keep in failed
            fail_count += 1
        
        save_progress(progress)
        
        if idx < len(batch_words):
            time.sleep(2.0)
    
    print(f"\n{ '='*60}")
    print(f"📊 Batch complete!")
    print(f"   - Success: {success_count}")
    print(f"   - Still failed: {fail_count}")
    print(f"   - Total images now: {len([f for f in os.listdir(IMAGE_DIR) if f.endswith('.jpg')])}")
    print(f"   - Remaining failed words: {len(progress['failed'])}")
    print(f"{ '='*60}")


if __name__ == "__main__":
    import sys
    batch_size = 100
    if len(sys.argv) > 1:
        try:
            batch_size = int(sys.argv[1])
        except ValueError:
            pass
    retry_failed(batch_size=batch_size)
