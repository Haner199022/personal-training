import { getPhotoConsent, revokePhotoConsent } from "../../services/api"

Page({
  data: {
    consented: false,        // whether photo consent is currently granted
    consentDate: "",         // YYYY-MM-DD, shown only when granted and available
    showConfirm: false,      // page-level revoke confirmation sheet
    revoking: false,         // guard against double-tap on confirm
  },

  async onLoad() {
    await this.loadConsent()
  },

  async loadConsent() {
    try {
      const r: any = await getPhotoConsent()
      // Backend field shape is not finalized; read defensively, default to not-consented.
      const granted = !!(r && (r.consented ?? r.consent ?? r.granted ?? r.status === "granted"))
      const raw = r && (r.consent_at || r.granted_at || r.updated_at || r.consented_at || "")
      this.setData({
        consented: granted,
        consentDate: granted ? this.fmtDate(raw) : "",
      })
    } catch (e) {
      // Endpoint may 404 / reject — degrade to default "未同意", never crash.
      this.setData({ consented: false, consentDate: "" })
    }
  },

  fmtDate(raw: string): string {
    if (!raw) return ""
    // Accept "2026-06-26", "2026-06-26T08:00:00Z", "2026/06/26" etc -> "YYYY-MM-DD"
    const m = String(raw).match(/(\d{4})[-/](\d{2})[-/](\d{2})/)
    return m ? `${m[1]}-${m[2]}-${m[3]}` : ""
  },

  openConfirm() {
    if (!this.data.consented) return // disabled when not consented
    this.setData({ showConfirm: true })
  },

  closeConfirm() {
    this.setData({ showConfirm: false })
  },

  // Stop the inner sheet tap from bubbling to the mask's close handler.
  noop() {},

  async confirmRevoke() {
    if (this.data.revoking) return
    this.setData({ revoking: true })
    try {
      await revokePhotoConsent()
      this.setData({ consented: false, consentDate: "", showConfirm: false })
      wx.showToast({ title: "已撤回", icon: "success" })
    } catch (e) {
      wx.showToast({ title: "撤回失败，请稍后再试", icon: "none" })
    } finally {
      this.setData({ revoking: false })
    }
  },
})
