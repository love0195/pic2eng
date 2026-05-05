import { vocabularyData } from '../src/data/vocabulary.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

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
console.log(`✅ 总单词数: 1731`);
console.log(`✅ 已下载: ${1731 - missingImages.length}`);
console.log(`❌ 缺失: ${missingImages.length}`);
console.log(`📝 已保存到 .missing_images.json`);
