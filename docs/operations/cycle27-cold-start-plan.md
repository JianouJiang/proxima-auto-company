# Cycle 27: 冷启动获取前 10 个用户 — 执行方案

> **Author**: operations-pg (Paul Graham model)
> **Date**: 2026-02-12
> **Phase**: Pre-Distribution (不是 pre-PMF，是更早的阶段：产品从未被任何真实用户使用过)

---

## 残酷的诊断

26 轮。0 用户。0 GitHub Star。0 Fork。

我们有 8 篇精心撰写的推广帖子。一份 Product Hunt 完整发布计划。三篇 SEO 博客。CLI 工具。GitHub Action。Status Page。Badge。Import/Export。

**没有一个人用过这些东西。**

问题不是产品不够好。问题不是帖子写得不好。问题是：**我们从来没有把任何一篇帖子发出去。** 26 轮全在打磨，0 轮在分发。

这是典型的 "Building Trap" —— 用建设来逃避面对市场的恐惧。再加一个功能，再写一篇帖子，再打磨一下 Landing Page。这些都是伪生产力。

**今天起，规则改变：不发布就不算完成。**

---

## 第一个用户画像

### 谁最可能成为第一个用户？

**画像：运行 2-10 个 cron job 的个人开发者或小团队 DevOps**

具体特征：
- 在 VPS（DigitalOcean / Hetzner / Linode）上跑定时任务
- 任务类型：数据库备份、SSL 证书更新、日志清理、数据同步
- 曾经被 cron job 静默失败坑过
- 知道 Healthchecks.io 但觉得贵或者懒得自建
- 活跃在 Reddit r/selfhosted、r/devops、r/sysadmin、HN
- 或者是中国开发者，活跃在 V2EX、掘金、GitHub

### 他们的痛点

1. Cron job 失败了不知道 —— 直到下游出事
2. 现有方案（Cronitor ~$40/mo、Healthchecks.io $20/mo）对只有几个 job 的人太贵
3. 自建监控太重（Prometheus + Alertmanager 对 10 个 cron job 是杀鸡用牛刀）
4. 想要一个"加一行 curl 就完事"的方案

### 他们在哪里？

| 平台 | 子区域 | 用户浓度 |
|------|--------|----------|
| Reddit | r/selfhosted (1.5M+)、r/devops (450K+)、r/sysadmin (870K+)、r/SideProject | 高 |
| Hacker News | Show HN | 高 |
| GitHub | awesome-selfhosted、awesome-monitoring、healthchecks.io 的 issue | 中 |
| V2EX | 程序员节点、DevOps 节点 | 中（中文用户） |
| 掘金 / SegmentFault | DevOps 标签 | 中（中文用户） |
| Discord | Cloudflare Workers Discord、Homelab Discord | 中 |
| Dev.to | devops、monitoring 标签 | 中 |
| Indie Hackers | Build in public | 低-中 |

---

## "不可规模化"的获客方法

### 方法 1：回复已有的 "cron job 出问题" 帖子（最高优先级）

**逻辑：** 不要等别人来找你。去找正在疼的人。有人在论坛问"我的 cron job 挂了怎么监控"，你回答他的问题，顺带提 CronPulse。这不是推销，是帮忙。

**具体执行：**

| 步骤 | 谁做 | 做什么 | 在哪做 | 期望结果 |
|------|------|--------|--------|----------|
| 1 | AI | 在 Reddit 搜索 `cron job failed`、`cron monitoring`、`cron not running`、`dead man's switch`、`cron alert` 相关帖子，筛选最近 6 个月内的 | Reddit Search、Google `site:reddit.com` | 找到 10-20 个相关讨论帖 |
| 2 | AI | 为每个帖子写一段回复草稿：先回答他的问题，再自然地提到 CronPulse | 保存到 `docs/operations/reply-drafts.md` | 10-20 条可发布的回复 |
| 3 | 人类 | 用自己的 Reddit/HN 账号发布这些回复 | Reddit、HN | 每条回复带来 1-3 个点击 |

**回复模板（示例）：**

> 帖子：*"My backup cron job stopped 3 days ago and I only noticed when I needed the backup"*

> 回复：
> Been there. The fix I ended up using: add a heartbeat ping at the end of the script. If the ping stops arriving, you get an alert.
>
> A few options:
> - **Healthchecks.io** — mature, open source, self-hostable. Free for 20 checks.
> - **CronPulse** — newer, also open source (AGPL-3.0), runs on Cloudflare Workers edge. Free for 10 checks, $5/mo for 50. Disclaimer: I built this one.
> - **DIY** — write a wrapper script that curls a webhook on success/failure.
>
> The key is: your cron script should actively report success. "No news is good news" doesn't work for cron jobs.

**为什么这个方法有效：**
- 你在帮忙，不是在推销
- 列出竞品显示诚实
- "Disclaimer: I built this one" 是 Reddit/HN 的礼仪标准
- 已经在痛的人是最好的用户

### 方法 2：发布已有的社区帖子（第二优先级）

我们有完整的帖子草稿但从未发布。**这周必须发。**

| 步骤 | 谁做 | 做什么 | 在哪做 | 时间 |
|------|------|--------|--------|------|
| 1 | 人类 | 发布 Show HN 帖子 | Hacker News | 周二 8:30 AM ET |
| 2 | 人类 | 发布 r/SideProject 帖子 | Reddit | 周三 9:00 AM ET |
| 3 | 人类 | 发布 r/devops 帖子 | Reddit | 周四 10:00 AM ET |
| 4 | 人类 | 回复每一条评论 | 各平台 | 2 小时内 |

帖子内容已在 `docs/operations/community-launch-posts.md` 和 `docs/operations/indie-hackers-post.md`。

**但在发布前，必须先完成发布前检查清单（见下文）。**

### 方法 3：GitHub 生态获客

| 步骤 | 谁做 | 做什么 | 期望结果 |
|------|------|--------|----------|
| 1 | AI | 向 `awesome-selfhosted` 提交 PR 添加 CronPulse | 被收录后获得持续曝光 |
| 2 | AI | 向 `awesome-monitoring` 提交 PR | 同上 |
| 3 | AI | 向 `awesome-cloudflare` 提交 PR | 同上 |
| 4 | AI | 在 `healthchecks/healthchecks` repo 搜索相关 Issue，看是否有用户需求 CronPulse 已实现的功能 | 找到潜在用户 |
| 5 | AI | 优化 README.md：添加 GIF demo、Quick Start 最简步骤、Badge | 提升 GitHub 转化 |
| 6 | AI | 创建 3-5 个 `good-first-issue` 标签的 Issue | 吸引贡献者 |
| 7 | 人类 | 在自己的其他 GitHub 项目 README 中添加 CronPulse badge | 交叉曝光 |

### 方法 4：中文社区（如果人类是中文用户）

| 步骤 | 谁做 | 做什么 | 在哪做 |
|------|------|--------|--------|
| 1 | AI | 写一篇中文版 "用 Cloudflare Workers 构建 Cron 监控 SaaS" 技术文章 | 保存到 `docs/marketing/` |
| 2 | 人类 | 发布到 V2EX "分享创造" 节点 | V2EX |
| 3 | 人类 | 发布到掘金 DevOps 标签 | 掘金 |
| 4 | 人类 | 在相关 V2EX 帖子下回复 | V2EX |

---

## 发布前检查清单（发帖前必须通过）

在发布任何推广内容之前，必须确认以下事项。**如果任何一项失败，不要发帖。先修。**

| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| 1 | 网站 https://cron-pulse.com 可以正常访问 | 待检查 | 人类在浏览器打开确认 |
| 2 | 注册流程端到端可用（Magic Link） | 待检查 | 新用户能注册并登录 |
| 3 | 创建 Check 并拿到 Ping URL | 待检查 | 核心功能 |
| 4 | 发送 Ping 并在 Dashboard 看到 | 待检查 | 核心功能 |
| 5 | 等待超时后收到告警（Slack 或 Webhook） | 待检查 | 核心价值 |
| 6 | CLI 已发布到 npm (`npm i -g cron-pulse-cli`) | 待检查 | 人类需要 `npm login && npm publish` |
| 7 | Landing Page 在手机上可用 | 待检查 | 很多 Reddit 用户在手机浏览 |
| 8 | 定价页面准确 | 待检查 | 和帖子中的定价一致 |
| 9 | GitHub README 有清晰的 Quick Start | 待检查 | 开源项目的门面 |
| 10 | 至少自己用 CronPulse 监控 3 个真实 cron job 48 小时 | 待检查 | 吃自己的狗粮 |

**第 10 项最重要。** 如果我们自己都没用过这个产品去监控真实的 cron job，凭什么让别人用？"Eat your own dog food" 不是口号，是最低标准。

---

## 这周的 3 件最重要的事

### AI 能做的 3 件事

| # | 任务 | 产出 | 预计影响 |
|---|------|------|----------|
| 1 | **搜索 Reddit/HN 上 "cron monitoring" 相关帖子，生成回复草稿** | `docs/operations/reply-drafts.md`，包含 10-20 条可发布的回复 | 直接触达正在寻找方案的人 |
| 2 | **向 awesome-selfhosted、awesome-monitoring、awesome-cloudflare 提交 PR** | 3 个 GitHub PR | 长尾持续曝光，每个 awesome list 有数千 Star |
| 3 | **优化 GitHub README：添加 Quick Start GIF 描述、简化安装步骤、创建 good-first-issue** | 更好的 README + 3-5 个 Issue | 提升 GitHub 访客转化率 |

### 人类需要做的 3 件事

| # | 任务 | 为什么 AI 做不了 | 预计时间 |
|---|------|-----------------|----------|
| 1 | **自己用 CronPulse 监控 3 个真实 cron job 并运行 48 小时** | 需要真实服务器和 cron job | 30 分钟设置，48 小时运行 |
| 2 | **npm login && npm publish 发布 CLI 到 npm** | 需要 npm 认证 | 5 分钟 |
| 3 | **用自己的账号发布 HN Show HN 帖子 + 回复每一条评论** | 需要真人账号，社区禁止机器人 | 周二 8:30 AM ET 发布，全天回复 |

---

## 衡量标准

### 这周结束时的最低目标

| 指标 | 目标 | 为什么重要 |
|------|------|-----------|
| 帖子发布数 | >= 1 篇（至少 HN Show HN） | 不发帖 = 不存在 |
| 网站注册数 | >= 3 | 证明有人看到了并且愿意试 |
| 创建 Check 的用户数 | >= 1 | 有人真的在用 |
| 发送过 Ping 的用户数 | >= 1 | **唯一真正重要的指标**：有人把 curl 加到了他的 cron job 里 |
| GitHub Star | >= 5 | 社区信号 |

### 什么指标不重要

- 页面浏览量（看了不注册 = 无效）
- 帖子 upvote 数（热闹不等于转化）
- 社交媒体 follower（follower 不是用户）

---

## 运营陷阱警告

### 陷阱 1：继续加功能而不发布
**症状：** "再加一个 multi-region ping 功能再发布"
**真相：** 0 用户的产品不需要 multi-region。先让一个人用起来。

### 陷阱 2：完美主义推迟发布
**症状：** "Landing Page 还需要再改改"
**真相：** 没有用户看过 Landing Page，你不知道哪里需要改。先发布，用数据说话。

### 陷阱 3：关注虚荣指标
**症状：** "我们的 HN 帖子拿到 50 个 upvote！"
**真相：** 如果 50 个 upvote 换来 0 个注册，upvote 毫无价值。唯一的指标是：有人把 curl 加到 cron job 里了吗？

### 陷阱 4：过早追求规模化
**症状：** "我们需要一个 Twitter bot 自动发推"
**真相：** 你还没有第一个用户。手动找。一个一个争取。当你有了 100 个用户再谈自动化。

### 陷阱 5：写帖子不发帖子
**症状：** 已经有 8 篇帖子草稿了，0 篇发布了。
**真相：** **这就是我们过去 26 轮犯的错。** 写帖子是伪生产力。发帖子才是真行动。

---

## 执行节奏

```
今天（周四）：
  - AI：搜索 Reddit/HN 相关帖子，生成回复草稿
  - AI：准备 awesome-list PR
  - 人类：npm publish CLI
  - 人类：开始用 CronPulse 监控自己的 cron job

周五：
  - 人类：继续 dogfooding（让 CronPulse 跑满 24 小时）
  - AI：优化 GitHub README
  - AI：完成 awesome-list PR 提交

周六（如果 dogfooding 发现 bug → 修复）

下周二：
  - 人类：发布 HN Show HN 帖子（8:30 AM ET）
  - 人类：全天回复评论
  - AI：实时准备评论回复建议

下周三：
  - 人类：发布 r/SideProject 帖子
  - 人类：在 10 个相关 Reddit 帖子下发回复

下周四：
  - 人类：发布 r/devops 帖子
  - 复盘第一批数据
```

---

## 核心原则

> "Do things that don't scale."

前 10 个用户不是通过"增长策略"来的。他们是通过你亲自找到他们、帮他们解决问题、给他们超预期的服务而来的。

如果这周结束，哪怕只有一个陌生人在他的服务器上加了 `curl https://cron-pulse.com/ping/xxx` —— 这就是成功。这一个人比 26 轮的所有功能开发加起来都有价值。

**停止建造。开始发货。**

---

> **Document**: `docs/operations/cycle27-cold-start-plan.md`
> **Version**: v1.0
> **Related**: `docs/operations/community-launch-posts.md`, `docs/operations/indie-hackers-post.md`
> **Next Action**: 人类先完成 dogfooding + npm publish，然后下周二发 HN
