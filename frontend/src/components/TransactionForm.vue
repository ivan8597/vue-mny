<template>
  <n-form
    ref="formRef"
    :model="formValue"
    :rules="rules"
    @submit.prevent="handleSubmit"
  >
    <n-form-item path="title" label="Название">
      <n-input v-model:value="formValue.title" />
    </n-form-item>
    <n-form-item path="amount" label="Сумма">
      <n-input-number v-model:value="formValue.amount" />
    </n-form-item>
    <n-form-item path="type" label="Тип">
      <n-select v-model:value="formValue.type" :options="typeOptions" />
    </n-form-item>
    <n-form-item path="category_id" label="Категория">
      <n-select v-model:value="formValue.category_id" :options="categoryOptions" />
    </n-form-item>
    <n-form-item path="description" label="Описание">
      <n-input v-model:value="formValue.description" type="textarea" />
    </n-form-item>
    <n-button type="primary" @click="handleSubmit">Создать</n-button>
  </n-form>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useCategoriesStore } from '@/stores/categories'
import { useTransactionsStore } from '@/stores/transactions'
import { useMessage } from 'naive-ui'
import { AxiosError } from 'axios'
import type { CreateTransactionDTO } from '@/types'
// import type { Category } from '@/types'

const props = defineProps<{
  showTransactionModal: { value: boolean }
}>()

const categoriesStore = useCategoriesStore()
const transactionsStore = useTransactionsStore()
const message = useMessage()

const formValue = ref({
  title: '',
  amount: 0,
  type: 'expense' as 'income' | 'expense',
  category_id: null as number | null,
  date: new Date().toISOString().split('T')[0],
  description: ''
})

const typeOptions = [
  { label: 'Доход', value: 'income' },
  { label: 'Расход', value: 'expense' }
]

const categoryOptions = computed(() => {
  console.log('Categories:', categoriesStore.categories)
  console.log('Current type:', formValue.value.type)
  if (!Array.isArray(categoriesStore.categories)) {
    console.error('Categories is not an array:', categoriesStore.categories)
    return []
  }
  const filtered = categoriesStore.categories.filter(c => c.type === formValue.value.type)
  console.log('Filtered categories:', filtered)
  return filtered.map(c => ({ label: c.name, value: c.id }))
})

onMounted(async () => {
  await categoriesStore.fetchCategories()
})

const rules = {
  title: { required: true, message: 'Введите название' },
  amount: { required: true, message: 'Введите сумму' },
  category_id: { required: true, message: 'Выберите категорию' }
}

const emit = defineEmits(['submit'])

const formRef = ref<any>(null)

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    console.log('Submitting transaction:', formValue.value)
    await transactionsStore.createTransaction(formValue.value as CreateTransactionDTO)
    props.showTransactionModal.value = false
    message.success('Транзакция создана')
  } catch (error) {
    if (error instanceof AxiosError) {
      console.error('Transaction error details:', error.response?.data)
      message.error(error.response?.data?.detail || 'Ошибка при создании транзакции')
    } else {
      message.error('Ошибка при создании транзакции')
    }
  }
}
</script> 