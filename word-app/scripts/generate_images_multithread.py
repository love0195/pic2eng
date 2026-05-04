import urllib.request
import urllib.parse
import json
import time
import os
import threading
from queue import Queue

vocabulary = {
    'furniture': ['sofa', 'table', 'chair', 'bed', 'desk', 'bookshelf', 'wardrobe', 'lamp', 'cabinet', 'stool', 'cupboard', 'drawer'],
    'appliances': ['refrigerator', 'television', 'washing', 'microwave', 'oven', 'dishwasher', 'airconditioner', 'computer', 'fan', 'heater', 'coffee', 'toaster'],
    'vehicles': ['car', 'bus', 'train', 'plane', 'bicycle', 'motorcycle', 'ship', 'boat', 'taxi', 'subway', 'truck', 'helicopter'],
    'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'parrot', 'turtle', 'snake', 'elephant', 'monkey', 'panda'],
    'fruits': ['apple', 'banana', 'orange', 'grape', 'watermelon', 'strawberry', 'pineapple', 'mango', 'peach', 'pear', 'lemon', 'cherry']
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

FAKE_SIZE = 176626
MAX_WAIT_PER_IMAGE = 60
CHECK_INTERVAL = 5

class ImageGenerator:
    def __init__(self):
        self.tasks = []
        self.results = {}
        self.lock = threading.Lock()
    
    def create_task(self, word, category):
        prompt = f"A simple cartoon illustration of a {word} on white background, clean design, single object"
        encoded_prompt = urllib.parse.quote(prompt)
        
        task = {
            'word': word,
            'category': category,
            'prompt': prompt,
            'url': f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={word}_{int(time.time()*1000)}",
            'filepath': os.path.join(save_dir, f"{word}.png"),
            'status': 'pending',
            'url_type': None
        }
        self.tasks.append(task)
        return task
    
    def submit_task(self, task):
        try:
            req = urllib.request.Request(task['url'], headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json, */*'
            })
            
            response = urllib.request.urlopen(req, timeout=30)
            content = response.read()
            content_type = response.headers.get('Content-Type', '')
            
            if len(content) == FAKE_SIZE:
                if 'image' in content_type or 'png' in content_type:
                    print(f"⚠️  {task['word']}: 返回占位图")
                else:
                    try:
                        json_data = json.loads(content.decode('utf-8'))
                        if 'task_id' in json_data:
                            task['status'] = 'processing'
                            task['task_id'] = json_data['task_id']
                            print(f"📝 {task['word']}: 任务已提交 (ID: {json_data['task_id']})")
                            return
                    except:
                        pass
                    
                    if 'image' in json_data:
                        img_data = json_data['image']
                        if isinstance(img_data, str):
                            if img_data.startswith('data:'):
                                img_data = img_data.split(',')[1]
                            try:
                                import base64
                                decoded = base64.b64decode(img_data)
                                if len(decoded) > 5000:
                                    with open(task['filepath'], 'wb') as f:
                                        f.write(decoded)
                                    task['status'] = 'completed'
                                    print(f"✅ {task['word']}: 直接返回图片")
                                    return
                            except:
                                pass
            
            with open(task['filepath'], 'wb') as f:
                f.write(content)
            task['status'] = 'completed'
            print(f"✅ {task['word']}: 保存成功")
            
        except Exception as e:
            print(f"❌ {task['word']}: 提交失败 - {e}")
            task['status'] = 'failed'
    
    def check_and_download(self, task):
        if task['status'] != 'processing' or 'task_id' not in task:
            return
        
        try:
            status_url = f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image/status?task_id={task['task_id']}"
            req = urllib.request.Request(status_url, headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json, */*'
            })
            
            response = urllib.request.urlopen(req, timeout=10)
            content = response.read()
            
            if len(content) == FAKE_SIZE:
                print(f"⏳ {task['word']}: 仍在生成中...")
                return False
            
            try:
                json_data = json.loads(content.decode('utf-8'))
                
                if json_data.get('status') == 'completed':
                    img_url = json_data.get('image_url')
                    if img_url:
                        img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(img_req, timeout=30) as img_response:
                            img_content = img_response.read()
                            if len(img_content) > 5000:
                                with open(task['filepath'], 'wb') as f:
                                    f.write(img_content)
                                task['status'] = 'completed'
                                print(f"✅ {task['word']}: 图片已生成并保存")
                                return True
                elif json_data.get('status') == 'failed':
                    task['status'] = 'failed'
                    print(f"❌ {task['word']}: 生成失败")
                    return True
                    
            except json.JSONDecodeError:
                with open(task['filepath'], 'wb') as f:
                    f.write(content)
                task['status'] = 'completed'
                print(f"✅ {task['word']}: 图片已生成并保存")
                return True
                
        except Exception as e:
            print(f"⚠️  {task['word']}: 检查失败 - {e}")
        
        return False
    
    def wait_for_completion(self):
        print("\n" + "=" * 70)
        print("等待图片生成完成...")
        print("=" * 70)
        
        start_time = time.time()
        max_wait = 300
        
        while True:
            pending_tasks = [t for t in self.tasks if t['status'] == 'processing']
            
            if not pending_tasks:
                completed = len([t for t in self.tasks if t['status'] == 'completed'])
                print(f"\n✅ 所有任务已完成: {completed}/{len(self.tasks)}")
                break
            
            if time.time() - start_time > max_wait:
                print(f"\n⚠️  等待超时")
                break
            
            print(f"\n⏳ 剩余 {len(pending_tasks)} 个任务待完成...")
            
            for task in pending_tasks:
                if self.check_and_download(task):
                    pass
            
            time.sleep(CHECK_INTERVAL)
        
        completed = len([t for t in self.tasks if t['status'] == 'completed'])
        print(f"\n完成统计: {completed}/{len(self.tasks)} 张图片")
    
    def run(self):
        print("=" * 70)
        print("第一阶段: 提交所有图片生成任务")
        print("=" * 70)
        
        for category, words in vocabulary.items():
            print(f"\n📂 分类: {category}")
            for word in words:
                task = self.create_task(word, category)
                self.submit_task(task)
                time.sleep(0.3)
        
        self.wait_for_completion()

if __name__ == '__main__':
    generator = ImageGenerator()
    generator.run()
