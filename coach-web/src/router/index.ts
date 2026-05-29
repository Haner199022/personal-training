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
export default router
