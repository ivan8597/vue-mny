<template>
  <div class="forecast-container">
    <n-card title="Прогноз расходов">
      <template #header-extra>
        <n-tag type="info">Бета</n-tag>
      </template>
      <p>Для построения прогноза требуется история расходов минимум за 2 месяца</p>
      <div v-if="chartData && chartData.months.length >= 2">
        <n-statistic label="Ожидаемые расходы в следующем месяце">
          <template #prefix>≈</template>
          {{ formatCurrency(getForecast()[0]) }}
        </n-statistic>
      </div>
      <n-empty v-else description="Недостаточно данных для прогноза" />
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NCard, NStatistic, NTag, NEmpty } from 'naive-ui'
import type { Transaction } from '@/types'
import dayjs from '@/plugins/dayjs'

const props = defineProps<{
  transactions: Transaction[]
}>()

// Подготовленные данные для графика
const chartData = computed(() => {
  // Фильтруем только расходные транзакции и сортируем по дате
  const expenses = [...props.transactions]
    .filter(t => t.type === 'expense')
    .sort((a, b) => dayjs(a.date).valueOf() - dayjs(b.date).valueOf())
  
  if (expenses.length === 0) {
    return null
  }
  
  // Группируем по месяцам
  const monthlyExpenses: Record<string, number> = {}
  
  expenses.forEach(tx => {
    const month = dayjs(tx.date).format('MMM YYYY')
    monthlyExpenses[month] = (monthlyExpenses[month] || 0) + tx.amount
  })
  
  // Если данные только за один месяц, добавляем предыдущий с нулем
  const months = Object.keys(monthlyExpenses)
  if (months.length === 1) {
    const prevMonth = dayjs(expenses[0].date).subtract(1, 'month').format('MMM YYYY')
    monthlyExpenses[prevMonth] = 0
  }
  
  // Получаем отсортированные массивы месяцев и сумм
  const sortedMonths = Object.keys(monthlyExpenses).sort((a, b) => 
    dayjs(a, 'MMM YYYY').valueOf() - dayjs(b, 'MMM YYYY').valueOf())
  
  const sortedValues = sortedMonths.map(month => monthlyExpenses[month])
  
  return {
    months: sortedMonths,
    values: sortedValues
  }
})

// Функция линейной регрессии (упрощенная)
function getForecast() {
  if (!chartData.value || chartData.value.months.length < 2) return [0, 0, 0]
  
  const values = chartData.value.values
  // Простой расчет тренда по последним точкам
  const last = values[values.length - 1]
  const prev = values[values.length - 2]
  const trend = last - prev
  
  // Генерируем прогноз на 3 месяца
  return [1, 2, 3].map(i => {
    const forecast = last + trend * i
    return Math.max(0, forecast) // Не допускаем отрицательных значений
  })
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0
  }).format(value)
}
</script>

<style scoped>
.forecast-container {
  width: 100%;
}
</style> 