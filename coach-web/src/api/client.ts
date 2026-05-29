import axios from "axios"

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE ?? "/api/v1", timeout: 15000 })

api.interceptors.request.use((cfg) => {
  const token = localStorage.getItem("pt_token")
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

export default api
