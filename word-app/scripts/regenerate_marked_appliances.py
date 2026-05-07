#!/usr/bin/env python3
import urllib.request
import urllib.parse
import os
import time
import json

IMAGES_DIR = '/workspace/word-app/public/images'
MARKED_FILE = '/workspace/word-app/marked_images.json'

WORDS = [
    ('dishwasher', 'dishwasher machine kitchen white cartoon style clean flat design simple'),
    ('iron', 'clothes iron pressing iron household appliance cartoon style flat design'),
    ('hairdryer', 'hair dryer electric styling tool pink purple cartoon style flat design'),
    ('speaker', 'audio speaker bluetooth speaker electronic device cartoon style flat design'),
    ('charger', 'phone charger charging cable electric plug cartoon style flat design'),
    ('battery', 'aa battery aa batteries pack cartoon style flat design'),
    ('electric_pot', 'electric pressure cooker kitchen appliance silver cartoon style flat design'),
    ('electric_blanket', 'electric blanket warm cozy bedding red cartoon style flat design'),
    ('heater', 'room heater electric heater warming device cartoon style flat design'),
]

def generate_image(word, prompt, retry=3):
    filename = f"{IMAGES_DIR}/{word}.jpg"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed=42&nologo=true"

    for attempt in range(retry):
        try:
            print(f"GENERATING: {word} (attempt {attempt+1})...")
            urllib.request.urlretrieve(url, filename)
            time.sleep(3)
            if os.path.exists(filename) and os.path.getsize(filename) > 5000:
                print(f"SUCCESS: {word}")
                return True
            else:
                print(f"FAILED: {word} - file too small")
        except Exception as e:
            print(f"ERROR: {word} - {e}")
        time.sleep(2)
    return False

if __name__ == '__main__':
    print(f"Generating {len(WORDS)} images...")
    success = []
    for word, prompt in WORDS:
        if generate_image(word, prompt):
            success.append(word)

    # 清空marked_images.json
    with open(MARKED_FILE, 'w') as f:
        json.dump([], f)
    print(f"\nDone! {len(success)} images regenerated.")
