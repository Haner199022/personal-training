/** 学员列表列定义（el-table-v2）。列集中此处，cellRenderer 用 JSX（文件须 .tsx）。 */
import type { Column } from "element-plus"

export interface StudentRow {
  id: number
  alias: string
  status: string
  source: string
  tags: { name: string; color: string }[]
  next_due_date: string | null
  remaining_sessions: number | null
  last_check_in_at: string | null
}

const STATUS_TONE: Record<string, string> = {
  active: "var(--c-data-green)", trial: "var(--c-data-cyan)", paused: "var(--c-data-yellow)",
  pending_renewal: "var(--c-data-yellow)", expired: "var(--c-text-mute)", churned: "var(--c-data-red)",
}
const STATUS_LABEL: Record<string, string> = {
  active: "在训", trial: "体验", paused: "暂停", pending_renewal: "待续费", expired: "已到期", churned: "已流失",
}
const SOURCE_LABEL: Record<string, string> = {
  private: "私单", gym_assigned: "场馆派", referral: "转介", trial_class: "试课", other: "其他",
}
const TAG_TONE: Record<string, string> = {
  cyan: "var(--c-data-cyan)", green: "var(--c-data-green)", yellow: "var(--c-data-yellow)",
}

export function useStudentColumns(onOpen: (id: number) => void): Column<StudentRow>[] {
  return [
    { key: "alias", dataKey: "alias", title: "学员", width: 130,
      cellRenderer: ({ rowData }) => <span style="font-weight:600">{rowData.alias}</span> },
    { key: "status", dataKey: "status", title: "状态", width: 110,
      cellRenderer: ({ rowData }) => {
        const t = STATUS_TONE[rowData.status] ?? "var(--c-text-mute)"
        return <span style={`display:inline-flex;align-items:center;gap:6px;color:${t};font-size:13px`}>
          <span style={`width:7px;height:7px;border-radius:50%;background:${t};box-shadow:0 0 8px ${t}`} />
          {STATUS_LABEL[rowData.status] ?? rowData.status}</span>
      } },
    { key: "source", dataKey: "source", title: "来源", width: 90,
      cellRenderer: ({ rowData }) => <span style="color:var(--c-text-mute);font-size:13px">{SOURCE_LABEL[rowData.source] ?? rowData.source}</span> },
    { key: "tags", dataKey: "tags", title: "标签", width: 130,
      cellRenderer: ({ rowData }) => <span style="display:flex;gap:6px">{(rowData.tags || []).map((tg: {name:string;color:string}) =>
        <span style={`font-size:12px;padding:2px 8px;border-radius:6px;color:${TAG_TONE[tg.color]||'var(--c-text-mute)'};background:var(--c-bg-elev-2)`}>{tg.name}</span>)}</span> },
    { key: "next_due_date", dataKey: "next_due_date", title: "包月到期", width: 120,
      cellRenderer: ({ rowData }) => <span style="color:var(--c-text-mute);font-size:13px">{rowData.next_due_date ?? "—"}</span> },
    { key: "remaining_sessions", dataKey: "remaining_sessions", title: "剩余课时", width: 100,
      cellRenderer: ({ rowData }) => <span style="font-size:13px">{rowData.remaining_sessions != null ? rowData.remaining_sessions + " 节" : "—"}</span> },
    { key: "last_check_in_at", dataKey: "last_check_in_at", title: "上次打卡", width: 120,
      cellRenderer: ({ rowData }) => <span style="color:var(--c-text-mute);font-size:13px">{rowData.last_check_in_at ?? "—"}</span> },
    { key: "op", title: "操作", width: 90,
      cellRenderer: ({ rowData }) => <span style="color:var(--c-brand);cursor:pointer;font-size:13px" onClick={() => onOpen(rowData.id)}>档案 →</span> },
  ]
}
