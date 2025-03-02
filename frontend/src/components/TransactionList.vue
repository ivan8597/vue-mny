<template>
  <n-data-table
    :columns="columns"
    :data="transactions"
    :pagination="pagination"
    :loading="loading"
  />
</template>

<script setup lang="ts">
import { h, ref, toRefs } from 'vue'
import { NTag } from 'naive-ui'
import type { Transaction } from '@/types'
import dayjs from '@/plugins/dayjs'

const loading = ref(false)
const pagination = { pageSize: 10 }

const props = defineProps<{
  transactions: Transaction[]
  categories?: any[]
}>()

// Используйте toRefs для деструктуризации props
const { transactions } = toRefs(props)

const columns = [
  { 
    title: 'Дата', 
    key: 'date',
    render(row: Transaction) {
      try {
        return row.date ? dayjs(row.date).format('DD.MM.YYYY') : '';
      } catch (error) {
        console.error('Invalid date:', row.date);
        return 'Неверная дата';
      }
    }
  },
  { title: 'Название', key: 'title' },
  { 
    title: 'Тип',
    key: 'type',
    render(row: Transaction) {
      const type = row.type
      const label = type === 'income' ? 'Доход' : 'Расход'
      return h(
        NTag,
        {
          type: type === 'income' ? 'success' : 'error'
        },
        { default: () => label }
      )
    }
  },
  { 
    title: 'Сумма', 
    key: 'amount',
    render(row: Transaction) {
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0
      }).format(row.amount);
    }
  },
  { title: 'Категория', key: 'category_name' }
]
</script>