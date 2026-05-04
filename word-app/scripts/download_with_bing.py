#!/usr/bin/env python3
"""
使用bing-image-downloader库获取图片
参考：https://github.com/gurugaurav/bing_image_downloader
"""
import os
import shutil
from pathlib import Path
from bing_image_downloader import downloader

# 配置
BASE_DIR = Path('/workspace/word-app')
IMAGES_DIR = BASE_DIR / 'public' / 'images'
TEMP_DIR = BASE_DIR / 'temp_downloads'

# 人体相关词汇
body_words = [
    'face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
    'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
    'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle'
]

def download_images():
    """下载图片"""
    print("=" * 70)
    print("🎯 使用 bing-image-downloader 下载图片")
    print("=" * 70)
    
    success_count = 0
    
    for i, word in enumerate(body_words, 1):
        print(f"\n\n{'#'*70}")
        print(f"# [{i}/{len(body_words)}] 下载: {word}")
        print('#'*70)
        
        # 搜索关键词（添加cartoon和educational关键字）
        query = f"{word} cartoon educational illustration"
        output_folder = TEMP_DIR / word
        
        # 如果已存在，先删除
        if output_folder.exists():
            shutil.rmtree(output_folder)
        
        try:
            print(f"🔍 搜索: {query}")
            # 下载图片
            downloader.download(
                query_string=query,
                limit=5,  # 下载5张图片
                output_dir=str(TEMP_DIR),
                adult_filter_off=True,
                force_replace=False,
                timeout=60,
                verbose=True
            )
            
            # 检查下载的图片
            if output_folder.exists():
                images = list(output_folder.glob('*.jpg')) + list(output_folder.glob('*.png'))
                print(f"  📁 下载了 {len(images)} 张图片")
                
                if images:
                    # 选择第一张图片
                    chosen_image = images[0]
                    
                    # 检查图片大小
                    size = chosen_image.stat().st_size
                    if size > 5000:  # 大于5KB
                        # 保存到目标位置
                        target_path = IMAGES_DIR / f"{word}.jpg"
                        
                        # 备份原图
                        if target_path.exists():
                            backup_path = IMAGES_DIR / f"{word}_bak.jpg"
                            target_path.rename(backup_path)
                            print(f"  📦 已备份原图")
                        
                        # 复制新图片
                        shutil.copy(chosen_image, target_path)
                        print(f"  ✅ 已保存: {target_path.name} ({size} bytes)")
                        success_count += 1
                    else:
                        print(f"  ⚠️ 图片太小: {size} bytes")
                else:
                    print(f"  ❌ 没有找到图片")
            else:
                print(f"  ❌ 下载失败")
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")
        
        print(f"\n📊 当前进度: {success_count}/{i} 成功")
    
    # 清理临时目录
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    
    print("\n" + "=" * 70)
    print("🎉 处理完成!")
    print("=" * 70)
    print(f"成功: {success_count}/{len(body_words)}")
    print("=" * 70)

if __name__ == "__main__":
    download_images()
