interface Options { url: string; method?: "GET" | "POST" | "PUT" | "DELETE"; data?: Record<string, unknown> }

export function request<T = unknown>(opts: Options): Promise<T> {
  const app = getApp<{ globalData: { apiBase: string } }>()
  const token = wx.getStorageSync("pt_stoken")
  return new Promise((resolve, reject) => {
    wx.request({
      url: app.globalData.apiBase + opts.url,
      method: opts.method ?? "GET",
      data: opts.data,
      header: token ? { Authorization: `Bearer ${token}` } : {},
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) resolve(res.data as T)
        else if (res.statusCode === 401) { wx.reLaunch({ url: "/pages/login/login" }); reject(res) }
        else reject(res)
      },
      fail: reject,
    })
  })
}
