#!/usr/bin/env python3
import os
import sys
import time
import json
import requests
import urllib.parse
from pathlib import Path

# 配置路径
BASE_DIR = Path(__file__).parent.parent
PUBLIC_DIR = BASE_DIR / 'public'
IMAGES_DIR = PUBLIC_DIR / 'images'
AUDIO_DIR = PUBLIC_DIR / 'audio'
PROGRESS_FILE = BASE_DIR / '.asset_download_progress.json'

# 确保目录存在
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def get_vocabulary_words():
    """从vocabulary.js获取所有单词"""
    vocab_file = BASE_DIR / 'src' / 'data' / 'vocabulary.js'
    if not vocab_file.exists():
        print("❌ 词汇文件不存在")
        return []
    
    content = vocab_file.read_text(encoding='utf-8')
    
    # 直接收集所有可能的单词
    words = [
        # 日常生活
        'sofa', 'chair', 'table', 'bed', 'wardrobe', 'desk', 'bookshelf', 'cabinet',
        'cupboard', 'drawer', 'lamp', 'stool', 'mirror', 'pillow', 'blanket', 'curtain',
        'carpet', 'cushion', 'sofa_bed', 'nightstand', 'armchair', 'rocking_chair',
        'dining_table', 'coffee_table', 'dressing_table', 'chest_of_drawers', 'tv_stand',
        'shelving_unit', 'bench', 'hammock',
        # 家用电器
        'refrigerator', 'television', 'washing_machine', 'microwave', 'oven', 'dishwasher',
        'airconditioner', 'computer', 'fan', 'coffee_machine', 'toaster', 'vacuum_cleaner',
        'iron', 'hairdryer', 'phone', 'router', 'speaker', 'charger', 'battery', 'remote_control',
        'rice_cooker', 'electric_pot', 'water_purifier', 'air_purifier', 'humidifier',
        'dehumidifier', 'heater', 'electric_blanket', 'electric_fan', 'electric_kettle',
        # 厨房用品
        'plate', 'bowl', 'cup', 'glass', 'fork', 'knife', 'spoon', 'chopsticks', 'pot',
        'pan', 'kettle', 'bottle', 'jar', 'spatula', 'ladle', 'colander', 'grater',
        'peeler', 'cutting_board', 'blender', 'mug', 'saucer', 'serving_dish',
        'draining_board', 'apron', 'kitchen_towel', 'tupperware', 'aluminum_foil',
        'plastic_wrap', 'trash_can',
        # 衣物配饰
        'shirt', 'pants', 'dress', 'jacket', 'coat', 'sweater', 'skirt', 'shorts',
        'socks', 'shoes', 'boots', 'sandals', 'hat', 'cap', 'scarf', 'gloves', 'belt',
        'tie', 'watch', 'glasses', 'umbrella', 'bag', 'wallet', 'ring', 'necklace',
        'earrings', 'bracelet', 'hoodie', 'jeans', 'suit', 'pajamas',
        # 浴室用品
        'toothbrush', 'toothpaste', 'soap', 'shampoo', 'conditioner', 'shower',
        'bathtub', 'towel', 'sink', 'comb', 'razor', 'floss', 'mouthwash', 'lotion',
        'sunscreen', 'makeup', 'moisturizer', 'deodorant', 'bathrobe', 'slippers',
        'scale', 'plunger', 'toilet_paper', 'tissue', 'cotton_ball', 'q_tips',
        'shower_gel', 'hair_brush',
        # 清洁用品
        'broom', 'mop', 'bucket', 'sponge', 'detergent', 'bleach', 'disinfectant',
        'spray', 'cloth', 'duster', 'vacuum', 'washing_powder', 'fabric_softener',
        'window_cleaner', 'furniture_polish', 'trash_bag', 'dustpan', 'scrub_brush',
        'rubber_gloves', 'laundry_basket', 'clothesline', 'clothespins', 'hanger',
        'ironing_board', 'steam_iron',
        # 自然世界-陆地动物
        'dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'parrot', 'turtle',
        'snake', 'elephant', 'monkey', 'panda', 'fox', 'giraffe', 'zebra', 'kangaroo',
        'koala', 'tiger', 'lion', 'bear', 'wolf', 'deer', 'pig', 'cow', 'sheep',
        'horse', 'goat', 'chicken', 'duck', 'mouse', 'squirrel', 'penguin', 'eagle',
        'owl', 'butterfly', 'bee', 'ant', 'spider', 'frog', 'crocodile', 'hippo',
        'rhino', 'camel', 'leopard', 'cheetah',
        # 海洋生物
        'whale', 'shark', 'dolphin', 'octopus', 'lobster', 'crab', 'jellyfish',
        'starfish', 'seahorse', 'seal', 'sea_turtle', 'shrimp', 'squid', 'coral',
        'shell', 'seaweed', 'swan', 'pelican', 'otter', 'orca', 'stingray', 'eel',
        'clownfish', 'tuna', 'salmon', 'swordfish', 'seabird', 'mermaid',
        # 植物花卉
        'rose', 'sunflower', 'tulip', 'daisy', 'flower', 'tree', 'grass', 'leaf',
        'mushroom', 'bamboo', 'palm_tree', 'pine_tree', 'cactus', 'fern', 'ivy',
        'clover', 'lavender', 'lily', 'lotus', 'orchid', 'cherry_blossom',
        'maple_tree', 'oak_tree', 'willow', 'coconut_tree', 'bush', 'hedge', 'garden',
        'lawn', 'forest', 'jungle', 'meadow', 'seed', 'sprout', 'root', 'branch',
        'trunk', 'bark', 'thorn', 'petal',
        # 天气季节
        'sun', 'moon', 'star', 'cloud', 'rain', 'snow', 'wind', 'thunder', 'lightning',
        'rainbow', 'fog', 'ice', 'water', 'river', 'lake', 'sea', 'mountain', 'valley',
        'spring', 'summer', 'autumn', 'winter', 'storm', 'typhoon', 'hurricane',
        'tornado', 'hail', 'dew', 'frost', 'rainy', 'sunny', 'cloudy', 'windy',
        'snowy', 'hot', 'cold', 'warm', 'cool',
        # 地理地貌
        'hill', 'ocean', 'island', 'beach', 'desert', 'canyon', 'cave', 'waterfall',
        'cliff', 'volcano', 'glacier', 'marsh', 'swamp', 'plain', 'plateau', 'shore',
        'coast', 'reef', 'pond', 'stream', 'creek',
        # 美食天地-水果
        'apple', 'banana', 'orange', 'strawberry', 'cherry', 'grape', 'watermelon',
        'pineapple', 'mango', 'peach', 'pear', 'lemon', 'kiwi', 'avocado', 'blueberry',
        'raspberry', 'blackberry', 'plum', 'apricot', 'coconut', 'pomegranate',
        'fig', 'grapefruit', 'melon', 'papaya', 'dragon_fruit', 'lychee', 'longan',
        'durian', 'persimmon', 'tangerine', 'guava', 'passion_fruit', 'pitaya',
        'star_fruit', 'jackfruit',
        # 蔬菜
        'carrot', 'tomato', 'potato', 'onion', 'garlic', 'broccoli', 'cabbage',
        'lettuce', 'spinach', 'celery', 'cucumber', 'pepper', 'corn', 'bean',
        'pea', 'eggplant', 'zucchini', 'asparagus', 'cauliflower', 'pumpkin',
        'radish', 'ginger', 'leek', 'scallion', 'chili', 'bell_pepper', 'capsicum',
        'bamboo_shoot', 'kale', 'artichoke', 'fennel', 'bok_choy', 'chives',
        'parsley', 'basil', 'mint', 'cilantro',
        # 饮料
        'juice', 'milk', 'coffee', 'tea', 'soda', 'beer', 'wine', 'cocktail',
        'smoothie', 'yogurt', 'milkshake', 'cocoa', 'honey', 'syrup', 'lemonade',
        'iced_tea', 'soy_milk', 'coconut_water', 'sparkling_water', 'apple_juice',
        'grape_juice', 'tomato_juice', 'energy_drink', 'sports_drink', 'green_tea',
        'black_tea', 'white_tea', 'oolong_tea', 'latte', 'cappuccino', 'espresso',
        'mocha', 'whisky', 'vodka', 'rum', 'champagne',
        # 美食佳肴
        'pizza', 'burger', 'sandwich', 'hotdog', 'french_fries', 'fried_chicken',
        'steak', 'noodles', 'rice', 'bread', 'cake', 'cookie', 'candy', 'chocolate',
        'ice_cream', 'pudding', 'pie', 'salad', 'soup', 'sushi', 'dumplings',
        'baozi', 'tofu', 'egg', 'cheese', 'bacon', 'sausage', 'hamburger', 'taco',
        'burrito', 'nachos', 'ramen', 'spaghetti', 'lasagna', 'curry', 'fried_rice',
        'chow_mein', 'hot_pot', 'bbq',
        # 零食小吃
        'popcorn', 'chips', 'pretzel', 'nuts', 'almonds', 'cashews', 'peanuts',
        'walnuts', 'pistachios', 'raisins', 'jelly', 'gummy_bears', 'lollipop',
        'candy_bar', 'gum', 'crackers', 'rice_cakes', 'granola_bar', 'dried_fruit',
        'beef_jerky', 'seaweed', 'edamame', 'mochi', 'taiyaki', 'takoyaki', 'croissant',
        'muffin', 'donut', 'bagel', 'waffle',
        # 食材调料
        'salt', 'sugar', 'pepper', 'oil', 'vinegar', 'soy_sauce', 'butter', 'flour',
        'cream', 'vanilla', 'cinnamon', 'mustard', 'mayonnaise', 'bbq_sauce',
        # 交通出行
        'bicycle', 'motorcycle', 'car', 'taxi', 'bus', 'train', 'plane', 'boat',
        'ship', 'truck', 'helicopter', 'subway', 'ambulance', 'firetruck', 'police_car',
        'school_bus', 'tractor', 'excavator', 'crane', 'bulldozer', 'scooter',
        'skateboard', 'rocket', 'spaceship', 'hot_air_balloon', 'van', 'suv',
        'sports_car', 'jeep', 'limousine', 'ferry', 'yacht', 'sailboat', 'canoe',
        'kayak', 'jet', 'fighter', 'cargo_ship',
        # 道路设施
        'road', 'highway', 'bridge', 'tunnel', 'station', 'airport', 'port',
        'parking_lot', 'gas_station', 'traffic_light', 'stop_sign', 'crosswalk',
        'sidewalk', 'street_lamp', 'fountain', 'statue', 'monument', 'clock_tower',
        'castle', 'intersection', 'overpass', 'underpass', 'roundabout', 'pavement',
        'speed_bump', 'toll_booth', 'rest_area', 'bus_stop', 'taxi_stand',
        # 旅行相关
        'luggage', 'backpack', 'passport', 'ticket', 'map', 'guidebook', 'camera',
        'suitcase', 'hotel', 'hostel', 'motel', 'resort', 'pool', 'spa', 'restaurant',
        'cafe', 'bar', 'souvenir', 'postcard', 'currency', 'visa', 'boarding_pass',
        'check_in', 'check_out', 'reservation', 'tour', 'guide',
        # 建筑场所
        'kitchen', 'bedroom', 'bathroom', 'living_room', 'door', 'window', 'wall',
        'floor', 'ceiling', 'stairs', 'balcony', 'garage', 'basement', 'attic',
        'yard', 'corridor', 'lobby', 'rooftop', 'fence', 'hallway', 'dining_room',
        'study', 'closet', 'laundry_room', 'playroom', 'office', 'nursery',
        'guest_room', 'pantry',
        # 公共建筑
        'school', 'hospital', 'library', 'tower', 'museum', 'theater', 'stadium',
        'church', 'temple', 'mosque', 'bank', 'post_office', 'police_station',
        'fire_station', 'prison', 'palace', 'market', 'mall', 'university',
        'cinema', 'concert_hall', 'gallery', 'zoo', 'aquarium', 'amusement_park',
        'theme_park', 'train_station', 'bus_station',
        # 城市设施
        'city', 'town', 'village', 'street', 'avenue', 'boulevard', 'alley',
        'plaza', 'park', 'playground', 'skyscraper', 'office_building', 'apartment',
        'house', 'villa', 'shrine', 'pagoda', 'lighthouse', 'windmill', 'dam',
        'pyramid', 'bench', 'atm', 'phone_booth', 'mailbox',
        # 身体部位
        'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth',
        'lip', 'chin', 'tongue', 'tooth', 'teeth', 'jaw', 'wrinkle', 'freckle',
        'mole', 'beard', 'mustache', 'eyelash', 'eyelid', 'pupil', 'iris',
        'nostril', 'smile', 'frown', 'dimple', 'pimple', 'scar', 'head', 'neck',
        'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot',
        'skin', 'hair', 'back', 'chest', 'waist', 'hip', 'thigh', 'calf', 'ankle',
        'wrist', 'palm', 'knuckle', 'thumb', 'index_finger', 'middle_finger',
        'ring_finger', 'little_finger', 'toe', 'heel', 'arch', 'spine',
        # 内脏器官
        'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney',
        'muscle', 'bone', 'blood', 'vein', 'artery', 'nerve', 'rib', 'skull',
        'pancreas', 'gallbladder', 'spleen', 'bladder', 'thyroid', 'tonsil',
        'appendix', 'diaphragm', 'esophagus', 'trachea', 'bronchus', 'windpipe',
        'gullet',
        # 健康医疗
        'medicine', 'pill', 'capsule', 'syrup', 'injection', 'bandage', 'plaster',
        'cotton', 'thermometer', 'stethoscope', 'blood_pressure', 'pulse', 'fever',
        'cough', 'headache', 'stomachache', 'cold', 'flu', 'allergy', 'nausea',
        'dizziness', 'fatigue', 'pain', 'wound', 'bruise', 'swelling', 'infection',
        'virus', 'bacteria', 'vaccine',
        # 时间日期
        'second', 'minute', 'hour', 'day', 'week', 'month', 'year', 'morning',
        'afternoon', 'evening', 'night', 'dawn', 'dusk', 'today', 'tomorrow',
        'yesterday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
        'saturday', 'sunday', 'spring', 'summer', 'autumn', 'winter', 'january',
        'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
        'october', 'november', 'december', 'midnight', 'noon',
        # 数字计数
        'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
        'nine', 'ten', 'hundred', 'thousand', 'million', 'billion', 'first',
        'second', 'third', 'double', 'triple', 'half', 'pair', 'dozen', 'single',
        'couple', 'group', 'score', 'few', 'several', 'many', 'lot', 'some',
        'all', 'each', 'every',
        # 节日纪念
        'birthday', 'wedding', 'anniversary', 'festival', 'holiday', 'christmas',
        'halloween', 'thanksgiving', 'easter', 'valentine', 'new_year', 'spring_festival',
        'mid_autumn', 'dragon_boat', 'lantern_festival', 'labor_day', 'national_day',
        'children_day', 'mother_day', 'father_day', 'teacher_day', 'memorial_day',
        'vacation', 'weekend', 'schedule', 'appointment', 'deadline', 'calendar',
        'clock', 'alarm',
        # 颜色
        'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'brown',
        'black', 'white', 'gray', 'gold', 'silver', 'cyan', 'navy', 'beige',
        'maroon', 'olive', 'coral', 'lavender', 'turquoise', 'violet', 'indigo',
        'scarlet', 'cream', 'ivory', 'khaki', 'salmon', 'tan', 'burgundy', 'teal',
        'magenta', 'peach', 'plum', 'mint', 'sky_blue', 'light_pink', 'dark_green',
        'light_blue',
        # 形状
        'circle', 'square', 'triangle', 'rectangle', 'star', 'heart', 'diamond',
        'oval', 'pentagon', 'hexagon', 'cylinder', 'cube', 'sphere', 'cone',
        'pyramid', 'line', 'curve', 'angle', 'edge', 'corner', 'semicircle',
        'quarter', 'spiral', 'zigzag', 'cross', 'arrow', 'ring', 'crescent',
        'parallelogram', 'octagon',
        # 材质
        'smooth', 'rough', 'soft', 'hard', 'shiny', 'dull', 'transparent',
        'opaque', 'flexible', 'rigid', 'thick', 'thin', 'heavy', 'light'
    ]
    
    # 去重
    seen = set()
    unique_words = []
    for word in words:
        if word not in seen:
            seen.add(word)
            unique_words.append(word)
    
    # 添加单词部分（用于复合词）
    all_words = list(unique_words)
    for word in unique_words:
        if '_' in word:
            parts = word.split('_')
            for part in parts:
                if part and part not in seen:
                    seen.add(part)
                    all_words.append(part)
    
    print(f"📋 共找到 {len(all_words)} 个唯一单词")
    return all_words

def load_progress():
    """加载下载进度"""
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {
        'downloaded_images': [],
        'downloaded_audio': [],
        'failed_images': [],
        'failed_audio': [],
        'current_group': 0
    }

def save_progress(progress):
    """保存下载进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def download_image(word, progress):
    """下载图片"""
    image_path = IMAGES_DIR / f'{word}.jpg'
    
    if image_path.exists() and os.path.getsize(image_path) > 10240:
        if word not in progress['downloaded_images']:
            progress['downloaded_images'].append(word)
        return True, '已存在'
    
    # Pollinations AI
    prompt = urllib.parse.quote(f"{word}, realistic, high quality, simple background")
    image_url = f"https://image.pollinations.ai/prompt/{prompt}?width=512&height=512&nologo=true"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(image_url, headers=headers, timeout=60)
        response.raise_for_status()
        
        # 保存图片
        with open(image_path, 'wb') as f:
            f.write(response.content)
        
        # 验证大小
        if os.path.getsize(image_path) > 10240:
            if word not in progress['downloaded_images']:
                progress['downloaded_images'].append(word)
            return True, '下载成功'
        else:
            os.remove(image_path)
            if word not in progress['failed_images']:
                progress['failed_images'].append(word)
            return False, '图片太小'
            
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 429:
            print("⚠️  触发429，等待10秒...")
            time.sleep(10)
        if word not in progress['failed_images']:
            progress['failed_images'].append(word)
        return False, f'HTTP错误: {e}'
    except Exception as e:
        if word not in progress['failed_images']:
            progress['failed_images'].append(word)
        return False, f'错误: {e}'

def download_audio(word, progress):
    """下载音频（使用Google TTS）"""
    audio_path = AUDIO_DIR / f'{word}.mp3'
    
    if audio_path.exists() and os.path.getsize(audio_path) > 1024:
        if word not in progress['downloaded_audio']:
            progress['downloaded_audio'].append(word)
        return True, '已存在'
    
    # Google Text-to-Speech
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={urllib.parse.quote(word)}&tl=en"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(tts_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 保存音频
        with open(audio_path, 'wb') as f:
            f.write(response.content)
        
        # 验证大小
        if os.path.getsize(audio_path) > 1024:
            if word not in progress['downloaded_audio']:
                progress['downloaded_audio'].append(word)
            return True, '下载成功'
        else:
            os.remove(audio_path)
            if word not in progress['failed_audio']:
                progress['failed_audio'].append(word)
            return False, '音频太小'
            
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 429:
            print("⚠️  触发429，等待10秒...")
            time.sleep(10)
        if word not in progress['failed_audio']:
            progress['failed_audio'].append(word)
        return False, f'HTTP错误: {e}'
    except Exception as e:
        if word not in progress['failed_audio']:
            progress['failed_audio'].append(word)
        return False, f'错误: {e}'

def git_commit(message):
    """提交到git"""
    print(f"\n📦 提交到Git: {message}")
    os.chdir(BASE_DIR)
    os.system('git add public/images/ public/audio/ .asset_download_progress.json')
    os.system(f'git commit -m "{message}"')
    os.system('git push')

def main():
    print("🚀 开始下载资源...")
    print(f"📁 图片目录: {IMAGES_DIR}")
    print(f"📁 音频目录: {AUDIO_DIR}\n")
    
    words = get_vocabulary_words()
    progress = load_progress()
    
    # 分成批次处理，每30个单词提交一次
    batch_size = 30
    total_batches = (len(words) + batch_size - 1) // batch_size
    
    print(f"📊 总共 {len(words)} 个单词，分为 {total_batches} 个批次\n")
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, len(words))
        batch_words = words[start_idx:end_idx]
        
        print(f"{'='*60}")
        print(f"📦 第 {batch_num + 1}/{total_batches} 批处理 ({len(batch_words)} 个单词)")
        print(f"{'='*60}\n")
        
        batch_images_success = 0
        batch_audio_success = 0
        
        for i, word in enumerate(batch_words):
            print(f"[{i+1}/{len(batch_words)}] 处理: {word}")
            
            # 下载图片
            print(f"   🖼️  下载图片...", end="", flush=True)
            success, msg = download_image(word, progress)
            if success:
                batch_images_success += 1
                print(f" ✅ {msg}")
            else:
                print(f" ❌ {msg}")
            
            # 下载音频
            print(f"   🔊 下载音频...", end="", flush=True)
            success, msg = download_audio(word, progress)
            if success:
                batch_audio_success += 1
                print(f" ✅ {msg}")
            else:
                print(f" ❌ {msg}")
            
            save_progress(progress)
            
            # 间隔
            time.sleep(2)
        
        print(f"\n{'='*60}")
        print(f"📊 第 {batch_num + 1} 批完成:")
        print(f"   🖼️  图片: {batch_images_success}/{len(batch_words)}")
        print(f"   🔊 音频: {batch_audio_success}/{len(batch_words)}")
        print(f"{'='*60}\n")
        
        # 提交这一批
        if batch_images_success > 0 or batch_audio_success > 0:
            git_commit(f"下载资源 - 第 {batch_num + 1}/{total_batches} 批 (图片: {len(progress['downloaded_images'])}，音频: {len(progress['downloaded_audio'])})")
        else:
            print("⚠️  这一批没有下载成功任何资源，继续下一批\n")
    
    print("✨ 所有批次处理完成！")
    print(f"📊 总计:")
    print(f"   🖼️  图片: {len(progress['downloaded_images'])}")
    print(f"   🔊 音频: {len(progress['downloaded_audio'])}")

if __name__ == '__main__':
    main()
