<template>
  <div class="main-layout">
    <n-layout>
      <n-layout-header class="header">
        <div class="logo">Vue Mny</div>
        <n-menu mode="horizontal" v-model:value="activeKey" :options="menuOptions" />
        <div class="user-actions">
          <n-button @click="handleLogout">Выйти</n-button>
        </div>
      </n-layout-header>
      
      <n-layout-content class="wide-layout">
        <slot></slot>
      </n-layout-content>
    </n-layout>
  </div>
</template>

<script setup lang="ts">
import { h, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const activeKey = ref(null)

function renderIcon(text: string) {
  return () => h('span', { class: 'menu-icon' }, text)
}

const menuOptions = [
  {
    label: 'Дашборд',
    key: 'dashboard',
    icon: renderIcon('📊'),
    onClick: () => router.push('/')
  },
  {
    label: 'Категории',
    key: 'categories',
    icon: renderIcon('📁'),
    onClick: () => router.push('/categories')
  },
  {
    label: 'Цели накопления',
    key: 'savings-goals',
    icon: renderIcon('🎯'),
    onClick: () => router.push('/savings-goals')
  }
]

const handleLogout = () => {
  authStore.logout()
}
</script>

<style scoped>
.wide-layout {
  max-width: 1800px;
  margin: 0 auto;
  padding: 0 40px;
  width: 100%;
}

.main-layout {
  min-height: 100vh;
}

.header {
  padding: 0 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.logo {
  font-size: 20px;
  font-weight: bold;
  margin-right: 40px;
}

.content {
  padding: 24px;
  background-color: #f0f2f5;
  min-height: calc(100vh - 64px);
}

.user-actions {
  margin-left: auto;
}

.menu-icon {
  font-size: 18px;
  margin-right: 4px;
}
</style> 