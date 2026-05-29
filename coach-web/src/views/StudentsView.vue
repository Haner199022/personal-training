<script setup lang="ts">
// C-2 学员列表 —— 用 el-table-v2（禁 el-table）
import { ref } from "vue"
import { useStudentColumns, type StudentRow } from "@/composables/columns/useStudentColumns"

const columns = useStudentColumns()
const data = ref<StudentRow[]>([])  // TODO: GET /coaches/me/students
</script>
<template>
  <div>
    <h1>学员</h1>
    <div style="height: 70vh">
      <el-auto-resizer>
        <template #default="{ height, width }">
          <el-table-v2 :columns="columns" :data="data" :width="width" :height="height" />
        </template>
      </el-auto-resizer>
    </div>
  </div>
</template>
