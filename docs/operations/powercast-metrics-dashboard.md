# PowerCast Launch Metrics Dashboard

**Last Updated:** 2026-02-21

所有指标每天更新（早上 9AM 检查一次即可）。

---

## 北极星指标（唯一重要的数字）

| 指标 | 当前值 | 本周目标 | 定义 |
|------|--------|----------|------|
| **付费客户数** | 0 | 1 | Stripe Dashboard 里的 active subscriptions |

**规则：如果这个数字不动，其他指标都是虚荣指标。**

---

## 第二层指标（通往收入的路径）

| 指标 | 当前值 | 本周目标 | 追踪方式 |
|------|--------|----------|----------|
| **真实对话数** | 0 | 3 | 定义：超过 2 轮往返的对话 |
| **Sample Report 下载** | 0 | 20 | Cloudflare Analytics 事件追踪 |
| **冷邮件回复率** | 0% | 20% | `projects/powercast/outreach_tracker.csv` |
| **社区讨论参与度** | 0 | 10 comments | Reddit + HN 帖子总评论数 |

---

## 流量指标（每周看一次就够）

| 指标 | Week 1 | Week 2 | Week 3 | Week 4 |
|------|--------|--------|--------|--------|
| **网站访问量** | 0 | | | |
| **Unique Visitors** | 0 | | | |
| **Bounce Rate** | - | | | |

**数据来源：** Cloudflare Web Analytics（已配置）

---

## 渠道效果追踪

| 渠道 | 发布数 | 点击数 | 对话数 | 转化数 | ROI 评分 |
|------|--------|--------|--------|--------|----------|
| **Reddit** | 0 | - | - | - | - |
| **Hacker News** | 0 | - | - | - | - |
| **冷邮件** | 0 | - | - | - | - |
| **LinkedIn** | 0 | - | - | - | - |
| **Zhihu** | 0 | - | - | - | - |
| **Twitter** | 0 | - | - | - | - |

**ROI 评分规则：**
- A：产生付费客户
- B：产生 3+ 真实对话
- C：产生 10+ 点击
- D：产生讨论但无转化
- F：无反应

**资源分配原则：**
- A/B 渠道：加倍投入
- C/D 渠道：维持现状
- F 渠道：2 周后停止

---

## 每日检查清单（5 分钟）

**早上 9 AM：**

- [ ] 检查 Stripe Dashboard（有新订阅吗？）
- [ ] 检查邮箱（有冷邮件回复吗？）
- [ ] 检查 Reddit/HN 帖子（有新评论吗？回复所有评论）
- [ ] 更新 `outreach_tracker.csv`（记录所有新动态）

**如果有新对话 → 立刻回复（不要等超过 2 小时）**

---

## 每周复盘（周五下午，15 分钟）

### Week 1 (2026-02-22 至 2026-02-28)

**目标：**
- [ ] 3 个真实对话
- [ ] 20 个 Sample Report 下载
- [ ] 20 封冷邮件发出，4 个回复

**实际结果：**
- 真实对话数：_
- Sample Report 下载：_
- 冷邮件回复率：_
- 付费客户：_

**What Worked（继续做）：**
1. _
2. _

**What Didn't Work（停止做）：**
1. _
2. _

**Next Week Priority：**
1. _
2. _

---

### Week 2 (2026-03-01 至 2026-03-07)

**目标：**
- [ ] 1 个付费客户
- [ ] 5 个真实对话
- [ ] 继续上周有效渠道，停止无效渠道

**实际结果：**
- 真实对话数：_
- Sample Report 下载：_
- 付费客户：_

**What Worked：**
1. _
2. _

**What Didn't Work：**
1. _
2. _

**Next Week Priority：**
1. _
2. _

---

## PMF 验证信号

### 积极信号（继续）

- [ ] 有人主动问"怎么付费？"
- [ ] 有人下载 Sample Report 后发邮件要更多信息
- [ ] 有人说"这个能帮我省钱/赚钱"
- [ ] 有人推荐给朋友
- [ ] 有人在社区里主动提到 PowerCast

### 警告信号（需要调整）

- [ ] 很多人下载 Sample Report 但没人问价格（免费样本展示的价值不够）
- [ ] 很多人说"有意思"但没人愿意试用（定价或定位有问题）
- [ ] 冷邮件回复率 < 5%（目标客户不对或文案有问题）
- [ ] Reddit/HN 帖子沉底无讨论（产品描述没吸引力）

### 失败信号（考虑 Pivot）

- [ ] 20 封冷邮件 0 回复
- [ ] Reddit/HN 帖子 0 评论（沉底）
- [ ] 有人回复"我自己能做"（目标客户能力太强）
- [ ] 有人回复"我们已经用 Amperon 了"（差异化不够）
- [ ] 2 周后仍然 0 真实对话

**如果出现 3 个以上失败信号 → 停下来，重新评估需求。**

---

## 不要追踪的虚荣指标

- ❌ Twitter follower count（除非你已经有 1000+ followers）
- ❌ LinkedIn profile views（没有转化就是噪音）
- ❌ 网站停留时间（早期样本量太小，不可信）
- ❌ Email open rate（现代邮件客户端会误报）

**唯一重要的：有人愿意付钱吗？**

---

## Cloudflare Analytics 配置

PowerCast 已配置 Cloudflare Web Analytics。

**查看方式：**
1. 登录 Cloudflare Dashboard
2. 进入 Pages 项目：`powercast`
3. 点击 "Analytics" 标签

**关键指标：**
- Page Views（总访问量）
- Unique Visitors（独立访问者）
- Top Pages（哪些页面最受欢迎）
- Referrers（流量来源：Reddit, HN, LinkedIn, Direct）

**如何添加事件追踪（Sample Report 下载）：**

在 `dashboard/sample_report.html` 的下载按钮上加：

```html
<a href="weekly_forecast.csv" download
   onclick="if(window.gtag){gtag('event','download',{event_category:'sample_report'})}">
  Download CSV
</a>
```

然后在 Cloudflare Analytics 里可以看到 "download" 事件数量。

---

## 冷邮件追踪（手动记录）

使用 `projects/powercast/outreach_tracker.csv` 记录所有冷邮件推广。

**每次发邮件后：**
1. 在 CSV 里加一行
2. 记录：日期、姓名、公司、邮箱、角色、来源、使用的模板、状态

**状态定义：**
- `pending`：已发送，等待回复
- `replied`：收到回复
- `interested`：表达兴趣，继续跟进
- `not_interested`：明确拒绝
- `no_response`：3 天后无回复
- `converted`：成为付费客户

**每天更新一次（早上 9 AM）。**

---

## 成功标准（2 周检查点）

**2026-03-07（第 2 周结束）时，必须达到以下之一：**

1. **至少 1 个付费客户** — 证明有人愿意为此付费
2. **至少 5 个真实对话 + 3 个人说"有用"** — 证明需求真实存在
3. **至少 100 个 Sample Report 下载 + 10% 的人问价格** — 证明产品有吸引力

**如果 3 个都没达到 → 问题不是渠道，是产品。**

这时候的选择：
1. **Pivot 定价** — 从 $99/month 降到 $49/month 或 $29/month
2. **Pivot 目标客户** — 从 B2B（能源公司）转向 B2C（个人交易者）
3. **Pivot 产品形态** — 从订阅服务变成一次性数据集销售
4. **放弃 PowerCast** — 承认需求不真实，转向 ConnectPath

**不要在一个没有 PMF 的产品上浪费 3 个月。**

---

## Next Action

**Today (2026-02-21):**
- [ ] 设置 Cloudflare Analytics 事件追踪（Sample Report 下载按钮）
- [ ] 创建 `outreach_tracker.csv` 文件

**Tomorrow (2026-02-22):**
- [ ] 发 Reddit 帖子
- [ ] 发 HN Show HN
- [ ] 开始找 20 个冷邮件目标联系人

**Every Day:**
- [ ] 早上 9 AM 检查指标（5 分钟）
- [ ] 回复所有新评论/邮件（不要延迟超过 2 小时）

**Every Friday:**
- [ ] 周复盘（15 分钟）
- [ ] 更新这个 dashboard

---

记住：**10 个真实客户 > 1000 个网站访问者。**

现在去追踪第一个真实对话。
