<template>
  <n-card title="Фильтры">
    <n-space vertical>
      <n-select
        v-model:value="period"
        :options="periodOptions"
        placeholder="Выберите период"
      />
      <n-date-picker
        v-if="period === 'custom'"
        v-model:value="dateRange"
        type="daterange"
        :shortcuts="shortcuts"
        start-placeholder="Начало"
        end-placeholder="Конец"
      />
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { NCard, NSpace, NSelect, NDatePicker } from 'naive-ui'

const emit = defineEmits(['filter'])

const period = ref('month')
const dateRange = ref<[number, number] | null>(null)

const periodOptions = [
  { label: 'Этот месяц', value: 'month' },
  { label: 'Этот квартал', value: 'quarter' },
  { label: 'Этот год', value: 'year' },
  { label: 'Произвольный период', value: 'custom' }
]

const shortcuts = {
  'Последние 7 дней': () => getDateRange(7),
  'Последние 30 дней': () => getDateRange(30),
  'Последние 90 дней': () => getDateRange(90)
}

function getDateRange(days: number): [number, number] {
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - days)
  return [start.getTime(), end.getTime()]
}

watch([period, dateRange], () => {
  let range: [Date, Date]
  
  if (period.value === 'custom' && dateRange.value) {
    range = [new Date(dateRange.value[0]), new Date(dateRange.value[1])]
  } else {
    const end = new Date()
    const start = new Date()
    
    switch (period.value) {
      case 'month':
        start.setDate(1)
        break
      case 'quarter':
        start.setMonth(Math.floor(start.getMonth() / 3) * 3)
        start.setDate(1)
        break
      case 'year':
        start.setMonth(0)
        start.setDate(1)
        break
    }
    
    range = [start, end]
  }
  
  emit('filter', range)
})
</script> 