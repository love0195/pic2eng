# 英语学习应用 (Word Learning App)

## 项目介绍
一个基于 Vue 3 + Vite 构建的移动端英语学习应用，包含分类词汇、图片展示和音频播放功能。

## 功能特点
- 📱 移动端友好的卡片式布局
- 🗂️ 12个分类的英语词汇
- 🖼️ 卡通插图风格图片（使用 Pollinations AI 生成）
- 🔊 点击图片或单词播放发音
- 🏷️ 底部标签栏切换分类

## 快速开始

### 安装依赖
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```

### 构建生产版本
```bash
npm run build
```

## 图片生成方法

### Pollinations AI（推荐方案）
项目使用 Pollinations AI 生成高质量卡通插图风格图片，这是我们的最终推荐方案！

#### 特点
- 免费、快速
- 生成高质量卡通插图
- 100% 成功率（已验证29张图片）

#### 使用方法
```bash
cd /workspace/word-app
python3 scripts/generate_pollinations.py
```

#### 详细文档
完整的操作流程文档请查看：
[Pollinations AI 图片生成操作流程](docs/superpowers/specs/2026-05-04-pollinations-ai-image-generation-workflow.md)

## 目录结构
```
/workspace/word-app/
├── public/
│   ├── audio/          # 词汇音频文件
│   ├── images/         # 词汇图片（卡通插图）
│   └── icons.svg       # 图标资源
├── src/
│   ├── data/
│   │   └── vocabulary.js  # 词汇数据
│   ├── App.vue        # 应用主组件
│   └── main.js        # 应用入口
├── docs/              # 文档目录
│   └── superpowers/
│       └── specs/     # 操作流程文档
├── scripts/           # 工具脚本
│   └── generate_pollinations.py  # Pollinations AI 图片生成脚本
└── vite.config.js     # Vite 配置
```

## 文档资源
- [Pollinations AI 图片生成操作流程](docs/superpowers/specs/2026-05-04-pollinations-ai-image-generation-workflow.md)
- [图片生成任务进度](docs/image_generation_tasks.md)
- [分类设计文档](docs/superpowers/specs/2026-05-04-body-categories-design.md)
- [词汇分类规则](docs/superpowers/specs/2026-05-04-vocabulary-sorting-rules.md)

## 技术栈
- Vue 3 (Composition API)
- Vite
- HTML5 Audio API

## 更新记录
- 2026-05-04: 使用 Pollinations AI 成功为29个人体相关词汇生成卡通插图！
- 2026-05-04: 项目初始创建，包含基础功能
