import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'))
  const user = ref(null)

  const login = async (email: string, password: string) => {
    // Логика входа
  }

  const register = async (email: string, password: string, name: string) => {
    // Логика регистрации
  }

  const logout = () => {
    // Логика выхода
  }

  return { token, user, login, register, logout }
}) 