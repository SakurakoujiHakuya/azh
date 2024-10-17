import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [vue()],
// })


// vite.config.js
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/upload': 'http://localhost:3000',
      '/run-script': 'http://localhost:3000',
      '/output': 'http://localhost:3000'
    }
  }
});