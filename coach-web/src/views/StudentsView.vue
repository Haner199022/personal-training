<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "@/api/client"
import { useStudentColumns, type StudentRow } from "@/composables/columns/useStudentColumns"
import { ElMessage } from "element-plus"

const router = useRouter()
const data = ref<StudentRow[]>([])
const loading = ref(true)
const columns = useStudentColumns((id) => router.push(`/students/${id}`))

const inviteOpen = ref(false), scanOpen = ref(false)
const invite = ref<{ code: string; expires_in_days: number; remaining_uses: number } | null>(null)

async function load() {
  try { data.value = (await api.get("/coaches/me/students")).data.items }
  catch { ElMessage.warning("拉取学员失败（后端未启动？）") }
  finally { loading.value = false }
}
onMounted(load)

async function genInvite() {
  inviteOpen.value = true
  invite.value = (await api.post("/coaches/me/invite-codes")).data
}
function copyCode() { if (invite.value) { navigator.clipboard?.writeText(invite.value.code); ElMessage.success("邀请码已复制") } }
</script>

<template>
  <div>
    <div class="head">
      <div>
        <div class="micro">C-2 · STUDENTS</div>
        <h1 class="h1" style="margin:8px 0 0">学员 <span class="count">{{ data.length }}</span></h1>
      </div>
      <div style="display:flex;gap:12px">
        <el-button @click="scanOpen = true">📷 扫码加学员</el-button>
        <el-button type="primary" @click="genInvite">＋ 邀请新学员</el-button>
      </div>
    </div>

    <div class="card table-wrap" v-loading="loading">
      <el-auto-resizer>
        <template #default="{ height, width }">
          <el-table-v2 :columns="columns" :data="data" :width="width" :height="height" :row-height="58" />
        </template>
      </el-auto-resizer>
    </div>

    <el-dialog v-model="inviteOpen" title="邀请学员" width="420">
      <div v-if="invite" class="invite">
        <div class="micro">小程序邀请码</div>
        <div class="code">{{ invite.code }}</div>
        <div class="qr">▓▓▓<br/>▓░▓<br/>▓▓▓</div>
        <div class="caption">有效期：{{ invite.expires_in_days }} 天 · 剩余使用次数：{{ invite.remaining_uses }}</div>
        <div class="caption" style="margin-top:10px">ⓘ 学员扫码后自动弹 3 个推送授权（报名/点评/训练提醒，ADR-0015），无需建群。</div>
        <div style="margin-top:16px;display:flex;gap:10px">
          <el-button @click="copyCode">复制邀请码</el-button>
          <el-button type="primary">一键发送到微信</el-button>
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="scanOpen" title="扫学员「我的二维码」" width="380">
      <div class="scan">
        <div class="cam">📷<br/>(摄像头)</div>
        <p class="caption">ⓘ 学员小程序 → 我 → 我的二维码。扫码后学员侧弹「确认加入张教练」，确认后落库。</p>
        <div class="caption">（MVP 反向加学员入口，C2；摄像头能力接入待真机）</div>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 28px; }
.count { color: var(--c-brand); font-size: 24px; }
.table-wrap { height: 66vh; padding: 12px; }
.invite { text-align: center; }
.code { font-size: 30px; font-weight: 800; letter-spacing: 0.1em; color: var(--c-brand); margin: 12px 0; }
.qr { font-family: monospace; line-height: 1; font-size: 28px; color: var(--c-text-base); margin: 12px 0; }
.scan { text-align: center; }
.cam { width: 140px; height: 140px; margin: 0 auto 16px; border: 1px dashed var(--c-border-strong); border-radius: 12px; display: grid; place-items: center; color: var(--c-text-mute); }
</style>
