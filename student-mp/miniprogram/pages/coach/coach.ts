import { getCoach } from "../../services/api"

Page({
  data: {
    name: "张教练",
    bio: "擅长力量训练与体型管理，多年带教经验。",
    specialties: ["力量训练", "体型管理", "赛事备赛"] as string[],
    serving: true,
    servingFor: "" as string,
    loaded: false,
  },

  async onLoad() {
    try {
      const coach = await getCoach()
      if (coach) {
        this.setData({
          name: coach.display_name || coach.name || "张教练",
          bio: coach.bio || "擅长力量训练与体型管理，多年带教经验。",
          specialties: (coach.specialties && coach.specialties.length)
            ? coach.specialties
            : ["力量训练", "体型管理", "赛事备赛"],
          serving: coach.serving !== false,
          servingFor: coach.serving_for || coach.served_for || "",
        })
      }
    } catch (e) {
      // 后端 coach 端点可能未实现或学员未绑定，保留占位资料，页面不崩。
    }
    this.setData({ loaded: true })
  },

  enterGroup() {
    wx.showToast({ title: "请扫码或通过企微进入服务群", icon: "none", duration: 2000 })
  },
})
