// wx.request 包一层 promise + 自动带 JWT。
interface Options {
  url: string
  method?: "GET" | "POST" | "PUT" | "DELETE"
  data?: Record<string, unknown>
}

export function request<T = unknown>(opts: Options): Promise<T> {
  const app = getApp<{ globalData: { apiBase: string; token: string | null } }>()
  return new Promise((resolve, reject) => {
    wx.request({
      url: app.globalData.apiBase + opts.url,
      method: opts.method ?? "GET",
      data: opts.data,
      header: app.globalData.token ? { Authorization: `Bearer ${app.globalData.token}` } : {},
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) resolve(res.data as T)
        else reject(res)
      },
      fail: reject,
    })
  })
}
