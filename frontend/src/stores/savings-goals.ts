import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api'



interface SavingsGoal {
  id: number
  name: string
  target_amount: number
  current_amount: number
  deadline?: string
  created_at: string
}





interface CreateSavingsGoalDTO {
  name: string
  target_amount: number
  current_amount?: number
  deadline?: string
}

export const useSavingsGoalsStore = defineStore('savingsGoals', () => {
  const savingsGoals = ref<SavingsGoal[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const fetchSavingsGoals = async () => {
    isLoading.value = true
    error.value = null
    try {
      const response = await api.get('/savings-goals')
      savingsGoals.value = response.data
    } catch (err: any) {
      console.error('Error fetching savings goals:', err)
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  const createSavingsGoal = async (goalData: CreateSavingsGoalDTO) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await api.post('/savings-goals', goalData)
      savingsGoals.value.push(response.data)
      return response.data
    } catch (err: any) {
      console.error('Error creating savings goal:', err)
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateSavingsGoal = async (id: number, data: Partial<CreateSavingsGoalDTO>) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await api.put(`/savings-goals/${id}`, data)
      const index = savingsGoals.value.findIndex((goal: SavingsGoal) => goal.id === id)
      if (index !== -1) {
        savingsGoals.value[index] = response.data
      }
      return response.data
    } catch (err: any) {
      console.error('Error updating savings goal:', err)
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteSavingsGoal = async (id: number) => {
    isLoading.value = true
    error.value = null
    try {
      await api.delete(`/savings-goals/${id}`)
      savingsGoals.value = savingsGoals.value.filter((goal: SavingsGoal) => goal.id !== id)
    } catch (err: any) {
      console.error('Error deleting savings goal:', err)
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    savingsGoals,
    isLoading,
    error,
    fetchSavingsGoals,
    createSavingsGoal,
    updateSavingsGoal,
    deleteSavingsGoal
  }
}) 