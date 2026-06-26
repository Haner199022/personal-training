import { getPhotos, getMetrics } from "../../services/api"

// One photo record: { date, url, body_fat? }
type Photo = { date: string; url?: string; body_fat?: number }

Page({
  data: {
    poseList: [
      { key: "front", label: "正面" },
      { key: "side", label: "侧面" },
      { key: "back", label: "背面" },
    ],
    pose: "front",
    photos: [] as Photo[],
    dateLabels: [] as string[],
    leftIndex: 0,
    rightIndex: 0,
    leftPhoto: null as Photo | null,
    rightPhoto: null as Photo | null,
    showSummary: false,
    summaryFrom: "",
    summaryTo: "",
  },

  async onLoad(options) {
    // 入口可带 ?pose=front/side/back
    const pose = options && options.pose ? String(options.pose) : "front"
    const valid = ["front", "side", "back"]
    this.setData({ pose: valid.indexOf(pose) >= 0 ? pose : "front" })
    await this.loadPhotos()
  },

  // 切换姿态 chip
  switchPose(e: WechatMiniprogram.TouchEvent) {
    const pose = e.currentTarget.dataset.pose as string
    if (!pose || pose === this.data.pose) return
    this.setData({ pose })
    this.loadPhotos()
  },

  // 拉取当前姿态照片，try/catch 优雅降级
  async loadPhotos() {
    let photos: Photo[] = []
    try {
      const res: any = await getPhotos(this.data.pose)
      const raw = Array.isArray(res) ? res : (res && res.items) ? res.items : []
      photos = (raw as any[]).map((p) => ({
        date: p.date || p.created_at || "—",
        url: p.url || p.image_url || "",
        body_fat: typeof p.body_fat === "number" ? p.body_fat : undefined,
      }))
    } catch (e) {
      photos = []
    }

    const dateLabels = photos.map((p) => p.date)
    // 默认：左=最早，右=最新
    const leftIndex = 0
    const rightIndex = photos.length > 0 ? photos.length - 1 : 0

    this.setData({
      photos,
      dateLabels,
      leftIndex,
      rightIndex,
      leftPhoto: photos.length > 0 ? photos[leftIndex] : null,
      rightPhoto: photos.length > 0 ? photos[rightIndex] : null,
    })
    this.refreshSummary()
  },

  // —— 日期选择 —— //
  onLeftPick(e: WechatMiniprogram.PickerChange) {
    const i = Number(e.detail.value)
    this.setData({ leftIndex: i, leftPhoto: this.data.photos[i] || null })
    this.refreshSummary()
  },
  onRightPick(e: WechatMiniprogram.PickerChange) {
    const i = Number(e.detail.value)
    this.setData({ rightIndex: i, rightPhoto: this.data.photos[i] || null })
    this.refreshSummary()
  },

  // —— ◀▶ 步进 —— //
  leftPrev() { this.stepLeft(-1) },
  leftNext() { this.stepLeft(1) },
  rightPrev() { this.stepRight(-1) },
  rightNext() { this.stepRight(1) },

  stepLeft(delta: number) {
    const n = this.data.photos.length
    if (n === 0) return
    let i = this.data.leftIndex + delta
    if (i < 0) i = 0
    if (i > n - 1) i = n - 1
    this.setData({ leftIndex: i, leftPhoto: this.data.photos[i] || null })
    this.refreshSummary()
  },
  stepRight(delta: number) {
    const n = this.data.photos.length
    if (n === 0) return
    let i = this.data.rightIndex + delta
    if (i < 0) i = 0
    if (i > n - 1) i = n - 1
    this.setData({ rightIndex: i, rightPhoto: this.data.photos[i] || null })
    this.refreshSummary()
  },

  // 同期体脂趋势：优先用照片自带 body_fat，缺失时回退 getMetrics 按日期匹配
  async refreshSummary() {
    const left = this.data.leftPhoto
    const right = this.data.rightPhoto
    if (!left || !right) {
      this.setData({ showSummary: false })
      return
    }

    let from = left.body_fat
    let to = right.body_fat

    if (from === undefined || to === undefined) {
      try {
        const res: any = await getMetrics()
        const raw = Array.isArray(res) ? res : (res && res.items) ? res.items : []
        const byDate: Record<string, number> = {}
        ;(raw as any[]).forEach((m) => {
          const d = m.date || m.created_at
          const bf = typeof m.body_fat === "number" ? m.body_fat : undefined
          if (d && bf !== undefined) byDate[String(d)] = bf
        })
        if (from === undefined && byDate[left.date] !== undefined) from = byDate[left.date]
        if (to === undefined && byDate[right.date] !== undefined) to = byDate[right.date]
      } catch (e) {
        // 取不到就隐藏汇总，不让页面崩溃
      }
    }

    if (from !== undefined && to !== undefined) {
      this.setData({
        showSummary: true,
        summaryFrom: String(from),
        summaryTo: String(to),
      })
    } else {
      this.setData({ showSummary: false })
    }
  },

  // 空态跳转去录入体脂数据（栈页）
  toMetric() {
    wx.navigateTo({ url: "/pages/metric/metric" })
  },
})
