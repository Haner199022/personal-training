import { defineStore } from "pinia"
import { ref } from "vue"
import api from "@/api/client"

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(localStorage.getItem("pt_token"))

  async function login(phone: string, password: string) {
    const { data } = await api.post("/auth/coach/login", { phone, password })
    token.value = data.access_token
    localStorage.setItem("pt_token", data.access_token)
  }
  function logout() {
    token.value = null
    localStorage.removeItem("pt_token")
  }
  return { token, login, logout }
})
