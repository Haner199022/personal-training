// 红线：教练端列表禁止 el-table，只用 el-table-v2（coach-web/tech-stack.md）
export default [
  {
    files: ["src/**/*.{ts,tsx,vue}"],
    rules: {
      "no-restricted-imports": ["error", {
        paths: [{
          name: "element-plus",
          importNames: ["ElTable", "ElTableColumn"],
          message: "禁用 el-table，请用 el-table-v2（虚拟滚动）。见 coach-web/tech-stack.md。",
        }],
      }],
    },
  },
]
