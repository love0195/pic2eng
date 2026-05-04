#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import json
from pathlib import Path

BASE_DIR = Path('/workspace/word-app')
LINKS_FILE = BASE_DIR / 'docs/image_generation_links.json'
IMAGES_DIR = BASE_DIR / 'public/images'
PLACEHOLDER_SIZE = 176626

def main():
    print("=" * 70)
    print("使用Playwright在真实浏览器中测试图片链接")
    print("=" * 70)
    
    with open(LINKS_FILE, 'r') as f:
        links_data = json.load(f)
    
    success_count = 0
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        for word, attempts in links_data.items():
            if not attempts:
                continue
            
            latest_attempt = attempts[-1]
            link = latest_attempt['link']
            attempt_num = latest_attempt.get('attempt', 1)
            
            print(f"\n📝 {word} (第 {attempt_num} 次尝试):")
            print(f"  打开链接: {link[:80]}...")
            
            try:
                page.goto(link, wait_until='networkidle', timeout=30000)
                
                # 检查页面内容是否是图片
                img_elements = page.query_selector_all('img')
                
                if img_elements:
                    print(f"  📸 找到 {len(img_elements)} 个图片元素")
                    
                    # 尝试下载第一张图片
                    img = img_elements[0]
                    img_src = img.get_attribute('src') or link
                    
                    print(f"  图片源: {img_src[:80]}...")
                    
                    # 访问图片并获取内容
                    response = page.request.get(img_src)
                    content = response.body()
                    size = len(content)
                    
                    if size != PLACEHOLDER_SIZE:
                        print(f"  ✅ 找到真实图片! ({size} bytes)")
                        
                        img_path = IMAGES_DIR / f'{word}.jpg'
                        with open(img_path, 'wb') as f:
                            f.write(content)
                        
                        print(f"  💾 已保存到: {img_path}")
                        success_count += 1
                    else:
                        print(f"  ⏳ 仍是占位图 ({size} bytes)")
                else:
                    print(f"  ❌ 未找到图片元素")
                    
                    # 截图看看页面内容
                    page.screenshot(path=f'/tmp/browser_test_{word}.png')
                    print(f"  📸 截图已保存到 /tmp/browser_test_{word}.png")
                    
            except Exception as e:
                print(f"  ❌ 错误: {e}")
        
        browser.close()
    
    print("\n" + "=" * 70)
    print(f"最终结果: {success_count}/{len(links_data)} 成功")
    print("=" * 70)

if __name__ == "__main__":
    main()
