import { getMetrics, getCheckIns } from "../../services/api"

// One bar in the CSS bar-chart.
interface Bar {
  label: string   // x-axis label (date / index)
  value: number   // raw value
  text: string    // value shown above the bar
  heightPct: number // 0..100, mapped against series min/max
}

// One day cell in the month calendar grid.
interface DayCell {
  day: number     // 1..31, 0 = blank padding cell
  symbol: string  // ● done / ○ missed / · no-session
  state: string   // 'done' | 'missed' | 'none' | 'blank'
}

const WEEK_HEADERS = ["一", "二", "三", "四", "五", "六", "日"]

// Map a raw numeric series to bar heights (5..100%), keeping a readable floor.
function toBars(rows: any[], field: string, unit: string): Bar[] {
  const series = rows
    .map((r) => {
      const v = Number(r && (r[field] ?? 0))
      const dateRaw = String((r && (r.metric_date || r.date)) || "")
      const label = dateRaw.length >= 10 ? dateRaw.slice(5) : dateRaw // MM-DD
      return { value: isNaN(v) ? 0 : v, label }
    })
    .filter((r) => r.value > 0)

  if (series.length === 0) return []
  // Keep the most recent ~10 points so the chart stays readable.
  const recent = series.slice(-10)
  const vals = recent.map((r) => r.value)
  const max = Math.max(...vals)
  const min = Math.min(...vals)
  const span = max - min || 1
  return recent.map((r) => {
    // Normalize into 12..100 so even the lowest bar stays visible.
    const pct = Math.round(12 + ((r.value - min) / span) * 88)
    return {
      label: r.label,
      value: r.value,
      text: `${r.value}${unit}`,
      heightPct: pct,
    }
  })
}

// Compute summary row from a numeric series (start / current / delta).
function summarize(rows: any[], field: string, unit: string) {
  const vals = rows
    .map((r) => Number(r && (r[field] ?? 0)))
    .filter((v) => !isNaN(v) && v > 0)
  if (vals.length === 0) return { start: "—", current: "—", delta: "—", deltaState: "none", count: 0 }
  const start = vals[0]
  const current = vals[vals.length - 1]
  const diff = Math.round((current - start) * 10) / 10
  const sign = diff > 0 ? "+" : ""
  return {
    start: `${start}${unit}`,
    current: `${current}${unit}`,
    delta: `${sign}${diff}${unit}`,
    // Lower weight/fat reads as progress (green); higher reads neutral (yellow).
    deltaState: diff < 0 ? "down" : diff > 0 ? "up" : "flat",
    count: vals.length,
  }
}

// Build a Mon-first month grid from check-in records.
function buildCalendar(items: any[]) {
  const now = new Date()
  const year = now.getFullYear()
  const month = now.getMonth() // 0-based
  const monthLabel = `${year} 年 ${month + 1} 月`

  // Map "YYYY-MM-DD" -> state for the current month.
  const dayState: Record<number, string> = {}
  let doneCount = 0
  let plannedCount = 0
  items.forEach((it) => {
    const dateRaw = String((it && (it.date || it.metric_date)) || "")
    if (dateRaw.length < 10) return
    const d = new Date(dateRaw.replace(/-/g, "/"))
    if (d.getFullYear() !== year || d.getMonth() !== month) return
    const day = d.getDate()
    // 'commented'/'completed' style truthiness => done; otherwise missed if a session existed.
    const done = !!(it.completed ?? it.done ?? it.checked_in ?? true)
    dayState[day] = done ? "done" : "missed"
    plannedCount += 1
    if (done) doneCount += 1
  })

  const firstDay = new Date(year, month, 1)
  // JS getDay(): 0=Sun..6=Sat -> convert to Mon-first 0..6.
  let lead = firstDay.getDay() - 1
  if (lead < 0) lead = 6
  const daysInMonth = new Date(year, month + 1, 0).getDate()

  const cells: DayCell[] = []
  for (let i = 0; i < lead; i++) {
    cells.push({ day: 0, symbol: "", state: "blank" })
  }
  for (let d = 1; d <= daysInMonth; d++) {
    const st = dayState[d]
    let symbol = "·"
    let state = "none"
    if (st === "done") { symbol = "●"; state = "done" }
    else if (st === "missed") { symbol = "○"; state = "missed" }
    cells.push({ day: d, symbol, state })
  }
  return { monthLabel, cells, doneCount, plannedCount }
}

Page({
  data: {
    tab: "weight" as "weight" | "fat" | "cal",
    // weight tab
    weightBars: [] as Bar[],
    weightSummary: { start: "—", current: "—", delta: "—", deltaState: "none", count: 0 } as any,
    // fat tab
    fatBars: [] as Bar[],
    fatSummary: { start: "—", current: "—", delta: "—", deltaState: "none", count: 0 } as any,
    metricsEmpty: true,
    // calendar tab
    weekHeaders: WEEK_HEADERS,
    monthLabel: "",
    calCells: [] as DayCell[],
    calDone: 0,
    calPlanned: 0,
    calEmpty: true,
  },

  async onShow() {
    if (!wx.getStorageSync("pt_stoken")) { wx.reLaunch({ url: "/pages/login/login" }); return }
    await Promise.all([this.loadMetrics(), this.loadCalendar()])
  },

  async loadMetrics() {
    try {
      const r = await getMetrics()
      const rows: any[] = (r && (r.items || r.metrics || r)) || []
      const list = Array.isArray(rows) ? rows : []
      // Oldest -> newest so start/current read correctly.
      const ordered = list.slice().sort((a, b) => {
        const da = String(a.metric_date || a.date || "")
        const db = String(b.metric_date || b.date || "")
        return da < db ? -1 : da > db ? 1 : 0
      })
      this.setData({
        weightBars: toBars(ordered, "weight", "kg"),
        weightSummary: summarize(ordered, "weight", "kg"),
        fatBars: toBars(ordered, "body_fat_rate", "%"),
        fatSummary: summarize(ordered, "body_fat_rate", "%"),
        metricsEmpty: ordered.length === 0,
      })
    } catch (e) {
      // Endpoint may 404 / reject — degrade to empty placeholder, never crash.
      this.setData({ weightBars: [], fatBars: [], metricsEmpty: true })
    }
  },

  async loadCalendar() {
    try {
      const r = await getCheckIns()
      const items: any[] = (r && (r.items || r)) || []
      const list = Array.isArray(items) ? items : []
      const cal = buildCalendar(list)
      this.setData({
        monthLabel: cal.monthLabel,
        calCells: cal.cells,
        calDone: cal.doneCount,
        calPlanned: cal.plannedCount,
        calEmpty: list.length === 0,
      })
    } catch (e) {
      this.setData({ calCells: [], calEmpty: true })
    }
  },

  switchTab(e: WechatMiniprogram.TouchEvent) {
    const tab = (e.currentTarget.dataset.tab as "weight" | "fat" | "cal") || "weight"
    this.setData({ tab })
  },

  toMetric() {
    wx.navigateTo({ url: "/pages/metric/metric" })
  },

  toPhotoCompare() {
    wx.navigateTo({ url: "/pages/photo-compare/photo-compare" })
  },
})
