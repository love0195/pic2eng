# 词汇分类排序规则与扩充计划

## 概述

本文档定义"看图学英语"应用中每个词汇分类的排序规则，以及内容扩充计划。

## 现有分类排序规则

### 1. furniture（家具篇）🛋️
**排序逻辑：按家庭空间布局顺序**
- 客厅家具：sofa、chair、table
- 卧室家具：bed、wardrobe
- 书房的家具：desk、bookshelf
- 储物家具：cabinet、cupboard、drawer
- 照明：lamp
- 其他：stool

### 2. appliances（电器篇）📺
**排序逻辑：按厨房→清洁→娱乐的空间顺序**
- 厨房电器：refrigerator、microwave、oven、dishwasher、coffee、toaster
- 清洁电器：washing
- 环境电器：airconditioner、fan
- 娱乐/办公电器：television、computer

### 3. vehicles（交通工具篇）🚗
**排序逻辑：按体型从小到大排序**
- 小型：bicycle、motorcycle
- 私家车：car、taxi
- 公共交通：bus、subway、train
- 大型/货运：truck
- 水上：boat、ship
- 航空：plane、helicopter

### 4. animals（动物篇）🐕
**排序逻辑：按与人类亲近程度排序**
- 宠物：dog、cat、rabbit、hamster
- 常见鸟类：bird、parrot
- 水生：fish、turtle
- 大型动物：elephant、monkey、panda、snake

### 5. fruits（水果篇）🍎
**排序逻辑：按常见程度排序**
- 最常见：apple、banana、orange
- 浆果类：strawberry、cherry、grape
- 大型水果：watermelon、pineapple
- 热带水果：mango、peach、pear、lemon

### 6. sea_animals（海洋动物篇）🐙
**排序逻辑：按体型从大到小排序**
- 巨型：whale
- 大型：shark、dolphin
- 中型：octopus、lobster、crab
- 小型：jellyfish、starfish、seahorse

### 7. mammals（哺乳动物篇）🦁
**排序逻辑：按食性分类，同类按体型排序**
- 猫科：lion、tiger
- 犬科：fox
- 长颈鹿科：giraffe
- 有袋类：kangaroo、koala
- 马科：zebra、deer

### 8. plants（植物篇）🌸
**排序逻辑：按园艺/用途分类**
- 观赏花：rose、sunflower、tulip、daisy、flower
- 食用/果树：mushroom
- 绿植：tree、grass、leaf

### 9. indoor（室内空间篇）🏠
**排序逻辑：按房间类型→建筑构件的顺序**
- 房间：kitchen、bedroom、bathroom、living_room
- 建筑构件：door、window、wall、floor、ceiling
- 楼梯：stairs

### 10. buildings（公共建筑篇）🏛️
**排序逻辑：按服务类型分类**
- 教育：school、library
- 医疗：hospital
- 宗教：church
- 地标：tower、castle、palace
- 交通/体育：stadium

---

## 新增分类

### 11. body（人体结构篇）👤
**排序逻辑：按人体结构从上到下、从外到内排序**
- 头部：head、face、eye、ear、nose、mouth、lip、tooth、tongue、neck、brain、forehead、eyebrow、cheek、chin
- 上肢：hand、finger、arm、elbow、shoulder
- 躯干：heart、lung、liver、stomach、intestine、kidney、muscle、skin
- 下肢：leg、knee、foot

### 12. food（食物篇）🍜
**排序逻辑：按三餐顺序分类**
- 早餐：bread、egg、milk
- 主食：rice、noodle、dumpling
- 肉类：chicken、beef、pork
- 蔬菜：tomato、potato、carrot、cabbage、onion
- 甜点：cake、cookie、ice_cream

### 13. clothing（服装篇）👕
**排序逻辑：按从头到脚的穿戴顺序**
- 头饰：hat、cap
- 上装：shirt、coat、jacket、dress、skirt
- 下装：pants、sock、shoe
- 配饰：bag

### 14. weather（天气篇）☀️
**排序逻辑：按自然现象分类**
- 晴朗：sun、cloud、sky
- 降水：rain、snow
- 温度：hot、cold
- 极端：storm、wind、rainbow

### 15. job（职业篇）👨‍💼
**排序逻辑：按服务对象分类**
- 教育：teacher、student
- 医疗：doctor、nurse
- 服务：chef、waiter、driver、police
- 创意：artist、singer
- 技术：engineer、programmer

### 16. nature（自然篇）🌍
**排序逻辑：按地理层级排序**
- 宇宙：sun、moon、star
- 大气：sky、cloud、rainbow
- 地表：mountain、river、lake、ocean、beach、desert
- 地理特征：island、forest

---

## 内容扩充

### 现有分类扩充（每个分类达到15-20个词）

| 分类 | 新增词汇 |
|------|----------|
| furniture | 添加 bathroom_cabinet（浴室柜）、coffee_table（茶几）、dining_table（餐桌）、nightstand（床头柜）、mirror（镜子）等 |
| appliances | 添加 rice_cooker（电饭煲）、blender（搅拌机）、vacuum（吸尘器）、iron（熨斗）、hair_dryer（吹风机）等 |
| vehicles | 添加 ambulance（救护车）、fire_truck（消防车）、taxi（已有）、helicopter（已有）、rocket（火箭）等 |
| animals | 添加 horse（马）、cow（牛）、pig（猪）、sheep（羊）、bear（熊）、wolf（狼）、squirrel（松鼠）等 |
| fruits | 添加 watermelon（已有）、pineapple（已有）、kiwi（猕猴桃）、coconut（椰子）、cherry（已有）、blueberry（蓝莓）等 |
| sea_animals | 保留现有，移除难以生成图片的 |
| mammals | 添加 bear、wolf、horse、cow、pig、sheep 等 |
| plants | 添加更多花朵和树木 |
| indoor | 补充更多室内物品 |
| buildings | 添加 park（公园）、supermarket（超市）、restaurant（餐厅）、bank（银行）等 |

---

## 图片生成问题词汇排除

以下词汇因难以生成清晰的卡通图片，将从分类中移除或替换：
- bookshelf（如已有合适图片则保留）
- bookshelf（可保留，已有多版本测试图片）
- bookself 相关待确认

---

## 实施步骤

1. 更新 vocabulary.js，按新排序规则重新排列
2. 扩充每个分类的词汇数量
3. 添加新分类（body、food、clothing、weather、job、nature）
4. 生成/下载缺失的图片和音频资源
5. 更新 App.vue 的分类图标配置
