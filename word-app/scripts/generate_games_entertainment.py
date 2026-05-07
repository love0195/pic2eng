#!/usr/bin/env python3
import urllib.request
import urllib.parse
import os
import time

IMAGES_DIR = '/workspace/word-app/public/images'

WORDS = [
    ('game', 'video game console controller cartoon style'),
    ('toy', 'colorful toys basket cartoon style'),
    ('puzzle', 'jigsaw puzzle pieces cartoon style'),
    ('chess', 'chess board pieces cartoon style'),
    ('card', 'playing cards hand cartoon style'),
    ('dice', 'dice cubes cartoon style'),
    ('board_game', 'board game box pieces cartoon style'),
    ('video_game', 'video game controller cartoon style'),
    ('controller', 'game controller cartoon style'),
    ('console', 'game console box cartoon style'),
    ('doll', 'doll toy dressed cartoon style'),
    ('teddy_bear', 'teddy bear plush toy cartoon style'),
    ('robot', 'friendly robot toy cartoon style'),
    ('lego', 'lego building blocks colorful cartoon style'),
    ('kite', 'kite flying wind cartoon style'),
    ('balloon', 'colorful balloons cartoon style'),
    ('yo_yo', 'yo-yo toy string cartoon style'),
    ('top', 'spinning top toy cartoon style'),
    ('marble', 'glass marbles colorful cartoon style'),
    ('slingshot', 'toy slingshot cartoon style'),
    ('bubble', 'soap bubble floating cartoon style'),
    ('playground', 'playground swings slides cartoon style'),
    ('swing', 'child swinging playground cartoon style'),
    ('slide', 'playground slide cartoon style'),
    ('sandbox', 'sand box toys children cartoon style'),
    ('seesaw', 'children seesaw playground cartoon style'),
    ('carousel', 'carousel merry-go-round cartoon style'),
    ('ferris_wheel', 'ferris wheel carnival cartoon style'),
    ('roller_coaster', 'roller coaster amusement park cartoon style'),
    ('haunted_house', 'halloween haunted house cartoon style'),
]

def generate_image(word, prompt, retry=3):
    filename = f"{IMAGES_DIR}/{word}.jpg"
    if os.path.exists(filename):
        print(f"SKIP: {word} (already exists)")
        return True

    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed=42&nologo=true"

    for attempt in range(retry):
        try:
            print(f"GENERATING: {word} (attempt {attempt+1})...")
            urllib.request.urlretrieve(url, filename)
            time.sleep(2)
            if os.path.exists(filename) and os.path.getsize(filename) > 5000:
                print(f"SUCCESS: {word}")
                return True
        except Exception as e:
            print(f"ERROR: {word} - {e}")
            time.sleep(3)

    return False

if __name__ == '__main__':
    print(f"Generating {len(WORDS)} images...")
    for word, prompt in WORDS:
        generate_image(word, prompt)
    print("Done!")
