import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: '../dist',  // 构建输出到上级的dist目录
    emptyOutDir: true,
  }
})