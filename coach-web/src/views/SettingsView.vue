<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import api from "@/api/client"
import { useAuthStore } from "@/stores/auth"
import { ElMessage } from "element-plus"

const router = useRouter(), auth = useAuthStore()
const p = ref<any>(null)
const newCert = ref("")

async function load() { p.value = (await api.get("/coaches/me/profile")).data }
onMounted(load)

async function save() {
  await api.put("/coaches/me/profile", {
    display_name: p.value.display_name, bio: p.value.bio, cert_tags: p.value.cert_tags,
    affiliated_studio: p.value.affiliated_studio, profile_intro_rich: p.value.profile_intro_rich,
    profile_published: p.value.profile_published, risk_days_threshold: p.value.risk_days_threshold,
  })
  ElMessage.success("已保存")
}
function addCert() { if (newCert.value) { p.value.cert_tags.push(newCert.value); newCert.value = "" } }
function logout() { auth.logout(); router.push("/login") }
</script>

<template>
  <div v-if="p" class="wrap">
    <div class="micro">C-8 · SETTINGS</div>
    <h1 class="h1" style="margin:8px 0 28px">设置</h1>

    <div class="card sec">
      <div class="h3">教练资料</div>
      <el-form label-width="80px" label-position="left" style="margin-top:14px">
        <el-form-item label="昵称"><el-input v-model="p.display_name" /></el-form-item>
        <el-form-item label="简介"><el-input v-model="p.bio" type="textarea" :rows="2" /></el-form-item>
        <el-form-item label="资质">
          <div class="chips">
            <span v-for="(c,i) in p.cert_tags" :key="i" class="chip">{{ c }} <span class="x" @click="p.cert_tags.splice(i,1)">×</span></span>
            <el-input v-model="newCert" size="small" style="width:120px" placeholder="+ 添加" @keyup.enter="addCert" />
          </div>
        </el-form-item>
        <el-form-item label="合作场馆"><el-input v-model="p.affiliated_studio" placeholder="（Persona B，可选）" /></el-form-item>
      </el-form>
    </div>

    <div class="card sec">
      <div class="h3">我的教练主页 <span class="caption">（S8 · 学员小程序「教练介绍」展示）</span></div>
      <el-input v-model="p.profile_intro_rich" type="textarea" :rows="3" style="margin-top:14px" placeholder="详细介绍，支持图文" />
      <div class="row" style="margin-top:14px">
        <span class="muted">名片二维码</span><span class="qr">▓░▓</span><el-button size="small">📥 下载</el-button>
        <span class="muted" style="margin-left:24px">状态</span>
        <el-switch v-model="p.profile_published" active-text="已发布" inactive-text="草稿" />
      </div>
    </div>

    <div class="card sec">
      <div class="h3">风险信号阈值 <span class="caption">（C6）</span></div>
      <el-form label-width="140px" label-position="left" inline style="margin-top:14px">
        <el-form-item label="连续未打卡天数"><el-input-number v-model="p.risk_days_threshold" :min="1" :max="30" size="small" /></el-form-item>
      </el-form>
    </div>

    <div class="card sec">
      <div class="row"><span class="muted">推送设置</span>
        <span>主推：订阅消息 + 站内信兜底；高级：企微群机器人（可选）</span>
        <el-button size="small" @click="router.push('/settings/push')">进入 →</el-button></div>
      <div class="row"><span class="muted">订阅套餐</span><span>当前：{{ p.subscription_tier }}</span>
        <el-button size="small">了解 Pro · ¥99/月</el-button></div>
      <div class="row"><span class="muted">手机号</span><span>{{ p.phone_masked }}</span></div>
    </div>

    <div style="display:flex;gap:12px;margin-top:8px">
      <el-button type="primary" @click="save">保存</el-button>
      <el-button @click="logout">退出登录</el-button>
    </div>
  </div>
</template>

<style scoped>
.wrap { max-width: 760px; }
.sec { margin-bottom: 20px; }
.chips { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.chip { font-size: 13px; padding: 3px 10px; border-radius: 6px; background: var(--c-bg-elev-2); }
.x { cursor: pointer; color: var(--c-text-mute); }
.row { display: flex; align-items: center; gap: 16px; padding: 10px 0; }
.row .muted { color: var(--c-text-mute); width: 90px; } .qr { font-family: monospace; }
</style>
