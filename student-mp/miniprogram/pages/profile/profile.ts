import { getMe, getCoach } from "../../services/api"

Page({
  data: {
    name: "学员",
    coachName: "",
    inGroup: false,
  },

  async onShow() {
    // tab page login guard
    if (!wx.getStorageSync("pt_stoken")) {
      wx.reLaunch({ url: "/pages/login/login" })
      return
    }
    await this.loadProfile()
  },

  async loadProfile() {
    // Load student name; graceful fallback to default "学员".
    try {
      const me = await getMe()
      this.setData({
        name: me.display_name || "学员",
        inGroup: !!me.in_group,
      })
    } catch (e) {
      this.setData({ name: "学员", inGroup: false })
    }

    // Load coach name; right-side label degrades silently on failure.
    try {
      const coach = await getCoach()
      this.setData({ coachName: (coach && coach.name) || "" })
    } catch (e) {
      this.setData({ coachName: "" })
    }
  },

  toCoach() {
    wx.navigateTo({ url: "/pages/coach/coach" })
  },

  toGroup() {
    wx.showToast({ title: "请在真机扫码加群", icon: "none" })
  },

  toPrivacy() {
    wx.navigateTo({ url: "/pages/privacy/privacy" })
  },

  toSettings() {
    wx.showToast({ title: "即将上线", icon: "none" })
  },

  toAbout() {
    wx.showToast({ title: "练程/练+ · 私教助理", icon: "none" })
  },
})
