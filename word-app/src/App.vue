<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { vocabularyData } from './data/vocabulary';

const currentGroup = ref(Object.keys(vocabularyData)[0]);
const currentCategory = ref('');
const playingIndex = ref(-1);
const showMobileNav = ref(false);

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
  const wordStr = typeof word === 'string' ? word : word.en;
  return `/audio/${wordStr}.mp3`;
}

function playPronunciation(word, index) {
  playingIndex.value = index;
  
  const wordParts = word.en.split('_');
  
  if (wordParts.length > 1) {
    playWordPartsSequentially(wordParts, 0);
  } else {
    const audio = new Audio();
    audio.src = getAudioUrl(word.en);
    
    audio.onended = () => {
      playingIndex.value = -1;
    };
    
    audio.onerror = () => {
      playingIndex.value = -1;
    };
    
    audio.play().catch(() => {
      playingIndex.value = -1;
    });
  }
}

function playWordPartsSequentially(parts, currentIndex) {
  if (currentIndex >= parts.length) {
    playingIndex.value = -1;
    return;
  }
  
  const part = parts[currentIndex];
  const audio = new Audio();
  audio.src = getAudioUrl(part);
  
  let hasStarted = false;
  
  audio.oncanplay = () => {
    if (!hasStarted) {
      hasStarted = true;
      audio.play().catch(() => {
        setTimeout(() => {
          playWordPartsSequentially(parts, currentIndex + 1);
        }, 300);
      });
    }
  };
  
  audio.onended = () => {
    setTimeout(() => {
      playWordPartsSequentially(parts, currentIndex + 1);
    }, 200);
  };
  
  audio.onerror = () => {
    setTimeout(() => {
      playWordPartsSequentially(parts, currentIndex + 1);
    }, 200);
  };
  
  setTimeout(() => {
    if (!hasStarted) {
      playWordPartsSequentially(parts, currentIndex + 1);
    }
  }, 3000);
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
  >
    <header class="app-header">
      <div class="header-content">
        <h1 class="app-title">
          <span class="title-icon">📚</span>
          <span>Picture English</span>
        </h1>
        <button 
          class="nav-toggle"
          @click="showMobileNav = !showMobileNav"
        >
          <span v-if="!showMobileNav">☰</span>
          <span v-else>✕</span>
        </button>
      </div>
    </header>

    <nav 
      class="nav-menu"
      :class="{ 'mobile-open': showMobileNav }"
    >
      <div class="nav-content">
        <div class="nav-section">
          <div class="nav-items">
            <button
              v-for="group in groupKeys"
              :key="group"
              class="nav-item"
              :class="{ active: currentGroup === group }"
              @click="switchGroup(group)"
            >
              <span class="nav-icon">{{ vocabularyData[group].icon }}</span>
              <span class="nav-label">{{ vocabularyData[group].groupName }}</span>
            </button>
          </div>
        </div>
        
        <div class="category-tabs" v-if="currentGroupData">
          <div class="category-scroll">
            <button
              v-for="catKey in categoryKeys"
              :key="catKey"
              class="category-tab"
              :class="{ active: currentCategory === catKey }"
              @click="switchCategory(catKey)"
            >
              <span class="tab-icon">{{ currentGroupData.categories[catKey].icon }}</span>
              <span class="tab-label">{{ currentGroupData.categories[catKey].name }}</span>
            </button>
          </div>
        </div>
      </div>
    </nav>

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
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
}

.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.header-content {
  max-width: 600px;
  margin: 0 auto;
  padding: 16px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.app-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  font-size: 24px;
}

.nav-toggle {
  display: none;
  padding: 8px 12px;
  border: none;
  background: #f5f7fa;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s;
}

.nav-toggle:hover {
  background: #e4e7ed;
}

.nav-menu {
  position: sticky;
  top: 60px;
  z-index: 90;
  background: white;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
}

.nav-content {
  max-width: 600px;
  margin: 0 auto;
  padding: 12px 16px;
}

.nav-section {
  margin-bottom: 12px;
}

.nav-items {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border: 1px solid #e4e7ed;
  background: white;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.nav-item:hover {
  border-color: #409eff;
  color: #409eff;
}

.nav-item.active {
  background: #409eff;
  border-color: #409eff;
  color: white;
}

.nav-icon {
  font-size: 16px;
}

.category-tabs {
  border-top: 1px solid #f0f0f0;
  padding-top: 12px;
}

.category-scroll {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
  -webkit-overflow-scrolling: touch;
}

.category-scroll::-webkit-scrollbar {
  display: none;
}

.category-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: none;
  background: #f5f7fa;
  border-radius: 16px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  flex-shrink: 0;
}

.category-tab:hover {
  background: #e4e7ed;
}

.category-tab.active {
  background: #67c23a;
  color: white;
}

.tab-icon {
  font-size: 14px;
}

.main-content {
  padding: 8px 12px 40px;
  max-width: 600px;
  margin: 0 auto;
}

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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.word-card.playing {
  transform: scale(1.02);
}

.card-inner {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: box-shadow 0.2s;
}

.word-card.playing .card-inner {
  box-shadow: 0 4px 16px rgba(64, 158, 255, 0.2);
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

.play-overlay {
  position: absolute;
  inset: 0;
  background: rgba(64, 158, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: pulse 1s infinite;
}

.play-icon {
  font-size: 32px;
  animation: bounce 0.6s infinite alternate;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.8;
  }
  50% {
    opacity: 1;
  }
}

@keyframes bounce {
  from {
    transform: scale(1);
  }
  to {
    transform: scale(1.2);
  }
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
}

@media (min-width: 768px) {
  .word-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
  
  .main-content {
    padding: 16px 24px 40px;
  }
  
  .nav-toggle {
    display: none;
  }
}

@media (max-width: 767px) {
  .nav-toggle {
    display: block;
  }
  
  .nav-items {
    display: none;
  }
  
  .nav-menu.mobile-open .nav-items {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding-top: 12px;
    border-top: 1px solid #f0f0f0;
  }
  
  .nav-menu.mobile-open .nav-section {
    margin-bottom: 0;
  }
}
</style>
