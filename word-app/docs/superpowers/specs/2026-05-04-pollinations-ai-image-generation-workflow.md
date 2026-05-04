# Pollinations AI 图片生成操作流程

## 说明
使用 Pollinations AI (https://image.pollinations.ai/) 为英语学习应用生成卡通插图风格图片的标准操作流程。

## 问题背景
- 原始图片生成API一直返回占位图（176626 bytes），无法生成真实图片
- Dreamstime缩略图质量差，不符合卡通插图风格要求
- 最终通过 Pollinations AI 完美解决了这个问题

## Pollinations AI 介绍
- **网站**: https://image.pollinations.ai/
- **特点**: 免费、快速、生成高质量卡通插图风格图片
- **API 格式**: `https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true`
- **成功率**: 29/29 (100%) - 已成功为所有29个人体相关词汇生成图片

## 操作流程

### 1. 准备工作

#### 1.1 确认词汇列表
首先确认需要生成图片的词汇列表，例如我们的人体相关词汇：
```
face, forehead, eye, eyebrow, ear, nose, cheek, mouth, lip, chin,
head, neck, shoulder, arm, elbow, hand, finger, leg, knee, foot, skin,
brain, heart, lung, liver, stomach, intestine, kidney, muscle
```

#### 1.2 编写提示词（Prompts）
为每个词汇编写专门的提示词，风格要统一，例如：
```
{word} cute cartoon, simple flat design, white background, kawaii style, clean lines, educational illustration
```

**内脏器官词汇可额外添加**: `anatomy diagram`

### 2. 使用脚本生成图片

#### 2.1 脚本文件位置
- 主脚本: `scripts/generate_pollinations.py`

#### 2.2 运行脚本
```bash
cd /workspace/word-app
python3 scripts/generate_pollinations.py
```

#### 2.3 脚本功能说明
脚本会自动完成以下步骤：
1. 遍历词汇列表
2. 为每个词汇生成 Pollinations AI URL
3. 下载图片（120秒超时）
4. 验证图片有效性（检查文件头，确保不是过小的无效文件）
5. 保存图片到 `public/images/` 目录
6. 备份原图（如果存在）为 `{word}_pollinations_bak.jpg`
7. 保存生成链接记录到 `docs/pollinations_results.json`
8. 每次请求间隔3秒，避免请求过快

### 3. 手动生成单张图片
如果某个词汇生成失败，可以手动重新生成：

```python
import urllib.request
import urllib.parse
from pathlib import Path

word = 'leg'
prompt = 'cute cartoon human leg, simple flat design, white background, kawaii style, clean lines'
encoded_prompt = urllib.parse.quote(prompt)
url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
content = urllib.request.urlopen(req, timeout=120).read()

img_path = Path('public/images') / f"{word}.jpg"
if img_path.exists():
    backup_path = Path('public/images') / f"{word}_bak.jpg"
    img_path.rename(backup_path)

with open(img_path, 'wb') as f:
    f.write(content)

print(f"✅ 已保存: {img_path.name} ({len(content)} bytes)")
```

### 4. 验证结果
检查所有图片是否已成功生成：

```python
from pathlib import Path

body_words = ['face', 'forehead', 'eye', 'eyebrow', 'ear', 'nose', 'cheek', 'mouth', 'lip', 'chin',
              'head', 'neck', 'shoulder', 'arm', 'elbow', 'hand', 'finger', 'leg', 'knee', 'foot', 'skin',
              'brain', 'heart', 'lung', 'liver', 'stomach', 'intestine', 'kidney', 'muscle']

img_dir = Path('public/images')
missing = []
valid = []

for word in body_words:
    img_path = img_dir / f"{word}.jpg"
    if img_path.exists():
        size = img_path.stat().st_size
        valid.append((word, size))
    else:
        missing.append(word)

print("=" * 70)
print(f"✅ 验证完成！")
print("=" * 70)
print(f"成功: {len(valid)}/{len(body_words)}")
if missing:
    print(f"❌ 缺失: {missing}")
print("=" * 70)
```

## 提示词最佳实践

### 通用提示词模板
```
cute cartoon {subject}, simple flat design, white background, kawaii style, clean lines, educational illustration
```

### 各类别提示词示例

#### 面部五官
```
cute cartoon human {word}, simple flat design, white background, kawaii style, clean lines
```
- cheek 可额外添加: `pink blush`
- mouth 可额外添加: `smiling`
- eye 可额外添加: `big eye`

#### 身体部位
```
cute cartoon human {word}, simple flat design, white background, kawaii style, clean lines
```
- hand 可额外添加: `five fingers`

#### 内脏器官
```
cute cartoon human {word}, simple flat design, white background, kawaii style, clean lines, anatomy diagram
```

## 文件保存规范

### 图片保存位置
- 主图片: `public/images/{word}.jpg`
- 备份图片: `public/images/{word}_pollinations_bak.jpg` (保留之前的版本)

### 链接记录保存
- 记录文件: `docs/pollinations_results.json`
- 记录信息: 提示词、URL、时间戳、尝试次数

## 历史记录
- 2026-05-04: 首次成功使用 Pollinations AI，为29个人体相关词汇生成卡通插图！
- 成功率: 29/29 (100%)
- 平均图片大小: ~15-25KB (合理的高质量图片大小)

## 注意事项
1. **URL编码**: 提示词需要进行 URL 编码
2. **请求间隔**: 每次请求间隔至少3秒，避免请求过快
3. **超时设置**: 下载超时建议设置为120秒
4. **User-Agent**: 请求时添加浏览器 User-Agent
5. **备份策略**: 保存新图片前先备份原图
6. **验证图片**: 保存前验证图片有效性（检查文件头和大小）

## 故障排查

### 问题: 图片太小或无效
**原因**: 可能是生成失败的占位图
**解决**: 重新运行脚本生成单张图片，或修改提示词后重新尝试

### 问题: 请求超时
**原因**: Pollinations AI 处理时间较长或网络问题
**解决**: 增加超时时间（建议120秒），或稍后重试

### 问题: 图片不符合预期风格
**原因**: 提示词不够精确
**解决**: 优化提示词，添加更多风格相关的关键词

## 替代方案（如果 Pollinations AI 不可用）
如果 Pollinations AI 暂时不可用，可以考虑：
1. 使用之前的 Dreamstime 缩略图作为临时方案
2. 尝试其他免费AI图片生成服务
3. 使用手绘或专业插画师作品

## 参考资源
- Pollinations AI 网站: https://image.pollinations.ai/
- 任务进度文档: docs/image_generation_tasks.md
- 图片生成脚本: scripts/generate_pollinations.py
- 链接记录: docs/pollinations_results.json
