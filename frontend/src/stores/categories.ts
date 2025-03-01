import { defineStore } from 'pinia'
import api from '@/api'

export interface Category {
  id: number
  name: string
  type: 'income' | 'expense'
}

export const useCategoriesStore = defineStore('categories', {
  state: () => ({
    categories: [] as Category[],
    loading: false,
    error: null as string | null
  }),

  actions: {
    async fetchCategories() {
      this.loading = true
      try {
        const response = await api.get('/api/categories')
        this.categories = response.data
      } catch (error: any) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async createCategory(category: Omit<Category, 'id'>) {
      this.loading = true
      try {
        const response = await api.post('/api/categories', category)
        this.categories.push(response.data)
      } catch (error: any) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    }
  }
}) 