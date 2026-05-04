<script setup>
import { ref } from 'vue';
import { vocabularyData } from './data/vocabulary';

const currentCategory = ref('furniture');
const playingIndex = ref(-1);

const categoryKeys = Object.keys(vocabularyData);

function getImageUrl(word) {
  return `/images/${word}.svg`;
}

function getAudioUrl(word) {
  return `/audio/${word}.mp3`;
}

function playPronunciation(word, index) {
  playingIndex.value = index;
  
  const audio = new Audio();
  audio.src = getAudioUrl(word);
  
  audio.onended = () => {
    playingIndex.value = -1;
  };
  
  audio.onerror = () => {
    playingIndex.value = -1;
    console.error(`Failed to load audio: ${word}`);
  };
  
  audio.play().catch(() => {
    playingIndex.value = -1;
  });
  
  setTimeout(() => {
    playingIndex.value = -1;
  }, 1000);
}

function switchCategory(category) {
  currentCategory.value = category;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
</script>

<template>
  <div class="app-container">
    <!-- Header -->
    <header class="app-header">
      <div class="header-content">
        <div class="header-left">
          <span class="logo">📚</span>
          <span class="app-name">看图学英语</span>
        </div>
        <div class="header-right">
          <span class="subtitle">点击图片或单词发音</span>
        </div>
      </div>
    </header>

    <!-- Category Tabs -->
    <div class="category-tabs">
      <div class="tabs-scroll">
        <button 
          v-for="(key, index) in categoryKeys" 
          :key="key"
          class="tab-item"
          :class="{ active: currentCategory === key }"
          @click="switchCategory(key)"
        >
          <span class="tab-icon">{{ vocabularyData[key].icon }}</span>
          <span class="tab-text">{{ vocabularyData[key].name }}</span>
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <main class="main-content">
      <div class="word-grid">
        <div 
          v-for="(word, index) in vocabularyData[currentCategory].words" 
          :key="word.en"
          class="word-card"
          :class="{ playing: playingIndex === index }"
          @click="playPronunciation(word.en, index)"
        >
          <div class="card-inner">
            <div class="image-wrapper">
              <img 
                :src="getImageUrl(word.en)" 
                :alt="word.en"
                class="word-image"
                loading="lazy"
              />
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
  </div>
</template>

<style scoped>
.app-container {
  max-width: 600px;
  margin: 0 auto;
  background: #f5f7fa;
  min-height: 100vh;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
}

/* Header */
.app-header {
  background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%);
  padding: 16px 20px 20px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(255, 107, 53, 0.2);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  font-size: 28px;
}

.app-name {
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
}

.header-right {
  text-align: right;
}

.subtitle {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.9);
}

/* Category Tabs */
.category-tabs {
  background: #ffffff;
  padding: 12px 0;
  position: sticky;
  top: 68px;
  z-index: 99;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}

.tabs-scroll {
  display: flex;
  gap: 8px;
  padding: 0 16px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.tabs-scroll::-webkit-scrollbar {
  display: none;
}

.tab-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  border-radius: 20px;
  background: #f5f7fa;
  font-size: 14px;
  font-weight: 500;
  color: #606266;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.25s ease;
}

.tab-item:hover {
  background: #ebeef5;
}

.tab-item.active {
  background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(255, 107, 53, 0.3);
}

.tab-icon {
  font-size: 16px;
}

/* Main Content */
.main-content {
  padding: 16px;
}

.word-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.word-card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.word-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.word-card:active {
  transform: scale(0.98);
}

.word-card.playing {
  animation: pulse 0.5s ease;
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
  background: #f9fafc;
}

.word-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 107, 53, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
}

.play-icon {
  font-size: 40px;
  animation: bounce 0.5s ease infinite alternate;
}

@keyframes bounce {
  from { transform: scale(1); }
  to { transform: scale(1.2); }
}

.word-info {
  padding: 12px;
  text-align: center;
}

.word-en {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.word-zh {
  font-size: 13px;
  color: #909399;
}

/* Responsive */
@media (min-width: 500px) {
  .word-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
