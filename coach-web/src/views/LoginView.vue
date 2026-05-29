<script setup lang="ts">
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const phone = ref(""), password = ref("")
const auth = useAuthStore(), router = useRouter()
async function onSubmit() {
  await auth.login(phone.value, password.value)
  router.push("/")
}
</script>
<template>
  <div class="login">
    <el-card style="width: 360px">
      <h2>教练登录</h2>
      <el-form @submit.prevent="onSubmit">
        <el-form-item><el-input v-model="phone" placeholder="手机号" /></el-form-item>
        <el-form-item><el-input v-model="password" type="password" placeholder="密码" /></el-form-item>
        <el-button type="primary" native-type="submit" style="width: 100%">登录</el-button>
      </el-form>
    </el-card>
  </div>
</template>
<style scoped>.login { display: grid; place-items: center; height: 70vh; }</style>
