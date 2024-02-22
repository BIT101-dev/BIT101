<template>
  <n-config-provider
      :theme-overrides="themeOverrides"
      :theme="theme"
    >
    <n-loading-bar-provider :loading-bar-style="{
      loading: {
        backgroundColor: 'var(--loading-bar-color)',
        boxShadow: 'var(--loading-bar-shadow)'
      }
    }">
      <GlobalComponents></GlobalComponents>
      <App />
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { GlobalThemeOverrides, darkTheme, lightTheme, useOsTheme } from 'naive-ui'
import LightThemeOverrides from '@/utils/naive-ui-light-theme-overrides.json'
import DarkThemeOverrides from '@/utils/naive-ui-dark-theme-overrides.json'
import GlobalComponents from '@/components/GlobalComponents.vue';
import App from "@/App.vue"

import "@/utils/globalThemeVars.css"
import { ref, watch } from 'vue';

const isDark = useOsTheme()
watch(isDark, () => {
  theme.value = isDark.value === "dark" ? darkTheme : lightTheme
})

const theme = ref<typeof darkTheme | typeof lightTheme>(isDark.value === "dark" ? darkTheme : lightTheme)
const themeOverrides = ref<GlobalThemeOverrides>(isDark.value === "dark" ? DarkThemeOverrides : LightThemeOverrides);
</script>

<style>
@font-face {
  font-family: "Noto Serif";
  src: local("Noto Serif SC Light"),
    local("Noto Serif SC"),
    local("Noto Serif CJK Light"),
    local("Noto Serif CJK"),
    local("Source Han Serif CN Light"),
    local("Source Han Serif CN");
  font-display: swap;
  font-weight: 300;
}

@font-face {
  font-family: "Noto Serif";
  src: local("Noto Serif SC Medium"),
    local("Noto Serif SC"),
    local("Noto Serif CJK Medium"),
    local("Noto Serif CJK"),
    local("Source Han Serif CN Medium"),
    local("Source Han Serif CN");
  font-display: swap;
  font-weight: 500;
}

@font-face {
  font-family: "Noto Serif";
  src: local("Noto Serif SC Bold"),
    local("Noto Serif CJK Bold"),
    local("Source Han Serif CN Bold");
  font-display: swap;
  font-weight: 700;
}

@font-face {
  font-family: "Noto Serif";
  src: local("Noto Serif SC Heavy"),
    local("Noto Serif CJK Heavy"),
    local("Source Han Serif CN Heavy");
  font-display: swap;
  font-weight: 800;
}

#app,
body {
  font-family: "Noto Serif", "Noto Serif SC", sans-serif;
  font-style: normal;
  font-weight: 500;
  font-size: 16px;
}

.container {
  max-width: 666px;
  margin: auto;
}

::selection {
  color: #fff;
  background: #00bcd4;
}
</style>
