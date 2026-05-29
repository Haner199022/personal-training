<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { ElMessage } from "element-plus"

const phone = ref(""), name = ref(""), pw = ref(""), pw2 = ref("")
const router = useRouter()
async function onSubmit() {
  if (pw.value !== pw2.value) return ElMessage.error("两次密码不一致")
  // 注册端点为骨架；这里给出占位提示（后端 register 待接）
  ElMessage.info("注册接口为骨架（后端 /auth/coach/register 待接）——演示请用 13800138000 / demo1234 登录")
  router.push("/login")
}
</script>
<template>
  <div class="wrap">
    <div class="card" style="width:380px">
      <h2 class="h2">注册教练账号</h2>
      <p class="caption" style="margin:6px 0 24px">注册即创建账号，套餐默认 free</p>
      <el-form @submit.prevent="onSubmit">
        <el-form-item><el-input v-model="phone" size="large" placeholder="手机号" /></el-form-item>
        <el-form-item><el-input v-model="name" size="large" placeholder="昵称" /></el-form-item>
        <el-form-item><el-input v-model="pw" type="password" size="large" placeholder="密码" show-password /></el-form-item>
        <el-form-item><el-input v-model="pw2" type="password" size="large" placeholder="确认密码" show-password /></el-form-item>
        <el-button type="primary" size="large" native-type="submit" style="width:100%">注册</el-button>
      </el-form>
      <div class="caption" style="margin-top:16px">已有账号？<RouterLink to="/login" style="color:var(--c-brand)">去登录 →</RouterLink></div>
    </div>
  </div>
</template>
<style scoped>.wrap { display: grid; place-items: center; height: 100vh; background: var(--c-bg) var(--gradient-brand-glow) no-repeat; }</style>
