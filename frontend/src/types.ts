export type TransactionType = 
  'INCOME' | 
  'EXPENSE' 

export interface CreateTransactionDTO {
  title: string
  amount: number
  type: 'INCOME' | 'EXPENSE'
  category_id: number | null
  date: string
  description: string
} 