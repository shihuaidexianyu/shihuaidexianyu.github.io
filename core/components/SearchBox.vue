<template>
    <div class="search-container">
        <div class="search-box">
            <div class="engine-indicator">
                <div class="engine-status">
                    <div class="status-dot" :class="{ active: engineStatus.google }"></div>
                    <div class="status-dot" :class="{ active: engineStatus.bing }"></div>
                </div>
            </div>

            <input type="text" v-model="searchQuery" @keyup.enter="handleSearch(searchQuery)" :placeholder="placeholder"
                class="search-input" />

            <button @click="handleSearch(searchQuery)" class="search-button">
                <svg class="search-icon" viewBox="0 0 24 24">
                    <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 
                             16 11.11 16 9.5 16 5.91 13.09 3 9.5 
                             3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 
                             0 3.09-.59 4.23-1.57l.27.28v.79l5 
                             4.99L20.49 19l-4.99-5zm-6 0C7.01 
                             14 5 11.99 5 9.5S7.01 5 9.5 5 14 
                             7.01 14 9.5 11.99 14 9.5 14z" />
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const searchQuery = ref('')
const placeholder = ref('')

const SEARCH_URLS = {
    google: 'https://www.google.com/search?q=',
    bing: 'https://www.bing.com/search?q='
}

const engineStatus = ref({
    google: false,
    bing: true,
    currentEngine: 'bing'
})

// 检测搜索引擎可用性
const checkSearchEngine = async (engine, retries = 2) => {
    // 为每个引擎定义多个检测端点
    const checkUrls = {
        google: ['https://www.google.com/favicon.ico', 'https://www.google.com/generate_204'],
        bing: ['https://www.bing.com/favicon.ico', 'https://www.bing.com/ping'],
    }[engine] || [`https://${engine}.com/favicon.ico`];

    for (let attempt = 0; attempt < retries; attempt++) {
        for (const url of checkUrls) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 3000);

                const response = await fetch(url, {
                    mode: 'no-cors',
                    cache: 'no-cache',
                    signal: controller.signal
                });

                clearTimeout(timeoutId);
                return true;
            } catch (error) {
                const errorType = error.name === 'AbortError' ? 'timeout' : 'network';
                console.warn(
                    `[Attempt ${attempt + 1}] ${engine} check failed:`,
                    `\nURL: ${url}`,
                    `\nType: ${errorType}`,
                    `\nError: ${error.message}`
                );
                continue;
            }
        }
        // 重试之间添加延迟
        if (attempt < retries - 1) {
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
    return false;
}

// 执行搜索
const handleSearch = (query) => {
    if (!query.trim()) return
    const engine = engineStatus.value.currentEngine
    const searchUrl = SEARCH_URLS[engine] + encodeURIComponent(query)
    window.open(searchUrl, '_blank')
}

// 添加调试日志
const updateEngineStatus = async () => {
    console.log('开始检查引擎状态');
    const googleStatus = await checkSearchEngine('google');
    const bingStatus = await checkSearchEngine('bing');
    console.log('检查结果:', { google: googleStatus, bing: bingStatus });

    engineStatus.value.google = googleStatus;
    engineStatus.value.bing = bingStatus;
    engineStatus.value.currentEngine = googleStatus ? 'google' : (bingStatus ? 'bing' : null);

    console.log('更新后的状态:', engineStatus.value);
};

onMounted(() => {
    updateEngineStatus()
})
</script>

<style scoped>
:root {
    --search-bg-light: rgba(255, 255, 255, 0.85);
    --search-bg-dark: rgba(29, 29, 29, 0.85);
    --search-shadow: rgba(0, 0, 0, 0.15);
    --search-shadow-hover: rgba(0, 0, 0, 0.25);
    --status-active: #10b981;
    --status-inactive: #ef4444;
}

.search-container {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    padding: 1rem;
    transition: all 0.3s ease;
}

.search-box {
    display: flex;
    align-items: center;
    background: var(--search-bg-light);
    backdrop-filter: blur(8px) saturate(150%);
    -webkit-backdrop-filter: blur(8px) saturate(150%);
    border: 1px solid var(--search-bg-light);
    border-radius: 16px;
    padding: 0.75rem;
    box-shadow: 0 8px 32px var(--search-shadow);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.search-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 48px var(--search-shadow-hover);
    border-color: rgba(255, 255, 255, 0.4);
}

.search-input {
    flex: 1;
    border: none;
    background: transparent;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    color: var(--vp-c-text-1);
    outline: none;
}
.search-button {
    background: none;
    border: none;
    padding: 0.5rem;
    cursor: pointer;
    opacity: 0.7;
    transition: all 0.2s ease;
}

.search-button:hover {
    opacity: 1;
    transform: scale(1.1);
}

.search-icon {
    width: 20px;
    height: 20px;
    fill: var(--vp-c-text-2);
}

.engine-status {
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 4px;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #ef4444;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.status-dot.active {
    background-color: #10b981;
}

/* 保持暗色模式的现有样式 */
@media (prefers-color-scheme: dark) {
    .search-box {
        background: var(--search-bg-dark);
        border-color: var(--search-bg-dark);
    }

    .search-box:hover {
        border-color: rgba(255, 255, 255, 0.15);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.45);
    }

    .status-dot {
        opacity: 0.8;
    }
}

@media (max-width: 768px) {
    .search-container {
        padding: 0.5rem;
    }

    .search-box {
        padding: 0.5rem;
    }

    .search-input {
        font-size: 0.9rem;
        padding: 0.4rem 0.75rem;
    }

}

@media (max-width: 480px) {
    .search-input {
        font-size: 0.875rem;
    }
}
</style>
