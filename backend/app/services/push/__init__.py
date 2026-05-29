"""三层推送服务（ADR-0010）。
Tier1 企微群机器人(主) / Tier2 一次性订阅消息 / Tier3 站内信(兜底)。
红线：HTTP handler 永不直接调 webhook —— 一律 enqueue。"""
