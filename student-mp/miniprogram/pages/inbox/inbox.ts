import { getInbox, markInboxRead } from "../../services/api"
Page({
  data: { items: [] as any[] },
  async onShow() {
    if (!wx.getStorageSync("pt_stoken")) { wx.reLaunch({ url: "/pages/login/login" }); return }
    await this.load()
  },
  async load() {
    try {
      const res = await getInbox()
      const list = res.items || res || []
      this.setData({ items: list })
    } catch (e) {
      this.setData({ items: [] })
    }
  },
  async tapItem(e: WechatMiniprogram.TouchEvent) {
    const id = e.currentTarget.dataset.id
    const link = e.currentTarget.dataset.link
    // Mark read on the server; ignore failures (endpoint may not exist yet).
    try { await markInboxRead(id) } catch (e) {}
    // Locally mark this item as read so the dot/label updates immediately.
    const items = (this.data.items as any[]).map(it => it.id === id ? { ...it, read: true } : it)
    this.setData({ items })
    // Navigate only when the message carries a link to a stack page.
    if (link) { wx.navigateTo({ url: link }) }
  },
})
