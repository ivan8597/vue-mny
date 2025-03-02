<template>
  <MainLayout>
    <div class="savings-goals-view">
      <h1>Цели накопления</h1>
      <SavingsGoalList />
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import SavingsGoalList from '@/components/SavingsGoalList.vue'
import MainLayout from '@/layouts/MainLayout.vue'
</script>

<style scoped>
.savings-goals-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style> 