<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import { useRouter } from "vue-router"
import api from "@/api/client"

const router = useRouter()
const dash = ref<any>({ student_total: 0, active: 0, uncommented: 0, risk_signals: [] })
const feed = ref<any[]>([])
const view = ref<"timeline" | "byStudent">("timeline")
const filter = ref<"all" | "uncommented">("all")

async function load() {
  dash.value = (await api.get("/coaches/me/dashboard")).data
  const status = filter.value === "uncommented" ? "uncommented" : "all"
  feed.value = (await api.get("/coaches/me/check-ins", { params: { status } })).data.items
}
onMounted(load)

const byStudent = computed(() => {
  const m: Record<string, any[]> = {}
  for (const c of feed.value) (m[c.student_name] ??= []).push(c)
  return Object.entries(m)
})
const kpis = computed(() => [
  { label: "学员总数", value: dash.value.student_total, tone: "cyan" },
  { label: "活跃学员", value: dash.value.active, tone: "green" },
  { label: "待点评", value: dash.value.uncommented, tone: "yellow" },
])
</script>

<template>
  <div>
    <div class="micro">TODAY · {{ new Date().toLocaleDateString("zh-CN") }}</div>
    <h1 class="h1" style="margin:8px 0 4px">今日概览</h1>
    <p class="lede" style="margin-bottom:32px">教练-学员周触达频次，是续课率的关键杠杆。</p>

    <div class="kpis">
      <div v-for="k in kpis" :key="k.label" class="card kpi" :class="`kpi-${k.tone}`">
        <div class="micro">{{ k.label }}</div>
        <div class="kpi-val">{{ k.value }}</div>
      </div>
    </div>

    <div class="card todo" v-if="dash.risk_signals.length">
      <div class="h3" style="margin-bottom:12px">📋 待办 · 风险信号</div>
      <div v-for="(s, i) in dash.risk_signals" :key="i" class="todo-row">⚠ {{ s }}</div>
    </div>

    <div class="card" style="margin-top:24px">
      <div class="feed-head">
        <div class="h3">打卡动态</div>
        <div class="controls">
          <el-radio-group v-model="view" size="small">
            <el-radio-button value="timeline">时间线</el-radio-button>
            <el-radio-button value="byStudent">按学员</el-radio-button>
          </el-radio-group>
          <el-select v-model="filter" size="small" style="width:120px" @change="load">
            <el-option label="全部" value="all" />
            <el-option label="未点评" value="uncommented" />
          </el-select>
        </div>
      </div>

      <el-empty v-if="!feed.length" description="暂无打卡" />

      <template v-else-if="view === 'timeline'">
        <div v-for="c in feed" :key="c.id" class="feed-row" @click="router.push(`/check-in/${c.id}`)">
          <span class="dot" :class="c.commented ? 'done' : 'pending'" />
          <span class="who">{{ c.student_name }}</span>
          <span class="muted">完成「{{ c.plan_title }}」 · 感受{{ c.feeling }}/5 RPE{{ c.rpe }}</span>
          <span class="tag" :class="c.commented ? 'g' : 'r'">{{ c.commented ? "✅已点评" : "🔴未点评" }}</span>
        </div>
      </template>

      <template v-else>
        <div v-for="[name, list] in byStudent" :key="name" class="grp">
          <span class="who">👤 {{ name }}</span>
          <span class="muted">本周打卡 {{ list.length }}</span>
          <span class="tag" :class="list.some(x=>!x.commented) ? 'r' : 'g'">
            {{ list.filter(x=>!x.commented).length ? `🔴 ${list.filter(x=>!x.commented).length} 待点评` : "✅ 全部已点评" }}
          </span>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.kpis { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.kpi-val { font-size: 44px; font-weight: 800; letter-spacing: -0.03em; margin-top: 12px; }
.kpi-green .kpi-val { color: var(--c-data-green); } .kpi-yellow .kpi-val { color: var(--c-data-yellow); } .kpi-cyan .kpi-val { color: var(--c-data-cyan); }
.kpi-green:hover { box-shadow: var(--glow-green); } .kpi-yellow:hover { box-shadow: var(--glow-yellow); } .kpi-cyan:hover { box-shadow: var(--glow-cyan); }
.todo { margin-top: 24px; border-left: 2px solid var(--c-data-yellow); }
.todo-row { color: var(--c-data-yellow); font-size: 14px; padding: 4px 0; }
.feed-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.controls { display: flex; gap: 12px; align-items: center; }
.feed-row { display: flex; align-items: center; gap: 12px; padding: 14px 0; border-bottom: 1px solid var(--c-border); cursor: pointer; }
.feed-row:hover { background: var(--c-bg-elev-2); }
.grp { display: flex; align-items: center; gap: 14px; padding: 14px 0; border-bottom: 1px solid var(--c-border); }
.dot { width: 8px; height: 8px; border-radius: 50%; }
.dot.done { background: var(--c-data-green); box-shadow: var(--glow-green); }
.dot.pending { background: var(--c-data-red); box-shadow: 0 0 10px var(--c-data-red-glow); }
.who { font-weight: 600; } .muted { color: var(--c-text-mute); font-size: 14px; flex: 1; }
.tag { font-size: 13px; } .tag.g { color: var(--c-data-green); } .tag.r { color: var(--c-data-red); }
</style>
