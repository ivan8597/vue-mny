<template>
  <div class="login-container">
    <n-card title="Вход" class="login-card">
      <n-form
        ref="formRef"
        :model="formValue"
        :rules="rules"
        @submit.prevent="handleSubmit"
      >
        <n-form-item path="email" label="Email">
          <n-input v-model:value="formValue.email" placeholder="Введите email" />
        </n-form-item>
        <n-form-item path="password" label="Пароль">
          <n-input
            v-model:value="formValue.password"
            type="password"
            placeholder="Введите пароль"
          />
        </n-form-item>
        <n-button type="primary" block @click="handleSubmit">
          Войти
        </n-button>
      </n-form>
      <div class="register-link">
        <n-button text @click="router.push('/register')">
          Зарегистрироваться
        </n-button>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useMessage } from 'naive-ui'
import { AxiosError } from 'axios'

const router = useRouter()
const authStore = useAuthStore()
const message = useMessage()

const formValue = ref({
  email: '',
  password: ''
})

const rules = {
  email: [
    { required: true, message: 'Введите email', trigger: 'blur' },
    { type: 'email', message: 'Некорректный email', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Введите пароль', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  try {
    await authStore.login({
      username: formValue.value.email,
      password: formValue.value.password
    })
    message.success('Успешный вход')
  } catch (error: unknown) {
    if (error instanceof AxiosError) {
      message.error(error.response?.data?.detail || 'Ошибка входа')
    } else {
      message.error('Ошибка входа')
    }
  }
}
</script>

<style scoped lang="scss">
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 20px;
}

.register-link {
  margin-top: 16px;
  text-align: center;
}
</style> 