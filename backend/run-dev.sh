#!/usr/bin/env bash
# Personal-Training 后端 · 本地 dev 启停脚本
# 端口 8001（8000 被 AI Team OS API 占用，勿改）。dev 用 SQLite 种子库 dev.db。
# 用法：  ./run-dev.sh        启动（持久化，关掉终端也不停）
#        ./run-dev.sh stop   停止
#        ./run-dev.sh status  状态
set -euo pipefail
cd "$(dirname "$0")"
PORT=8001
LOG=/tmp/pt_backend.log
PIDFILE=/tmp/pt_backend.pid

port_pids() { lsof -ti:"$PORT" 2>/dev/null || true; }

case "${1:-start}" in
  stop)
    pids=$(port_pids)
    [ -n "$pids" ] && { echo "$pids" | xargs kill -9 2>/dev/null || true; echo "已停止 (pids: $pids)"; } || echo "未在运行"
    rm -f "$PIDFILE"
    ;;
  status)
    pids=$(port_pids)
    if [ -n "$pids" ]; then
      code=$(curl -s -o /dev/null -w '%{http_code}' --noproxy '*' --max-time 4 "http://127.0.0.1:$PORT/api/v1/health" 2>/dev/null || echo 000)
      echo "运行中 (pid $pids) · health $code · http://127.0.0.1:$PORT/api/v1"
    else
      echo "未运行"
    fi
    ;;
  start|*)
    if [ -n "$(port_pids)" ]; then echo "已在运行：$(port_pids)（先 ./run-dev.sh stop 可重启）"; exit 0; fi
    [ -d .venv ] || { echo "缺 .venv，先：python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt"; exit 1; }
    # 持久化：nohup + disown，脱离当前终端会话
    nohup .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port "$PORT" >"$LOG" 2>&1 </dev/null &
    echo $! >"$PIDFILE"; disown || true
    for _ in $(seq 1 15); do
      sleep 1
      [ "$(curl -s -o /dev/null -w '%{http_code}' --noproxy '*' --max-time 4 "http://127.0.0.1:$PORT/api/v1/health" 2>/dev/null)" = 200 ] && { echo "✓ 已启动 · http://127.0.0.1:$PORT/api/v1/health · 日志 $LOG"; exit 0; }
    done
    echo "✗ 启动后 15s 内未就绪，看日志：tail -30 $LOG"; tail -8 "$LOG" 2>/dev/null; exit 1
    ;;
esac
