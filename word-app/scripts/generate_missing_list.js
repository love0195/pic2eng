const { vocabularyData } = require('../src/data/vocabulary');
const fs = require('fs');
const path = require('path');

const imageDir = path.join(__dirname, '../public/images');
const existingImages = new Set();

if (fs.existsSync(imageDir)) {
  fs.readdirSync(imageDir).forEach(file => {
    existingImages.add(file.replace('.jpg', ''));
  });
}

const missingImages = [];

for (const groupKey in vocabularyData) {
  const group = vocabularyData[groupKey];
  for (const catKey in group.categories) {
    const category = group.categories[catKey];
    for (const word of category.words) {
      if (!existingImages.has(word.en)) {
        missingImages.push(word.en);
      }
    }
  }
}

fs.writeFileSync(path.join(__dirname, '../.missing_images.json'), JSON.stringify(missingImages, null, 2));
console.log(`✅ 生成缺失图片列表: ${missingImages.length} 个`);
console.log(`📝 已保存到 .missing_images.json`);
