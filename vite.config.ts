/*
 * @Author: flwfdd
 * @Date: 2022-05-28 00:01:07
 * @LastEditTime: 2023-09-17 15:52:25
 * @Description: 
 * _(:з」∠)_
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Components({
    resolvers: [NaiveUiResolver()]
  })],
  resolve: {
    alias: {
      '@': resolve(__dirname, "src")
    }
  },
  server: {
    port: 3000,
  }
})
