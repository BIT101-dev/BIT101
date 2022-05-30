/*
 * @Author: flwfdd
 * @Date: 2022-05-28 00:01:07
 * @LastEditTime: 2022-05-28 15:52:08
 * @Description: 
 * _(:з」∠)_
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
const path = require('path');

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Components({
    resolvers: [NaiveUiResolver()]
  })],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, "src")
    }
  }
})
