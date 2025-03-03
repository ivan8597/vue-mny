import axios from 'axios'

const api = axios.create({ 
  baseURL: '/api',  // Используем относительный путь для проксирования через nginx
  headers: {
    'Content-Type': 'application/json'
  }
})

// Перехватчик для обработки ошибок
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.status, error.response?.data)
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Перехватчик для добавления токена
api.interceptors.request.use(config => {
  console.log('Request URL:', config.url)
  console.log('Full URL:', (config.baseURL || '') + (config.url || ''))
  console.log('Adding token to request')
  const token = localStorage.getItem('token')
  console.log('Token:', token)
  if (token) {
    if (config.headers) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
  }
  console.log('Final headers:', config.headers)
  return config
})

export default api 