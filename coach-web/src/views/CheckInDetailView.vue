<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "@/api/client"
import { ElMessage } from "element-plus"

const route = useRoute(), router = useRouter()
const cid = Number(route.params.id)
const d = ref<any>(null)
const templates = ref<string[]>([])
const comment = ref("")

async function load() {
  d.value = (await api.get(`/coaches/me/check-ins/${cid}`)).data
  templates.value = (await api.get(`/coaches/me/comment-templates`)).data.items
}
onMounted(load)

function insert(t: string) { comment.value += (comment.value ? " " : "") + t }
async function send() {
  if (!comment.value.trim()) return ElMessage.warning("请输入点评")
  await api.post(`/coaches/me/check-ins/${cid}/comment`, { text: comment.value })
  ElMessage.success("点评已发送")
  comment.value = ""
  await load()
}
</script>

<template>
  <div v-if="d">
    <div class="micro"><span class="back" @click="router.push('/')">← 返回</span> · C-7 · CHECK-IN</div>
    <h1 class="h1" style="margin:8px 0 6px">{{ d.student_name }} · {{ d.date }} · {{ d.plan_title }}</h1>
    <p class="lede" style="margin-bottom:24px">学员感受 {{ d.feeling }}/5 · 主观吃力 RPE {{ d.rpe }}/10</p>

    <div class="card sec">
      <div class="h3" style="margin-bottom:6px">学员留言</div>
      <p class="body">「{{ d.note }}」</p>
    </div>

    <div class="card sec">
      <div class="h3" style="margin-bottom:12px">完成情况（教练规定 vs 学员实际）</div>
      <div v-for="(s, i) in d.sets_detail" :key="i" class="exblock">
        <div class="exname">{{ s.exercise }} <span class="caption">（{{ s.prescribed }}）</span></div>
        <div class="sets">
          <span v-for="(a, j) in s.actual" :key="j" class="set" :class="{ warn: String(a).includes('⚠') }">{{ a }}</span>
        </div>
      </div>
    </div>

    <div class="card sec">
      <div class="h3" style="margin-bottom:12px">教练点评</div>
      <div class="tpls">
        <span class="micro" style="align-self:center">常用语：</span>
        <span v-for="t in templates" :key="t" class="tpl" @click="insert(t)">{{ t }}</span>
      </div>
      <el-input v-model="comment" type="textarea" :rows="3" placeholder="给学员的点评…" style="margin:12px 0" />
      <div class="photos">配图（E6）：<span class="ph">图1</span><span class="ph">➕</span>
        <span class="caption" style="margin-left:auto">🎙 语音点评 MVP+1</span></div>
      <el-button type="primary" style="margin-top:14px" @click="send">发送点评</el-button>

      <div v-if="d.comments.length" class="divider" style="margin:18px 0" />
      <div v-for="(c, i) in d.comments" :key="i" class="prev">💬 {{ c.text }}</div>
    </div>
  </div>
</template>

<style scoped>
.back { cursor: pointer; color: var(--c-brand); } .sec { margin-bottom: 18px; }
.exblock { padding: 10px 0; border-bottom: 1px solid var(--c-border); }
.exname { font-weight: 600; margin-bottom: 8px; }
.sets { display: flex; gap: 10px; flex-wrap: wrap; }
.set { font-size: 13px; padding: 4px 10px; border-radius: 6px; background: var(--c-bg-elev-2); }
.set.warn { color: var(--c-data-yellow); }
.tpls { display: flex; gap: 8px; flex-wrap: wrap; }
.tpl { font-size: 13px; padding: 4px 12px; border-radius: 16px; background: var(--c-brand-soft); color: var(--c-brand); cursor: pointer; }
.photos { display: flex; align-items: center; gap: 10px; }
.ph { width: 48px; height: 48px; border-radius: 8px; background: var(--c-bg-elev-2); display: grid; place-items: center; font-size: 12px; color: var(--c-text-mute); }
.prev { padding: 8px 0; color: var(--c-text-base); }
</style>
