# 图片资源标记

## 人体相关分类图片 - 当前状态

以下是当前三个新分类使用的图片来源标记：

### ✅ 面部五官 (face) - 10个词
- face.jpg: ⚠️ 临时占位 - 需替换
- forehead.jpg: ⚠️ 临时占位 - 需替换
- eye.jpg: ⚠️ 临时占位 - 需替换
- eyebrow.jpg: ⚠️ 临时占位 - 需替换
- ear.jpg: ⚠️ 临时占位 - 需替换
- nose.jpg: ⚠️ 临时占位 - 需替换
- cheek.jpg: ⚠️ 临时占位 - 需替换
- mouth.jpg: ⚠️ 临时占位 - 需替换
- lip.jpg: ⚠️ 临时占位 - 需替换
- chin.jpg: ⚠️ 临时占位 - 需替换

### ✅ 身体部位 (body) - 11个词
- head.jpg: ⚠️ 临时占位 - 需替换
- neck.jpg: ⚠️ 临时占位 - 需替换
- shoulder.jpg: ⚠️ 临时占位 - 需替换
- arm.jpg: ⚠️ 临时占位 - 需替换
- elbow.jpg: ⚠️ 临时占位 - 需替换
- hand.jpg: ⚠️ 临时占位 - 需替换
- finger.jpg: ⚠️ 临时占位 - 需替换
- leg.jpg: ⚠️ 临时占位 - 需替换
- knee.jpg: ⚠️ 临时占位 - 需替换
- foot.jpg: ⚠️ 临时占位 - 需替换
- skin.jpg: ⚠️ 临时占位 - 需替换

### ✅ 内脏器官 (organs) - 8个词
- brain.jpg: ⚠️ 临时占位 - 需替换
- heart.jpg: ⚠️ 临时占位 - 需替换
- lung.jpg: ⚠️ 临时占位 - 需替换
- liver.jpg: ⚠️ 临时占位 - 需替换
- stomach.jpg: ⚠️ 临时占位 - 需替换
- intestine.jpg: ⚠️ 临时占位 - 需替换
- kidney.jpg: ⚠️ 临时占位 - 需替换
- muscle.jpg: ⚠️ 临时占位 - 需替换

## 说明
- ⚠️: 使用picsum.photos下载的随机图片，内容与词汇可能不匹配
- 总计: 29张图片需替换

## 尝试记录

### 2026-05-04 尝试记录
1. **图片生成API**: 返回176626字节占位图，无法生成真实图片
2. **PNGTree/Freepik**: 返回403 Forbidden，禁止爬虫访问
3. **维基百科**: SSL连接超时
4. **Picsum**: 成功下载，但是随机图片，与词汇内容不匹配

### 推荐方案
1. **手动下载**: 在本地浏览器访问以下网站搜索并下载：
   - https://pngtree.com (需注册)
   - https://freepik.com (需注册)
   - https://pixabay.com (免费，无需注册)
   
2. **使用Pixabay API**: 
   - 注册获取API密钥: https://pixabay.com/api/
   - 免费API每小时5000次请求
   
3. **本地浏览器自动化**: 在本地环境使用Playwright/Selenium爬取
