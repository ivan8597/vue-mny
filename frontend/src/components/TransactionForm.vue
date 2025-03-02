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
    <!-- <n-form-item path="description" label="Описание">
      <n-input v-model:value="formValue.description" type="textarea" />
    </n-form-item> -->
    <n-button type="primary" @click="handleSubmit">Создать</n-button>
  </n-form>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useCategoriesStore } from '@/stores/categories'
import { useTransactionsStore } from '@/stores/transactions'
import { useMessage } from 'naive-ui'
import { AxiosError } from 'axios'
import type { CreateTransactionDTO, TransactionType } from '@/types'
import dayjs from 'dayjs'
// import type { Category } from '@/types'

const props = defineProps<{
  showTransactionModal: { value: boolean }
}>()

const categoriesStore = useCategoriesStore()
const transactionsStore = useTransactionsStore()
const message = useMessage()

const formValue = ref({
  title: '',
  amount: null,
  type: 'expense' as TransactionType,
  category_id: null,
  date: dayjs().format('YYYY-MM-DD'),
  description: ''
})

const typeOptions = [
  { label: 'Доход', value: 'income' },
  { label: 'Расход', value: 'expense' }
]

// Добавим наблюдатель за изменением типа транзакции
watch(() => formValue.value.type, () => {
  // При изменении типа сбрасываем выбранную категорию, т.к. категории фильтруются по типу
  formValue.value.category_id = null
  // После изменения типа убедимся, что категории загружены
  if (categoriesStore.categories.length === 0) {
    categoriesStore.fetchCategories()
  }
})

const categoryOptions = computed(() => {
  console.log('Categories:', categoriesStore.categories)
  console.log('Current type:', formValue.value.type)
  if (!Array.isArray(categoriesStore.categories)) {
    console.error('Categories is not an array:', categoriesStore.categories)
    return []
  }
  const filtered = categoriesStore.categories.filter(c => c.type === formValue.value.type)
  console.log('Filtered categories:', filtered)
  return filtered.map(c => ({ 
    label: c.name, 
    value: c.id,
    // Добавляем дополнительную информацию для отладки
    disabled: false,
    key: `${c.id}-${c.type}` 
  }))
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
    await transactionsStore.createTransaction({
      ...formValue.value,
      amount: formValue.value.amount || 0,
      category_id: formValue.value.category_id || 0
    } as CreateTransactionDTO)
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