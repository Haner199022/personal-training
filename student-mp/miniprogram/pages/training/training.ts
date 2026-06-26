import { getPlan, submitCheckIn } from "../../services/api"
Page({
  data: {
    title: "", note: "", exercises: [] as any[],
    demoOpen: false, demo: null as any,
    finishing: false, feeling: 4, rpe: 7, comment: "",
  },
  async onLoad() {
    const r = await getPlan()
    const sess = r.plan?.detail?.sessions?.[0]
    if (!sess) { wx.showToast({ title: "暂无今日计划", icon: "none" }); return }
    const exercises = (sess.exercises || []).map((e: any) => ({ ...e, done: false }))
    this.setData({ title: sess.title, note: "重点感受臀部发力，深蹲下蹲到大腿平行", exercises, planTitle: r.plan.title } as any)
  },
  showDemo(e: WechatMiniprogram.TouchEvent) { this.setData({ demoOpen: true, demo: this.data.exercises[e.currentTarget.dataset.i] }) },
  closeDemo() { this.setData({ demoOpen: false }) },
  toggleDone(e: WechatMiniprogram.TouchEvent) {
    const i = e.currentTarget.dataset.i; const ex = this.data.exercises
    ex[i].done = !ex[i].done; this.setData({ exercises: ex })
  },
  finish() { this.setData({ finishing: true }) },
  setFeel(e: WechatMiniprogram.TouchEvent) { this.setData({ feeling: Number(e.currentTarget.dataset.v) }) },
  onRpe(e: WechatMiniprogram.SliderChange) { this.setData({ rpe: e.detail.value }) },
  onComment(e: WechatMiniprogram.Input) { this.setData({ comment: e.detail.value }) },
  async submit() {
    const sets = this.data.exercises.map(ex => ({ exercise: ex.name, prescribed: `${ex.sets}×${ex.reps} @${ex.weight}`, actual: ["done"] }))
    try {
      const r = await submitCheckIn({ plan_title: (this.data as any).planTitle, feeling: this.data.feeling, rpe: this.data.rpe, note: this.data.comment, sets_detail: sets })
      wx.redirectTo({ url: `/pages/checkin-result/checkin-result?id=${r.id}` })
    } catch (e) { wx.showToast({ title: "提交失败", icon: "none" }) }
  },
})
