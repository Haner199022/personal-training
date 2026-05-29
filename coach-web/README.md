# coach-web

Vue 3.5 + Vite 5 + TS + Element Plus + Pinia。spec: vault `coach-web/tech-stack.md` + `wireframes.md`(v5)。

```bash
npm install      # 或 pnpm install
npm run dev      # http://localhost:5173, /api 代理到 :8000
```

## 红线
- 列表**只用 `el-table-v2`**，禁 `el-table`（eslint `no-restricted-imports` 已锁）。
- 列定义集中在 `src/composables/columns/`，`cellRenderer` 用 JSX。
- 页面编号对齐 wireframes C-0…C-9。
