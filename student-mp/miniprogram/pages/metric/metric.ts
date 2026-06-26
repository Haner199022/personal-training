import { addMetric, getPhotoConsent, setPhotoConsent } from "../../services/api"

function today(): string {
  const d = new Date()
  const m = `${d.getMonth() + 1}`.padStart(2, "0")
  const day = `${d.getDate()}`.padStart(2, "0")
  return `${d.getFullYear()}-${m}-${day}`
}

Page({
  data: {
    metricDate: today(),
    weight: "",
    bodyFatRate: "",
    muscleMass: "",
    waist: "",
    chest: "",
    arm: "",
    thigh: "",
    notes: "",
    consented: false,
    showConsent: false,
    pendingPose: "",
    photos: {} as any, // { front, side, back } -> local temp file path
    submitting: false,
  },

  async onLoad() {
    try {
      const r = await getPhotoConsent()
      if (r && r.consent) this.setData({ consented: true })
    } catch (e) {
      // Endpoint may be unimplemented (404 reject); default to not consented.
      this.setData({ consented: false })
    }
  },

  onDateChange(e: WechatMiniprogram.PickerChange) {
    this.setData({ metricDate: String(e.detail.value) })
  },
  onWeight(e: WechatMiniprogram.Input) { this.setData({ weight: e.detail.value }) },
  onBodyFat(e: WechatMiniprogram.Input) { this.setData({ bodyFatRate: e.detail.value }) },
  onMuscle(e: WechatMiniprogram.Input) { this.setData({ muscleMass: e.detail.value }) },
  onWaist(e: WechatMiniprogram.Input) { this.setData({ waist: e.detail.value }) },
  onChest(e: WechatMiniprogram.Input) { this.setData({ chest: e.detail.value }) },
  onArm(e: WechatMiniprogram.Input) { this.setData({ arm: e.detail.value }) },
  onThigh(e: WechatMiniprogram.Input) { this.setData({ thigh: e.detail.value }) },
  onNotes(e: WechatMiniprogram.Input) { this.setData({ notes: e.detail.value }) },

  // —— Photo upload flow with PIPL consent gate —— //
  tapUpload(e: WechatMiniprogram.TouchEvent) {
    const pose = (e.currentTarget.dataset.pose as string) || "front"
    if (!this.data.consented) {
      this.setData({ showConsent: true, pendingPose: pose })
      return
    }
    this.choosePhoto(pose)
  },

  closeConsent() {
    this.setData({ showConsent: false, pendingPose: "" })
  },

  async agreeConsent() {
    try {
      await setPhotoConsent()
    } catch (e) {
      // Backend not ready yet — proceed locally; consent re-checked on next load.
    }
    const pose = this.data.pendingPose
    this.setData({ consented: true, showConsent: false, pendingPose: "" })
    this.choosePhoto(pose)
  },

  choosePhoto(pose: string) {
    wx.chooseMedia({
      count: 1,
      mediaType: ["image"],
      sourceType: ["album", "camera"],
      success: (res) => {
        const file = res.tempFiles && res.tempFiles[0]
        if (!file) return
        const photos = Object.assign({}, this.data.photos)
        photos[pose] = file.tempFilePath
        this.setData({ photos })
        // Upload is best-effort and non-blocking; failure does not interrupt entry.
      },
      fail: () => {
        // User cancelled or chooser failed — silently ignore, do not crash.
      },
    })
  },

  async submit() {
    if (this.data.submitting) return
    const weight = this.data.weight.trim()
    const bodyFat = this.data.bodyFatRate.trim()
    if (!weight) { wx.showToast({ title: "请填写体重", icon: "none" }); return }
    if (!bodyFat) { wx.showToast({ title: "请填写体脂率", icon: "none" }); return }

    const circumferences: any = {}
    if (this.data.waist.trim()) circumferences.waist = Number(this.data.waist)
    if (this.data.chest.trim()) circumferences.chest = Number(this.data.chest)
    if (this.data.arm.trim()) circumferences.arm = Number(this.data.arm)
    if (this.data.thigh.trim()) circumferences.thigh = Number(this.data.thigh)

    const payload: any = {
      metric_date: this.data.metricDate,
      weight: Number(weight),
      body_fat_rate: Number(bodyFat),
      circumferences,
      notes: this.data.notes.trim(),
    }
    if (this.data.muscleMass.trim()) payload.muscle_mass = Number(this.data.muscleMass)

    this.setData({ submitting: true })
    try {
      await addMetric(payload)
      wx.showToast({ title: "已上传", icon: "success" })
      setTimeout(() => wx.navigateBack(), 700)
    } catch (e) {
      wx.showToast({ title: "上传失败，请稍后再试", icon: "none" })
    } finally {
      this.setData({ submitting: false })
    }
  },
})
