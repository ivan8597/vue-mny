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
  { title: 'Сумма', key: 'amount' },
  { title: 'Категория', key: 'category_name' }
]

const props = defineProps<{
  transactions: Transaction[]
}>()
</script> 