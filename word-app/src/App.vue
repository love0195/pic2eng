<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { vocabularyData } from './data/vocabulary';

const currentGroup = ref(Object.keys(vocabularyData)[0]);
const currentCategory = ref('');
const playingIndex = ref(-1);
const showMobileNav = ref(false);
const touchStartX = ref(0);
const touchEndX = ref(0);

const groupKeys = computed(() => Object.keys(vocabularyData));

const currentGroupData = computed(() => vocabularyData[currentGroup.value]);

const categoryKeys = computed(() => {
  if (!currentGroupData.value) return [];
  return Object.keys(currentGroupData.value.categories);
});

const currentWords = computed(() => {
  if (!currentCategory.value || !currentGroupData.value) return [];
  const category = currentGroupData.value.categories[currentCategory.value];
  return category ? category.words : [];
});

const totalWordsCount = computed(() => {
  if (!currentGroupData.value) return 0;
  return Object.values(currentGroupData.value.categories)
    .reduce((sum, cat) => sum + cat.words.length, 0);
});

function initCategory() {
  if (categoryKeys.value.length > 0 && !currentCategory.value) {
    currentCategory.value = categoryKeys.value[0];
  }
}

function switchGroup(groupKey) {
  currentGroup.value = groupKey;
  currentCategory.value = '';
  initCategory();
  showMobileNav.value = false;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function switchCategory(categoryKey) {
  currentCategory.value = categoryKey;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function getImageUrl(word) {
  return `/images/${word.en}.jpg`;
}

function getAudioUrl(word) {
  return `/audio/${word.en}.mp3`;
}

function playPronunciation(word, index) {
  playingIndex.value = index;
  
  const wordParts = word.en.split('_');
  
  async function playParts() {
    for (let i = 0; i < wordParts.length; i++) {
      const part = wordParts[i];
      const audio = new Audio();
      audio.src = getAudioUrl(part);
      
      await new Promise((resolve) => {
        audio.onended = resolve;
        audio.onerror = resolve;
        audio.play().catch(resolve);
        
        setTimeout(() => resolve(), 2000);
      });
      
      if (i < wordParts.length - 1) {
        await new Promise(r => setTimeout(r, 300));
      }
    }
    playingIndex.value = -1;
  }
  
  playParts();
  
  setTimeout(() => {
    playingIndex.value = -1;
  }, 2000 * wordParts.length + 500);
}

function handleTouchStart(e) {
  touchStartX.value = e.touches[0].clientX;
}

function handleTouchMove(e) {
  touchEndX.value = e.touches[0].clientX;
}

function handleTouchEnd() {
  const diff = touchStartX.value - touchEndX.value;
  const threshold = 80;
  
  if (Math.abs(diff) > threshold) {
    const currentIndex = groupKeys.value.indexOf(currentGroup.value);
    if (diff > 0 && currentIndex < groupKeys.value.length - 1) {
      switchGroup(groupKeys.value[currentIndex + 1]);
    } else if (diff < 0 && currentIndex > 0) {
      switchGroup(groupKeys.value[currentIndex - 1]);
    }
  }
  
  touchStartX.value = 0;
  touchEndX.value = 0;
}

function handleKeyDown(e) {
  if (e.key === 'Escape') {
    showMobileNav.value = false;
  }
}

onMounted(() => {
  initCategory();
  document.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyDown);
});
</script>

<template>
  <div 
    class="app-container"
    @touchstart="handleTouchStart"
    @touchmove="handleTouchMove"
    @touchend="handleTouchEnd"
  >
    <header class="app-header">
      <div class="header-content">
        <div class="header-left">
          <span class="logo">{{ currentGroupData?.icon || '📚' }}</span>
          <div class="header-text">
            <span class="app-name">看图学英语</span>
            <span class="group-name">{{ currentGroupData?.groupName || '' }}</span>
          </div>
        </div>
        <div class="header-right">
          <span class="word-count">{{ totalWordsCount }} 词</span>
          <button class="nav-toggle" @click="showMobileNav = !showMobileNav">
            <span class="nav-icon">☰</span>
          </button>
        </div>
      </div>
    </header>

    <nav class="group-nav" :class="{ 'show': showMobileNav }">
      <div class="nav-overlay" @click="showMobileNav = false"></div>
      <div class="nav-content">
        <div class="nav-header">
          <span>选择分类</span>
          <button class="close-btn" @click="showMobileNav = false">✕</button>
        </div>
        <div class="group-list">
          <button
            v-for="groupKey in groupKeys"
            :key="groupKey"
            class="group-item"
            :class="{ active: currentGroup === groupKey }"
            @click="switchGroup(groupKey); showMobileNav = false"
          >
            <span class="group-icon">{{ vocabularyData[groupKey].icon }}</span>
            <span class="group-name-text">{{ vocabularyData[groupKey].groupName }}</span>
            <span class="group-count">
              {{ Object.keys(vocabularyData[groupKey].categories).length }} 个分类
            </span>
          </button>
        </div>
      </div>
    </nav>

    <div class="category-tabs">
      <div class="tabs-scroll">
        <button 
          v-for="catKey in categoryKeys" 
          :key="catKey"
          class="tab-item"
          :class="{ active: currentCategory === catKey }"
          @click="switchCategory(catKey)"
        >
          <span class="tab-icon">{{ currentGroupData?.categories[catKey]?.icon }}</span>
          <span class="tab-text">{{ currentGroupData?.categories[catKey]?.name }}</span>
          <span class="tab-count">{{ currentGroupData?.categories[catKey]?.words?.length }}</span>
        </button>
      </div>
    </div>

    <div class="category-info">
      <span class="category-title">
        {{ currentGroupData?.categories[currentCategory]?.icon }}
        {{ currentGroupData?.categories[currentCategory]?.name }}
      </span>
      <span class="category-subtitle">点击卡片听发音</span>
    </div>

    <main class="main-content">
      <div class="word-grid">
        <div 
          v-for="(word, index) in currentWords" 
          :key="word.en"
          class="word-card"
          :class="{ playing: playingIndex === index }"
          @click="playPronunciation(word, index)"
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
              <div class="play-overlay" v-if="playingIndex === index">
                <span class="play-icon">🔊</span>
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

    <footer class="app-footer">
      <div class="swipe-hint">
        <span class="hint-icon">👆</span>
        <span>左右滑动切换分类</span>
      </div>
    </footer>
  </div>
</template>

<style scoped>
* {
  -webkit-tap-highlight-color: transparent;
  -webkit-touch-callout: none;
}

.app-container {
  max-width: 100%;
  margin: 0 auto;
  background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
  min-height: 100vh;
  padding-bottom: env(safe-area-inset-bottom);
  user-select: none;
  overflow-x: hidden;
}

.app-header {
  background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%);
  padding: 12px 16px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 600px;
  margin: 0 auto;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  font-size: 32px;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.header-text {
  display: flex;
  flex-direction: column;
}

.app-name {
  font-size: 18px;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.group-name {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.9);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.word-count {
  background: rgba(255, 255, 255, 0.2);
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 12px;
  color: #ffffff;
  font-weight: 500;
}

.nav-toggle {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.nav-toggle:active {
  transform: scale(0.95);
  background: rgba(255, 255, 255, 0.3);
}

.group-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 200;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
}

.group-nav.show {
  pointer-events: auto;
  opacity: 1;
}

.nav-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
}

.nav-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 85%;
  max-width: 320px;
  height: 100%;
  background: #ffffff;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  transform: translateX(-100%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow-y: auto;
}

.group-nav.show .nav-content {
  transform: translateX(0);
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 16px;
  border-bottom: 1px solid #eef2f7;
  background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%);
  color: #ffffff;
  font-weight: 600;
  font-size: 16px;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.group-list {
  padding: 12px;
}

.group-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: none;
  border-radius: 12px;
  background: #f8fafc;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 8px;
  text-align: left;
}

.group-item:active {
  transform: scale(0.98);
  background: #eef2f7;
}

.group-item.active {
  background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%);
  color: #ffffff;
}

.group-icon {
  font-size: 28px;
}

.group-name-text {
  flex: 1;
  font-size: 15px;
  font-weight: 500;
}

.group-count {
  font-size: 11px;
  color: #909399;
  background: #eef2f7;
  padding: 4px 8px;
  border-radius: 10px;
}

.group-item.active .group-count {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
}

.category-tabs {
  background: #ffffff;
  padding: 10px 0;
  position: sticky;
  top: 60px;
  z-index: 99;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.tabs-scroll {
  display: flex;
  gap: 8px;
  padding: 0 12px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  scroll-snap-type: x mandatory;
}

.tabs-scroll::-webkit-scrollbar {
  display: none;
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 10px 14px;
  border: none;
  border-radius: 12px;
  background: #f5f7fa;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
  min-width: 70px;
  scroll-snap-align: start;
  flex-shrink: 0;
}

.tab-item:active {
  transform: scale(0.95);
}

.tab-item.active {
  background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
}

.tab-icon {
  font-size: 22px;
}

.tab-text {
  font-size: 11px;
  font-weight: 600;
}

.tab-count {
  font-size: 10px;
  background: rgba(0, 0, 0, 0.08);
  padding: 2px 6px;
  border-radius: 8px;
}

.tab-item.active .tab-count {
  background: rgba(255, 255, 255, 0.25);
}

.category-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  max-width: 600px;
  margin: 0 auto;
}

.category-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.category-subtitle {
  font-size: 12px;
  color: #909399;
}

.main-content {
  padding: 8px 12px 100px;
  max-width: 600px;
  margin: 0 auto;
}

.word-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.word-card {
  background: #ffffff;
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.word-card:active {
  transform: scale(0.97);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.word-card.playing {
  animation: pulse 0.5s ease;
  box-shadow: 0 4px 16px rgba(255, 107, 53, 0.3);
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.03); }
}

.card-inner {
  display: flex;
  flex-direction: column;
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

.word-card:active .word-image {
  transform: scale(1.05);
}

.play-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 107, 53, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.15s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.play-icon {
  font-size: 36px;
  animation: bounce 0.4s ease infinite alternate;
}

@keyframes bounce {
  from { transform: scale(1); }
  to { transform: scale(1.15); }
}

.word-info {
  padding: 10px;
  text-align: center;
}

.word-en {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 2px;
  line-height: 1.3;
}

.word-zh {
  font-size: 12px;
  color: #909399;
}

.app-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px;
  padding-bottom: calc(12px + env(safe-area-inset-bottom));
  background: linear-gradient(180deg, rgba(248, 250, 252, 0) 0%, rgba(248, 250, 252, 0.95) 20%, rgba(248, 250, 252, 1) 100%);
  pointer-events: none;
}

.swipe-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 12px;
  color: #c0c4cc;
}

.hint-icon {
  font-size: 16px;
}

@media (min-width: 500px) {
  .word-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }
  
  .word-en {
    font-size: 15px;
  }
  
  .word-zh {
    font-size: 13px;
  }
  
  .app-footer {
    display: none;
  }
}

@media (min-width: 768px) {
  .word-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
  
  .main-content {
    padding: 16px 24px 120px;
  }
  
  .nav-toggle {
    display: none;
  }
}
</style>
