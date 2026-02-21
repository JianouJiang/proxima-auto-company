# PowerCast Daily Operations Checklist

**每天 5-10 分钟，确保不漏任何真实对话。**

---

## 早上 9:00 AM（5 分钟）

### 1. 检查收入

- [ ] 打开 Stripe Dashboard：https://dashboard.stripe.com
- [ ] 看 "Payments" 页面：有新订阅吗？
- [ ] 如果有新客户：立刻发欢迎邮件（见下方模板）

---

### 2. 检查邮箱（Gmail）

- [ ] 看收件箱：有冷邮件回复吗？
- [ ] 如果有回复：
  - 记录到 `projects/powercast/outreach_tracker.csv`（状态改为 `replied`）
  - **2 小时内回复**（不要拖到晚上）
- [ ] 如果有人问"怎么买？"：
  - 发送 Stripe 付款链接
  - 提供免费试用 2 周（先建立信任）

---

### 3. 检查社区讨论（Reddit + HN）

- [ ] 打开你发的 Reddit 帖子：有新评论吗？
- [ ] 打开你发的 HN Show HN：有新评论吗？
- [ ] **回复每一个评论**（即使是批评）
- [ ] 记录有价值的反馈到 `docs/operations/user-feedback.md`

---

### 4. 检查 Cloudflare Analytics

- [ ] 打开 Cloudflare Dashboard → Pages → powercast → Analytics
- [ ] 看昨天的数据：
  - Page Views（访问量）
  - Unique Visitors（独立访问者）
  - Top Referrers（流量来自哪里？Reddit? HN? Direct?）
- [ ] 如果某个渠道流量突然增加：去那个渠道看看发生了什么

---

### 5. 更新 Metrics Dashboard

- [ ] 打开 `docs/operations/powercast-metrics-dashboard.md`
- [ ] 更新核心指标：
  - 付费客户数
  - 真实对话数
  - Sample Report 下载数（从 Cloudflare Analytics 看）
  - 冷邮件回复率（从 `outreach_tracker.csv` 算）

---

## 晚上（根据当天进度决定是否执行）

### 6. 发冷邮件（如果还没发完 20 封）

- [ ] 打开 `outreach_tracker.csv`
- [ ] 看今天的目标：还需要发几封？
- [ ] 从 LinkedIn 找 2-3 个目标联系人
- [ ] 用模板写邮件（记得个性化第一句话）
- [ ] 发送
- [ ] 记录到 CSV

**每天发 3-5 封，不要一次发 20 封（太机械）。**

---

### 7. 参与社区讨论（如果加入了 Discord/Slack）

- [ ] 打开能源行业社区（Discord/Slack）
- [ ] 浏览最新讨论（5 分钟）
- [ ] 回答 1-2 个问题（展示专业性）
- [ ] **不要主动推销产品**（除非有人问"有什么工具推荐？"）

---

## 每周一早上（额外 15 分钟）

### 8. 发布本周免费预测

- [ ] 运行 `python3 projects/powercast/models/train_simple_model.py`
- [ ] 运行 `python3 projects/powercast/reports/generate_report.py`
- [ ] 把生成的 `weekly_forecast.html` 和 `weekly_forecast.csv` 上传到 dashboard
- [ ] 在 Reddit/HN/Twitter/Zhihu 发布："本周免费预测已更新"
- [ ] 发给所有正在试用的用户（如果有的话）

---

## 每周五下午（15 分钟复盘）

### 9. 周复盘

- [ ] 打开 `docs/operations/powercast-metrics-dashboard.md`
- [ ] 填写本周的 "实际结果"
- [ ] 回答 3 个问题：
  1. What Worked？（继续做）
  2. What Didn't Work？（停止做）
  3. Next Week Priority？（下周重点）

- [ ] 检查 PMF 信号：
  - 有积极信号吗？（有人主动问价格、推荐给朋友）
  - 有警告信号吗？（下载量高但无人询价、回复率低）
  - 有失败信号吗？（0 回复、0 讨论、0 对话）

- [ ] 如果有 3 个以上失败信号：写一份 "Pivot or Quit" 备忘录给 CEO

---

## 紧急情况响应

### 如果有人回复冷邮件说"我想试试"

**立刻执行（不要等）：**

1. 回复邮件：
   ```
   Hi [Name],

   Great! I'd like to offer you a 2-week free trial before you commit.

   I'll send you this Monday's forecast report manually. If it's useful,
   we can set up a paid subscription after the trial.

   Sound good?

   Best,
   [Your Name]
   ```

2. 把他加入试用名单：`projects/powercast/trial_users.csv`
   - 列：Name, Email, Start Date, Status, Notes

3. 下周一手动给他发预测报告（用他的名字个性化邮件）

4. 2 周后跟进：
   ```
   Hi [Name],

   You've been using PowerCast for 2 weeks. Has it been useful?

   If you'd like to continue, here's the subscription link: [Stripe link]

   If not, no worries — would appreciate any feedback on what could be better.

   Thanks,
   [Your Name]
   ```

---

### 如果有人在 Reddit/HN 说"这个有用，我会买"

**立刻执行：**

1. 回复评论：
   ```
   Thanks! I'd love to give you a free 2-week trial first to make sure
   it actually solves your problem.

   If you're open to it, shoot me an email at [your email] and I'll
   set it up.
   ```

2. 如果他发邮件：按上面的 "试用流程" 处理

---

### 如果有人说"这个不行，因为 [具体原因]"

**不要防御性回复。正确回应：**

1. 感谢反馈：
   ```
   Thanks for the honest feedback. You're right that [acknowledge their point].

   Quick question: if I fixed [specific issue], would this be useful for you?
   Or is there a deeper problem I'm missing?
   ```

2. 记录到 `docs/operations/user-feedback.md`

3. 如果 3 个人提出同样的问题 → 这是真实需求信号，优先修复

---

## 新客户欢迎邮件模板

当 Stripe 收到第一笔订阅时，立刻发这封邮件。

**主题：** Welcome to PowerCast — Here's What to Expect

**正文：**
```
Hi [Name],

Thanks for subscribing to PowerCast!

Here's what you'll receive:

1. Every Monday at 8 AM CT: 7-day ERCOT price forecast
   - HTML report (charts + analysis)
   - CSV file (raw data for your models)

2. Weekly accuracy report (how well last week's forecast performed)

3. Direct access to me via email for questions or custom requests

First forecast goes out this Monday. If you need anything before then,
just reply to this email.

Looking forward to hearing if this saves you time/money.

Best,
[Your Name]
Founder, PowerCast
```

---

## 失败客户挽回邮件模板

如果有人订阅后 1 周就取消，发这封邮件。

**主题：** Quick question about PowerCast

**正文：**
```
Hi [Name],

I noticed you canceled your PowerCast subscription. No problem at all —
just wanted to ask:

Was there something missing, or was the forecast not accurate enough?

Always looking to improve, so any feedback would be super helpful.

Thanks,
[Your Name]
```

---

## 工具清单（每天用到的）

| 工具 | 用途 | 链接 |
|------|------|------|
| **Stripe Dashboard** | 检查收入 | https://dashboard.stripe.com |
| **Gmail** | 检查邮件回复 | https://mail.google.com |
| **Cloudflare Analytics** | 查看流量 | Cloudflare Dashboard → Pages → powercast |
| **outreach_tracker.csv** | 记录冷邮件推广 | `projects/powercast/outreach_tracker.csv` |
| **metrics-dashboard.md** | 追踪核心指标 | `docs/operations/powercast-metrics-dashboard.md` |
| **user-feedback.md** | 记录用户反馈 | `docs/operations/user-feedback.md` |

---

## 时间分配（每天总计 30 分钟）

- **早上检查**（5 分钟）：邮件、社区、指标
- **回复邮件/评论**（10 分钟）：所有新对话 2 小时内回复
- **发冷邮件**（10 分钟）：每天 3-5 封
- **参与社区讨论**（5 分钟）：回答 1-2 个问题

**如果某天有真实对话 → 优先处理对话，其他都可以暂停。**

**记住：1 个真实对话 > 10 封冷邮件。**

---

## Next Action

**今天（2026-02-21）：**
- [ ] 读完这份 checklist
- [ ] 设置日历提醒（每天早上 9 AM）
- [ ] 创建 `user-feedback.md` 文件

**明天（2026-02-22）：**
- [ ] 执行第一次早上检查
- [ ] 发 Reddit 帖子
- [ ] 发 HN Show HN
- [ ] 开始找 20 个冷邮件目标

**每天之后：**
- [ ] 严格执行这份 checklist（不要跳过）

---

做不可规模化的事。现在开始。
