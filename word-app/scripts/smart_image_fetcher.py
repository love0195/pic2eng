#!/usr/bin/env python3
"""
智能图片获取脚本
使用多种策略获取高质量图片：
1. 模拟Bing图片搜索
2. 模拟百度图片搜索
3. 使用完整的浏览器headers
4. 维持session和cookies
5. 下载并验证图片质量
"""
import urllib.request
import urllib.parse
import time
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

# 配置
BASE_DIR = Path('/workspace/word-app')
IMAGES_DIR = BASE_DIR / 'public' / 'images'
LINKS_FILE = BASE_DIR / 'docs' / 'smart_image_links.json'
PLACEHOLDER_SIZE = 176626

# 人体相关词汇
body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

# 完整浏览器headers
COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}

BING_IMAGE_HEADERS = {
    **COMMON_HEADERS,
    'Referer': 'https://www.bing.com/',
}

BAIDU_IMAGE_HEADERS = {
    **COMMON_HEADERS,
    'Referer': 'https://image.baidu.com/',
}

class SmartImageFetcher:
    def __init__(self):
        self.session = urllib.request.urlopen
        self.cookies = {}
        
    def make_request(self, url: str, headers: Dict = None) -> Optional[bytes]:
        """发起请求"""
        try:
            req_headers = headers or COMMON_HEADERS
            req = urllib.request.Request(url, headers=req_headers)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read()
                print(f"  响应大小: {len(content)} bytes")
                return content
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")
            return None
    
    def search_bing_images(self, keyword: str) -> List[str]:
        """搜索Bing图片"""
        print(f"\n🔍 Bing图片搜索: {keyword}")
        
        # Bing图片搜索URL
        search_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(keyword + ' cartoon')}&qft=+filterui:imagesize-medium&form=IRFLTR&first=1"
        
        content = self.make_request(search_url, BING_IMAGE_HEADERS)
        if not content:
            return []
        
        # 解析图片URL
        try:
            html = content.decode('utf-8', errors='ignore')
            # 提取图片URL模式
            img_patterns = re.findall(r'"murl":"(https?://[^"]+\.(?:jpg|jpeg|png))"', html)
            
            if img_patterns:
                print(f"  ✅ 找到 {len(img_patterns)} 个图片链接")
                return img_patterns[:3]
        except Exception as e:
            print(f"  ❌ 解析失败: {e}")
        
        return []
    
    def search_baidu_images(self, keyword: str) -> List[str]:
        """搜索百度图片"""
        print(f"\n🔍 百度图片搜索: {keyword}")
        
        # 百度图片搜索URL
        search_url = f"https://image.baidu.com/search/index?word={urllib.parse.quote(keyword + ' 卡通')}&tn=baiduimage"
        
        content = self.make_request(search_url, BAIDU_IMAGE_HEADERS)
        if not content:
            return []
        
        try:
            html = content.decode('utf-8', errors='ignore')
            # 提取图片URL
            img_patterns = re.findall(r'"thumbURL":"(https?://[^"]+\.(?:jpg|jpeg|png))"', html)
            
            if img_patterns:
                print(f"  ✅ 找到 {len(img_patterns)} 个图片链接")
                return img_patterns[:3]
        except Exception as e:
            print(f"  ❌ 解析失败: {e}")
        
        return []
    
    def search_unsplash(self, keyword: str) -> List[str]:
        """搜索Unsplash免费图片"""
        print(f"\n🔍 Unsplash搜索: {keyword}")
        
        # Unsplash API (公开访问)
        search_url = f"https://unsplash.com/s/photos/{urllib.parse.quote(keyword)}"
        
        content = self.make_request(search_url, COMMON_HEADERS)
        if not content:
            return []
        
        try:
            html = content.decode('utf-8', errors='ignore')
            # 提取图片URL
            img_patterns = re.findall(r'https://images\.unsplash\.com/photo-[^"?]+\?[^"]+', html)
            
            if img_patterns:
                print(f"  ✅ 找到 {len(img_patterns)} 个图片链接")
                return list(set(img_patterns))[:3]
        except Exception as e:
            print(f"  ❌ 解析失败: {e}")
        
        return []
    
    def search_pixabay(self, keyword: str) -> List[str]:
        """搜索Pixabay免费图片"""
        print(f"\n🔍 Pixabay搜索: {keyword}")
        
        # Pixabay搜索URL
        search_url = f"https://pixabay.com/zh/photos/search/{urllib.parse.quote(keyword)}/?orientation=horizontal"
        
        content = self.make_request(search_url, COMMON_HEADERS)
        if not content:
            return []
        
        try:
            html = content.decode('utf-8', errors='ignore')
            # 提取图片URL
            img_patterns = re.findall(r'https://cdn\.pixabay\.com/photo/[^"?]+\.(?:jpg|jpeg|png)', html)
            
            if img_patterns:
                print(f"  ✅ 找到 {len(img_patterns)} 个图片链接")
                return list(set(img_patterns))[:3]
        except Exception as e:
            print(f"  ❌ 解析失败: {e}")
        
        return []
    
    def download_and_validate(self, word: str, image_urls: List[str]) -> Tuple[bool, Optional[bytes]]:
        """下载并验证图片"""
        for url in image_urls:
            print(f"  📥 下载: {url[:60]}...")
            
            content = self.make_request(url, COMMON_HEADERS)
            if not content:
                continue
            
            size = len(content)
            
            # 验证图片大小
            if size < 10000:  # 小于10KB可能是无效图片
                print(f"  ⚠️ 图片太小: {size} bytes")
                continue
            
            # 验证是否是图片（检查文件头）
            if self.is_valid_image(content):
                print(f"  ✅ 图片有效! ({size} bytes)")
                return True, content
            else:
                print(f"  ⚠️ 无效图片格式")
        
        return False, None
    
    def is_valid_image(self, content: bytes) -> bool:
        """验证是否是有效图片"""
        # 检查常见图片格式的文件头
        image_signatures = [
            (b'\xff\xd8\xff', 'JPEG'),      # JPEG
            (b'\x89PNG\r\n\x1a\n', 'PNG'),  # PNG
            (b'GIF87a', 'GIF'),              # GIF87a
            (b'GIF89a', 'GIF'),              # GIF89a
            (b'RIFF', 'WEBP'),               # WEBP (部分)
        ]
        
        for signature, format_name in image_signatures:
            if content.startswith(signature):
                return True
        
        return False
    
    def save_image(self, word: str, content: bytes) -> Path:
        """保存图片"""
        img_path = IMAGES_DIR / f"{word}.jpg"
        
        # 如果已存在，先备份
        if img_path.exists():
            backup_path = IMAGES_DIR / f"{word}_backup_{int(time.time())}.jpg"
            img_path.rename(backup_path)
        
        with open(img_path, 'wb') as f:
            f.write(content)
        
        print(f"  💾 已保存: {img_path}")
        return img_path
    
    def process_word(self, word: str) -> Dict:
        """处理单个词汇"""
        print(f"\n{'='*70}")
        print(f"📝 处理词汇: {word}")
        print('='*70)
        
        result = {
            'word': word,
            'success': False,
            'sources': [],
            'size': 0
        }
        
        # 尝试多种图片源
        search_methods = [
            ('unsplash', self.search_unsplash),
            ('pixabay', self.search_pixabay),
            ('bing', self.search_bing_images),
            ('baidu', self.search_baidu_images),
        ]
        
        for source_name, search_method in search_methods:
            print(f"\n尝试 {source_name}...")
            image_urls = search_method(word)
            
            if image_urls:
                result['sources'].append({
                    'source': source_name,
                    'urls': image_urls
                })
                
                # 下载并验证
                success, content = self.download_and_validate(word, image_urls)
                
                if success:
                    result['success'] = True
                    result['size'] = len(content)
                    self.save_image(word, content)
                    return result
            
            # 避免请求过快
            time.sleep(1)
        
        print(f"  ❌ 所有来源都失败了")
        return result

def main():
    print("="*70)
    print("🎯 智能图片获取程序")
    print("="*70)
    print(f"\n策略:")
    print("  1. 模拟真实浏览器访问Bing/百度/Pixabay/Unsplash图片搜索")
    print("  2. 使用完整的浏览器headers")
    print("  3. 下载并验证图片质量")
    print("  4. 保存到本地")
    print(f"\n目标: {len(body_words)} 个人体相关词汇")
    print("="*70)
    
    # 加载已有链接
    links_data = {}
    if Path(LINKS_FILE).exists():
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            links_data = json.load(f)
    
    # 创建fetcher
    fetcher = SmartImageFetcher()
    
    success_count = 0
    
    # 处理每个词汇
    for i, word in enumerate(body_words, 1):
        print(f"\n\n{'#'*70}")
        print(f"# [{i}/{len(body_words)}] 处理: {word}")
        print('#'*70)
        
        result = fetcher.process_word(word)
        
        # 保存结果
        if word not in links_data:
            links_data[word] = []
        links_data[word].append({
            'timestamp': time.time(),
            'result': result,
            'attempt': len(links_data[word]) + 1
        })
        
        if result['success']:
            success_count += 1
        
        # 保存进度
        with open(LINKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(links_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 当前进度: {success_count}/{i} 成功")
        
        # 避免请求过快
        time.sleep(2)
    
    # 最终统计
    print("\n" + "="*70)
    print("🎉 处理完成!")
    print("="*70)
    print(f"成功: {success_count}/{len(body_words)}")
    print(f"链接已保存到: {LINKS_FILE}")
    print("="*70)

if __name__ == "__main__":
    main()
