export type TransactionType = 
  'income' | 
  'expense'

export interface Transaction {
  id: number
  title: string
  amount: number
  type: TransactionType
  category_id: number
  date: string
  description: string
  user_id: number
}

export interface CreateTransactionDTO {
  title: string
  amount: number
  type: TransactionType
  category_id: number | null
  date: string
  description: string
} 