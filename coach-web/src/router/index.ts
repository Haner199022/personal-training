import { createRouter, createWebHistory } from "vue-router"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/login", name: "login", component: () => import("@/views/LoginView.vue") },
    { path: "/", name: "dashboard", component: () => import("@/views/DashboardView.vue") },
    { path: "/students", name: "students", component: () => import("@/views/StudentsView.vue") },
    { path: "/plan", name: "plan", component: () => import("@/views/PlanEditorView.vue") },
    { path: "/check-in/:id", name: "checkin", component: () => import("@/views/CheckInDetailView.vue") },
  ],
})

// 简单守卫：未登录一律回 /login
router.beforeEach((to) => {
  const authed = !!localStorage.getItem("pt_token")
  if (!authed && to.name !== "login") return { name: "login" }
  if (authed && to.name === "login") return { name: "dashboard" }
})

export default router
