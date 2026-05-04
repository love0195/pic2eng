import urllib.request
import os

filepath = '/workspace/word-app/test_images/bookshelf_first.jpg'

# 读取文件头
with open(filepath, 'rb') as f:
    header = f.read(100)

print("文件头分析:")
print(f"  前10字节(hex): {header[:10].hex()}")
print(f"  文件签名: {header[:8]}")

# JPEG文件以 FF D8 FF 开头
if header[:3] == b'\xff\xd8\xff':
    print("  ✅ 这是有效的JPEG文件")
elif header[:4] == b'\x89PNG':
    print("  ✅ 这是PNG文件")
else:
    print("  ❓ 未知文件格式")

# 检查文件大小
size = os.path.getsize(filepath)
print(f"\n文件大小: {size} bytes")

# 尝试用PIL打开并获取基本信息
try:
    from PIL import Image
    img = Image.open(filepath)
    print(f"\n图片信息:")
    print(f"  格式: {img.format}")
    print(f"  尺寸: {img.size}")
    print(f"  模式: {img.mode}")
except ImportError:
    print("\n(未安装PIL，无法获取图片详细信息)")
except Exception as e:
    print(f"\n打开图片失败: {e}")
