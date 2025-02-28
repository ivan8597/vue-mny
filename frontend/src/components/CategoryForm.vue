<template>
  <n-form
    ref="formRef"
    :model="formValue"
    :rules="rules"
    @submit.prevent="handleSubmit"
  >
    <n-form-item path="name" label="Название">
      <n-input v-model:value="formValue.name" />
    </n-form-item>
    <n-form-item path="type" label="Тип">
      <n-select v-model:value="formValue.type" :options="typeOptions" />
    </n-form-item>
    <n-button type="primary" @click="handleSubmit">Создать</n-button>
  </n-form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { TransactionType } from '@/types'
import { useCategoriesStore } from '@/stores/categories'
import { useMessage } from 'naive-ui'

const categoriesStore = useCategoriesStore()
const message = useMessage()

const formValue = ref({
  name: '',
  type: 'expense' as 'income' | 'expense'
})

const typeOptions = [
  { label: 'Доход', value: 'income' },
  { label: 'Расход', value: 'expense' }
]

const rules = {
  name: { required: true, message: 'Введите название категории' }
}

const handleSubmit = async () => {
  try {
    await categoriesStore.createCategory(formValue.value)
    message.success('Категория создана')
  } catch (error) {
    message.error('Ошибка при создании категории')
  }
}
</script>

<style>
  /* No changes to style section */
</style> 