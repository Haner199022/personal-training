import { wxLogin, getMe } from "../../services/api"
Page({
  data: { loading: false },
  async onLogin() {
    this.setData({ loading: true })
    try {
      await wxLogin()
      const me = await getMe()
      if (me.bound) wx.switchTab({ url: "/pages/home/home" })
      else wx.redirectTo({ url: "/pages/join/join" })
    } catch (e) {
      wx.showToast({ title: "登录失败（后端未启动？）", icon: "none" })
    } finally { this.setData({ loading: false }) }
  },
})
