<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from "vue-router"
import { computed } from "vue"

const route = useRoute()
const isAuthShell = computed(() => route.name !== "login")
</script>

<template>
  <!-- 登录页：无侧栏全幅 -->
  <RouterView v-if="!isAuthShell" />

  <!-- 主框架：左暗色导航 + 右内容 -->
  <div v-else class="shell">
    <aside class="aside">
      <div class="brand">
        <div class="brand-mark">PT</div>
        <div>
          <div class="brand-name">私教助理</div>
          <div class="micro">COACH CONSOLE</div>
        </div>
      </div>

      <nav class="nav">
        <RouterLink to="/" class="nav-item">今日概览</RouterLink>
        <RouterLink to="/students" class="nav-item">学员</RouterLink>
        <RouterLink to="/plan" class="nav-item">训练计划</RouterLink>
      </nav>

      <div class="aside-foot">
        <div class="divider" style="margin-bottom:16px" />
        <div class="micro">v7 · DARK MAGAZINE</div>
      </div>
    </aside>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.shell { display: grid; grid-template-columns: 248px 1fr; height: 100vh; }

.aside {
  background: var(--c-bg-elev);
  border-right: 1px solid var(--c-border);
  padding: 28px 22px;
  display: flex; flex-direction: column;
}
.brand { display: flex; align-items: center; gap: 12px; margin-bottom: 40px; }
.brand-mark {
  width: 40px; height: 40px; border-radius: 11px;
  background: var(--c-brand); color: #fff; font-weight: 800;
  display: grid; place-items: center; font-size: 16px;
  box-shadow: var(--shadow-cta-strong);
}
.brand-name { font-weight: 700; font-size: 16px; letter-spacing: -0.01em; }

.nav { display: flex; flex-direction: column; gap: 6px; }
.nav-item {
  color: var(--c-text-mute); text-decoration: none;
  padding: 11px 14px; border-radius: 10px; font-size: 14px;
  transition: all .15s ease;
}
.nav-item:hover { color: var(--c-text-base); background: var(--c-bg-elev-2); }
.nav-item.router-link-active {
  color: var(--c-text-base); background: var(--c-brand-soft);
  box-shadow: inset 2px 0 0 var(--c-brand);
}

.aside-foot { margin-top: auto; }

.content {
  padding: 48px 56px; overflow-y: auto;
  background: var(--c-bg) var(--gradient-brand-glow) no-repeat;
}
</style>
