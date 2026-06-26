import { joinCoach } from "../../services/api"
Page({
  data: { code: "" },
  onInput(e: WechatMiniprogram.Input) { this.setData({ code: e.detail.value }) },
  async submit() {
    if (!this.data.code.trim()) { wx.showToast({ title: "请输入邀请码", icon: "none" }); return }
    try {
      const r = await joinCoach(this.data.code)
      wx.showToast({ title: `已加入 ${r.coach_name}`, icon: "success" })
      setTimeout(() => wx.switchTab({ url: "/pages/home/home" }), 800)
    } catch (e) { wx.showToast({ title: "邀请码无效", icon: "none" }) }
  },
})
