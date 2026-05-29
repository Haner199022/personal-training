# personal-training (code) — Claude Code 规则

## 这是代码仓库（与 vault 相反）

- ✅ 这里**写代码、跑测试、建 CI**。superpowers 等开发流程在这里正常适用。
- ❌ **不要把 spec / ADR / PLAN / research 写到这里** —— 那些活在 Obsidian vault。
- 读 spec 去 vault：`…/Documents/Claude Code/Projects/Personal-Training/`

## 跨机器铁律（这次踩过坑）

- 本仓库**只在本机本地**，靠 git remote 跨机器同步。**第一次有产出就 push 到私有远程**。
- 远程地址记到 vault `_shared/deployment.md`，换机器先 `git clone`。
- iCloud 不同步代码（ADR-0004/0009）—— 别指望 vault 帮你带代码。

## 技术栈红线（来自 vault，落地时复核）

- 后端：FastAPI + SQLAlchemy 2.0（async）+ PG 16；API 一律 `/api/v1/` 前缀。
- 多租户：所有业务查询带 `WHERE coach_id = ?`，哪怕 MVP 单教练（养习惯，Phase 2 上 RLS 改造量=0）。
- 推送：HTTP handler **永不**直接调 webhook —— 必须 enqueue（群机器人 20 msg/min/桶，按 coach_id 分桶）。
- webhook URL：fernet 加密存 BYTEA，key 走 `WEBHOOK_ENCRYPT_KEY` env，不进 DB/git。
- 教练端列表：**禁止 `el-table`，只用 `el-table-v2`**（eslint 锁）。
- 体脂照：腾讯云 COS 上海/广州，禁跨境；签名 URL；PIPL 单独同意。

## 语言

- 注释/文档：中文 OK；标识符 / API 字段 / 表名：英文 snake_case。
