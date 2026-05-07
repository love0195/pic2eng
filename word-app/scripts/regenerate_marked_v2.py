#!/usr/bin/env python3
import urllib.request
import urllib.parse
import os
import time
import json
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

IMAGES_DIR = '/workspace/word-app/public/images'
MARKED_FILE = '/workspace/word-app/marked_images.json'

WORDS = [
    ('dishwasher', 'dishwasher kitchen appliance white clean cartoon flat design'),
    ('iron', 'clothes iron pressing appliance cartoon flat design'),
    ('hairdryer', 'hair dryer styling tool pink cartoon flat design'),
    ('speaker', 'audio speaker electronic device cartoon flat design'),
    ('charger', 'phone charger cable plug cartoon flat design'),
    ('battery', 'aa battery pack cartoon flat design'),
    ('electric_pot', 'electric pressure cooker kitchen silver cartoon flat design'),
    ('electric_blanket', 'electric blanket warm cozy red cartoon flat design'),
    ('heater', 'room heater electric warming cartoon flat design'),
]

def generate_image(word, prompt, retry=5):
    filename = f"{IMAGES_DIR}/{word}.jpg"
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed=100&nologo=true"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    }

    for attempt in range(retry):
        try:
            print(f"GENERATING: {word} (attempt {attempt+1})...")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ssl_context, timeout=60) as response:
                data = response.read()
                with open(filename, 'wb') as f:
                    f.write(data)
            time.sleep(5)
            if os.path.exists(filename) and os.path.getsize(filename) > 5000:
                print(f"SUCCESS: {word}")
                return True
            else:
                print(f"FAILED: {word} - file too small or invalid")
        except Exception as e:
            print(f"ERROR: {word} - {e}")
        time.sleep(3)
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
