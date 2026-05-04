import os

images_dir = '/workspace/word-app/public/images'
audio_dir = '/workspace/word-app/public/audio'

categories = {
    'face': ['face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin'],
    'body': ['head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin'],
    'organs': ['brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle']
}

print("Resource Verification Report")
print("=" * 60)

total_words = 0
missing_images = []
missing_audio = []

for cat, words in categories.items():
    print(f"\n{cat.upper()} ({len(words)} words):")
    for word in words:
        total_words += 1
        img_path = os.path.join(images_dir, f"{word}.jpg")
        audio_path = os.path.join(audio_dir, f"{word}.mp3")
        
        img_ok = os.path.exists(img_path)
        audio_ok = os.path.exists(audio_path)
        
        status = "  OK" if (img_ok and audio_ok) else "  MISSING"
        if not img_ok:
            missing_images.append(word)
            status += f" (image)"
        if not audio_ok:
            missing_audio.append(word)
            status += f" (audio)"
        
        print(f"  {word}: {'✓' if img_ok else '✗'}img {'✓' if audio_ok else '✗'}audio")

print("\n" + "=" * 60)
print(f"Total: {total_words} words")
print(f"Images: {total_words - len(missing_images)}/{total_words} OK")
print(f"Audio: {total_words - len(missing_audio)}/{total_words} OK")

if missing_images:
    print(f"\nMissing images: {missing_images}")
if missing_audio:
    print(f"\nMissing audio: {missing_audio}")
