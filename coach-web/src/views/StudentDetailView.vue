<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "@/api/client"
import { ElMessage } from "element-plus"

const route = useRoute(), router = useRouter()
const sid = Number(route.params.id)
const d = ref<any>(null)
const tab = ref("train")
const metrics = ref<any[]>([])
const metricOpen = ref(false)
const newMetric = ref<any>({ date: new Date().toISOString().slice(0, 10), weight_kg: null, body_fat_pct: null, waist_cm: null, chest_cm: null, arm_cm: null })

const SRC: Record<string, string> = { private: "私单", gym_assigned: "场馆派", referral: "转介", trial_class: "试课", other: "其他" }

async function load() {
  d.value = (await api.get(`/coaches/me/students/${sid}`)).data
  metrics.value = (await api.get(`/coaches/me/students/${sid}/metrics`)).data.items
}
onMounted(load)

const riskSignals = computed(() => {
  const r: string[] = []
  if (!d.value) return r
  if (d.value.next_due_date) {
    const days = Math.round((+new Date(d.value.next_due_date) - Date.now()) / 86400000)
    if (days <= 7) r.push(`包月将于 ${days} 天内到期（${d.value.next_due_date}）`)
  }
  return r
})
const latest = computed(() => metrics.value.at(-1))
const first = computed(() => metrics.value[0])

async function saveProfile() {
  await api.put(`/coaches/me/students/${sid}`, { alias: d.value.alias, goal: d.value.goal, health_notes: d.value.health_notes,
    next_due_date: d.value.next_due_date, remaining_sessions: d.value.remaining_sessions })
  ElMessage.success("资料已保存")
}
async function saveMetric() {
  await api.post(`/coaches/me/students/${sid}/metrics`, newMetric.value)
  metricOpen.value = false
  ElMessage.success("已录入体脂")
  await load()
}
</script>

<template>
  <div v-if="d">
    <div class="micro"><span class="back" @click="router.push('/students')">← 返回</span> · C-3 学员档案</div>
    <h1 class="h1" style="margin:8px 0 4px">{{ d.alias }}
      <span class="sub">{{ d.gender === 1 ? "男" : "女" }} · {{ d.height_cm }}cm · {{ SRC[d.source] }}</span>
    </h1>
    <p class="lede" style="margin-bottom:4px">{{ d.goal }}</p>
    <div class="tags">
      <span v-for="t in d.tags" :key="t.name" class="tagchip" :class="`t-${t.color}`">{{ t.name }}</span>
    </div>

    <div v-if="riskSignals.length" class="card risk">
      <div class="h3" style="margin-bottom:8px;color:var(--c-data-yellow)">⚠ 风险信号</div>
      <div v-for="(s,i) in riskSignals" :key="i" class="risk-row">· {{ s }}</div>
      <el-button size="small" style="margin-top:10px">我已知悉，本周不再提示</el-button>
    </div>

    <el-tabs v-model="tab" class="tabs">
      <!-- 训练 -->
      <el-tab-pane label="训练" name="train">
        <div class="card">
          <div class="row"><span class="muted">当前计划</span><span>5月增肌周期 W3</span>
            <el-button size="small" @click="router.push(`/students/${sid}/plan`)">查看/编辑计划</el-button></div>
          <div class="row"><span class="muted">本周完成度</span><span>周一✅ 周二✅ 周三— 周四⏳ 周五⏳</span></div>
          <div class="row"><span class="muted">打卡热力</span><span class="heat">▓▓░▓▓░░ ▓▓▓▓░░░ ▓▓░░░░░</span></div>
        </div>
      </el-tab-pane>

      <!-- 体脂 -->
      <el-tab-pane label="体脂" name="body">
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <div class="h3">近期体脂</div>
            <div style="display:flex;gap:10px">
              <el-button size="small" @click="metricOpen = true">＋ 帮学员录体脂</el-button>
              <el-button size="small" type="primary" @click="router.push(`/students/${sid}/body`)">查看完整趋势 →</el-button>
            </div>
          </div>
          <div v-if="latest" class="stats">
            <div class="stat"><div class="micro">体脂率</div><div class="big" style="color:var(--c-data-green)">{{ latest.body_fat_pct?.toFixed(1) }}%</div>
              <div class="caption">{{ first?.body_fat_pct?.toFixed(1) }} → {{ latest.body_fat_pct?.toFixed(1) }}</div></div>
            <div class="stat"><div class="micro">体重</div><div class="big" style="color:var(--c-data-cyan)">{{ latest.weight_kg?.toFixed(1) }}kg</div>
              <div class="caption">{{ first?.weight_kg?.toFixed(1) }} → {{ latest.weight_kg?.toFixed(1) }}</div></div>
            <div class="stat"><div class="micro">腰围</div><div class="big">{{ latest.waist_cm?.toFixed(0) }}cm</div>
              <div class="caption">{{ first?.waist_cm?.toFixed(0) }} → {{ latest.waist_cm?.toFixed(0) }}</div></div>
          </div>
          <el-empty v-else description="暂无体脂记录" />
        </div>
      </el-tab-pane>

      <!-- 资料 -->
      <el-tab-pane label="资料" name="info">
        <div class="card">
          <div class="h3" style="margin-bottom:14px">基本信息</div>
          <el-form label-width="90px" label-position="left">
            <el-form-item label="备注名"><el-input v-model="d.alias" /></el-form-item>
            <el-form-item label="训练目标"><el-input v-model="d.goal" type="textarea" :rows="2" /></el-form-item>
            <el-form-item label="开始合作">{{ d.coaching_started_at }} <span class="caption" style="margin-left:8px">（H2 实际合作起始）</span></el-form-item>
          </el-form>
          <div class="divider" style="margin:12px 0" />
          <div class="h3" style="margin-bottom:14px">服务台账 <span class="caption">（手动维护，不接支付）</span></div>
          <el-form label-width="90px" label-position="left" inline>
            <el-form-item label="包月到期"><el-input v-model="d.next_due_date" style="width:140px" /></el-form-item>
            <el-form-item label="剩余课时"><el-input v-model.number="d.remaining_sessions" style="width:90px" /></el-form-item>
            <el-form-item label="累计付款">{{ d.lifetime_paid_yuan }} 元</el-form-item>
          </el-form>
          <div class="divider" style="margin:12px 0" />
          <div class="h3" style="margin-bottom:14px">健康备忘 <span class="caption">（禁忌动作在编辑计划时红色警告）</span></div>
          <el-input v-model="d.health_notes" type="textarea" :rows="2" placeholder="伤病史 / 用药 / 健康备注" />
          <div class="caption" style="margin-top:8px">禁忌动作 ID：{{ d.contraindicated_exercise_ids.length ? d.contraindicated_exercise_ids.join(", ") : "无" }}</div>
          <div style="margin-top:18px;display:flex;gap:12px">
            <el-button type="primary" @click="saveProfile">保存资料</el-button>
            <el-button>停止服务 ▾</el-button>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="metricOpen" title="帮学员录体脂" width="420">
      <el-form label-width="70px" label-position="left">
        <el-form-item label="日期"><el-input v-model="newMetric.date" /></el-form-item>
        <el-form-item label="体重"><el-input v-model.number="newMetric.weight_kg" placeholder="kg" /></el-form-item>
        <el-form-item label="体脂率"><el-input v-model.number="newMetric.body_fat_pct" placeholder="%" /></el-form-item>
        <el-form-item label="腰围"><el-input v-model.number="newMetric.waist_cm" placeholder="cm" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="metricOpen=false">取消</el-button><el-button type="primary" @click="saveMetric">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<style scoped>
.back { cursor: pointer; color: var(--c-brand); } .sub { font-size: 16px; color: var(--c-text-mute); font-weight: 400; }
.tags { display: flex; gap: 8px; margin: 10px 0 20px; }
.tagchip { font-size: 12px; padding: 3px 10px; border-radius: 6px; background: var(--c-bg-elev-2); }
.t-cyan { color: var(--c-data-cyan); } .t-green { color: var(--c-data-green); } .t-yellow { color: var(--c-data-yellow); }
.risk { border-left: 2px solid var(--c-data-yellow); margin-bottom: 16px; }
.risk-row { color: var(--c-data-yellow); font-size: 14px; padding: 2px 0; }
.row { display: flex; align-items: center; gap: 16px; padding: 12px 0; border-bottom: 1px solid var(--c-border); }
.row .muted { color: var(--c-text-mute); width: 90px; } .heat { font-family: monospace; letter-spacing: 2px; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.stat { background: var(--c-bg-elev-2); border-radius: 12px; padding: 18px; }
.big { font-size: 30px; font-weight: 800; margin: 6px 0; }
</style>
