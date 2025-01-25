import { defineConfig } from 'vitepress'
import sidebarItems from './sidebarItems'
// Vite 配置
const viteConfig = {
  assetsInclude: ['**/*.jpg', '**/*.JPG', '**/*.jpeg', '**/*.JPEG', '**/*.gif', '**/*.GIF']
}
export default defineConfig({
  vite: viteConfig,
  title: "Home",
  lastUpdated: true, // 使用 git 提交获取时间戳，使默认主题能够显示页面的上次更新时间
  ignoreDeadLinks: true, // 不会因死链接而使构建失败
  markdown: {
    lineNumbers: true, // 显示代码行数
    math: true, // 支持数学公式
    image: {
      // 启用图片懒加载
      lazyLoading: true
    }
  },
  description: "a place to place my soul",
  themeConfig: {
    sidebar: [
      ...sidebarItems // 合并生成的侧边栏
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/shihuaidexianyu' }
    ]
  }
})
