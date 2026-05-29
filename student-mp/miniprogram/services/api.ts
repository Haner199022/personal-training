// API 封装：wx.request + 自家 JWT。学员登录走 wx.login → /auth/student/wx-login。
import { request } from "../utils/request"

export function wxLogin() {
  return new Promise<string>((resolve, reject) => {
    wx.login({
      success: async ({ code }) => {
        try {
          const { access_token } = await request<{ access_token: string }>({
            url: "/auth/student/wx-login",
            method: "POST",
            data: { code },
          })
          wx.setStorageSync("pt_token", access_token)
          resolve(access_token)
        } catch (e) {
          reject(e)
        }
      },
      fail: reject,
    })
  })
}

export const joinCoach = (code: string) =>
  request({ url: "/students/me/join", method: "POST", data: { invite_code: code } })

export const getTodayTraining = () => request({ url: "/students/me/today", method: "GET" })
