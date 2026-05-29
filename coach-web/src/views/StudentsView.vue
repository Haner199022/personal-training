<script setup lang="ts">
import { ref, onMounted } from "vue"
import api from "@/api/client"
import { useStudentColumns, type StudentRow } from "@/composables/columns/useStudentColumns"
import { ElMessage } from "element-plus"

const columns = useStudentColumns()
const data = ref<StudentRow[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await api.get<{ items: StudentRow[] }>("/coaches/me/students")
    data.value = res.data.items
  } catch {
    ElMessage.warning("拉取学员失败（后端未启动？）")
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="students">
    <div class="head">
      <div>
        <div class="micro">C-2 · STUDENTS</div>
        <h1 class="h1" style="margin:8px 0 0">学员 <span class="count">{{ data.length }}</span></h1>
      </div>
      <el-button type="primary">＋ 生成邀请码</el-button>
    </div>

    <div class="card table-wrap" v-loading="loading">
      <el-auto-resizer>
        <template #default="{ height, width }">
          <el-table-v2 :columns="columns" :data="data" :width="width" :height="height" :row-height="56" />
        </template>
      </el-auto-resizer>
    </div>
  </div>
</template>

<style scoped>
.head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 28px; }
.count { color: var(--c-brand); font-size: 24px; vertical-align: middle; }
.table-wrap { height: 64vh; padding: 12px; }
</style>
