<template>
  <n-card title="Статистика по категориям">
    <n-tabs type="line" animated>
      <n-tab-pane name="expenses" tab="Расходы">
        <n-data-table
          :columns="columns"
          :data="expenseStats"
          :pagination="{ pageSize: 10 }"
        />
      </n-tab-pane>
      <n-tab-pane name="income" tab="Доходы">
        <n-data-table
          :columns="columns"
          :data="incomeStats"
          :pagination="{ pageSize: 10 }"
        />
      </n-tab-pane>
    </n-tabs>
  </n-card>
</template>

<script setup lang="ts">
import { computed, h } from 'vue'
import { NCard, NDataTable, NTabs, NTabPane, type DataTableColumns } from 'naive-ui'
import type { Transaction } from '@/types'
import { useCategoriesStore } from '@/stores/categories'
// import type { Category } from '@/stores/categories'

const props = defineProps<{
  transactions: Transaction[]
}>()

const categoriesStore = useCategoriesStore()

const columns: DataTableColumns = [
  { title: 'Категория', key: 'name' },
  { title: 'Сумма', key: 'amount' },
  { title: 'Количество', key: 'count' },
  { title: '% от общего', key: 'percentage' },
  { 
    title: 'Тренд', 
    key: 'trend',
    render: (row: Record<string, any>) => {
      const trend = row.trend > 0 ? '↑' : row.trend < 0 ? '↓' : '→'
      const color = row.trend > 0 ? '#18a058' : row.trend < 0 ? '#d03050' : '#2080f0'
      return h('span', { style: { color } }, `${trend} ${Math.abs(row.trend)}%`)
    }
  }
]

const expenseStats = computed(() => {
  const stats = new Map<number, { 
    name: string
    amount: number
    count: number
    percentage: number
    trend: number
  }>()
  
  const totalExpenses = props.transactions
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0)

  props.transactions
    .filter(t => t.type === 'expense')
    .forEach(t => {
      const category = categoriesStore.categories.find(c => c.id === t.category_id)
      if (!category) return

      const current = stats.get(category.id) || {
        name: category.name,
        amount: 0,
        count: 0,
        percentage: 0,
        trend: 0
      }

      current.amount += t.amount
      current.count++
      current.percentage = (current.amount / totalExpenses) * 100

      // Простой расчет тренда: сравниваем с предыдущим месяцем
      const prevMonth = new Date()
      prevMonth.setMonth(prevMonth.getMonth() - 1)
      const prevAmount = props.transactions
        .filter(pt => 
          pt.type === 'expense' && 
          pt.category_id === category.id &&
          new Date(pt.date) < prevMonth
        )
        .reduce((sum, t) => sum + t.amount, 0)

      current.trend = prevAmount ? ((current.amount - prevAmount) / prevAmount) * 100 : 0

      stats.set(category.id, current)
    })

  return Array.from(stats.values())
    .sort((a, b) => b.amount - a.amount)
    .map(stat => ({
      ...stat,
      amount: new Intl.NumberFormat('ru-RU', { 
        style: 'currency', 
        currency: 'RUB',
        maximumFractionDigits: 0 
      }).format(stat.amount),
      percentage: Math.round(stat.percentage * 10) / 10,
      trend: Math.round(stat.trend * 10) / 10
    }))
})

const incomeStats = computed(() => {
  const stats = new Map<number, { 
    name: string
    amount: number
    count: number
    percentage: number
    trend: number
  }>()
  
  const totalIncome = props.transactions
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0)

  props.transactions
    .filter(t => t.type === 'income')
    .forEach(t => {
      const category = categoriesStore.categories.find(c => c.id === t.category_id)
      if (!category) return

      const current = stats.get(category.id) || {
        name: category.name,
        amount: 0,
        count: 0,
        percentage: 0,
        trend: 0
      }

      current.amount += t.amount
      current.count++
      current.percentage = (current.amount / totalIncome) * 100

      const prevMonth = new Date()
      prevMonth.setMonth(prevMonth.getMonth() - 1)
      const prevAmount = props.transactions
        .filter(pt => 
          pt.type === 'income' && 
          pt.category_id === category.id &&
          new Date(pt.date) < prevMonth
        )
        .reduce((sum, t) => sum + t.amount, 0)

      current.trend = prevAmount ? ((current.amount - prevAmount) / prevAmount) * 100 : 0

      stats.set(category.id, current)
    })

  return Array.from(stats.values())
    .sort((a, b) => b.amount - a.amount)
    .map(stat => ({
      ...stat,
      amount: new Intl.NumberFormat('ru-RU', { 
        style: 'currency', 
        currency: 'RUB',
        maximumFractionDigits: 0 
      }).format(stat.amount),
      percentage: Math.round(stat.percentage * 10) / 10,
      trend: Math.round(stat.trend * 10) / 10
    }))
})
</script> 