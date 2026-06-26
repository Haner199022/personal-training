import { getMe, getToday, getCheckIns, getInbox } from "../../services/api"
Page({
  data: { name: "", today: null as any, unread: 0, recent: [] as any[] },
  async onShow() {
    if (!wx.getStorageSync("pt_stoken")) { wx.reLaunch({ url: "/pages/login/login" }); return }
    try {
      const me = await getMe()
      if (!me.bound) { wx.redirectTo({ url: "/pages/join/join" }); return }
      const [today, inbox, cis] = await Promise.all([getToday(), getInbox(), getCheckIns()])
      this.setData({ name: me.display_name, today, unread: inbox.unread, recent: cis.items.slice(0, 3) })
    } catch (e) {}
  },
  startTraining() { wx.navigateTo({ url: "/pages/training/training" }) },
  toInbox() { wx.switchTab({ url: "/pages/inbox/inbox" }) },
})
