<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import api from "@/api/client"

const all = ref<any[]>([])
const q = ref(""), cat = ref("all"), onlyFav = ref(false)
const drawer = ref(false), cur = ref<any>(null)
const CAT: Record<string, string> = { strength: "力量", cardio: "有氧", mobility: "灵活" }

async function load() { all.value = (await api.get("/exercises")).data.items }
onMounted(load)

const list = computed(() => all.value.filter(e =>
  (cat.value === "all" || e.category === cat.value) &&
  (!onlyFav.value || e.favorite) &&
  (!q.value || e.name.includes(q.value))))

async function toggleFav(e: any) {
  const r = (await api.post(`/coaches/me/exercises/${e.id}/favorite`)).data
  e.favorite = r.favorite
}
function open(e: any) { cur.value = e; drawer.value = true }
</script>

<template>
  <div>
    <div class="micro">C-5 · EXERCISE LIBRARY</div>
    <div class="head">
      <h1 class="h1" style="margin:8px 0 0">动作库 <span class="count">系统预置 {{ all.length }}</span></h1>
      <div style="display:flex;gap:10px;align-items:center">
        <el-input v-model="q" placeholder="搜索🔍" style="width:160px" size="small" />
        <el-select v-model="cat" size="small" style="width:110px">
          <el-option label="全部分类" value="all" /><el-option label="力量" value="strength" />
          <el-option label="有氧" value="cardio" /><el-option label="灵活" value="mobility" />
        </el-select>
        <el-checkbox v-model="onlyFav">⭐ 仅看收藏</el-checkbox>
        <el-button size="small" disabled>＋ 新建自建动作（MVP+1）</el-button>
      </div>
    </div>

    <div class="grid">
      <div v-for="e in list" :key="e.id" class="card ex" @click="open(e)">
        <div class="ex-top">
          <span class="star" :class="{ on: e.favorite }" @click.stop="toggleFav(e)">{{ e.favorite ? "★" : "☆" }}</span>
          <span class="cat">{{ CAT[e.category] }}</span>
        </div>
        <div class="ex-name">{{ e.name }}</div>
        <div class="ex-muscle">💪 {{ e.target_primary.join("·") }}</div>
        <div class="caption" style="margin-top:6px">▶ 演示素材 · 点开看解剖图</div>
      </div>
    </div>

    <el-drawer v-model="drawer" :title="cur?.name" size="440">
      <div v-if="cur">
        <div class="demo">▶ 演示素材（E4，采购授权）</div>
        <div class="anat">
          <div class="micro" style="margin-bottom:10px">肌肉联动（E1 解剖图高亮）</div>
          <div class="body-svg">
            <div class="muscle primary">主练</div>
            <div class="muscle secondary">辅助</div>
          </div>
          <div style="margin-top:14px"><span class="dot pri" /> 主练：{{ cur.target_primary.join("、") }}</div>
          <div style="margin-top:6px"><span class="dot sec" /> 辅助：{{ cur.target_secondary.join("、") || "—" }}</div>
        </div>
        <div class="divider" style="margin:18px 0" />
        <div class="micro" style="margin-bottom:8px">动作要领</div>
        <p class="body">{{ cur.cues }}</p>
        <div class="caption" style="margin-top:10px">默认单位：kg × reps · MVP 只读，自建留 MVP+1</div>
      </div>
    </el-drawer>
  </div>
</template>

<style scoped>
.head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 24px; flex-wrap: wrap; gap: 12px; }
.count { color: var(--c-brand); font-size: 16px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 16px; }
.ex { cursor: pointer; transition: box-shadow .15s; } .ex:hover { box-shadow: var(--shadow-cta-strong); }
.ex-top { display: flex; justify-content: space-between; align-items: center; }
.star { font-size: 18px; color: var(--c-text-mute); cursor: pointer; } .star.on { color: var(--c-data-yellow); }
.cat { font-size: 12px; color: var(--c-text-mute); }
.ex-name { font-size: 18px; font-weight: 700; margin: 10px 0 6px; }
.ex-muscle { color: var(--c-data-cyan); font-size: 13px; }
.demo { height: 160px; border-radius: 12px; background: var(--c-bg-elev-2); display: grid; place-items: center; color: var(--c-text-mute); margin-bottom: 18px; }
.body-svg { display: flex; gap: 12px; }
.muscle { flex: 1; height: 90px; border-radius: 10px; display: grid; place-items: center; font-size: 13px; }
.muscle.primary { background: var(--c-brand-soft); color: var(--c-brand); box-shadow: inset 0 0 0 1px var(--c-brand); }
.muscle.secondary { background: var(--c-bg-elev-2); color: var(--c-text-mute); }
.dot { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 8px; }
.dot.pri { background: var(--c-brand); } .dot.sec { background: var(--c-text-mute); }
</style>
