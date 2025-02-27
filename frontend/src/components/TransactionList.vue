<template>
  <n-data-table
    :columns="columns"
    :data="transactions"
    :pagination="pagination"
    :loading="loading"
  />
</template>

<script setup lang="ts">
import { h, ref } from 'vue'
import { NTag } from 'naive-ui'
import type { Transaction } from '@/types'

const loading = ref(false)
const pagination = { pageSize: 10 }

const columns = [
  { title: 'Дата', key: 'date' },
  { title: 'Название', key: 'title' },
  { 
    title: 'Тип',
    key: 'type',
    render(row: Transaction) {
      return h(
        NTag,
        { type: row.type === 'income' ? 'success' : 'error' },
        { default: () => row.type === 'income' ? 'Доход' : 'Расход' }
      )
    }
  },
  { title: 'Сумма', key: 'amount' },
  { title: 'Категория', key: 'category_name' }
]

defineProps<{
  transactions: Transaction[]
}>()
</script> 