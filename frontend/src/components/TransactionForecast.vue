<template>
  <n-card title="Прогноз расходов">
    <div class="chart-container">
      <Line :data="chartData" :options="forecastOptions" />
    </div>
  </n-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { ChartOptions } from 'chart.js'
import type { Transaction } from '@/types'
import dayjs from '@/plugins/dayjs'

const props = defineProps<{
  transactions: Transaction[]
}>()

// Функция для линейной регрессии
function linearRegression(data: number[]): { slope: number; intercept: number } {
  const n = data.length
  let sumX = 0
  let sumY = 0
  let sumXY = 0
  let sumXX = 0
  
  for (let i = 0; i < n; i++) {
    sumX += i
    sumY += data[i]
    sumXY += i * data[i]
    sumXX += i * i
  }
  
  const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX)
  const intercept = (sumY - slope * sumX) / n
  
  return { slope, intercept }
}

// Функция для прогноза
function forecast(regression: { slope: number; intercept: number }, data: number[], periods: number): number[] {
  const result = []
  const start = data.length
  
  for (let i = 0; i < periods; i++) {
    result.push(regression.slope * (start + i) + regression.intercept)
  }
  
  return result
}

// Подготовка данных для графика
const chartData = computed(() => {
  // Группируем транзакции по месяцам
  const monthlyExpenses: Record<string, number> = {}
  
  props.transactions
    .filter(t => t.type === 'expense')
    .forEach(t => {
      const month = dayjs(t.date).format('MMM YYYY')
      monthlyExpenses[month] = (monthlyExpenses[month] || 0) + t.amount
    })

  const monthLabels = Object.keys(monthlyExpenses)
  const monthlyData = Object.values(monthlyExpenses)

  // Рассчитываем регрессию
  const regression = linearRegression(monthlyData)
  
  // Прогноз на 3 месяца
  const forecastData = forecast(regression, monthlyData, 3)

  // Генерируем метки для будущих месяцев
  const futureLables = Array.from({ length: 3 }, (_, i) => {
    return dayjs()
      .add(i + 1, 'month')
      .format('MMM YYYY')
  })

  return {
    labels: [...monthLabels, ...futureLables],
    datasets: [
      {
        label: 'Фактические данные',
        data: monthlyData,
        borderColor: '#41b883'
      },
      {
        label: 'Прогноз',
        data: [...Array(monthlyData.length).fill(null), ...forecastData],
        borderColor: '#ff7e67',
        borderDash: [5, 5]
      }
    ]
  }
})

const forecastOptions: ChartOptions<'line'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const
    },
    title: {
      display: true,
      text: 'Прогноз расходов'
    }
  },
  scales: {
    y: {
      type: 'linear',
      beginAtZero: true,
      ticks: {
        callback: function(value: number | string) {
          if (typeof value !== 'number') return ''
          return new Intl.NumberFormat('ru-RU', {
            style: 'currency',
            currency: 'RUB',
            maximumFractionDigits: 0
          }).format(value)
        }
      }
    }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
</style> 