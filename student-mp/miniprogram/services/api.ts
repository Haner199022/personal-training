// 学员端 API 封装。
import { request } from "../utils/request"

export function wxLogin(): Promise<string> {
  return new Promise((resolve, reject) => {
    wx.login({
      success: async ({ code }) => {
        try {
          const r = await request<{ access_token: string }>({ url: "/auth/student/wx-login", method: "POST", data: { code } })
          wx.setStorageSync("pt_stoken", r.access_token)
          resolve(r.access_token)
        } catch (e) { reject(e) }
      },
      fail: reject,
    })
  })
}

export const getMe = () => request<any>({ url: "/students/me" })
export const getToday = () => request<any>({ url: "/students/me/today" })
export const getPlan = () => request<any>({ url: "/students/me/plan" })
export const joinCoach = (invite_code: string) => request<any>({ url: "/students/me/join", method: "POST", data: { invite_code } })
export const submitCheckIn = (data: any) => request<{ id: number }>({ url: "/students/me/check-ins", method: "POST", data })
export const getCheckIns = () => request<any>({ url: "/students/me/check-ins" })
export const getCheckInResult = (id: number) => request<any>({ url: `/students/me/check-ins/${id}` })
export const getMetrics = () => request<any>({ url: "/students/me/metrics" })
export const addMetric = (data: any) => request<any>({ url: "/students/me/metrics", method: "POST", data })
export const getCoach = () => request<any>({ url: "/students/me/coach" })
export const getInbox = () => request<any>({ url: "/students/me/inbox" })

// —— 以下端点后端尚未实现（MVP 逐步补），页面侧 try/catch 优雅降级 —— //
export const markInboxRead = (id: number) => request<any>({ url: `/students/me/inbox/${id}/read`, method: "POST" })
export const getPhotos = (pose: string) => request<any>({ url: `/students/me/photos?pose=${pose}` })
export const getPhotoConsent = () => request<any>({ url: "/students/me/photos/consent-status" })
export const setPhotoConsent = () => request<any>({ url: "/students/me/photos/consent", method: "POST", data: { consent: true } })
export const revokePhotoConsent = () => request<any>({ url: "/students/me/photos/consent/revoke", method: "POST", data: { confirm: true } })
