<script setup lang="ts">
// C-7 打卡详情 + 点评（E6 配图）—— 骨架
import { useRoute } from "vue-router"
const route = useRoute()
</script>
<template><div><h1>打卡详情 #{{ route.params.id }}</h1><el-empty description="点评占位（C-7）" /></div></template>
