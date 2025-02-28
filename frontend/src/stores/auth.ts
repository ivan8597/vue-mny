import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import api from '@/api'
import { useRouter } from 'vue-router'
import { AxiosError } from 'axios'

interface LoginCredentials {
  username: string
  password: string
}

interface RegisterData {
  email: string
  password: string
  name: string
}

interface User {
  id: number
  email: string
  name: string
}

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)

  const login = async (credentials: LoginCredentials) => {
    try {
      console.log('Login attempt with:', { email: credentials.username })
      if (token.value) {
        console.log('Already have token:', token.value)
        await router.push('/')
        return
      }
      const formData = new URLSearchParams()
      formData.append('grant_type', 'password')
      formData.append('username', credentials.username)
      formData.append('password', credentials.password)
      
      const response = await api.post('/api/auth/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      console.log('Response status:', response.status)
      console.log('Response headers:', response.headers)
      console.log('Response data:', response.data)

      token.value = response.data.access_token
      if (token.value) {
        localStorage.setItem('token', token.value)
      }
      await router.push('/')
    } catch (error) {
      if (error instanceof AxiosError) {
        console.error('Request config:', error.config)
        console.error('Response status:', error.response?.status)
        console.error('Response data:', error.response?.data)
        console.error('Response headers:', error.response?.headers)
      }
      throw error
    }
  }

  const register = async (userData: RegisterData) => {
    try {
      const response = await api.post('/api/auth/register', userData)
      await login({ username: userData.email, password: userData.password })
    } catch (error) {
      console.error('Register error:', error)
      throw error
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    router.push('/login')
  }

  return { token, user, login, register, logout }
}) 