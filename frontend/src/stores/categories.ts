import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'

interface Category {
  id: number
  name: string
  type: 'INCOME' | 'EXPENSE'
}



export const useCategoriesStore = defineStore('categories', () => {
  const categories = ref<Category[]>([])

  const fetchCategories = async () => {
    console.log('Fetching categories...')
    const response = await api.get('/api/categories')
    console.log('Categories response:', response.data)
    if (!Array.isArray(response.data)) {
      console.error('Invalid categories data:', response.data)
      categories.value = []
      return
    }
    categories.value = response.data
  }

  const createCategory = async (data: { name: string; type: 'INCOME' | 'EXPENSE' }) => {
    const response = await api.post('/api/categories', data)
    categories.value.push(response.data)
    return response.data
  }

  return {
    categories,
    fetchCategories,
    createCategory
  }
}) 