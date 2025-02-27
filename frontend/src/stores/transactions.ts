import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'
import type { Transaction, CreateTransactionDTO } from '@/types'

export const useTransactionsStore = defineStore('transactions', () => {
  const transactions = ref<Transaction[]>([])
  const summary = ref({
    income: 0,
    expense: 0,
    balance: 0
  })

  const fetchTransactions = async () => {
    const response = await api.get('/api/transactions')
    transactions.value = response.data
  }

  const fetchSummary = async () => {
    const response = await api.get('/api/transactions/summary')
    summary.value = response.data
  }

  const createTransaction = async (data: CreateTransactionDTO) => {
    const response = await api.post('/api/transactions', data)
    transactions.value.unshift(response.data)
    await fetchSummary()
  }

  return {
    transactions,
    summary,
    fetchTransactions,
    fetchSummary,
    createTransaction
  }
}) 