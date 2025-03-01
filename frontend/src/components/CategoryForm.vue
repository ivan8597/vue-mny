<template>
  <n-form ref="formRef" :model="formData" :rules="rules">
    <n-form-item label="Название" path="name">
      <n-input v-model:value="formData.name" placeholder="Введите название категории" />
    </n-form-item>
    <n-form-item label="Тип" path="type">
      <n-select 
        v-model:value="formData.type"
        :options="typeOptions"
        placeholder="Выберите тип категории"
      />
    </n-form-item>
    <n-space justify="end">
      <n-button type="primary" @click="handleSubmit">
        Создать
      </n-button>
    </n-space>
  </n-form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { FormInst } from 'naive-ui'
import { 
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NButton,
  NSpace
} from 'naive-ui'

const formRef = ref<FormInst | null>(null)
const formData = ref({
  name: '',
  type: 'expense' as 'income' | 'expense'
})

const typeOptions = [
  { label: 'Доход', value: 'income' },
  { label: 'Расход', value: 'expense' }
]

const rules = {
  name: {
    required: true,
    message: 'Пожалуйста, введите название категории',
    trigger: 'blur'
  },
  type: {
    required: true,
    message: 'Пожалуйста, выберите тип категории',
    trigger: 'change'
  }
}

const emit = defineEmits(['submit'])

const handleSubmit = () => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      emit('submit', formData.value)
      formData.value = {
        name: '',
        type: 'expense'
      }
    }
  })
}
</script>

<style>
  /* No changes to style section */
</style> 