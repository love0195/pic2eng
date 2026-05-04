#!/usr/bin/env python3
"""
使用requests模拟真实浏览器访问Bing图片搜索
基于更好的会话维持和header模拟
"""
import urllib.request
import urllib.parse
import time
import json
import re
import ssl
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# 配置
BASE_DIR = Path('/workspace/word-app')
IMAGES_DIR = BASE_DIR / 'public' / 'images'
LINKS_FILE = BASE_DIR / 'docs' / 'bing_image_results.json'

# 人体相关词汇
body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

# 完整的浏览器headers（模拟Chrome）
COMPREHENSIVE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.91',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
}

class BrowserSimulator:
    def __init__(self):
        self.session = None
        self.cookies = {}
        
    def create_session(self):
        """创建会话"""
        # 创建SSL上下文
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # 创建opener
        self.session = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ssl_context),
            urllib.request.HTTPCookieProcessor()
        )
        
        # 添加headers
        self.session.addheaders = [(k, v) for k, v in COMPREHENSIVE_HEADERS.items()]
        
        return self.session
    
    def search_bing_images(self, keyword: str, limit: int = 10) -> List[Dict]:
        """搜索Bing图片"""
        print(f"\n🔍 Bing图片搜索: {keyword}")
        
        if not self.session:
            self.create_session()
        
        # 构建搜索URL
        query = f"{keyword} cartoon illustration educational"
        search_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&first=0"
        
        print(f"  📡 请求: {search_url}")
        
        try:
            response = self.session.open(search_url, timeout=30)
            html = response.read().decode('utf-8', errors='ignore')
            
            print(f"  📄 响应大小: {len(html)} bytes")
            
            # 提取图片URL
            image_urls = self.extract_bing_image_urls(html)
            
            print(f"  ✅ 找到 {len(image_urls)} 个图片")
            
            return image_urls[:limit]
            
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            return []
    
    def extract_bing_image_urls(self, html: str) -> List[Dict]:
        """从HTML中提取Bing图片URL"""
        images = []
        
        # 方法1: 提取JSON数据中的URL
        json_patterns = [
            r'"murl":"([^"]+\.(?:jpg|jpeg|png))"',
            r'"turl":"([^"]+\.(?:jpg|jpeg|png))"',
            r'"mid":"([^"]+\.(?:jpg|jpeg|png))"',
            r'"m":"({[^}]+})"',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                if isinstance(match, str) and self.is_valid_image_url(match):
                    images.append({
                        'url': match,
                        'type': 'direct'
                    })
        
        # 方法2: 提取data-src
        data_src_pattern = r'data-src="([^"]+\.(?:jpg|jpeg|png))"'
        matches = re.findall(data_src_pattern, html, re.IGNORECASE)
        for match in matches:
            if self.is_valid_image_url(match):
                images.append({
                    'url': match,
                    'type': 'data-src'
                })
        
        # 方法3: 提取img src
        img_src_pattern = r'<img[^>]+src="([^"]+\.(?:jpg|jpeg|png))"[^>]*>'
        matches = re.findall(img_src_pattern, html, re.IGNORECASE)
        for match in matches:
            if self.is_valid_image_url(match):
                images.append({
                    'url': match,
                    'type': 'img-src'
                })
        
        # 去重
        seen = set()
        unique_images = []
        for img in images:
            if img['url'] not in seen:
                seen.add(img['url'])
                unique_images.append(img)
        
        return unique_images
    
    def is_valid_image_url(self, url: str) -> bool:
        """验证URL是否有效"""
        if not url:
            return False
        
        # 排除小图标
        invalid_patterns = ['icon', 'logo', 'avatar', 'placeholder', 'data:image', 'base64']
        for pattern in invalid_patterns:
            if pattern in url.lower():
                return False
        
        # 必须包含图片扩展名
        extensions = ['.jpg', '.jpeg', '.png', '.gif']
        if not any(ext in url.lower() for ext in extensions):
            return False
        
        return True
    
    def download_image(self, url: str, timeout: int = 30) -> Optional[bytes]:
        """下载图片"""
        try:
            req = urllib.request.Request(url, headers=COMPREHENSIVE_HEADERS)
            with self.session.open(req, timeout=timeout) as response:
                return response.read()
        except Exception as e:
            print(f"  ❌ 下载失败: {e}")
            return None
    
    def validate_image(self, content: bytes) -> bool:
        """验证图片"""
        if len(content) < 5000:  # 小于5KB可能是无效图片
            return False
        
        # 检查文件头
        valid_signatures = [
            b'\xff\xd8\xff',  # JPEG
            b'\x89PNG\r\n\x1a\n',  # PNG
            b'GIF87a',  # GIF
            b'GIF89a',  # GIF
        ]
        
        for sig in valid_signatures:
            if content.startswith(sig):
                return True
        
        return False

def main():
    print("=" * 70)
    print("🎯 Bing图片搜索爬虫")
    print("=" * 70)
    print(f"目标: {len(body_words)} 个人体相关词汇")
    print("=" * 70)
    
    # 创建爬虫
    crawler = BrowserSimulator()
    
    # 创建会话
    crawler.create_session()
    
    # 先访问Bing首页建立会话
    print("\n🌐 建立Bing会话...")
    try:
        crawler.session.open("https://www.bing.com", timeout=30)
        print("  ✅ 会话建立成功")
        time.sleep(2)
    except Exception as e:
        print(f"  ⚠️ 会话建立失败: {e}")
    
    # 搜索并下载
    results = {}
    success_count = 0
    
    for i, word in enumerate(body_words, 1):
        print(f"\n\n{'#'*70}")
        print(f"# [{i}/{len(body_words)}] 搜索: {word}")
        print('#'*70)
        
        # 搜索图片
        images = crawler.search_bing_images(word, limit=5)
        
        result = {
            'word': word,
            'images_found': len(images),
            'images': images,
            'success': False
        }
        
        if images:
            # 尝试下载第一张图片
            for img in images:
                print(f"\n  📥 尝试下载: {img['url'][:60]}...")
                
                content = crawler.download_image(img['url'])
                if content and crawler.validate_image(content):
                    # 保存图片
                    img_path = IMAGES_DIR / f"{word}.jpg"
                    
                    # 备份原图
                    if img_path.exists():
                        backup_path = IMAGES_DIR / f"{word}_bing_bak.jpg"
                        img_path.rename(backup_path)
                    
                    with open(img_path, 'wb') as f:
                        f.write(content)
                    
                    print(f"  ✅ 已保存: {img_path.name} ({len(content)} bytes)")
                    result['success'] = True
                    result['saved_size'] = len(content)
                    success_count += 1
                    break
                else:
                    print(f"  ⚠️ 图片无效或下载失败")
        
        results[word] = result
        
        # 保存进度
        with open(LINKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 当前进度: {success_count}/{i} 成功")
        
        # 避免请求过快
        time.sleep(3)
    
    # 最终统计
    print("\n" + "=" * 70)
    print("🎉 处理完成!")
    print("=" * 70)
    print(f"成功: {success_count}/{len(body_words)}")
    print(f"结果已保存到: {LINKS_FILE}")
    print("=" * 70)

if __name__ == "__main__":
    main()
