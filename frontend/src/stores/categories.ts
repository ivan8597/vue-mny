import { defineStore } from 'pinia'
import api from '@/api'
// import { computed } from 'vue'

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

  getters: {
    categoriesById: (state) => {
      const result: Record<number, Category> = {}
      state.categories.forEach(category => {
        result[category.id] = category
      })
      return result
    },

    getCategoryById: (state) => {
      return (id: number) => state.categories.find(c => c.id === id)
    }
  },

  actions: {
    async fetchCategories() {
      this.loading = true
      try {
        const response = await api.get('/categories')
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
        const response = await api.post('/categories', category)
        this.categories.push(response.data)
        return response.data
      } catch (error: any) {
        this.error = error.message
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchCategoriesByIds(ids: number[]) {
      if (ids.length === 0) return
      if (this.categories.length === 0) {
        await this.fetchCategories()
      }
    }
  }
}) 