import urllib.request
import os

audio_dir = '/workspace/word-app/public/audio'
word = 'face'

url = f"http://dict.youdao.com/dictvoice?audio={word}&type=2"
filepath = os.path.join(audio_dir, f"{word}.mp3")

print(f"Downloading audio for: {word}")

try:
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    response = urllib.request.urlopen(req, timeout=30)
    content = response.read()
    
    if len(content) > 1000:
        with open(filepath, 'wb') as f:
            f.write(content)
        print(f"Downloaded: {filepath} ({len(content)} bytes)")
    else:
        print(f"Content too small: {len(content)} bytes")
except Exception as e:
    print(f"Error: {e}")
