// 学员端入口。视觉：暖色系（橙）强化能量感，对比教练端冷色蓝。
App<{ globalData: { token: string | null; apiBase: string } }>({
  globalData: {
    token: wx.getStorageSync("pt_token") || null,
    // 真机指向备案后的 HTTPS 域名；开发期在「开发者工具」勾「不校验合法域名」
    apiBase: "https://api.example.com/api/v1",
  },
  onLaunch() {
    // wx.login → code 换 JWT 的时机放在「加入教练 / 首次需要鉴权」时触发
  },
})
