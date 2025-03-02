<template>
  <div class="savings-goal-form">
    <n-form
      ref="formRef"
      :model="formState"
      :rules="rules"
      label-placement="left"
    >
      <n-form-item label="Название" path="name">
        <n-input v-model:value="formState.name" placeholder="Название цели" />
      </n-form-item>
      
      <n-form-item label="Целевая сумма" path="target_amount">
        <n-input-number 
          v-model:value="formState.target_amount" 
          :min="1" 
          :precision="2"
          style="width: 100%"
          placeholder="Сумма" 
        />
      </n-form-item>
      
      <n-form-item label="Текущая сумма" path="current_amount">
        <n-input-number 
          v-model:value="formState.current_amount" 
          :min="0" 
          :precision="2"
          style="width: 100%"
          placeholder="Текущий прогресс" 
        />
      </n-form-item>
      
      <n-form-item label="Дата достижения" path="deadline">
        <n-date-picker 
          v-model:value="formState.deadline"
          style="width: 100%"
          type="date"
          placeholder="Выберите дату"
        />
      </n-form-item>
      
      <n-space justify="end">
        <n-button @click="handleCancel">
          Отмена
        </n-button>
        <n-button type="primary" @click="handleSubmit" :loading="isSubmitting">
          {{ savingsGoal ? 'Обновить' : 'Создать' }}
        </n-button>
      </n-space>
    </n-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import dayjs from '@/plugins/dayjs'
import { FormInst } from 'naive-ui'

interface SavingsGoal {
  id: number
  name: string
  target_amount: number
  current_amount: number
  deadline?: string
  created_at: string
}

const props = defineProps<{
  savingsGoal?: SavingsGoal
}>()

const emit = defineEmits(['submit', 'cancel'])
const formRef = ref<FormInst | null>(null)
const isSubmitting = ref(false)

const formState = reactive({
  name: '',
  target_amount: 0,
  current_amount: 0,
  deadline: null as any
})

const rules = {
  name: [
    { required: true, message: 'Введите название цели' }
  ],
  target_amount: [
    { required: true, type: 'number', message: 'Введите целевую сумму' }
  ]
}

onMounted(() => {
  if (props.savingsGoal) {
    formState.name = props.savingsGoal.name
    formState.target_amount = props.savingsGoal.target_amount
    formState.current_amount = props.savingsGoal.current_amount
    formState.deadline = props.savingsGoal.deadline 
      ? dayjs(props.savingsGoal.deadline).valueOf() 
      : null
  }
})

const handleSubmit = () => {
  formRef.value?.validate(async (errors) => {
    if (errors) return
    
    isSubmitting.value = true
    try {
      const data = {
        name: formState.name,
        target_amount: formState.target_amount,
        current_amount: formState.current_amount,
        deadline: formState.deadline ? dayjs(formState.deadline).format('YYYY-MM-DD') : undefined
      }
      emit('submit', data)
    } finally {
      isSubmitting.value = false
    }
  })
}

const handleCancel = () => {
  emit('cancel')
}
</script>

<style scoped>
.savings-goal-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}
</style> 