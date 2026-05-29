<script setup lang="ts">
import { RouterView, RouterLink } from "vue-router"
</script>

<template>
  <el-container style="height: 100vh">
    <el-aside width="200px" class="aside">
      <h2 class="logo">私教助理</h2>
      <nav class="nav">
        <RouterLink to="/">今日概览</RouterLink>
        <RouterLink to="/students">学员</RouterLink>
        <RouterLink to="/plan">训练计划</RouterLink>
      </nav>
    </el-aside>
    <el-main><RouterView /></el-main>
  </el-container>
</template>

<style scoped>
.aside { background: #1f2329; color: #fff; padding: 16px; }
.logo { font-size: 18px; margin: 0 0 24px; }
.nav { display: flex; flex-direction: column; gap: 12px; }
.nav a { color: #c0c4cc; text-decoration: none; }
.nav a.router-link-active { color: #409eff; font-weight: 600; }
</style>
