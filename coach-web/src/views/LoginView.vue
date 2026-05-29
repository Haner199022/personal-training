<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"
import { ElMessage } from "element-plus"

const phone = ref("13800138000")
const password = ref("demo1234")
const loading = ref(false)
const auth = useAuthStore(), router = useRouter()

async function onSubmit() {
  loading.value = true
  try {
    await auth.login(phone.value, password.value)
    router.push("/")
  } catch {
    ElMessage.error("登录失败，请检查手机号 / 密码（或后端未启动）")
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login">
    <div class="login-left">
      <div class="micro">PERSONAL TRAINING · COACH</div>
      <h1 class="hero">把 1 个学员的<br />服务质量，<br />复制给 20 个。</h1>
      <p class="lede">教练的远程私教助理 —— 训练、饮食、打卡、体脂，串成一条闭环。</p>
      <div class="quote-attr">— v7 暗色杂志风（重建基线）</div>
    </div>

    <div class="login-right">
      <div class="card login-card">
        <h2 class="h2">教练登录</h2>
        <p class="caption" style="margin:6px 0 24px">输入手机号与密码进入控制台</p>
        <el-form @submit.prevent="onSubmit">
          <el-form-item>
            <el-input v-model="phone" size="large" placeholder="手机号" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="password" type="password" size="large" placeholder="密码" show-password />
          </el-form-item>
          <el-button type="primary" size="large" native-type="submit" :loading="loading" style="width:100%">
            登录
          </el-button>
        </el-form>
        <div class="caption" style="margin-top:16px">演示账号：13800138000 / demo1234</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login { display: grid; grid-template-columns: 1.1fr 0.9fr; height: 100vh; }
.login-left {
  padding: 80px 64px; display: flex; flex-direction: column; justify-content: center;
  background: var(--c-bg) var(--gradient-brand-glow) no-repeat;
  border-right: 1px solid var(--c-border);
}
.hero { font-size: 52px; line-height: 1.08; letter-spacing: -0.03em; margin: 18px 0 24px; font-weight: 800; }
.login-right { display: grid; place-items: center; padding: 40px; }
.login-card { width: 380px; }
</style>
