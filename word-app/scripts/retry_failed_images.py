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
        return True
    
    # Remove words already in processed
    to_retry = [w for w in failed_words if w not in processed]
    # Also check if file already exists
    to_retry = [w for w in to_retry if not os.path.exists(os.path.join(IMAGE_DIR, f"{w}.jpg")) or os.path.getsize(os.path.join(IMAGE_DIR, f"{w}.jpg")) <= 10000]
    
    total_to_retry = len(to_retry)
    total_failed = len(failed_words)
    total_processed = len(processed)
    
    print(f"\n{'='*70}")
    print(f"📊 当前进度报告")
    print(f"{'='*70}")
    print(f"   ✅ 已处理单词: {total_processed}")
    print(f"   ❌ 失败单词: {total_failed}")
    print(f"   📥 待处理: {total_to_retry}")
    print(f"   📦 当前批次: {batch_size}")
    print(f"   🖼️  已下载图片: {len([f for f in os.listdir(IMAGE_DIR) if f.endswith('.jpg')])}")
    print(f"{'='*70}\n")
    
    if total_to_retry == 0:
        print("✅ 所有失败单词都已处理完毕或文件已存在！")
        return True
    
    # Take first batch
    batch_words = to_retry[:batch_size]
    success_count = 0
    fail_count = 0
    
    print(f"🔄 正在处理第1批 ({len(batch_words)} 个单词)...\n")
    
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
    
    # 打印批次结果
    print(f"\n{'='*70}")
    print(f"📊 第1批处理完成:")
    print(f"   ✅ 成功: {success_count}")
    print(f"   ❌ 失败: {fail_count}")
    print(f"   🖼️  图片总数: {len([f for f in os.listdir(IMAGE_DIR) if f.endswith('.jpg')])}")
    print(f"   📋 剩余失败单词: {len(progress['failed'])}")
    print(f"{'='*70}")
    
    # 如果这一批全部失败，结束任务
    if success_count == 0:
        print("\n⚠️  这一批全部失败，结束任务")
        return False
    
    # 如果这一批有部分成功，继续下一批
    print("\n✅ 这一批有部分成功，继续下一批...")
    return True


def retry_continuously(batch_size=30):
    """连续处理多批，直到某一批全部失败"""
    batch_num = 1
    
    while True:
        print(f"\n{'#'*70}")
        print(f"# 第 {batch_num} 批处理")
        print(f"{'#'*70}\n")
        
        should_continue = retry_failed(batch_size=batch_size)
        
        if not should_continue:
            print("\n🎉 所有批次处理完成！")
            break
        
        batch_num += 1
        time.sleep(3)  # 批次之间休息3秒


if __name__ == "__main__":
    import sys
    batch_size = 30
    if len(sys.argv) > 1:
        try:
            batch_size = int(sys.argv[1])
        except ValueError:
            pass
    retry_continuously(batch_size=batch_size)
