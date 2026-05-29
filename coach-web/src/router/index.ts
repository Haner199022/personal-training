import { createRouter, createWebHistory } from "vue-router"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/login", name: "login", component: () => import("@/views/LoginView.vue") },
    { path: "/register", name: "register", component: () => import("@/views/RegisterView.vue") },
    { path: "/", name: "dashboard", component: () => import("@/views/DashboardView.vue") },
    { path: "/students", name: "students", component: () => import("@/views/StudentsView.vue") },
    { path: "/students/:id", name: "student-detail", component: () => import("@/views/StudentDetailView.vue") },
    { path: "/students/:id/body", name: "body-trend", component: () => import("@/views/BodyTrendView.vue") },
    { path: "/students/:id/plan", name: "plan-editor", component: () => import("@/views/PlanEditorView.vue") },
    { path: "/check-in/:id", name: "checkin", component: () => import("@/views/CheckInDetailView.vue") },
    { path: "/exercises", name: "exercises", component: () => import("@/views/ExercisesView.vue") },
    { path: "/settings", name: "settings", component: () => import("@/views/SettingsView.vue") },
    { path: "/settings/push", name: "push", component: () => import("@/views/PushSettingsView.vue") },
  ],
})

router.beforeEach((to) => {
  const authed = !!localStorage.getItem("pt_token")
  const open = to.name === "login" || to.name === "register"
  if (!authed && !open) return { name: "login" }
  if (authed && to.name === "login") return { name: "dashboard" }
})

export default router
