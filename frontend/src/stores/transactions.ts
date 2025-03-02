import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'
import { useCategoriesStore, type Category } from './categories'
import type { CreateTransactionDTO, Transaction } from '@/types'

export const useTransactionsStore = defineStore('transactions', () => {
  const transactions = ref<Transaction[]>([])
  const summary = ref({
    income: 0,
    expense: 0,
    balance: 0
  })
  const loading = ref(false)
  const categoriesById = ref<Record<number, Category>>({})

  const categoriesStore = useCategoriesStore()

  const fetchTransactions = async (params?: { startDate?: string, endDate?: string }) => {
    loading.value = true
    try {
      const response = await api.get('/transactions', { params })
      transactions.value = await loadTransactionCategories(response.data)
      return response.data
    } catch (error) {
      console.error('Error fetching transactions:', error)
      return []
    } finally {
      loading.value = false
    }
  }

  const fetchSummary = async (params?: { startDate?: string, endDate?: string }) => {
    try {
      const response = await api.get('/transactions/summary', { params })
      summary.value = response.data
      return response.data
    } catch (error) {
      console.error('Error fetching summary:', error)
      throw error
    }
  }

  const createTransaction = async (data: CreateTransactionDTO) => {
    try {
      const response = await api.post('/transactions', data)
      const transactionWithCategory = await loadTransactionCategories([response.data])
      transactions.value.unshift(transactionWithCategory[0])
      await fetchSummary()
      return response.data
    } catch (error) {
      console.error('Error creating transaction:', error)
      throw error
    }
  }

  async function loadTransactionCategories(transactions: Transaction[]) {
    const missingCategoryIds = transactions
      .filter(t => t.category_id && !categoriesById.value[t.category_id])
      .map(t => t.category_id)
    
    if (missingCategoryIds.length > 0) {
      await categoriesStore.fetchCategories()
      categoriesById.value = categoriesStore.categoriesById
    }
    
    return transactions.map(transaction => ({
      ...transaction,
      category_name: transaction.category_id 
        ? categoriesStore.getCategoryById(transaction.category_id)?.name || 'Неизвестная категория'
        : ''
    }))
  }

  return {
    transactions,
    summary,
    loading,
    fetchTransactions,
    fetchSummary,
    createTransaction
  }
}) 