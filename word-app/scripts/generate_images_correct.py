import urllib.request
import urllib.parse
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

vocabulary = {
    'furniture': ['sofa', 'table', 'chair', 'bed', 'desk', 'bookshelf', 'wardrobe', 'lamp', 'cabinet', 'stool', 'cupboard', 'drawer'],
    'appliances': ['refrigerator', 'television', 'washing', 'microwave', 'oven', 'dishwasher', 'airconditioner', 'computer', 'fan', 'heater', 'coffee', 'toaster'],
    'vehicles': ['car', 'bus', 'train', 'plane', 'bicycle', 'motorcycle', 'ship', 'boat', 'taxi', 'subway', 'truck', 'helicopter'],
    'animals': ['dog', 'cat', 'bird', 'fish', 'rabbit', 'hamster', 'parrot', 'turtle', 'snake', 'elephant', 'monkey', 'panda'],
    'fruits': ['apple', 'banana', 'orange', 'grape', 'watermelon', 'strawberry', 'pineapple', 'mango', 'peach', 'pear', 'lemon', 'cherry']
}

save_dir = '/workspace/word-app/public/images'
os.makedirs(save_dir, exist_ok=True)

PLACEHOLDER_SIZE = 176626
MAX_WAIT_ROUNDS = 20
CHECK_INTERVAL = 5

class ImageDownloader:
    def __init__(self):
        self.tasks = []
    
    def dispatch_all_tasks(self):
        print("=" * 70)
        print("第一阶段: 派发所有图片生成任务")
        print("=" * 70)
        
        for category, words in vocabulary.items():
            print(f"\n📂 分类: {category}")
            for word in words:
                task = self.create_task(word, category)
                print(f"📝 {task['word']}: 任务已提交")
                time.sleep(0.2)
        
        print(f"\n✅ 任务派发完成: {len(self.tasks)} 个任务")
    
    def create_task(self, word, category):
        prompt = f"A simple cartoon illustration of a {word} on white background, clean design, single object"
        encoded_prompt = urllib.parse.quote(prompt)
        
        task = {
            'word': word,
            'category': category,
            'url': f"https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt={encoded_prompt}&image_size=square&session_id={word}_{int(time.time()*1000)}",
            'filepath': os.path.join(save_dir, f"{word}.png"),
            'status': 'pending',
            'size': 0
        }
        self.tasks.append(task)
        return task
    
    def download_image(self, task):
        try:
            req = urllib.request.Request(task['url'], headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read()
                task['size'] = len(content)
                
                with open(task['filepath'], 'wb') as f:
                    f.write(content)
                
                if task['size'] == PLACEHOLDER_SIZE:
                    task['status'] = 'placeholder'
                    return False
                else:
                    task['status'] = 'done'
                    return True
            
        except Exception as e:
            task['status'] = 'error'
            return False
    
    def wait_for_real_images(self):
        print("\n" + "=" * 70)
        print("第二阶段: 等待图片生成完成")
        print("=" * 70)
        
        placeholder_count = len([t for t in self.tasks if t['status'] == 'placeholder'])
        print(f"\n📊 初始状态: {placeholder_count} 个占位图待处理")
        
        for round_num in range(MAX_WAIT_ROUNDS):
            pending_tasks = [t for t in self.tasks if t['status'] == 'placeholder']
            
            if not pending_tasks:
                print(f"\n✅ 所有图片已生成完成！")
                return True
            
            print(f"\n⏳ 第 {round_num + 1} 轮检查: {len(pending_tasks)} 个图片待刷新...")
            print(f"   等待 {CHECK_INTERVAL} 秒...")
            time.sleep(CHECK_INTERVAL)
            
            success_count = 0
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(self.download_image, task) for task in pending_tasks]
                
                for i, future in enumerate(as_completed(futures)):
                    task = pending_tasks[i]
                    if future.result():
                        success_count += 1
                        print(f"   ✅ {task['word']}: 图片已就绪 ({task['size']} bytes)")
                    else:
                        print(f"   ⏳ {task['word']}: 仍在生成中 ({task['size']} bytes)")
            
            print(f"   本轮完成: {success_count}/{len(pending_tasks)}")
        
        return False
    
    def run(self):
        self.dispatch_all_tasks()
        
        print("\n" + "=" * 70)
        print("第一轮下载: 获取所有初始图片")
        print("=" * 70)
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.download_image, task) for task in self.tasks]
            
            for i, future in enumerate(as_completed(futures)):
                task = self.tasks[i]
                status_icon = "✅" if future.result() else "⏳"
                print(f"   {status_icon} {task['word']}: {task['size']} bytes")
        
        if self.wait_for_real_images():
            print("\n" + "=" * 70)
            completed = len([t for t in self.tasks if t['status'] == 'done'])
            print(f"最终统计: {completed}/{len(self.tasks)} 张真实图片")
            print(f"保存位置: {save_dir}")
            print("=" * 70)
        else:
            print("\n⚠️  部分图片可能仍是占位图，请手动检查")

if __name__ == '__main__':
    downloader = ImageDownloader()
    downloader.run()
