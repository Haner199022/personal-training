// 学员端入口。v7 暗色杂志风（与教练端统一品牌紫，见 2026-05-27 体检：两端 token 一致）。
App<{ globalData: { apiBase: string } }>({
  globalData: {
    // dev 指向本机后端；真机需备案 HTTPS 域名 + 开发者工具勾「不校验合法域名」
    // dev 后端走 8001（8000 被 AI Team OS API 占用）；真机需备案 HTTPS 域名 + 开发者工具勾「不校验合法域名」
    apiBase: "http://127.0.0.1:8001/api/v1",
  },
  onLaunch() {
    if (!wx.getStorageSync("pt_stoken")) {
      // 未登录：交由首页守卫跳登录（tabBar 页无法 redirect 到非 tab，故登录用 reLaunch）
    }
  },
})
