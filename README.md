# personal-training (code)

> 自由私人教练「学员服务 + SaaS 订阅」平台 —— **代码仓库**。
> 设计文档 / spec / ADR / PLAN 全部在 Obsidian vault 内：
> `…/Documents/Claude Code/Projects/Personal-Training/`
> 本仓库只放可运行代码，**vault 不放代码、代码仓库不放 spec**（ADR-0003/0004/0009）。

## 子项目

| 目录 | 角色 | 技术栈 | spec |
|---|---|---|---|
| `backend/`    | 服务端 API | Python 3.12 + FastAPI + SQLAlchemy 2.0 + PostgreSQL 16 + Redis | vault `backend/tech-stack.md` |
| `coach-web/`  | 教练端 Web 后台 | Vue 3.5 + Vite 5 + TS + Element Plus（列表用 `el-table-v2`） | vault `coach-web/tech-stack.md` |
| `student-mp/` | 学员端微信小程序 | 原生 + TS + WeUI | vault `student-mp/tech-stack.md` |

## 现状

🟢 **scaffold（骨架）** —— 2026-05-29 按 vault spec 从零重建（Plan B）。
原机器的 v7 暗色杂志风实现 + 13 个未提交文件未同步到本机、无远程可拉，已无法恢复；本骨架是新基线。

## 起步

```bash
# backend
cd backend && python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # 填 DB / 微信 / 加密 key
uvicorn app.main:app --reload # http://127.0.0.1:8000/api/v1/health

# coach-web
cd coach-web && npm install && npm run dev

# student-mp
# 用「微信开发者工具」导入 student-mp/ 目录（需 AppID）
```

详见各子目录 README / vault `plan/student-mp-setup-2026-05-20.md`。
