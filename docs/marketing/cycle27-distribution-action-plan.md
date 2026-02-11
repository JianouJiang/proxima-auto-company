# CronPulse -- Cycle 27 分发行动计划

> **Author**: marketing-godin (Seth Godin model)
> **Date**: 2026-02-12
> **Core Diagnosis**: 26 个周期，0 用户。问题不是子弹不够，是从未开枪。

---

## 诊断：为什么 26 轮还是 0 用户？

Seth Godin 会说：**你不是没有产品，你是没有分发。**

子弹库存盘点：
- 3 篇 SEO 博客文章（全部使用错误 URL `cronpulse.dev`，已过时）
- 4 份 Product Hunt 发布文档（从未执行）
- 4 篇社区帖子草稿（HN/Reddit，从未发布，内容过时）
- 1 篇 Dev.to 技术文章（未发布）
- 1 篇 Indie Hackers 帖子（未发布）
- CLI 工具（未发布到 npm）
- GitHub Action（未上 Marketplace）
- GitHub 仓库（0 stars, 0 forks, 仅 2 个 issue）

**核心问题：所有分发物料要么过时，要么从未触达用户。产品本身缺少内置传播机制。**

---

## 第一部分：AI 可自主执行的行动

这些行动不需要人工登录任何平台，可以在本周期内完成。

### P0：修复过时物料（立即执行）

#### 1. 修复博客文章中的错误 URL

**优先级**: P0
**预期效果**: SEO 基础修复 -- 所有指向 `cronpulse.dev` 的链接改为 `cron-pulse.com`

三篇博客文章全部使用了错误的域名 `cronpulse.dev`：
- `docs/marketing/blog-01-monitor-cron-jobs.md` -- 13 处 `cronpulse.dev` 引用
- `docs/marketing/blog-02-cron-failures.md` -- 12 处 `cronpulse.dev` 引用
- `docs/marketing/blog-03-comparison.md` -- 8 处 `cronpulse.dev` 引用

所有 URL 需替换为 `cron-pulse.com`。

#### 2. 更新比较文章中的过时信息

**优先级**: P0
**预期效果**: 比较页面是高购买意向的 SEO 流量入口，内容必须准确

`blog-03-comparison.md` 中以下信息已过时，需要更新：
- "Self-hosted option: No" → CronPulse 已开源，支持 self-host
- "Start/Fail signals: Coming soon" → 已实现（/ping/:id/start, /ping/:id/fail）
- "Status badges: Coming soon" → 已实现（/badge/:id）
- "Team management: Coming soon" → 仍未实现（保持）
- "Cron expression parsing: Interval-based" → 已支持 cron expression（Cycle 24）
- 开源状态需反映：AGPL-3.0 (server) / MIT (CLI + GitHub Action)
- 需添加 CLI 和 GitHub Action 作为差异化优势
- 纠正自称 "cloud-only, no self-hosted option" → 开源可 self-host

#### 3. 更新社区帖子草稿

**优先级**: P0
**预期效果**: 确保人工发布时帖子内容准确、有力

`docs/operations/community-launch-posts.md` 需要更新：
- 删除 "email alerts coming soon" -- 邮件已上线
- 删除 "running on free workers.dev subdomain" / "early preview" -- 现在是正式产品
- 添加开源状态（AGPL-3.0）
- 添加 CLI 和 GitHub Action 作为差异化
- 添加 start/fail 信号、status badge、cron expression 等新功能
- URL 确保使用 `cron-pulse.com`（大部分已更新，但 soft-launch 相关描述需删除）
- 更新 FAQ 回复模板

`docs/marketing/ph-launch-final.md` FAQ 部分需要更新：
- "What is on the roadmap?" 中列出的近期功能大部分已完成
  - Cron expression parsing ✅
  - Start/fail signals ✅
  - Check groups ✅
  - Status badges ✅
  - 需要更新为当前真正的 roadmap items

### P0：产品内置传播机制

#### 4. 在 Public Status Page 添加 "Powered by CronPulse" 水印

**优先级**: P0
**预期效果**: 每个用户的 status page 成为一个免费广告位，病毒传播

当前 public status page (`/status/:userId`) 没有任何指向 CronPulse 的归属链接。每个用户分享给他们的客户/团队的 status page 都是一个潜在的获客入口。

实施方案：在 status page 底部添加：
```
Monitoring powered by CronPulse — Open-source cron job monitoring
```
链接指向 `https://cron-pulse.com?utm_source=status-page&utm_medium=referral`

免费用户强制显示，付费用户可选择隐藏（作为付费功能的一部分）。

#### 5. 在 Status Badge SVG 中嵌入链接元数据

**优先级**: P1
**预期效果**: 每个嵌入 README 的 badge 都能引导点击回 CronPulse

当前 badge endpoint (`/badge/:checkId`) 生成的 SVG 没有关联的链接。用户在 README 中展示 badge 时，建议文档示例包含指向 CronPulse 的链接：

```markdown
[![CronPulse Status](https://cron-pulse.com/badge/YOUR_CHECK_ID)](https://cron-pulse.com)
```

确保 API 文档和 dashboard 中 badge 的复制按钮输出的 markdown 默认包含链接。

### P1：GitHub 生态分发优化

#### 6. 优化 GitHub 仓库可发现性

**优先级**: P1
**预期效果**: 提高 GitHub 搜索排名和 Explore 页面曝光概率

当前 topics: `cloudflare-workers`, `cron-jobs`, `cron-monitoring`, `devops`, `monitoring`, `serverless`, `typescript`

建议补充的 topics（GitHub 限制 20 个）：
- `open-source`
- `dead-mans-switch`
- `heartbeat-monitoring`
- `self-hosted`
- `cloudflare-d1`
- `hono`
- `cron`
- `alerting`
- `uptime-monitoring`

Description 当前："Open-source cron job monitoring built on Cloudflare Workers. One curl, instant alerts." -- 已经不错，但可以强化：
- 建议改为："Open-source cron job monitoring on Cloudflare Workers. One curl, instant alerts. CLI + GitHub Action included. Self-hostable."

#### 7. 创建 Good First Issues 吸引贡献者

**优先级**: P1
**预期效果**: 吸引开源贡献者，增加 star/fork，建立社区

当前仅 2 个 issue（Docker 本地开发、Telegram 通知）。需要创建 8-10 个标记为 `good first issue` 和 `help wanted` 的 issue：

| Issue 标题 | 类型 | 标签 |
|-----------|------|------|
| Add Discord notification channel | feature | `good first issue`, `help wanted` |
| Add Telegram notification channel | feature | `good first issue`, `help wanted` |
| Add PagerDuty native integration | feature | `help wanted` |
| Improve mobile responsive design on dashboard | enhancement | `good first issue` |
| Add dark/light theme toggle | enhancement | `good first issue` |
| Add French / German / Japanese localization | i18n | `good first issue`, `help wanted` |
| Write Terraform provider for CronPulse | feature | `help wanted` |
| Add Prometheus metrics export endpoint | feature | `help wanted` |
| Add Docker Compose setup for local development | docs | `good first issue` |
| Create browser extension for check status | feature | `help wanted` |

每个 issue 需要包含：
- 清晰的问题描述
- 预期行为
- 相关代码位置指引
- 技术方向建议

#### 8. 优化 GitHub README

**优先级**: P1
**预期效果**: 提高 star 转化率，README 是 GitHub 上的 landing page

当前 README 结构合理，但缺少：

1. **npm 安装命令**（CLI 发布后添加）：
```bash
npm install -g cron-pulse-cli
cronpulse init "My Backup" --every 1h
```

2. **GitHub Action 使用示例**：
```yaml
- uses: nicepkg/cronpulse/github-action@main
  with:
    check-id: YOUR_CHECK_ID
```

3. **Status badge 展示**：在 README 顶部用自己的 CronPulse badge 展示自己的服务状态

4. **"Powered by" 列表**：预留一个 "Used by" 区域，初期可以用 "Add your project!" 的 PR 模板

5. **Star History** 图表链接（等有 star 后添加）

6. **快速对比表格**：与 Healthchecks.io / Cronitor 的简洁对比

#### 9. 准备 awesome-* 列表 PR

**优先级**: P1
**预期效果**: awesome 列表是开源项目的长期被动流量来源

可提交 PR 的列表：
- `awesome-selfhosted` -- 最有价值，12K+ stars，监控类别
- `awesome-cloudflare` -- Cloudflare 生态，Workers 类别
- `awesome-sysadmin` -- 系统管理工具，监控类别
- `awesome-devops` -- DevOps 工具链
- `awesome-monitoring` -- 监控工具集合

每个 PR 需要：
- 遵循该列表的格式要求
- 简短描述（一行）
- 确保 CronPulse 满足该列表的收录标准（通常要求开源、有 README、活跃维护）

**注意**：awesome-selfhosted 通常要求一定的 star 数。建议等社区帖子发布后、获得初始 star 再提交。

### P1：SEO 内容优化

#### 10. 创建新的 SEO 内容策略

**优先级**: P1
**预期效果**: 长尾关键词带来持续的有机搜索流量

现有 3 篇文章覆盖的关键词：
- "how to monitor cron jobs" (blog-01)
- "cron job failures" (blog-02)
- "healthchecks.io vs cronitor vs cronpulse" (blog-03)

建议新增的高价值长尾关键词文章：

| 关键词 | 文章标题 | 搜索意图 |
|--------|---------|---------|
| `cron job not running` | "Why Your Cron Job Is Not Running: 7 Common Causes and Fixes" | 问题诊断 |
| `crontab monitoring` | "Crontab Monitoring: The Complete Setup Guide" | 教程 |
| `kubernetes cronjob monitoring` | "How to Monitor Kubernetes CronJobs with Heartbeat Pings" | 教程 |
| `github actions scheduled workflow monitoring` | "Monitor GitHub Actions Scheduled Workflows with CronPulse" | 教程 |
| `dead mans switch monitoring` | "Dead Man's Switch for Servers: How Heartbeat Monitoring Works" | 概念 |
| `cronitor alternative` | "CronPulse vs Cronitor: Open-Source Cron Monitoring Compared" | 比较 |
| `healthchecks.io alternative` | "CronPulse vs Healthchecks.io: Which Cron Monitor Fits Your Stack?" | 比较 |
| `self hosted cron monitoring` | "Self-Hosted Cron Monitoring on Cloudflare Workers" | 教程 |
| `systemd timer monitoring` | "How to Monitor systemd Timers with Heartbeat Pings" | 教程 |

优先产出比较类文章（"vs" 类关键词），因为搜索这些的用户购买意向最高。

#### 11. 检查现有博客 SEO 元素

**优先级**: P1
**预期效果**: 确保已有内容获得最大搜索可见度

现有文章缺少的 SEO 元素（需要在部署的博客页面中确认）：
- `<title>` 标签是否包含主关键词
- `<meta description>` 是否存在且包含关键词
- `<h1>` 是否唯一且包含关键词
- 内部链接（文章之间是否相互链接）
- Schema.org 结构化数据（Article type）
- Open Graph 和 Twitter Card meta tags
- Canonical URL 设置

### P2：内容分发准备

#### 12. 创建 One-Pager 介绍文档

**优先级**: P2
**预期效果**: 方便社交分享和快速了解产品

创建一份简洁的一页介绍（`docs/marketing/cronpulse-one-pager.md`）：

```
CronPulse -- Open-Source Cron Job Monitoring

Problem: Cron jobs fail silently. You find out days later.
Solution: One curl. Instant alerts.

How it works:
  curl -fsS https://cron-pulse.com/ping/YOUR_CHECK_ID

Features: Email/Slack/Webhook alerts | Start/Fail signals |
          Status badges | Cron expression parsing | Groups |
          Public status page | REST API | CLI tool | GitHub Action

Open Source: AGPL-3.0 (server) | MIT (CLI + GitHub Action)
Self-Host: Deploy to your own Cloudflare account
Pricing: Free (10 checks) | $5/mo (50) | $15/mo (200) | $49/mo (1000)

GitHub: github.com/nicepkg/cronpulse
Website: cron-pulse.com
```

#### 13. 更新 Dev.to 文章

**优先级**: P2
**预期效果**: 技术社区的长期被动流量

`docs/marketing/devto-cloudflare-workers-saas.md` 需要更新：
- 移除 "early preview" 相关措辞
- 添加开源状态
- 添加 CLI 和 GitHub Action 部分
- 确保 URL 使用 `cron-pulse.com`
- 设置 `published: true`（人工发布时）

---

## 第二部分：需人工执行的行动

AI 无法登录外部平台账号。以下行动需要创始人（人类）手动执行。

### P0：必须立即做的（本周）

#### 1. 发布 CLI 到 npm

**预期时间**: 15 分钟
**预期效果**: npm 是开发者工具的第一发现渠道。`npm install -g cron-pulse-cli` 是最自然的入口。每周 npm 搜索 "cron monitor" 的人可能就是你的用户。

```bash
cd projects/cronpulse/cli
npm login
npm publish
```

发布后 AI 可以更新 README 和文档中的安装命令。

#### 2. 发布 GitHub Action 到 Marketplace

**预期时间**: 30 分钟
**预期效果**: GitHub Marketplace 有自然搜索流量。CI/CD 用户天然需要 cron 监控。

需要将 `github-action/` 目录独立为一个仓库，或在当前仓库中创建一个 action.yml 在根目录并发布 Release。

#### 3. 在 Cloudflare Dashboard 开启 "Always Use HTTPS"

**预期时间**: 2 分钟
**预期效果**: HTTP 不重定向 HTTPS 会影响 SEO 排名和用户信任。

### P1：本周内做的

#### 4. 发布 Show HN 帖子

**预期时间**: 5 分钟发帖 + 全天回复评论
**预期效果**: HN 是 CronPulse 目标用户最密集的社区。一个成功的 Show HN 可以带来 50-200 个注册。

使用 `docs/marketing/ph-launch-final.md` 中的 Show HN 模板（AI 将在本周期更新为最新状态）。

**最佳时间**: 周二或周三，8:00-9:00 AM ET。

#### 5. 发布 Reddit 帖子（r/selfhosted, r/devops, r/SideProject）

**预期时间**: 每个帖子 5 分钟 + 持续回复
**预期效果**: Reddit 是长尾流量来源。r/selfhosted 社区对开源工具极其友好。

与 HN 帖子错开 2-3 天。使用更新后的模板。

**注意**: 不同社区用不同的帖子。r/selfhosted 强调开源和 self-host，r/devops 强调生产实践，r/SideProject 强调构建故事。

#### 6. 发布 Dev.to 技术文章

**预期时间**: 10 分钟（文章已写好）
**预期效果**: Dev.to 是 SEO 强站，文章会在 Google 中获得好排名

使用 `docs/marketing/devto-cloudflare-workers-saas.md`（AI 将更新为最新内容）。

#### 7. 发布 Indie Hackers 帖子

**预期时间**: 10 分钟
**预期效果**: IH 社区对 Build in Public 的项目有天然好感

使用 `docs/operations/indie-hackers-post.md`。

### P2：两周内做的

#### 8. 创建 Product Hunt 账号并预热

**预期时间**: 2-3 小时/周，持续 2 周
**预期效果**: PH 是一次性大曝光机会，但需要社区预热

按照 `docs/marketing/ph-launch-final.md` 的 T-14 到 T-1 计划执行。建议在 Reddit/HN 帖子发布 2 周后进行 PH launch。

#### 9. 向 awesome-* 列表提交 PR

**预期时间**: 每个 PR 10 分钟
**预期效果**: 长期被动流量，awesome-selfhosted 有 200K+ stars

建议在获得 10+ GitHub stars 后提交，提高被接受概率。

#### 10. 提交到目录网站

**预期时间**: 每个网站 5-10 分钟
**预期效果**: 反向链接提升 SEO，部分目录有自然流量

目标目录：
- AlternativeTo（作为 Healthchecks.io / Cronitor 的替代品）
- SaaSHub
- DevHunt
- ToolFinder
- StackShare

---

## 优先级总结

### AI 本周期执行清单

| # | 行动 | 优先级 | 预期效果 |
|---|------|--------|---------|
| 1 | 修复博客文章 URL (`cronpulse.dev` → `cron-pulse.com`) | P0 | SEO 基础修复 |
| 2 | 更新比较文章过时内容 | P0 | 高意向流量页面准确性 |
| 3 | 更新社区帖子草稿 | P0 | 人工发布前内容就绪 |
| 4 | 添加 "Powered by CronPulse" 到 status page | P0 | 内置病毒传播 |
| 5 | 优化 badge 复制功能含链接 | P1 | 每个 README badge 成为入口 |
| 6 | 补充 GitHub topics | P1 | 提高搜索可发现性 |
| 7 | 创建 Good First Issues | P1 | 吸引贡献者 |
| 8 | 优化 GitHub README | P1 | 提高 star 转化率 |
| 9 | 准备 awesome-* PR 内容 | P1 | 长期被动流量准备 |
| 10 | 新 SEO 文章策略 | P1 | 长尾搜索流量规划 |
| 11 | 检查现有博客 SEO | P1 | 最大化已有内容价值 |
| 12 | 创建 One-Pager | P2 | 快速分享物料 |
| 13 | 更新 Dev.to 文章 | P2 | 技术社区准备 |

### 人工执行清单

| # | 行动 | 优先级 | 预期时间 | 预期效果 |
|---|------|--------|---------|---------|
| 1 | npm publish CLI | P0 | 15 分钟 | 打通最大分发渠道 |
| 2 | GitHub Action Marketplace | P0 | 30 分钟 | CI/CD 用户获取 |
| 3 | 开启 HTTPS 重定向 | P0 | 2 分钟 | SEO + 信任 |
| 4 | Show HN 帖子 | P1 | 5 分钟 + 全天 | 50-200 注册 |
| 5 | Reddit 帖子 x3 | P1 | 15 分钟 + 持续 | 长尾流量 |
| 6 | Dev.to 文章 | P1 | 10 分钟 | SEO 被动流量 |
| 7 | Indie Hackers | P1 | 10 分钟 | Build in Public |
| 8 | Product Hunt | P2 | 2-3 周准备 | 一次性大曝光 |
| 9 | awesome-* PRs | P2 | 50 分钟 | 长期被动流量 |
| 10 | 目录提交 | P2 | 30-50 分钟 | 反向链接 + 流量 |

---

## 核心信念

**26 个周期 0 用户不是产品问题，是分发问题。**

CronPulse 已经拥有一个成熟的、差异化的产品：
- 开源 (AGPL-3.0 / MIT)
- 全球边缘网络 (300+ 节点)
- CLI + GitHub Action + REST API
- Start/Fail 信号、Cron Expression、Status Badge、Groups、Public Status Page
- 激进定价 ($5/50 checks)

这个产品值得被谈论 -- 它是一头紫牛。但一头紫牛如果关在谷仓里，谁也看不见。

**现在是开门的时候了。**

Purple Cow 提醒：产品本身就是最好的营销。但产品需要被看到。分发不是事后诸葛亮，是产品成功的前提条件。一个没有用户看到的优秀产品，等于一个不存在的产品。

---

> **Document**: `docs/marketing/cycle27-distribution-action-plan.md`
> **Version**: v1.0
> **Related**: `ph-launch-final.md`, `community-launch-posts.md`, `blog-01/02/03`
