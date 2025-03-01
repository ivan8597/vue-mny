<template>
  <div class="charts">
    <n-grid :cols="2" :x-gap="24">
      <n-grid-item>
        <n-card title="Динамика по месяцам">
          <div class="chart-container">
            <Line :data="monthlyData" :options="lineOptions" />
          </div>
        </n-card>
      </n-grid-item>
      <n-grid-item>
        <n-card title="Расходы по категориям">
          <div class="chart-container">
            <Pie :data="categoryData" :options="pieOptions" />
          </div>
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Line, Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js'
import { NGrid, NGridItem, NCard } from 'naive-ui'
import type { Transaction } from '@/types'
import { useCategoriesStore } from '@/stores/categories'
import type { Category } from '@/stores/categories'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

const categoriesStore = useCategoriesStore()
const props = defineProps<{
  transactions: Transaction[]
  previousTransactions?: Transaction[]
  categories: Category[]
}>()

// Данные для линейного графика (по месяцам)
const monthlyData = computed(() => {
  const months = {} as Record<string, { income: number; expense: number }>
  const prevMonths = {} as Record<string, { income: number; expense: number }>
  
  props.transactions.forEach(t => {
    const month = new Date(t.date).toLocaleString('ru', { month: 'short' })
    if (!months[month]) {
      months[month] = { income: 0, expense: 0 }
    }
    if (t.type === 'income') {
      months[month].income += t.amount
    } else {
      months[month].expense += t.amount
    }
  })

  props.previousTransactions?.forEach(t => {
    const month = new Date(t.date).toLocaleString('ru', { month: 'short' })
    if (!prevMonths[month]) {
      prevMonths[month] = { income: 0, expense: 0 }
    }
    if (t.type === 'income') {
      prevMonths[month].income += t.amount
    } else {
      prevMonths[month].expense += t.amount
    }
  })

  return {
    labels: Object.keys(months),
    datasets: [
      {
        label: 'Доходы',
        data: Object.values(months).map(m => m.income),
        borderColor: '#2ec7c9',
        backgroundColor: '#2ec7c9',
        tension: 0.1
      },
      {
        label: 'Расходы',
        data: Object.values(months).map(m => m.expense),
        borderColor: '#d87a80',
        backgroundColor: '#d87a80',
        tension: 0.1
      },
      {
        label: 'Доходы (пред. период)',
        data: Object.values(prevMonths).map(m => m.income),
        borderColor: '#2ec7c9',
        backgroundColor: '#2ec7c9',
        borderDash: [5, 5],
        tension: 0.1
      },
      {
        label: 'Расходы (пред. период)',
        data: Object.values(prevMonths).map(m => m.expense),
        borderColor: '#d87a80',
        backgroundColor: '#d87a80',
        borderDash: [5, 5],
        tension: 0.1
      }
    ]
  }
})

// Данные для круговой диаграммы (по категориям)
const categoryData = computed(() => {
  const categories = {} as Record<string, number>
  
  props.transactions
    .filter(t => t.type === 'expense')
    .forEach(t => {
      const category = categoriesStore.categories.find((c: Category) => c.id === t.category_id)?.name || 'Без категории'
      categories[category] = (categories[category] || 0) + t.amount
    })

  return {
    labels: Object.keys(categories),
    datasets: [{
      data: Object.values(categories),
      backgroundColor: [
        '#2ec7c9',
        '#b6a2de',
        '#5ab1ef',
        '#ffb980',
        '#d87a80',
        '#8d98b3',
        '#e5cf0d',
        '#97b552',
        '#95706d',
        '#dc69aa'
      ]
    }]
  }
})

const lineOptions: ChartOptions<'line'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const
    },
    title: {
      display: true,
      text: 'Динамика доходов и расходов'
    }
  },
  scales: {
    y: {
      type: 'linear',
      beginAtZero: true,
      ticks: {
        callback: function(tickValue: number | string) {
          if (typeof tickValue !== 'number') return ''
          return new Intl.NumberFormat('ru-RU', { 
            style: 'currency', 
            currency: 'RUB',
            maximumFractionDigits: 0
          }).format(tickValue)
        }
      }
    }
  }
}

const pieOptions: ChartOptions<'pie'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const
    },
    title: {
      display: true,
      text: 'Распределение расходов'
    },
    tooltip: {
      callbacks: {
        label: (context: any) => {
          const value = context.raw;
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
.charts {
  margin-top: 24px;
}

.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
</style> 