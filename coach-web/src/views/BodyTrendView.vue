<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "@/api/client"
import * as echarts from "echarts"
import { ElMessage } from "element-plus"

const route = useRoute(), router = useRouter()
const sid = Number(route.params.id)
const metrics = ref<any[]>([])
const blur = ref(true)
const elFat = ref<HTMLElement>(), elWeight = ref<HTMLElement>(), elGirth = ref<HTMLElement>()

const AXIS = "#8a8a96", SPLIT = "#26262e"
function baseOpt(dates: string[], series: any[]) {
  return {
    backgroundColor: "transparent",
    grid: { left: 44, right: 20, top: 24, bottom: 28 },
    tooltip: { trigger: "axis" },
    legend: { textStyle: { color: AXIS }, top: 0 },
    xAxis: { type: "category", data: dates, axisLine: { lineStyle: { color: SPLIT } }, axisLabel: { color: AXIS } },
    yAxis: { type: "value", scale: true, axisLine: { lineStyle: { color: SPLIT } }, splitLine: { lineStyle: { color: SPLIT } }, axisLabel: { color: AXIS } },
    series,
  }
}
const line = (name: string, data: number[], color: string) => ({
  name, type: "line", data, smooth: true, symbolSize: 7,
  lineStyle: { color, width: 2 }, itemStyle: { color },
  areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: color + "33" }, { offset: 1, color: color + "00" }]) },
})

async function load() {
  metrics.value = (await api.get(`/coaches/me/students/${sid}/metrics`)).data.items
  await nextTick()
  const dates = metrics.value.map(m => m.date.slice(5))
  echarts.init(elFat.value!).setOption(baseOpt(dates, [line("体脂率 %", metrics.value.map(m => m.body_fat_pct), "#00E676")]))
  echarts.init(elWeight.value!).setOption(baseOpt(dates, [line("体重 kg", metrics.value.map(m => m.weight_kg), "#00D4FF")]))
  echarts.init(elGirth.value!).setOption(baseOpt(dates, [
    line("腰 cm", metrics.value.map(m => m.waist_cm), "#A855F7"),
    line("胸 cm", metrics.value.map(m => m.chest_cm), "#FFB800"),
    line("臂 cm", metrics.value.map(m => m.arm_cm), "#FF3B3B"),
  ]))
}
onMounted(load)

function reveal() {
  ElMessage.info("（演示）需密码二次验证；3 分钟后自动重新遮挡")
  blur.value = false
  setTimeout(() => (blur.value = true), 180000)
}
</script>

<template>
  <div>
    <div class="micro"><span class="back" @click="router.push(`/students/${sid}`)">← 返回</span> · C-6 · BODY TREND</div>
    <div class="head">
      <h1 class="h1" style="margin:8px 0 0">体脂趋势</h1>
      <div style="display:flex;gap:10px;align-items:center">
        <el-select model-value="90" size="small" style="width:120px">
          <el-option label="最近 90 天" value="90" /><el-option label="最近 30 天" value="30" /><el-option label="最近 365 天" value="365" />
        </el-select>
        <el-button size="small">📥 导出周报（PDF）</el-button>
      </div>
    </div>

    <div class="card chart-card"><div class="micro">体脂率 %</div><div ref="elFat" class="chart" /></div>
    <div class="card chart-card"><div class="micro">体重 kg</div><div ref="elWeight" class="chart" /></div>
    <div class="card chart-card"><div class="micro">围度 cm（多线趋势）</div><div ref="elGirth" class="chart" /></div>

    <div class="card">
      <div class="row"><div class="h3">体脂照对比</div>
        <div><span class="caption">🔒 默认模糊（S6 PIPL）</span>
          <el-button size="small" v-if="blur" @click="reveal" style="margin-left:10px">👁 显示</el-button>
          <el-button size="small" v-else @click="blur = true" style="margin-left:10px">🔒 立即遮挡</el-button></div>
      </div>
      <div class="photos">
        <div class="photo" :class="{ blur }">前 · 3/01</div>
        <span class="arrow">⇄</span>
        <div class="photo" :class="{ blur }">前 · 5/20</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.back { cursor: pointer; color: var(--c-brand); }
.head { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 24px; }
.chart-card { margin-bottom: 18px; } .chart { height: 200px; margin-top: 8px; }
.row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.photos { display: flex; align-items: center; gap: 20px; justify-content: center; }
.photo { width: 150px; height: 190px; border-radius: 12px; background: var(--c-bg-elev-2); display: grid; place-items: center; color: var(--c-text-mute); transition: filter .3s; }
.photo.blur { filter: blur(18px); } .arrow { color: var(--c-text-mute); font-size: 22px; }
</style>
