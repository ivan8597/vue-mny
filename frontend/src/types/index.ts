export interface Transaction {
  id: number
  title: string
  amount: number
  type: 'income' | 'expense'
  category_id: number
  description?: string
  date: string
  user_id: number
}

export interface Category {
  id: number
  name: string
  type: 'income' | 'expense'
}

export interface User {
  id: number
  email: string
  name: string
}

export interface CreateTransactionDTO {
  title: string
  amount: number
  type: 'income' | 'expense'
  category_id: number
  description?: string
}

export interface Summary {
  total_income: number
  total_expenses: number
  balance: number
}

export interface SavingsGoal {
  id: number
  name: string
  target_amount: number
  current_amount: number
  deadline?: string
  created_at: string
  user_id: number
}

export interface CreateSavingsGoalDTO {
  name: string
  target_amount: number
  current_amount?: number
  deadline?: string
} 