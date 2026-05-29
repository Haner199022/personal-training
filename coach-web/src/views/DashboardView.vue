<script setup lang="ts">
import { ref, onMounted } from "vue"
import api from "@/api/client"

interface Kpi { label: string; value: string; tone: "green" | "yellow" | "cyan" }
const kpis = ref<Kpi[]>([
  { label: "今日已打卡", value: "—", tone: "green" },
  { label: "待点评", value: "—", tone: "yellow" },
  { label: "活跃学员", value: "—", tone: "cyan" },
])
const studentCount = ref<number | null>(null)

onMounted(async () => {
  try {
    const { data } = await api.get<{ items: unknown[] }>("/coaches/me/students")
    studentCount.value = data.items.length
    kpis.value[2].value = String(data.items.length)
    kpis.value[0].value = "0"
    kpis.value[1].value = "0"
  } catch {
    /* 后端未启动时保持占位 */
  }
})
</script>

<template>
  <div>
    <div class="micro">TODAY · {{ new Date().toLocaleDateString("zh-CN") }}</div>
    <h1 class="h1" style="margin:8px 0 4px">今日概览</h1>
    <p class="lede" style="margin-bottom:36px">教练-学员周触达频次，是续课率的关键杠杆。</p>

    <div class="kpis">
      <div v-for="k in kpis" :key="k.label" class="card kpi" :class="`kpi-${k.tone}`">
        <div class="micro">{{ k.label }}</div>
        <div class="kpi-val">{{ k.value }}</div>
      </div>
    </div>

    <div class="card" style="margin-top:28px">
      <div class="h3" style="margin-bottom:4px">打卡 Feed</div>
      <p class="caption">C-1 / E5：可按学员聚合、筛选 —— 实现后此处实时滚动学员打卡。</p>
      <el-empty description="暂无打卡（接入打卡接口后显示）" />
    </div>
  </div>
</template>

<style scoped>
.kpis { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.kpi { transition: box-shadow .2s ease; }
.kpi-val { font-size: 44px; font-weight: 800; letter-spacing: -0.03em; margin-top: 12px; }
.kpi-green .kpi-val { color: var(--c-data-green); }
.kpi-yellow .kpi-val { color: var(--c-data-yellow); }
.kpi-cyan .kpi-val { color: var(--c-data-cyan); }
.kpi-green:hover  { box-shadow: var(--glow-green); }
.kpi-yellow:hover { box-shadow: var(--glow-yellow); }
.kpi-cyan:hover   { box-shadow: var(--glow-cyan); }
</style>
