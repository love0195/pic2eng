<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { vocabularyData } from './data/vocabulary';

// 页面状态
const currentPage = ref('home'); // 'home', 'random', 'category', 'play'

// 分类选择
const selectedGroup = ref(null);
const selectedCategory = ref(null);

// 播放模式
const isPlaying = ref(false);
const currentPlayIndex = ref(0);
const playWords = ref([]);
let playTimer = null;

const groupKeys = computed(() => Object.keys(vocabularyData));

function getAllCategories() {
  const categories = [];
  for (const groupKey of groupKeys.value) {
    const group = vocabularyData[groupKey];
    for (const catKey in group.categories) {
      categories.push({
        groupKey,
        catKey,
        name: group.categories[catKey].name,
        icon: group.categories[catKey].icon,
        words: group.categories[catKey].words
      });
    }
  }
  return categories;
}

function getGroupCategories(groupKey) {
  const group = vocabularyData[groupKey];
  const categories = [];
  for (const catKey in group.categories) {
    categories.push({
      catKey,
      name: group.categories[catKey].name,
      icon: group.categories[catKey].icon,
      words: group.categories[catKey].words
    });
  }
  return categories;
}

function goToHome() {
  currentPage.value = 'home';
  selectedGroup.value = null;
  selectedCategory.value = null;
  stopPlay();
}

function goToRandom() {
  const categories = getAllCategories();
  const randomCat = categories[Math.floor(Math.random() * categories.length)];
  selectedGroup.value = randomCat.groupKey;
  selectedCategory.value = randomCat;
  currentPage.value = 'category';
}

function selectGroup(groupKey) {
  selectedGroup.value = groupKey;
}

function selectCategory(category) {
  selectedCategory.value = category;
  currentPage.value = 'category';
}

function startPlayMode() {
  playWords.value = [...selectedCategory.value.words];
  shuffleArray(playWords.value);
  currentPlayIndex.value = 0;
  isPlaying.value = true;
  currentPage.value = 'play';
  startAutoPlay();
}

function togglePlay() {
  if (isPlaying.value) {
    stopPlay();
  } else {
    isPlaying.value = true;
    startAutoPlay();
  }
}

function stopPlay() {
  isPlaying.value = false;
  if (playTimer) {
    clearTimeout(playTimer);
    playTimer = null;
  }
}

function nextCard() {
  currentPlayIndex.value = (currentPlayIndex.value + 1) % playWords.value.length;
  if (isPlaying.value) {
    startAutoPlay();
  }
}

function prevCard() {
  currentPlayIndex.value = (currentPlayIndex.value - 1 + playWords.value.length) % playWords.value.length;
  if (isPlaying.value) {
    startAutoPlay();
  }
}

function startAutoPlay() {
  stopPlay();
  isPlaying.value = true;
  
  const word = playWords.value[currentPlayIndex.value];
  
  // 播放3遍，每遍间隔0.5秒
  let playCount = 0;
  const playNext = () => {
    if (playCount >= 3) {
      // 播放完3遍后，停留2秒，然后下一张
      playTimer = setTimeout(() => {
        if (isPlaying.value) {
          nextCard();
        }
      }, 2000);
      return;
    }
    
    playCount++;
    playPronunciationOnce(word, () => {
      if (isPlaying.value && playCount < 3) {
        playTimer = setTimeout(playNext, 500);
      } else if (isPlaying.value && playCount >= 3) {
        playTimer = setTimeout(() => {
          if (isPlaying.value) {
            nextCard();
          }
        }, 2000);
      }
    });
  };
  
  playNext();
}

function getImageUrl(word) {
  return `/images/${word.en}.jpg`;
}

function getAudioUrl(word) {
  const wordStr = typeof word === 'string' ? word : word.en;
  return `/audio/${wordStr}.mp3`;
}

function playPronunciationOnce(word, onComplete) {
  const wordParts = word.en.split('_');
  
  if (wordParts.length > 1) {
    playWordPartsSequentially(wordParts, 0, onComplete);
  } else {
    const audio = new Audio();
    audio.src = getAudioUrl(word.en);
    
    audio.onended = () => {
      onComplete();
    };
    
    audio.onerror = () => {
      onComplete();
    };
    
    audio.play().catch(() => {
      onComplete();
    });
  }
}

function playWordPartsSequentially(parts, currentIndex, onComplete) {
  if (currentIndex >= parts.length) {
    onComplete();
    return;
  }
  
  const part = parts[currentIndex];
  const audio = new Audio();
  audio.src = getAudioUrl(part);
  
  audio.onended = () => {
    setTimeout(() => {
      playWordPartsSequentially(parts, currentIndex + 1, onComplete);
    }, 40);
  };
  
  audio.onerror = () => {
    setTimeout(() => {
      playWordPartsSequentially(parts, currentIndex + 1, onComplete);
    }, 40);
  };
  
  audio.play().catch(() => {
    setTimeout(() => {
      playWordPartsSequentially(parts, currentIndex + 1, onComplete);
    }, 40);
  });
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

function getPrevWord() {
  if (playWords.value.length === 0) return null;
  const index = (currentPlayIndex.value - 1 + playWords.value.length) % playWords.value.length;
  return playWords.value[index];
}

function getNextWord() {
  if (playWords.value.length === 0) return null;
  const index = (currentPlayIndex.value + 1) % playWords.value.length;
  return playWords.value[index];
}

function getCurrentWord() {
  if (playWords.value.length === 0) return null;
  return playWords.value[currentPlayIndex.value];
}

onUnmounted(() => {
  stopPlay();
});
</script>

<template>
  <div class="app-container">
    <!-- 首页 -->
    <div v-if="currentPage === 'home'" class="page-content">
      <header class="page-header">
        <h1 class="page-title">
          <span class="title-icon">📚</span>
          <span>Picture English</span>
        </h1>
      </header>
      
      <main class="home-content">
        <!-- 如果没选分组，显示分组 -->
        <div v-if="!selectedGroup" class="group-grid">
          <div
            v-for="groupKey in groupKeys"
            :key="groupKey"
            class="group-card"
            @click="selectGroup(groupKey)"
          >
            <span class="group-icon">{{ vocabularyData[groupKey].icon }}</span>
            <span class="group-name">{{ vocabularyData[groupKey].groupName }}</span>
          </div>
        </div>
        
        <!-- 如果选了分组，显示该分组的分类 -->
        <div v-else class="category-page">
          <button class="back-btn" @click="selectedGroup = null">
            <span>← 返回</span>
          </button>
          <div class="category-grid">
            <div
              v-for="cat in getGroupCategories(selectedGroup)"
              :key="cat.catKey"
              class="category-card"
              @click="selectCategory(cat)"
            >
              <span class="category-icon">{{ cat.icon }}</span>
              <span class="category-name">{{ cat.name }}</span>
              <span class="category-count">{{ cat.words.length }}个</span>
            </div>
          </div>
        </div>
      </main>
    </div>
    
    <!-- 分类页面 -->
    <div v-else-if="currentPage === 'category'" class="page-content">
      <header class="page-header">
        <button class="back-btn" @click="goToHome">
          <span>← 返回</span>
        </button>
        <h1 class="page-title">
          <span>{{ selectedCategory?.icon }}</span>
          <span>{{ selectedCategory?.name }}</span>
        </h1>
        <button class="play-btn-header" @click="startPlayMode">
          ▶️
        </button>
      </header>
      
      <main class="category-content">
        <div class="word-grid">
          <div
            v-for="(word, index) in selectedCategory?.words"
            :key="word.en"
            class="word-card"
            @click="playPronunciationOnce(word, () => {})"
          >
            <div class="card-inner">
              <div class="image-wrapper">
                <img
                  :src="getImageUrl(word)"
                  :alt="word.en"
                  class="word-image"
                  loading="lazy"
                  @error="(e) => { e.target.style.display = 'none'; e.target.parentElement.querySelector('.no-image').style.display = 'flex'; }"
                />
                <div class="no-image" style="display: none;">
                  <span class="no-image-icon">📝</span>
                  <span class="no-image-text">{{ word.en }}</span>
                </div>
              </div>
              <div class="word-info">
                <div class="word-en">{{ word.en }}</div>
                <div class="word-zh">{{ word.zh }}</div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
    
    <!-- 播放页面 -->
    <div v-else-if="currentPage === 'play'" class="page-content play-page">
      <header class="page-header">
        <button class="back-btn" @click="() => { stopPlay(); currentPage = 'category' }">
          <span>← 返回</span>
        </button>
        <h1 class="page-title">播放中...</h1>
      </header>
      
      <main class="play-content">
        <div class="cards-container">
          <!-- 上一个卡片 -->
          <div class="side-card" @click="prevCard">
            <div v-if="getPrevWord()" class="mini-card">
              <div class="image-wrapper">
                <img
                  :src="getImageUrl(getPrevWord())"
                  :alt="getPrevWord().en"
                  class="word-image"
                  @error="(e) => { e.target.style.display = 'none'; }"
                />
              </div>
              <div class="word-info">
                <div class="word-en">{{ getPrevWord()?.en }}</div>
              </div>
            </div>
          </div>
          
          <!-- 当前卡片 -->
          <div class="main-card">
            <div v-if="getCurrentWord()" class="large-card-inner">
              <div class="image-wrapper">
                <img
                  :src="getImageUrl(getCurrentWord())"
                  :alt="getCurrentWord().en"
                  class="word-image"
                  @error="(e) => { e.target.style.display = 'none'; e.target.parentElement.querySelector('.no-image').style.display = 'flex'; }"
                />
                <div class="no-image" style="display: none;">
                  <span class="no-image-icon">📝</span>
                  <span class="no-image-text">{{ getCurrentWord()?.en }}</span>
                </div>
              </div>
              <div class="word-info">
                <div class="word-en">{{ getCurrentWord()?.en }}</div>
                <div class="word-zh">{{ getCurrentWord()?.zh }}</div>
              </div>
            </div>
          </div>
          
          <!-- 下一个卡片 -->
          <div class="side-card" @click="nextCard">
            <div v-if="getNextWord()" class="mini-card">
              <div class="image-wrapper">
                <img
                  :src="getImageUrl(getNextWord())"
                  :alt="getNextWord().en"
                  class="word-image"
                  @error="(e) => { e.target.style.display = 'none'; }"
                />
              </div>
              <div class="word-info">
                <div class="word-en">{{ getNextWord()?.en }}</div>
              </div>
            </div>
          </div>
        </div>
      </main>
      
      <!-- 播放控制 -->
      <div class="play-controls">
        <button class="control-btn" @click="prevCard">⏮️</button>
        <button class="play-toggle-btn" @click="togglePlay">
          <span v-if="isPlaying">⏸️</span>
          <span v-else>▶️</span>
        </button>
        <button class="control-btn" @click="nextCard">⏭️</button>
      </div>
    </div>
    
    <!-- 底部导航栏 -->
    <nav class="bottom-nav" v-if="currentPage !== 'play'">
      <button
        class="nav-item"
        :class="{ active: currentPage === 'home' || currentPage === 'category' }"
        @click="goToHome"
      >
        <span class="nav-label">首页</span>
      </button>
      <button
        class="nav-item"
        :class="{ active: currentPage === 'random' }"
        @click="goToRandom"
      >
        <span class="nav-label">随机</span>
      </button>
    </nav>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
  display: flex;
  flex-direction: column;
  padding-bottom: 70px;
  padding-bottom: env(safe-area-inset-bottom, 0) + 70px;
}

.page-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-header {
  background: white;
  padding: 12px 16px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  gap: 12px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-btn {
  padding: 8px 12px;
  border: none;
  background: #f5f7fa;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s;
}

.back-btn:hover {
  background: #e4e7ed;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.title-icon {
  font-size: 22px;
}

.play-btn-header {
  padding: 8px 16px;
  border: none;
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  border-radius: 20px;
  font-size: 20px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  flex-shrink: 0;
}

.play-btn-header:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
}

.home-content, .category-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

/* 分组和分类网格 */
.group-grid, .category-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.group-card, .category-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.group-card:hover, .category-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.group-icon, .category-icon {
  font-size: 36px;
}

.group-name, .category-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.category-count {
  font-size: 12px;
  color: #909399;
}

/* 单词卡片 */
.word-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.word-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.word-card:hover {
  transform: translateY(-2px);
}

.card-inner {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.image-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  background: linear-gradient(135deg, #f8fafc 0%, #eef2f7 100%);
  overflow: hidden;
}

.no-image {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, #f8fafc 0%, #eef2f7 100%);
  color: #909399;
}

.no-image-icon {
  font-size: 48px;
}

.no-image-text {
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.word-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.word-card:hover .word-image {
  transform: scale(1.05);
}

.word-info {
  padding: 12px;
  text-align: center;
}

.word-en {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
  word-break: break-word;
}

.word-zh {
  font-size: 12px;
  color: #909399;
}

/* 播放页面 */
.play-page {
  padding-bottom: 0;
}

.play-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 10px;
}

.cards-container {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  max-width: 500px;
}

.side-card {
  flex: 1;
  opacity: 0.5;
  cursor: pointer;
  transition: opacity 0.2s;
}

.side-card:hover {
  opacity: 0.7;
}

.mini-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.mini-card .image-wrapper {
  aspect-ratio: 1;
}

.mini-card .word-info {
  padding: 8px;
}

.mini-card .word-en {
  font-size: 10px;
}

.main-card {
  flex: 2;
}

.large-card-inner {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transform: scale(1.25);
}

.large-card-inner .image-wrapper {
  aspect-ratio: 1;
}

.large-card-inner .word-info {
  padding: 16px;
}

.large-card-inner .word-en {
  font-size: 20px;
}

.large-card-inner .word-zh {
  font-size: 16px;
}

/* 播放控制 */
.play-controls {
  background: white;
  padding: 16px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  padding-bottom: calc(16px + env(safe-area-inset-bottom, 0));
}

.control-btn {
  width: 50px;
  height: 50px;
  border: none;
  background: #f5f7fa;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}

.control-btn:hover {
  background: #e4e7ed;
  transform: scale(1.1);
}

.play-toggle-btn {
  width: 70px;
  height: 70px;
  border: none;
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  border-radius: 50%;
  font-size: 28px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
  transition: transform 0.2s, box-shadow 0.2s;
}

.play-toggle-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.5);
}

/* 底部导航 */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  display: flex;
  border-top: 1px solid #e4e7ed;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.04);
  z-index: 100;
  padding-bottom: env(safe-area-inset-bottom, 0);
}

.bottom-nav .nav-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 12px;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: background 0.2s;
}

.bottom-nav .nav-item:hover {
  background: #f5f7fa;
}

.bottom-nav .nav-item.active {
  color: #409eff;
}

.bottom-nav .nav-label {
  font-size: 14px;
  font-weight: 500;
}

/* 响应式 */
@media (min-width: 500px) {
  .group-grid, .category-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }
  
  .word-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }
}

@media (min-width: 768px) {
  .group-grid, .category-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
  
  .word-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
}
</style>
