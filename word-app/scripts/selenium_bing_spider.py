#!/usr/bin/env python3
"""
使用Selenium实现Bing图片爬虫
参考：https://github.com/CatchZeng/bing_images
"""
import time
import json
import urllib.request
import urllib.parse
from pathlib import Path
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 配置
BASE_DIR = Path('/workspace/word-app')
IMAGES_DIR = BASE_DIR / 'public' / 'images'
LINKS_FILE = BASE_DIR / 'docs' / 'selenium_bing_results.json'

# 人体相关词汇
body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

class BingImageSpider:
    def __init__(self):
        self.driver = None
        
    def init_driver(self):
        """初始化Chrome浏览器"""
        print("🚀 初始化Chrome浏览器...")
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            print("  ✅ Chrome浏览器初始化成功")
            return True
        except Exception as e:
            print(f"  ❌ Chrome初始化失败: {e}")
            return False
    
    def search_images(self, keyword: str, max_images: int = 10) -> List[str]:
        """搜索Bing图片"""
        print(f"\n🔍 搜索: {keyword}")
        
        query = f"{keyword} cartoon illustration educational simple"
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&first=1"
        
        print(f"  📡 打开: {url}")
        
        try:
            self.driver.get(url)
            
            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "iusc"))
            )
            
            # 滚动加载更多图片
            image_urls = []
            scroll_count = 0
            max_scrolls = 3
            
            while len(image_urls) < max_images and scroll_count < max_scrolls:
                # 获取图片元素
                image_elements = self.driver.find_elements(By.CLASS_NAME, "iusc")
                print(f"  📸 找到 {len(image_elements)} 个图片元素")
                
                for elem in image_elements:
                    try:
                        m_attr = elem.get_attribute("m")
                        if m_attr:
                            m_json = json.loads(m_attr)
                            img_url = m_json.get("murl", "")
                            if img_url and img_url not in image_urls:
                                image_urls.append(img_url)
                    except Exception:
                        continue
                
                if len(image_urls) >= max_images:
                    break
                
                # 滚动加载更多
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                scroll_count += 1
            
            print(f"  ✅ 提取到 {len(image_urls)} 个图片URL")
            return image_urls[:max_images]
            
        except Exception as e:
            print(f"  ❌ 搜索失败: {e}")
            return []
    
    def download_image(self, url: str, save_path: Path) -> bool:
        """下载图片"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.bing.com/'
            }
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read()
            
            # 验证图片
            if len(content) < 5000:
                return False
            
            # 检查文件头
            valid_signatures = [b'\xff\xd8\xff', b'\x89PNG', b'GIF8']
            is_valid = any(content.startswith(sig) for sig in valid_signatures)
            
            if not is_valid:
                return False
            
            # 保存图片
            with open(save_path, 'wb') as f:
                f.write(content)
            
            print(f"  ✅ 已保存: {save_path.name} ({len(content)} bytes)")
            return True
            
        except Exception as e:
            print(f"  ❌ 下载失败: {e}")
            return False
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()

def main():
    print("=" * 70)
    print("🎯 Selenium Bing图片爬虫")
    print("=" * 70)
    print(f"目标: {len(body_words)} 个人体相关词汇")
    print("=" * 70)
    
    spider = BingImageSpider()
    
    if not spider.init_driver():
        print("❌ 无法初始化浏览器，退出")
        return
    
    results = {}
    success_count = 0
    
    try:
        for i, word in enumerate(body_words, 1):
            print(f"\n\n{'#'*70}")
            print(f"# [{i}/{len(body_words)}] 处理: {word}")
            print('#'*70)
            
            result = {
                'word': word,
                'success': False,
                'urls': [],
                'saved_size': 0
            }
            
            # 搜索图片
            image_urls = spider.search_images(word, max_images=5)
            result['urls'] = image_urls
            
            if image_urls:
                # 尝试下载第一张有效图片
                for img_url in image_urls:
                    print(f"  📥 尝试下载: {img_url[:60]}...")
                    
                    # 备份原图
                    img_path = IMAGES_DIR / f"{word}.jpg"
                    if img_path.exists():
                        backup_path = IMAGES_DIR / f"{word}_sel_bak.jpg"
                        img_path.rename(backup_path)
                    
                    if spider.download_image(img_url, img_path):
                        result['success'] = True
                        result['saved_size'] = img_path.stat().st_size
                        success_count += 1
                        break
            else:
                print(f"  ⚠️ 没有找到图片")
            
            results[word] = result
            
            # 保存进度
            with open(LINKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n📊 当前进度: {success_count}/{i} 成功")
            
            # 避免请求过快
            time.sleep(2)
    
    finally:
        spider.close()
    
    # 最终统计
    print("\n" + "=" * 70)
    print("🎉 处理完成!")
    print("=" * 70)
    print(f"成功: {success_count}/{len(body_words)}")
    print(f"结果已保存到: {LINKS_FILE}")
    print("=" * 70)

if __name__ == "__main__":
    main()
