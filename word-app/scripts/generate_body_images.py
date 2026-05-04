import urllib.request
import urllib.parse
import base64
import time
import os

categories = {
    'face': ['face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin'],
    'body': ['head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin'],
    'organs': ['brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle']
}

prompts = {
    'face': "A simple cartoon illustration of a human face on white background, clean design, educational style",
    'forehead': "A simple cartoon illustration of a human forehead on white background, clean design, educational style",
    'eye': "A simple cartoon illustration of a human eye on white background, clean design, educational style",
    'eyebrow': "A simple cartoon illustration of a human eyebrow on white background, clean design, educational style",
    'ear': "A simple cartoon illustration of a human ear on white background, clean design, educational style",
    'nose': "A simple cartoon illustration of a human nose on white background, clean design, educational style",
    'cheek': "A simple cartoon illustration of a human cheek on white background, clean design, educational style",
    'mouth': "A simple cartoon illustration of a human mouth on white background, clean design, educational style",
    'lip': "A simple cartoon illustration of human lips on white background, clean design, educational style",
    'chin': "A simple cartoon illustration of a human chin on white background, clean design, educational style",
    'head': "A simple cartoon illustration of a human head on white background, clean design, educational style",
    'neck': "A simple cartoon illustration of a human neck on white background, clean design, educational style",
    'shoulder': "A simple cartoon illustration of a human shoulder on white background, clean design, educational style",
    'arm': "A simple cartoon illustration of a human arm on white background, clean design, educational style",
    'elbow': "A simple cartoon illustration of a human elbow on white background, clean design, educational style",
    'hand': "A simple cartoon illustration of a human hand on white background, clean design, educational style",
    'finger': "A simple cartoon illustration of a human finger on white background, clean design, educational style",
    'leg': "A simple cartoon illustration of a human leg on white background, clean design, educational style",
    'knee': "A simple cartoon illustration of a human knee on white background, clean design, educational style",
    'foot': "A simple cartoon illustration of a human foot on white background, clean design, educational style",
    'skin': "A simple cartoon illustration of human skin cross-section on white background, clean design, educational style",
    'brain': "A simple cartoon illustration of a human brain on white background, clean design, educational style, anatomy diagram",
    'heart': "A simple cartoon illustration of a human heart on white background, clean design, educational style, anatomy diagram",
    'lung': "A simple cartoon illustration of human lungs on white background, clean design, educational style, anatomy diagram",
    'liver': "A simple cartoon illustration of a human liver on white background, clean design, educational style, anatomy diagram",
    'stomach': "A simple cartoon illustration of a human stomach on white background, clean design, educational style, anatomy diagram",
    'intestine': "A simple cartoon illustration of human intestines on white background, clean design, educational style, anatomy diagram",
    'kidney': "A simple cartoon illustration of a human kidney on white background, clean design, educational style, anatomy diagram",
    'muscle': "A simple cartoon illustration of a human muscle on white background, clean design, educational style, anatomy diagram"
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

def try_decode_as_base64(data, filename):
    try:
        decoded = base64.b64decode(data)
        if len(decoded) > 5000 and decoded[:4] in [b'\x89PNG', b'\xff\xd8\xff', b'GIF8', b'RIFF']:
            with open(filename, 'wb') as f:
                f.write(decoded)
            print(f"  Base64 decoded: {filename} ({len(decoded)} bytes)")
            return True
    except:
        pass
    return False

def generate_image(word, prompt, max_wait=120):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id=body_{word}_{int(time.time())}"
    
    filename = f"{word}.jpg"
    filepath = os.path.join(save_dir, filename)
    
    print(f"  Generating: {filename}")
    
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, image/png, image/*, */*'
            })
            
            response = urllib.request.urlopen(req, timeout=90)
            content = response.read()
            
            if try_decode_as_base64(content, filepath):
                return True
            
            if len(content) > 5000:
                with open(filepath, 'wb') as f:
                    f.write(content)
                print(f"  Saved directly: {filename} ({len(content)} bytes)")
                return True
            
            try:
                data = json.loads(content)
                if 'image' in data:
                    return try_decode_as_base64(data['image'], filepath)
                if 'url' in data:
                    img_response = urllib.request.urlopen(data['url'], timeout=30)
                    img_content = img_response.read()
                    if len(img_content) > 5000:
                        with open(filepath, 'wb') as f:
                            f.write(img_content)
                        print(f"  Downloaded from URL: {filename}")
                        return True
            except:
                pass
            
            print(f"  Attempt {attempt + 1} failed, retrying...")
            time.sleep(2)
            
        except Exception as e:
            print(f"  Error: {e}, retrying...")
            time.sleep(2)
    
    return False

all_words = []
for cat, words in categories.items():
    all_words.extend(words)

print(f"Total words to generate: {len(all_words)}")
print("=" * 50)

success_count = 0
failed_words = []

for word in all_words:
    prompt = prompts.get(word, f"A simple cartoon illustration of a {word} on white background, clean design, educational style")
    
    if generate_image(word, prompt):
        success_count += 1
    else:
        failed_words.append(word)
    
    time.sleep(1)

print("=" * 50)
print(f"Completed: {success_count}/{len(all_words)} images generated")
if failed_words:
    print(f"Failed words: {failed_words}")
