# backend

FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL 16 + Redis。spec: vault `backend/tech-stack.md`。

## 起步
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # 填 DATABASE_URL / 微信 / WEBHOOK_ENCRYPT_KEY
uvicorn app.main:app --reload
# → http://127.0.0.1:8000/api/v1/health  ·  /docs
```

## 迁移
```bash
docker run -d --name pt-pg -e POSTGRES_PASSWORD=pwd -e POSTGRES_DB=personal_training -p 5432:5432 postgres:16
alembic revision --autogenerate -m "init core tables"
alembic upgrade head
```

## 结构
```
app/
├── main.py              # FastAPI 入口, /api/v1 前缀
├── core/                # config(pydantic-settings) + security(JWT/bcrypt)
├── db/                  # Base + async engine/session
├── models/              # coach / student / coach_student / invite_code (核心4表)
├── api/v1/              # health / auth (其余路由按 wireframes 补)
├── services/push/       # 三层推送骨架 (dispatcher + tier1/2/3 + 限流队列)
└── workers/push.py      # 推送消费 worker
```

## 红线
- API 全部 `/api/v1/` 前缀。
- 业务查询带 `coach_id`（Phase 2 上 RLS 改造量=0）。
- 推送一律 enqueue，群机器人 20 msg/min/桶；webhook fernet 加密存。
- 核心 4 表只是骨架，完整 16 表见 vault `_shared/data-model.md` v5，逐步 migration。
