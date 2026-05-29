# student-mp

微信小程序原生 + TS + WeUI。spec: vault `student-mp/tech-stack.md` + `wireframes.md`(v5) + `plan/student-mp-setup-2026-05-20.md`。

## 起步
1. 把 `project.config.json` 里的 `appid` 换成真实 AppID（Phase 1 注册后获得）。
2. 用「微信开发者工具」导入本目录。
3. `npm install` 后在开发者工具里「工具 → 构建 npm」。
4. 开发期勾「不校验合法域名」；真机需备案后的 HTTPS 域名。

## 页面 ↔ wireframes
home=S-1 / join=S-2 / training=S-3 / checkin-result=S-4 / body=S-5,S-6 / coach=教练介绍。

## 红线
- 不踩医疗（不写治疗/血压）、不接支付（PLAN 已砍）。
- 订阅消息一次授权一次推送；首页弹窗一次性请求 3 模板（见 tech-stack.md）。
