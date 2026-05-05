# Word App - 英语单词学习应用

一个纯静态的英语单词学习应用，包含图片、音频和多种学习模式。

## 📋 项目特点

- ✅ **纯静态部署** - 无需 Node 运行环境，直接用浏览器打开即可
- ✅ **无外部依赖** - 所有资源均本地化，无需运行时访问在线资源
- ✅ **完整功能** - 分类浏览、点击发音、随机播放
- ✅ **复合词支持** - 自动拆分复合词并顺序播放

## 🚀 快速开始

### 直接使用（推荐）

1. 下载 `dist/` 目录的所有内容
2. 用浏览器打开 `dist/index.html`
3. 开始学习！

### 开发模式

```bash
npm install
npm run dev
```

### 构建生产版本

```bash
npm run build
```

构建产物位于 `dist/` 目录，可直接部署到任何静态托管服务。

## 📁 目录结构

```
word-app/
├── dist/                  # 生产构建产物（纯静态）
│   ├── index.html        # 入口页面
│   ├── assets/           # 编译后的 JS/CSS
│   ├── images/           # 单词图片（约 1700+ 张）
│   └── audio/            # 单词发音（约 1900+ 个）
├── public/               # 原始资源文件
│   ├── images/
│   └── audio/
├── src/                  # 源代码
│   ├── data/vocabulary.js  # 单词数据
│   ├── App.vue         # 主应用组件
│   └── main.js         # 入口
└── scripts/             # 资源下载脚本
```

## 📦 资源下载说明

### 图片下载（Pollinations AI）

使用脚本从 Pollinations AI 生成并下载单词图片：

```bash
python3 scripts/download_missing_images.py
```

- 服务：Pollinations AI
- API：`https://image.pollinations.ai/prompt/{word}?width=512&height=512`
- 分批处理：每 30 个单词自动提交到 Git

### 音频下载（有道词典）

使用脚本从有道词典 TTS API 下载单词发音：

```bash
python3 scripts/download_missing_audio.py
```

**有道词典 TTS API 使用方法：**

- API 地址：`http://dict.youdao.com/dictvoice?audio={word}&type=2`
- 参数说明：
  - `audio`：要发音的单词（需 URL 编码）
  - `type`：发音类型（2 为美式发音，1 为英式发音）

**特点：**
- 免费使用，无需 API Key
- 支持英语单词发音
- 返回 MP3 格式音频
- 下载后保存到 `public/audio/` 目录

**复合词处理：**
复合词会自动拆分为单个单词，分别下载发音：
例如 "school_bus" → "school.mp3" + "bus.mp3"

## 🎯 功能说明

### 1. 分类浏览
- 按主题分组（日常生活、自然、美食等）
- 点击分类查看单词卡片
- 点击卡片播放发音

### 2. 复合词发音
- 自动识别复合词（以下划线分隔）
- 依次播放每个部分的发音
- 单词间隔 40ms

### 3. 随机播放模式
- 三张卡片循环展示
- 自动播放发音（每个单词 3 遍）
- 支持手动切换

## 🔍 无外部依赖确认

本项目已确保**无运行时外部依赖**：

✅ **JavaScript** - 只有 Vue 3，已打包到本地
✅ **CSS** - 完全自包含，无外部 CDN
✅ **图片** - 全部本地化到 `dist/images/`
✅ **音频** - 全部本地化到 `dist/audio/`
✅ **字体** - 使用系统默认字体栈
✅ **图标** - 内置 emoji，无需外部资源

唯一的 HTTP 请求是下载脚本在构建阶段使用的 Pollinations AI 和有道词典 API，但这些仅用于资源生成，不会在运行时调用。

## 📊 当前进度

- **单词总数**：1731
- **图片完成度**：约 70%（持续下载中）
- **音频完成度**：100%

## 🤝 开发说明

### 调整复合词间隔

编辑 [src/App.vue](file:///workspace/word-app/src/App.vue#L193-L210)：

```javascript
audio.onended = () => {
  setTimeout(() => {
    playWordPartsSequentially(parts, currentIndex + 1, onComplete);
  }, 40); // 修改这里的毫秒数
}
```

### 添加新单词

编辑 [src/data/vocabulary.js](file:///workspace/word-app/src/data/vocabulary.js)，按现有格式添加单词。

## 📝 许可证

MIT
