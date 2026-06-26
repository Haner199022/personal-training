import { getCheckInResult } from "../../services/api"

Page({
  data: {
    id: 0,
    title: "今日训练",
    // 教练点评
    hasComment: false,
    comment: "",
    coachName: "",
    // 订阅提示展示态
    subDone: false,
  },

  async onLoad(options: Record<string, string>) {
    const id = Number(options.id || 0)
    this.setData({ id })
    if (!id) return
    try {
      const r = await getCheckInResult(id)
      const comment = (r && (r.coach_comment || r.comment)) || ""
      this.setData({
        title: (r && (r.plan_title || r.title)) || "今日训练",
        hasComment: !!comment,
        comment,
        coachName: (r && (r.coach_name || r.coach)) || "教练",
      })
    } catch (e) {
      // 端点未实现 / 404 时优雅降级为占位态，不让页面崩溃。
    }
  },

  // 订阅提示 —— 一次性微信订阅消息（占位，模板 id 待后端下发）
  declineSub() {
    this.setData({ subDone: true })
  },

  acceptSub() {
    try {
      wx.requestSubscribeMessage({
        tmplIds: [],
        success: () => {
          this.setData({ subDone: true })
          wx.showToast({ title: "已设置提醒", icon: "success" })
        },
        fail: () => {
          this.setData({ subDone: true })
          wx.showToast({ title: "稍后可在设置开启", icon: "none" })
        },
      })
    } catch (e) {
      this.setData({ subDone: true })
      wx.showToast({ title: "稍后可在设置开启", icon: "none" })
    }
  },

  goHome() {
    wx.switchTab({ url: "/pages/home/home" })
  },
})
