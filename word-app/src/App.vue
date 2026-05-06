<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { vocabularyData } from './data/vocabulary';

// 页面状态
const currentPage = ref('home'); // 'home', 'random', 'category', 'play', 'debug'

// 分类选择
const selectedGroup = ref(null);
const selectedCategory = ref(null);

// 播放模式
const isPlaying = ref(false);
const currentPlayIndex = ref(0);
const playWords = ref([]);
let playTimer = null;

// 调试模式
const debugMode = ref(false);
const badImages = ref([]);

const groupKeys = computed(() => Object.keys(vocabularyData));

function loadBadImages() {
  try {
    const saved = localStorage.getItem('badImages');
    if (saved) {
      badImages.value = JSON.parse(saved);
    }
  } catch (e) {
    badImages.value = [];
  }
}

function saveBadImages() {
  localStorage.setItem('badImages', JSON.stringify(badImages.value));
}

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

function goToDebug() {
  currentPage.value = 'debug';
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
  
  let playCount = 0;
  const playNext = () => {
    if (playCount >= 3) {
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

function markBadImage(word, zh, group, category) {
  const existing = badImages.value.find(item => item.en === word);
  if (!existing) {
    badImages.value.push({
      en: word,
      zh: zh,
      group: group,
      category: category,
      markedAt: new Date().toISOString()
    });
    saveBadImages();
  }
}

function removeBadImage(word) {
  badImages.value = badImages.value.filter(item => item.en !== word);
  saveBadImages();
}

function isBadImage(word) {
  return badImages.value.some(item => item.en === word);
}

function toggleDebugMode() {
  debugMode.value = !debugMode.value;
}

onMounted(() => {
  loadBadImages();
});

onUnmounted(() => {
  stopPlay();
});
</script>

<template>
  <div class="app-container">
    <!-- 调试模式指示器 -->
    <div v-if="debugMode" class="debug-indicator">
      <span>🔧 调试模式</span>
    </div>
    
    <!-- 首页 -->
    <div v-if="currentPage === 'home'" class="page-content">
      <header class="page-header">
        <h1 class="page-title">
          <span class="title-icon">📚</span>
          <span>Picture English</span>
        </h1>
        <div class="header-actions">
          <button class="debug-toggle-btn" @click="toggleDebugMode">
            {{ debugMode ? '关闭调试' : '调试模式' }}
          </button>
          <button v-if="badImages.length > 0" class="bad-images-btn" @click="goToDebug">
            📝 待审核 ({{ badImages.length }})
          </button>
        </div>
      </header>
      
      <main class="home-content">
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
                <!-- 调试模式下显示标记按钮 -->
                <button
                  v-if="debugMode"
                  class="mark-bad-btn"
                  :class="{ marked: isBadImage(word.en) }"
                  @click.stop="markBadImage(word.en, word.zh, selectedCategory?.name, selectedCategory?.name)"
                  :title="isBadImage(word.en) ? '已标记不合适' : '标记为不合适'"
                >
                  {{ isBadImage(word.en) ? '✓' : '⚠️' }}
                </button>
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
          <div class="side-card" @click="prevCard">
            <div v-if="getPrevWord()" class="mini-card">
              <div class="image-wrapper">
                <img
                  :src="getImageUrl(getPrevWord())"
                  :alt="getPrevWord().en"
                  class="word-image"
                  @error="(e) => { e.target.style.display = 'none'; }"
                />
                <button
                  v-if="debugMode"
                  class="mark-bad-btn small"
                  :class="{ marked: isBadImage(getPrevWord()?.en) }"
                  @click.stop="markBadImage(getPrevWord()?.en, getPrevWord()?.zh, '', '')"
                >
                  {{ isBadImage(getPrevWord()?.en) ? '✓' : '⚠️' }}
                </button>
              </div>
              <div class="word-info">
                <div class="word-en">{{ getPrevWord()?.en }}</div>
              </div>
            </div>
          </div>
          
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
                <button
                  v-if="debugMode"
                  class="mark-bad-btn large"
                  :class="{ marked: isBadImage(getCurrentWord()?.en) }"
                  @click.stop="markBadImage(getCurrentWord()?.en, getCurrentWord()?.zh, '', '')"
                  :title="isBadImage(getCurrentWord()?.en) ? '已标记不合适' : '标记为不合适'"
                >
                  {{ isBadImage(getCurrentWord()?.en) ? '✓' : '⚠️' }}
                </button>
              </div>
              <div class="word-info">
                <div class="word-en">{{ getCurrentWord()?.en }}</div>
                <div class="word-zh">{{ getCurrentWord()?.zh }}</div>
              </div>
            </div>
          </div>
          
          <div class="side-card" @click="nextCard">
            <div v-if="getNextWord()" class="mini-card">
              <div class="image-wrapper">
                <img
                  :src="getImageUrl(getNextWord())"
                  :alt="getNextWord().en"
                  class="word-image"
                  @error="(e) => { e.target.style.display = 'none'; }"
                />
                <button
                  v-if="debugMode"
                  class="mark-bad-btn small"
                  :class="{ marked: isBadImage(getNextWord()?.en) }"
                  @click.stop="markBadImage(getNextWord()?.en, getNextWord()?.zh, '', '')"
                >
                  {{ isBadImage(getNextWord()?.en) ? '✓' : '⚠️' }}
                </button>
              </div>
              <div class="word-info">
                <div class="word-en">{{ getNextWord()?.en }}</div>
              </div>
            </div>
          </div>
        </div>
      </main>
      
      <div class="play-controls">
        <button class="control-btn" @click="prevCard">⏮️</button>
        <button class="play-toggle-btn" @click="togglePlay">
          <span v-if="isPlaying">⏸️</span>
          <span v-else>▶️</span>
        </button>
        <button class="control-btn" @click="nextCard">⏭️</button>
      </div>
    </div>
    
    <!-- 调试页面 - 待审核图片 -->
    <div v-else-if="currentPage === 'debug'" class="page-content">
      <header class="page-header">
        <button class="back-btn" @click="goToHome">
          <span>← 返回</span>
        </button>
        <h1 class="page-title">
          <span>📝</span>
          <span>待审核图片</span>
        </h1>
        <span class="bad-count">{{ badImages.length }} 个</span>
      </header>
      
      <main class="debug-content">
        <div v-if="badImages.length === 0" class="empty-state">
          <span class="empty-icon">✅</span>
          <p>没有待审核的图片</p>
          <p class="empty-hint">在调试模式下点击图片右上角的⚠️按钮标记不合适的图片</p>
        </div>
        
        <div v-else class="bad-images-grid">
          <div
            v-for="item in badImages"
            :key="item.en"
            class="bad-image-card"
          >
            <div class="image-wrapper">
              <img
                :src="getImageUrl(item)"
                :alt="item.en"
                class="word-image"
                @error="(e) => { e.target.style.display = 'none'; e.target.parentElement.querySelector('.no-image').style.display = 'flex'; }"
              />
              <div class="no-image" style="display: none;">
                <span class="no-image-icon">📝</span>
                <span class="no-image-text">{{ item.en }}</span>
              </div>
            </div>
            <div class="word-info">
              <div class="word-en">{{ item.en }}</div>
              <div class="word-zh">{{ item.zh }}</div>
              <div class="word-category">{{ item.category }}</div>
            </div>
            <div class="action-buttons">
              <button class="action-btn approve-btn" @click="removeBadImage(item.en)">
                ✅ 符合
              </button>
              <button class="action-btn reject-btn">
                ❌ 不符合
              </button>
            </div>
          </div>
        </div>
      </main>
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

.debug-indicator {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: #f59e0b;
  color: white;
  padding: 4px 12px;
  text-align: center;
  font-size: 12px;
  font-weight: 500;
  z-index: 200;
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
  top: 30px;
  z-index: 100;
}

.debug-mode-on .page-header {
  top: 42px;
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

.header-actions {
  display: flex;
  gap: 8px;
}

.debug-toggle-btn {
  padding: 6px 12px;
  border: 1px solid #f59e0b;
  background: #fffbeb;
  border-radius: 6px;
  font-size: 12px;
  color: #d97706;
  cursor: pointer;
  transition: all 0.2s;
}

.debug-toggle-btn:hover {
  background: #fef3c7;
}

.bad-images-btn {
  padding: 6px 12px;
  border: none;
  background: #fef2f2;
  border-radius: 6px;
  font-size: 12px;
  color: #dc2626;
  cursor: pointer;
  transition: all 0.2s;
}

.bad-images-btn:hover {
  background: #fee2e2;
}

.bad-count {
  font-size: 14px;
  color: #dc2626;
  font-weight: 500;
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

.home-content, .category-content, .debug-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.group-grid, .category-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  padding-bottom: 100px;
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

.word-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  padding-bottom: 100px;
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

.word-category {
  font-size: 10px;
  color: #a0aec0;
}

/* 标记按钮 */
.mark-bad-btn {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  z-index: 10;
}

.mark-bad-btn:hover {
  background: rgba(0, 0, 0, 0.8);
  transform: scale(1.1);
}

.mark-bad-btn.marked {
  background: #dc2626;
}

.mark-bad-btn.small {
  width: 20px;
  height: 20px;
  font-size: 10px;
}

.mark-bad-btn.large {
  width: 36px;
  height: 36px;
  font-size: 16px;
}

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
  transform: scale(1.5);
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

/* 调试页面 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 16px;
  color: #64748b;
  margin: 8px 0;
}

.empty-hint {
  font-size: 12px !important;
  color: #94a3b8 !important;
}

.bad-images-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  padding-bottom: 100px;
}

.bad-image-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.bad-image-card .image-wrapper {
  aspect-ratio: 1;
}

.bad-image-card .word-info {
  padding: 10px;
}

.action-buttons {
  display: flex;
  gap: 4px;
  padding: 0 10px 10px;
}

.action-btn {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.approve-btn {
  background: #dcfce7;
  color: #16a34a;
}

.approve-btn:hover {
  background: #bbf7d0;
}

.reject-btn {
  background: #fee2e2;
  color: #dc2626;
}

.reject-btn:hover {
  background: #fecaca;
}

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

@media (min-width: 500px) {
  .group-grid, .category-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }
  
  .word-grid, .bad-images-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }
}

@media (min-width: 768px) {
  .group-grid, .category-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
  
  .word-grid, .bad-images-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
}
</style>
