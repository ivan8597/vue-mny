import axios from 'axios'

const api = axios.create({ 
  baseURL: '',
  headers: {
    'Content-Type': 'application/json'
  }
})

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