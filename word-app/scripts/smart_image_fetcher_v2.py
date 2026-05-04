#!/usr/bin/env python3
"""
智能图片获取脚本 v2
改进版：
1. 优化Bing/百度图片搜索的正则表达式
2. 添加更多免费图片源
3. 改进图片验证逻辑
4. 更好的错误处理
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
LINKS_FILE = BASE_DIR / 'docs' / 'smart_image_links_v2.json'
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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

BING_HEADERS = {
    **COMMON_HEADERS,
    'Referer': 'https://www.bing.com/',
}

BAIDU_HEADERS = {
    **COMMON_HEADERS,
    'Referer': 'https://image.baidu.com/',
    'Cookie': 'BAIDUID=test; BIDUPSID=test; PSTM=1234567890',
}

class SmartImageFetcherV2:
    def __init__(self):
        self.cookies = {}
        
    def make_request(self, url: str, headers: Dict = None) -> Optional[bytes]:
        """发起请求"""
        try:
            req_headers = headers or COMMON_HEADERS
            req = urllib.request.Request(url, headers=req_headers)
            
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read()
                return content
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")
            return None
    
    def extract_bing_images(self, html: str) -> List[str]:
        """从Bing页面提取图片"""
        urls = []
        
        # 多种正则表达式模式
        patterns = [
            r'"murl":"(https?://[^"]+\.(?:jpg|jpeg|png))"',
            r'"turl":"(https?://[^"]+\.(?:jpg|jpeg|png))"',
            r'"mid":"(https?://[^"]+\.(?:jpg|jpeg|png))"',
            r'data-src="(https?://[^"]+\.(?:jpg|jpeg|png))"',
            r'img src="(https?://[^"]+\.(?:jpg|jpeg|png))"',
            r'"src":"(https?://[^"]+\.(?:jpg|jpeg|png))"',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            urls.extend(matches)
        
        # 去重
        urls = list(dict.fromkeys(urls))
        
        # 过滤掉小图片和无效URL
        urls = [u for u in urls if self.is_valid_url(u)]
        
        return urls[:5]
    
    def extract_baidu_images(self, html: str) -> List[str]:
        """从百度页面提取图片"""
        urls = []
        
        patterns = [
            r'"thumbURL":"(https?://[^"]+\.(?:jpg|jpeg|png))"',
            r'"middleURL":"(https?://[^"]+\.(?:jpg|jpeg|png))"',
            r'"hoverURL":"(https?://[^"]+\.(?:jpg|jpeg|png))"',
            r'"objURL":"(https?://[^"]+\.(?:jpg|jpeg|png))"',
            r'data-src="(https?://[^"]+\.(?:jpg|jpeg|png))"',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            urls.extend(matches)
        
        # 去重
        urls = list(dict.fromkeys(urls))
        
        # 过滤
        urls = [u for u in urls if self.is_valid_url(u)]
        
        return urls[:5]
    
    def is_valid_url(self, url: str) -> bool:
        """验证URL是否有效"""
        if not url:
            return False
        
        # 排除小图标和无效链接
        invalid_patterns = ['icon', 'logo', 'avatar', 'placeholder', 'data:image']
        for pattern in invalid_patterns:
            if pattern in url.lower():
                return False
        
        # 必须包含图片扩展名
        if not any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            return False
        
        return True
    
    def search_bing_images(self, keyword: str) -> List[str]:
        """搜索Bing图片"""
        print(f"\n🔍 Bing图片搜索: {keyword}")
        
        # 尝试不同的Bing搜索URL
        search_urls = [
            f"https://www.bing.com/images/search?q={urllib.parse.quote(keyword + ' cartoon educational')}&first=1",
            f"https://www.bing.com/images/search?q={urllib.parse.quote(keyword + ' simple illustration')}&qft=+filterui:imagesize-medium",
            f"https://cn.bing.com/images/search?q={urllib.parse.quote(keyword + ' 卡通')}&first=1",
        ]
        
        for search_url in search_urls:
            print(f"  尝试: {search_url[:70]}...")
            content = self.make_request(search_url, BING_HEADERS)
            
            if not content:
                continue
            
            try:
                html = content.decode('utf-8', errors='ignore')
                urls = self.extract_bing_images(html)
                
                if urls:
                    print(f"  ✅ 找到 {len(urls)} 个图片")
                    return urls
            except Exception as e:
                print(f"  ❌ 解析失败: {e}")
        
        return []
    
    def search_baidu_images(self, keyword: str) -> List[str]:
        """搜索百度图片"""
        print(f"\n🔍 百度图片搜索: {keyword}")
        
        # 尝试不同的百度搜索URL
        search_urls = [
            f"https://image.baidu.com/search/index?word={urllib.parse.quote(keyword + ' 卡通 教育')}&tn=baiduimage",
            f"https://image.baidu.com/search/index?word={urllib.parse.quote(keyword)}&tn=baiduimage&ipn=r",
            f"https://image.baidu.com/search/flip?word={urllib.parse.quote(keyword + ' 简笔画')}",
        ]
        
        for search_url in search_urls:
            print(f"  尝试: {search_url[:70]}...")
            content = self.make_request(search_url, BAIDU_HEADERS)
            
            if not content:
                continue
            
            try:
                html = content.decode('utf-8', errors='ignore')
                urls = self.extract_baidu_images(html)
                
                if urls:
                    print(f"  ✅ 找到 {len(urls)} 个图片")
                    return urls
            except Exception as e:
                print(f"  ❌ 解析失败: {e}")
        
        return []
    
    def search_wikimedia(self, keyword: str) -> List[str]:
        """搜索Wikimedia Commons免费图片"""
        print(f"\n🔍 Wikimedia搜索: {keyword}")
        
        search_url = f"https://commons.wikimedia.org/w/index.php?search={urllib.parse.quote(keyword)}+cartoon&title=Special:MediaSearch&go=Go"
        
        content = self.make_request(search_url, COMMON_HEADERS)
        if not content:
            return []
        
        try:
            html = content.decode('utf-8', errors='ignore')
            urls = re.findall(r'"https://upload\.wikimedia\.org/[^"]+\.(?:jpg|jpeg|png)"', html)
            urls = list(dict.fromkeys(urls))
            urls = [u.strip('"') for u in urls]
            
            if urls:
                print(f"  ✅ 找到 {len(urls)} 个图片")
                return urls[:5]
        except Exception as e:
            print(f"  ❌ 解析失败: {e}")
        
        return []
    
    def search_openclipart(self, keyword: str) -> List[str]:
        """搜索Openclipart免费矢量图"""
        print(f"\n🔍 Openclipart搜索: {keyword}")
        
        search_url = f"https://openclipart.org/search/?query={urllib.parse.quote(keyword)}"
        
        content = self.make_request(search_url, COMMON_HEADERS)
        if not content:
            return []
        
        try:
            html = content.decode('utf-8', errors='ignore')
            # 提取SVG或PNG下载链接
            urls = re.findall(r'https://openclipart\.org/image/[^"]+', html)
            urls = list(dict.fromkeys(urls))
            
            if urls:
                print(f"  ✅ 找到 {len(urls)} 个图片")
                return urls[:3]
        except Exception as e:
            print(f"  ❌ 解析失败: {e}")
        
        return []
    
    def download_and_validate(self, word: str, image_urls: List[str]) -> Tuple[bool, Optional[bytes], str]:
        """下载并验证图片"""
        for url in image_urls:
            print(f"  📥 下载: {url[:60]}...")
            
            content = self.make_request(url, COMMON_HEADERS)
            if not content:
                continue
            
            size = len(content)
            
            # 验证图片大小
            if size < 5000:  # 小于5KB可能是无效图片
                print(f"  ⚠️ 图片太小: {size} bytes")
                continue
            
            # 验证是否是图片
            if self.is_valid_image(content):
                print(f"  ✅ 图片有效! ({size} bytes)")
                return True, content, url
            else:
                print(f"  ⚠️ 无效图片格式")
        
        return False, None, ""
    
    def is_valid_image(self, content: bytes) -> bool:
        """验证是否是有效图片"""
        image_signatures = [
            (b'\xff\xd8\xff', 'JPEG'),
            (b'\x89PNG\r\n\x1a\n', 'PNG'),
            (b'GIF87a', 'GIF'),
            (b'GIF89a', 'GIF'),
        ]
        
        for signature, _ in image_signatures:
            if content.startswith(signature):
                return True
        
        return False
    
    def save_image(self, word: str, content: bytes) -> Path:
        """保存图片"""
        img_path = IMAGES_DIR / f"{word}.jpg"
        
        # 备份原图
        if img_path.exists():
            backup_path = IMAGES_DIR / f"{word}_bak_{int(time.time())}.jpg"
            img_path.rename(backup_path)
            print(f"  📦 已备份原图到: {backup_path.name}")
        
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
            'size': 0,
            'downloaded_url': ''
        }
        
        # 尝试多种图片源
        search_methods = [
            ('bing', self.search_bing_images),
            ('baidu', self.search_baidu_images),
            ('wikimedia', self.search_wikimedia),
            ('openclipart', self.search_openclipart),
        ]
        
        for source_name, search_method in search_methods:
            print(f"\n尝试 {source_name}...")
            image_urls = search_method(word)
            
            if image_urls:
                result['sources'].append({
                    'source': source_name,
                    'count': len(image_urls)
                })
                
                # 下载并验证
                success, content, url = self.download_and_validate(word, image_urls)
                
                if success:
                    result['success'] = True
                    result['size'] = len(content)
                    result['downloaded_url'] = url
                    self.save_image(word, content)
                    return result
            
            # 避免请求过快
            time.sleep(1)
        
        print(f"  ❌ 所有来源都失败了")
        return result

def main():
    print("="*70)
    print("🎯 智能图片获取程序 v2")
    print("="*70)
    print(f"\n目标: {len(body_words)} 个人体相关词汇")
    print("策略: Bing/百度/Wikimedia/Openclipart图片搜索")
    print("="*70)
    
    # 加载已有链接
    links_data = {}
    if Path(LINKS_FILE).exists():
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            links_data = json.load(f)
    
    # 创建fetcher
    fetcher = SmartImageFetcherV2()
    
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
