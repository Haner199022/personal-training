# 部署指南 — Personal-Training 后端

单机部署：腾讯云轻量 **4C8G** + Docker Compose。
拓扑：`nginx(443/80) → api(8000) → db(postgres16) + redis(7)`，certbot 出 Let's Encrypt 证书，HTTPS 强制（微信小程序要求）。

---

## 1. 准备服务器

```bash
# 安装 Docker（含 compose 插件，官方脚本）
curl -fsSL https://get.docker.com | sh
sudo systemctl enable --now docker

# 验证
docker --version
docker compose version
```

放行安全组/防火墙端口：**80**（ACME 验证）、**443**（HTTPS）。22 按需。

---

## 2. 拉代码 + 配置环境变量

```bash
git clone <你的仓库地址> personal-training
cd personal-training/deploy

cp .env.prod.example .env.prod
vim .env.prod      # 把所有 CHANGE_ME 改成真实值
```

`.env.prod` 必填项（生成命令见文件内注释）：

| 变量 | 说明 |
| --- | --- |
| `PG_PASSWORD` / `DATABASE_URL` 里的密码 | **两处密码必须一致** |
| `JWT_SECRET` | `python -c "import secrets; print(secrets.token_urlsafe(48))"` |
| `WEBHOOK_ENCRYPT_KEY` | `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"` |
| `WX_APP_ID` / `WX_APP_SECRET` | 微信小程序后台获取 |
| `COS_*` | 腾讯云 COS 体脂照存储 |

> `.env.prod` 已被 `.gitignore` 排除，**绝不要提交**。`APP_ENV=prod` 会触发后端 fail-fast：弱密钥或 sqlite 直接拒绝启动。

---

## 3. 首次申请 SSL 证书（certbot）

`nginx/personal-training.conf` 里的 `api.example.com` 先全部替换成你的真实域名，且该域名已解析到本机公网 IP。

证书还没有时 nginx 的 443 段会因找不到证书启动失败，所以**先只起 nginx 的 80**来过 ACME，再补证书：

```bash
# 1) 临时只起 db/redis/api（不依赖证书）
docker compose up -d db redis api

# 2) 用 webroot 模式申证（域名 + 邮箱替换成你的）
docker compose run --rm --service-ports certbot certonly \
  --webroot -w /var/www/certbot \
  -d api.example.com \
  --email you@example.com \
  --agree-tos --no-eff-email

# 3) 证书就位后再起 nginx
docker compose up -d nginx
```

> 若 80 端口此刻无人监听导致 ACME 失败，可改用 standalone 模式：
> `docker compose run --rm -p 80:80 certbot certonly --standalone -d api.example.com --email you@example.com --agree-tos --no-eff-email`，成功后再 `docker compose up -d`。

证书续期（建议加 cron，每月跑一次）：

```bash
docker compose run --rm certbot renew
docker compose exec nginx nginx -s reload
```

---

## 4. 启动全部服务

```bash
docker compose up -d
docker compose ps          # 各服务应为 healthy / running
```

初始化数据库表结构（首次部署执行一次，之后每次有迁移时执行）：

```bash
docker compose exec api alembic upgrade head
```

健康检查：

```bash
curl -fsS https://api.example.com/api/v1/health
```

---

## 5. 常用运维命令

| 操作 | 命令 |
| --- | --- |
| 查看日志 | `docker compose logs -f api` |
| 重建并重启 api（改了代码后） | `docker compose up -d --build api` |
| 重载 nginx 配置 | `docker compose exec nginx nginx -s reload` |
| 停止全部 | `docker compose down`（加 `-v` 会删数据卷，谨慎） |
| 进数据库 | `docker compose exec db psql -U app_user -d personal_training` |

---

## 6. 域名白名单提示（微信小程序）

部署完成后，到**微信小程序后台 → 开发 → 开发设置 → 服务器域名**，把
`https://api.example.com` 加入 **request 合法域名**（如有上传走后端则同时加 uploadFile）。
小程序只接受 **HTTPS** 且**已 ICP 备案**的域名，自签证书无效——本方案的 Let's Encrypt 证书满足要求。
