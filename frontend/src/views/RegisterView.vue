<template>
  <div class="register-container">
    <n-card title="Регистрация" class="register-card">
      <n-form
        ref="formRef"
        :model="formValue"
        :rules="rules"
        @submit.prevent="handleSubmit"
      >
        <n-form-item path="name" label="Имя">
          <n-input v-model:value="formValue.name" placeholder="Введите имя" />
        </n-form-item>
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
        <n-form-item path="username" label="Логин">
          <n-input v-model:value="formValue.username" placeholder="Введите логин" />
        </n-form-item>
        <n-button type="primary" block @click="handleSubmit">
          Зарегистрироваться
        </n-button>
      </n-form>
      <div class="login-link">
        <n-button text @click="router.push('/login')">
          Уже есть аккаунт? Войти
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
  name: '',
  email: '',
  password: '',
  username: ''
})

const rules = {
  name: [{ required: true, message: 'Введите имя', trigger: 'blur' }],
  email: [
    { required: true, message: 'Введите email', trigger: 'blur' },
    { type: 'email', message: 'Некорректный email', trigger: 'blur' }
  ],
  password: [{ required: true, message: 'Введите пароль', trigger: 'blur' }]
}

const handleSubmit = async () => {
  console.log('Sending registration data:', formValue.value)
  try {
    await authStore.register({
      email: formValue.value.email,
      password: formValue.value.password,
      name: formValue.value.name,
      username: formValue.value.username
    })
    router.push('/login')
  } catch (error: unknown) {
    if (error instanceof AxiosError) {
      console.log('Registration validation error:', error.response?.data)
    }
    message.error('Ошибка при регистрации')
  }
}
</script>

<style scoped lang="scss">
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.register-card {
  width: 100%;
  max-width: 400px;
  padding: 20px;
}

.login-link {
  margin-top: 16px;
  text-align: center;
}
</style> 