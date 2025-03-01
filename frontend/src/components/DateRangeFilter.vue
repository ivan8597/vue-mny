<template>
  <div class="date-filter">
    <a-select v-model:value="period" style="width: 200px" @change="handlePeriodChange">
      <a-select-option value="7">Последние 7 дней</a-select-option>
      <a-select-option value="30">Последние 30 дней</a-select-option>
      <a-select-option value="90">Последние 90 дней</a-select-option>
      <a-select-option value="custom">Произвольный период</a-select-option>
    </a-select>
    
    <a-range-picker 
      v-if="period === 'custom'"
      v-model:value="dateRange"
      @change="handleDateChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { Dayjs } from 'dayjs';
import dayjs from '@/plugins/dayjs';

const period = ref('30');
const dateRange = ref<[Dayjs, Dayjs]>([dayjs().subtract(30, 'day'), dayjs()]);

const emit = defineEmits(['update:dateRange']);

const handlePeriodChange = (value: string) => {
  if (value !== 'custom') {
    const days = parseInt(value);
    dateRange.value = [dayjs().subtract(days, 'day'), dayjs()];
    emit('update:dateRange', dateRange.value);
  }
};

const handleDateChange = (dates: [Dayjs, Dayjs]) => {
  emit('update:dateRange', dates);
};
</script>

<style scoped>
.date-filter {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}
</style> 