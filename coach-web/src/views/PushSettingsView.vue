<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "@/api/client"
import { ElMessage } from "element-plus"

const router = useRouter()
const s = ref<any>(null)
const advOpen = ref(false)

const TEMPLATES = [
  { name: "训练打卡提醒", desc: "每日 18:00 给当天未打卡学员", on: true },
  { name: "教练点评通知", desc: "教练点评打卡后实时推", on: true },
  { name: "报名/续费提醒", desc: "操作即弹窗，高授权率", on: true },
]

async function load() { s.value = (await api.get("/coaches/me/push-settings")).data }
onMounted(load)
async function save() {
  await api.put("/coaches/me/push-settings", { subscribe_enabled: s.value.subscribe_enabled, inbox_enabled: s.value.inbox_enabled })
  ElMessage.success("已保存推送设置")
}
</script>

<template>
  <div v-if="s" class="wrap">
    <div class="micro"><span class="back" @click="router.push('/settings')">← 设置</span> · C-9 · PUSH</div>
    <h1 class="h1" style="margin:8px 0 6px">推送设置</h1>
    <p class="lede" style="margin-bottom:24px">主推：一次性订阅 + 站内信兜底（ADR-0015）。企微群机器人降为可选高级通道。</p>

    <div class="card sec">
      <div class="h3" style="margin-bottom:14px">主推通道</div>
      <div class="row"><div><div class="t">订阅消息</div><div class="caption">事件触发式（点评/报名/提醒），健身行业无长期订阅资格</div></div>
        <el-switch v-model="s.subscribe_enabled" /></div>
      <div class="row"><div><div class="t">站内信兜底</div><div class="caption">每个事件至少落站内信，学员进小程序补看</div></div>
        <el-switch v-model="s.inbox_enabled" /></div>
    </div>

    <div class="card sec">
      <div class="h3" style="margin-bottom:14px">订阅模板状态</div>
      <div v-for="t in TEMPLATES" :key="t.name" class="row">
        <div><div class="t">{{ t.name }}</div><div class="caption">{{ t.desc }}</div></div>
        <span class="badge" :class="t.on ? 'on' : ''">{{ t.on ? "已启用" : "未启用" }}</span>
      </div>
    </div>

    <div class="card sec">
      <div class="adv-head" @click="advOpen = !advOpen">
        <span class="h3">▾ 高级：企业微信群机器人（可选）</span>
        <span class="badge" :class="s.enterprise_wechat_configured ? 'on' : ''">{{ s.enterprise_wechat_configured ? "已配置" : "未配置" }}</span>
      </div>
      <div v-if="advOpen" style="margin-top:14px">
        <p class="caption">适合 10+ 学员的工作室教练。webhook URL 加密存储（fernet），20 msg/min 限频走队列。</p>
        <el-input placeholder="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=..." style="margin-top:10px" />
        <el-button size="small" style="margin-top:10px">保存并测试推送</el-button>
      </div>
    </div>

    <el-button type="primary" @click="save">保存</el-button>
  </div>
</template>

<style scoped>
.wrap { max-width: 720px; } .back { cursor: pointer; color: var(--c-brand); }
.sec { margin-bottom: 20px; }
.row { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--c-border); }
.t { font-weight: 600; }
.badge { font-size: 12px; padding: 3px 10px; border-radius: 6px; background: var(--c-bg-elev-2); color: var(--c-text-mute); }
.badge.on { color: var(--c-data-green); }
.adv-head { display: flex; justify-content: space-between; align-items: center; cursor: pointer; }
</style>
