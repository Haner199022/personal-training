/**
 * 学员列表列定义（el-table-v2）。
 * 约定：列定义集中在 composables/columns/，cellRenderer 用 JSX（文件必须 .tsx）。
 * 见 coach-web/tech-stack.md「为什么第一天就用 el-table-v2」。
 */
import type { Column } from "element-plus"

export interface StudentRow {
  id: number
  alias: string
  status: string
  last_check_in_at: string | null
}

const STATUS_TONE: Record<string, string> = {
  active: "var(--c-data-green)",
  trial: "var(--c-data-cyan)",
  paused: "var(--c-data-yellow)",
  pending_renewal: "var(--c-data-yellow)",
  expired: "var(--c-text-mute)",
  churned: "var(--c-data-red)",
}
const STATUS_LABEL: Record<string, string> = {
  active: "在训", trial: "体验", paused: "暂停",
  pending_renewal: "待续费", expired: "已到期", churned: "已流失",
}

export function useStudentColumns(): Column<StudentRow>[] {
  return [
    {
      key: "alias", dataKey: "alias", title: "学员", width: 220,
      cellRenderer: ({ rowData }) => (
        <span style="font-weight:600;color:var(--c-text-base)">{rowData.alias}</span>
      ),
    },
    {
      key: "status", dataKey: "status", title: "状态", width: 160,
      cellRenderer: ({ rowData }) => {
        const tone = STATUS_TONE[rowData.status] ?? "var(--c-text-mute)"
        return (
          <span style={`display:inline-flex;align-items:center;gap:6px;color:${tone};font-size:13px`}>
            <span style={`width:7px;height:7px;border-radius:50%;background:${tone};box-shadow:0 0 8px ${tone}`} />
            {STATUS_LABEL[rowData.status] ?? rowData.status}
          </span>
        )
      },
    },
    {
      key: "last_check_in_at", dataKey: "last_check_in_at", title: "最近打卡", width: 200,
      cellRenderer: ({ rowData }) => (
        <span style="color:var(--c-text-mute)">{rowData.last_check_in_at ?? "—"}</span>
      ),
    },
  ]
}
