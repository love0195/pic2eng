# 图片资源标记

## 人体相关分类图片 - 当前状态

### ✅ 面部五官 (face) - 10个词
- face.jpg: ✅ 已替换 (39KB) - 卡通表情脸
- forehead.jpg: ✅ 已替换 (13KB) - 额头解剖图
- eye.jpg: ✅ 已替换 (31KB) - 卡通眼睛
- eyebrow.jpg: ✅ 已替换 (24KB) - 眉毛插图
- ear.jpg: ✅ 已替换 (16KB) - 耳朵解剖图
- nose.jpg: ✅ 已替换 (116KB) - 卡通鼻子
- cheek.jpg: ✅ 已替换 (12KB) - 脸颊解剖图
- mouth.jpg: ✅ 已替换 (18KB) - 卡通嘴巴
- lip.jpg: ✅ 已替换 (34KB) - 红唇插图
- chin.jpg: ✅ 已替换 (20KB) - 下巴解剖图

### ✅ 身体部位 (body) - 11个词
- head.jpg: ✅ 已替换 (21KB) - 卡通头部
- neck.jpg: ✅ 已替换 (15KB) - 脖子解剖图
- shoulder.jpg: ✅ 已替换 (8KB) - 肩膀解剖图
- arm.jpg: ✅ 已替换 (61KB) - 卡通手臂
- elbow.jpg: ✅ 已替换 (19KB) - 肘部解剖图
- hand.jpg: ✅ 已替换 (13KB) - 卡通手
- finger.jpg: ✅ 已替换 (17KB) - 手指解剖图
- leg.jpg: ✅ 已替换 (19KB) - 卡通腿
- knee.jpg: ✅ 已替换 (26KB) - 膝盖解剖图
- foot.jpg: ✅ 已替换 (8KB) - 卡通脚
- skin.jpg: ✅ 已替换 (18KB) - 皮肤解剖图

### ✅ 内脏器官 (organs) - 8个词
- brain.jpg: ✅ 已替换 (35KB) - 卡通大脑
- heart.jpg: ✅ 已替换 (22KB) - 卡通心脏
- lung.jpg: ✅ 已替换 (31KB) - 肺部解剖图
- liver.jpg: ✅ 已替换 (39KB) - 肝脏解剖图
- stomach.jpg: ✅ 已替换 (11KB) - 卡通胃
- intestine.jpg: ✅ 已替换 (8KB) - 肠道解剖图
- kidney.jpg: ✅ 已替换 (20KB) - 肾脏解剖图
- muscle.jpg: ✅ 已替换 (18KB) - 肌肉解剖图

## 说明
- ✅: 已从Dreamstime下载的卡通/解剖插图
- 图片来源: Dreamstime缩略图
- 总计: 29张图片全部已替换

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
