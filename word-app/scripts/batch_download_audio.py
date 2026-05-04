#!/usr/bin/env python3
import urllib.request
import urllib.parse
import urllib.error
import os
import time
import re

AUDIO_DIR = "public/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def get_vocabulary_words():
    words = set()
    with open('src/data/vocabulary.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    en_matches = re.findall(r"en:\s*['\"]([^'\"]+)['\"]", content)
    for word in en_matches:
        words.add(word)
    
    return list(words)

def download_audio(word, max_retries=3):
    filename = os.path.join(AUDIO_DIR, f"{word}.mp3")
    
    if os.path.exists(filename):
        file_size = os.path.getsize(filename)
        if file_size > 1000:
            return True, "exists"
        else:
            os.remove(filename)
    
    url = f"http://dict.youdao.com/dictvoice?audio={urllib.parse.quote(word)}&type=2"
    
    for attempt in range(max_retries):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                content_type = response.headers.get('Content-Type', '')
                data = response.read()
                
                if len(data) < 1000:
                    if attempt < max_retries - 1:
                        time.sleep(1)
                        continue
                    return False, f"too small ({len(data)} bytes)"
                
                with open(filename, 'wb') as f:
                    f.write(data)
                
                return True, f"downloaded ({len(data)} bytes)"
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                return False, str(e)
    
    return False, "failed"

def main():
    words = get_vocabulary_words()
    print(f"Found {len(words)} unique words")
    
    existing = 0
    downloaded = 0
    failed = 0
    failed_list = []
    
    for i, word in enumerate(words):
        success, status = download_audio(word)
        
        if success:
            if status == "exists":
                existing += 1
            else:
                downloaded += 1
        else:
            failed += 1
            failed_list.append((word, status))
        
        if (i + 1) % 20 == 0:
            print(f"Progress: {i + 1}/{len(words)} - Downloaded: {downloaded}, Existing: {existing}, Failed: {failed}")
        
        time.sleep(0.2)
    
    print(f"\n{'='*50}")
    print(f"Total: {len(words)} words")
    print(f"Downloaded: {downloaded}")
    print(f"Already existed: {existing}")
    print(f"Failed: {failed}")
    
    if failed_list:
        print(f"\nFailed words ({len(failed_list)}):")
        for word, status in failed_list[:30]:
            print(f"  - {word}: {status}")
        if len(failed_list) > 30:
            print(f"  ... and {len(failed_list) - 30} more")

if __name__ == "__main__":
    main()
