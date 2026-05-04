# 人体相关词汇分类设计文档

## 概述

为"看图学英语"应用新增三个词汇分类：面部五官、身体部位、内脏器官，每个分类包含8-12个基础词汇，适合儿童学习。

## 分类结构

| 分类键 | 中文名 | 图标 | 词汇数 |
|--------|--------|------|--------|
| face | 面部五官篇 | 👤 | 10个 |
| body | 身体部位篇 | 🦵 | 11个 |
| organs | 内脏器官篇 | ❤️ | 8个 |

## 详细词汇列表

### 1. face（面部五官篇）👤

**排序逻辑：从上到下、从整体到局部**

| 英文 | 中文 |
|------|------|
| face | 脸 |
| forehead | 额头 |
| eye | 眼睛 |
| eyebrow | 眉毛 |
| ear | 耳朵 |
| nose | 鼻子 |
| cheek | 脸颊 |
| mouth | 嘴 |
| lip | 嘴唇 |
| chin | 下巴 |

### 2. body（身体部位篇）🦵

**排序逻辑：从上到下的身体顺序**

| 英文 | 中文 |
|------|------|
| head | 头 |
| neck | 脖子 |
| shoulder | 肩膀 |
| arm | 手臂 |
| elbow | 肘 |
| hand | 手 |
| finger | 手指 |
| leg | 腿 |
| knee | 膝盖 |
| foot | 脚 |
| skin | 皮肤 |

### 3. organs（内脏器官篇）❤️

**排序逻辑：按重要性和位置排列**

| 英文 | 中文 |
|------|------|
| brain | 大脑 |
| heart | 心脏 |
| lung | 肺 |
| liver | 肝脏 |
| stomach | 胃 |
| intestine | 肠 |
| kidney | 肾脏 |
| muscle | 肌肉 |

## 资源状态

### 音频资源

所有词汇的音频文件已存在于 `public/audio/` 目录中，无需额外下载。

### 图片资源

需要为以下词汇生成图片：

- 面部五官：face, forehead, eye, eyebrow, ear, nose, cheek, mouth, lip, chin（10张）
- 身体部位：head, neck, shoulder, arm, elbow, hand, finger, leg, knee, foot, skin（11张）
- 内脏器官：brain, heart, lung, liver, stomach, intestine, kidney, muscle（8张）

图片生成使用现有脚本模式，调用 API 生成卡通风格图片。

## 实施步骤

1. 更新 `src/data/vocabulary.js`，添加三个新分类
2. 生成缺失的图片资源
3. 验证所有资源完整性
4. 测试应用功能

## 技术依赖

- 图片生成 API：`https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image`
- 图片风格：白色背景的卡通插图，适合儿童学习
