/**
 * 学员列表列定义（el-table-v2）。
 * 约定：所有列定义集中在 composables/columns/，cellRenderer 用 JSX。
 * 见 coach-web/tech-stack.md「为什么第一天就用 el-table-v2」。
 */
import type { Column } from "element-plus"

export interface StudentRow {
  id: number
  alias: string
  status: string
  last_check_in_at: string | null
}

export function useStudentColumns(): Column<StudentRow>[] {
  return [
    { key: "alias", dataKey: "alias", title: "学员", width: 140 },
    { key: "status", dataKey: "status", title: "状态", width: 100 },
    {
      key: "last_check_in_at",
      dataKey: "last_check_in_at",
      title: "最近打卡",
      width: 160,
      cellRenderer: ({ rowData }) => <span>{rowData.last_check_in_at ?? "—"}</span>,
    },
  ]
}
