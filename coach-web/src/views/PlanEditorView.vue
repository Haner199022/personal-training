<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "@/api/client"
import { ElMessage } from "element-plus"

const route = useRoute(), router = useRouter()
const sid = Number(route.params.id)
const plans = ref<any[]>([])
const templates = ref<any[]>([])
const detail = ref<any>(null)
const student = ref<any>(null)
const tplOpen = ref(false)

async function load() {
  student.value = (await api.get(`/coaches/me/students/${sid}`)).data
  plans.value = (await api.get(`/coaches/me/students/${sid}/plans`)).data.items
  templates.value = (await api.get(`/coaches/me/plan-templates`)).data.items
  detail.value = plans.value[0] ?? null
}
onMounted(load)

function isContra(name: string): boolean {
  // 演示：禁忌动作 ID 列表存在则提示（真实需 name→id 映射）
  return (student.value?.contraindicated_exercise_ids?.length ?? 0) > 0 && name.includes("深蹲")
}
function publish() { ElMessage.success("已发布给学员（未打卡课次覆盖更新）") }
function saveDraft() { ElMessage.success("已保存为草稿") }
</script>

<template>
  <div v-if="student">
    <div class="micro"><span class="back" @click="router.push(`/students/${sid}`)">← {{ student.alias }}</span> · C-4 训练计划</div>
    <div class="head">
      <h1 class="h1" style="margin:8px 0 0">训练计划编辑</h1>
      <div style="display:flex;gap:10px">
        <el-button @click="tplOpen = true">📋 我的训练模板</el-button>
        <el-button>⧉ 从已有计划复制</el-button>
      </div>
    </div>

    <div v-if="detail" class="card">
      <el-form inline label-position="top">
        <el-form-item label="计划名"><el-input v-model="detail.title" style="width:240px" /></el-form-item>
        <el-form-item label="目标"><el-input v-model="detail.goal" style="width:240px" /></el-form-item>
        <el-form-item label="状态"><span class="badge">{{ detail.status }}</span></el-form-item>
      </el-form>

      <div class="h3" style="margin:8px 0 12px">课次列表 <el-button size="small" style="float:right">＋ 添加课次</el-button></div>
      <div v-for="(sess, si) in detail.detail.sessions" :key="si" class="session">
        <div class="sess-head">{{ sess.day }} · {{ sess.title }}</div>
        <div v-for="(ex, ei) in sess.exercises" :key="ei" class="exrow">
          <div class="exname">· {{ ex.name }}
            <span v-if="isContra(ex.name)" class="contra">⚠ 该学员禁忌</span>
          </div>
          <div class="exmeta">{{ ex.sets }}×{{ ex.reps }} @{{ ex.weight }} 　💪 {{ ex.primary }} 　
            <span class="link">▶演示</span> · <span class="link">上次 62.5kg×9 [带入⤵]</span></div>
        </div>
      </div>

      <div style="margin-top:18px;display:flex;gap:12px">
        <el-button @click="saveDraft">保存为草稿</el-button>
        <el-button type="primary" @click="publish">发布给学员</el-button>
        <el-button>💾 另存为我的模板</el-button>
      </div>
    </div>
    <el-empty v-else description="暂无计划，点新建" />

    <el-dialog v-model="tplOpen" title="📋 我的训练模板" width="480">
      <div v-for="t in templates" :key="t.id" class="tpl">
        <div><div class="t">{{ t.title }}</div><div class="caption">{{ t.goal }}</div></div>
        <el-button size="small" type="primary">复制新建</el-button>
      </div>
      <el-empty v-if="!templates.length" description="还没有模板" />
    </el-dialog>
  </div>
</template>

<style scoped>
.back { cursor: pointer; color: var(--c-brand); }
.head { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 24px; }
.session { background: var(--c-bg-elev-2); border-radius: 12px; padding: 16px; margin-bottom: 12px; }
.sess-head { font-weight: 700; margin-bottom: 12px; }
.exrow { padding: 8px 0; border-top: 1px solid var(--c-border); }
.exname { font-weight: 600; } .contra { color: var(--c-data-red); font-size: 12px; margin-left: 10px; }
.exmeta { color: var(--c-text-mute); font-size: 13px; margin-top: 4px; } .link { color: var(--c-data-cyan); cursor: pointer; }
.badge { font-size: 12px; padding: 3px 10px; border-radius: 6px; background: var(--c-brand-soft); color: var(--c-brand); }
.tpl { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid var(--c-border); }
.t { font-weight: 600; }
</style>
