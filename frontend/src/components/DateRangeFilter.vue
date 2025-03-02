<template>
  <div class="date-filter">
    <n-select v-model:value="period" style="width: 200px" @update:value="handlePeriodChange" :options="periodOptions" />
    
    <n-date-picker
      v-model:value="localDateRange"
      type="daterange"
      clearable
      :shortcuts="shortcuts"
      @update:value="handleDateChange"
      @confirm="handleConfirm"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { NDatePicker } from 'naive-ui';
import { Dayjs } from 'dayjs';
import dayjs from '@/plugins/dayjs';

const props = defineProps<{
  dateRange: [Dayjs, Dayjs] | null
}>();

const emit = defineEmits(['update:dateRange']);

const period = ref('30');

const localDateRange = ref<[number, number] | null>(null);

// При изменении props.dateRange обновляем локальное состояние
watch(() => props.dateRange, (newRange) => {
  if (newRange && Array.isArray(newRange) && newRange[0] && newRange[1]) {
    // Преобразуем Dayjs объекты в timestamp для n-date-picker
    localDateRange.value = [
      newRange[0].valueOf(),
      newRange[1].valueOf()
    ];
  }
}, { immediate: true });

const periodOptions = [
  { label: 'Последние 7 дней', value: '7' },
  { label: 'Последние 30 дней', value: '30' },
  { label: 'Последние 90 дней', value: '90' },
  { label: 'Произвольный период', value: 'custom' }
];

// Добавляем быстрые шаблоны выбора периодов
const shortcuts = {
  'Последние 7 дней': () => {
    const end = new Date().getTime();
    const start = new Date();
    start.setDate(start.getDate() - 7);
    return [start.getTime(), end] as [number, number];
  },
  'Последние 30 дней': () => {
    const end = new Date().getTime();
    const start = new Date();
    start.setDate(start.getDate() - 30);
    return [start.getTime(), end] as [number, number];
  },
  'Последние 90 дней': () => {
    const end = new Date().getTime();
    const start = new Date();
    start.setDate(start.getDate() - 90);
    return [start.getTime(), end] as [number, number];
  },
  'Текущая неделя': () => getDateRange(7),
  'Текущий месяц': () => getDateRange(30),
  'Последние 3 месяца': () => getDateRange(90)
};

function getDateRange(days: number): [number, number] {
  const end = new Date().getTime();
  const start = new Date();
  start.setDate(start.getDate() - days);
  return [start.getTime(), end] as [number, number];
}

const handlePeriodChange = (value: string) => {
  if (value !== 'custom') {
    const days = parseInt(value);
    const newDateRange: [Dayjs, Dayjs] = [dayjs().subtract(days, 'day'), dayjs()];
    emit('update:dateRange', newDateRange);
  }
};

const handleConfirm = () => {
  console.log('Date range confirmed')
  window.dispatchEvent(new Event('resize'))
}

const handleDateChange = (dates: [number, number] | null) => {
  console.log('Date change:', dates)
  if (!dates) {
    emit('update:dateRange', null)
    return
  }
  
  const dayjs1 = dayjs(dates[0])
  const dayjs2 = dayjs(dates[1])
  
  if (dayjs1.isValid() && dayjs2.isValid()) {
    console.log('Emitting date range:', {
      start: dayjs1.format('YYYY-MM-DD'),
      end: dayjs2.format('YYYY-MM-DD')
    })
    emit('update:dateRange', [dayjs1, dayjs2])
  }
}
</script>

<style scoped>
.date-filter {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  align-items: center;
}

.date-picker {
  min-width: 300px;
}
</style> 