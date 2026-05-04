#!/usr/bin/env python3
import os
import time
import urllib.request
import urllib.parse
import json

IMAGE_DIR = "public/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def get_vocabulary_data():
    try:
        with open('src/data/vocabulary.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        words = []
        en_matches = re.findall(r"en:\s*['\"]([^'\"]+)['\"]", content)
        return en_matches
    except Exception as e:
        print(f"Error reading vocabulary: {e}")
        return []

def generate_image_url(word, style="cartoon"):
    prompt = f"{word}, white background, simple cartoon illustration, clean design"
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed={hash(word) % 1000000}&nologo=true"

def download_image(word, max_retries=3):
    filename = os.path.join(IMAGE_DIR, f"{word}.jpg")
    
    if os.path.exists(filename):
        file_size = os.path.getsize(filename)
        if file_size > 10000:
            return True, "exists"
    
    url = generate_image_url(word)
    
    for attempt in range(max_retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
                
                if len(data) > 10000:
                    with open(filename, 'wb') as f:
                        f.write(data)
                    return True, f"downloaded ({len(data)} bytes)"
                else:
                    return False, f"too small ({len(data)} bytes)"
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return False, str(e)
    
    return False, "failed"

def main():
    words = get_vocabulary_data()
    print(f"Found {len(words)} words to process")
    
    results = {"success": 0, "exists": 0, "failed": 0, "failed_list": []}
    
    for i, word in enumerate(words):
        success, status = download_image(word)
        
        if success:
            if status == "exists":
                results["exists"] += 1
            else:
                results["success"] += 1
        else:
            results["failed"] += 1
            results["failed_list"].append((word, status))
        
        if (i + 1) % 10 == 0:
            print(f"Progress: {i + 1}/{len(words)} - Success: {results['success']}, Exists: {results['exists']}, Failed: {results['failed']}")
        
        time.sleep(0.3)
    
    print(f"\n{'='*50}")
    print(f"Total: {len(words)} words")
    print(f"New downloads: {results['success']}")
    print(f"Already existed: {results['exists']}")
    print(f"Failed: {results['failed']}")
    
    if results["failed_list"]:
        print(f"\nFailed words:")
        for word, status in results["failed_list"][:20]:
            print(f"  - {word}: {status}")
        if len(results["failed_list"]) > 20:
            print(f"  ... and {len(results['failed_list']) - 20} more")

if __name__ == "__main__":
    main()
