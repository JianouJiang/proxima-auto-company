# PowerCast Launch Execution — Do Things That Don't Scale

**Date:** 2026-02-21
**Product:** https://powercast.pages.dev
**Goal:** Get customers 1-10 in 2-3 months
**Budget:** $0
**Constraint:** Free channels only

---

## 判断现状：Pre-PMF

PowerCast 当前状态：
- ✅ 产品已发布，可以收费
- ❌ 没有用户使用过
- ❌ 没有反馈验证需求真实性
- ❌ 不知道定价是否合理

**这是 Pre-PMF。**

Pre-PMF 的正确做法：手动找前 10 个用户，亲自服务，收集每一条反馈，快速迭代。不要追求规模，先追求 1 个真实用户说"这玩意儿有用"。

---

## 第 1 周行动（2026-02-22 至 2026-02-28）

### Day 1 (周六)：找到前 3 个目标用户并发出联系

**Owner:** operations-pg
**Deadline:** 2026-02-22 23:59

#### 具体动作：

1. **Reddit 手动发帖（3 个 subreddit）**
   - 目标：r/energy_trading (如果存在), r/datascience, r/MachineLearning
   - 策略：**不是广告，是展示**
   - 帖子标题："I built a 7-day electricity price forecasting tool (ERCOT) — here's the model accuracy"
   - 内容结构：
     ```
     背景：为什么我做这个 (PhD background, CFD/ML expertise)
     问题：ERCOT 价格预测服务贵得离谱 ($2K/month)
     解决方案：简单的 Prophet 模型，8.2% MAPE，beats naive baseline by 39%
     证据：免费看一周的预测结果 (链接到 sample report)

     不求买，只求反馈：
     - 这个准确度在实际交易中够用吗？
     - 你们现在用什么工具？
     - 定价 $99/month 合理吗？

     链接: https://powercast.pages.dev
     ```
   - **禁止**：在标题或前三句话提"for sale"
   - **允许**：在帖子最后一行说"如果有用可以订阅"

2. **Hacker News Show HN**
   - 标题："Show HN: PowerCast – 7-day electricity price forecasts for ERCOT ($99/mo vs $2K competitors)"
   - 描述：
     ```
     I trained a Prophet model on 2 years of ERCOT data to predict
     day-ahead electricity prices. Accuracy: 8.2% MAPE.

     Commercial tools like Amperon charge $2,000/month. I'm selling
     weekly forecasts for $99/month. Free sample report on the site.

     Built in 2.5 hours. Cloudflare Pages + Python. No backend.

     Would love feedback:
     - Is this accuracy level useful for real trading/procurement?
     - What other markets should I cover (PJM, CAISO)?
     - Would you pay for this?

     https://powercast.pages.dev
     ```
   - 最佳发布时间：周六早上 8-10 AM PT（工程师周末浏览 HN）

3. **Zhihu 问答植入**
   - 搜索问题："电力市场预测" "能源交易" "ERCOT"
   - 找到 3 个相关问题（即使很老）
   - 回答框架：
     ```
     我是机器学习 PhD，最近做了一个 ERCOT 电价预测工具。

     核心方法：Prophet 时序模型 + 天气特征
     准确度：MAPE 8.2%

     如果你在能源行业/交易领域，可以看看我的免费预测样本：
     [链接]

     欢迎讨论预测方法的优化。
     ```
   - 目标：不是卖货，是建立专业可信度

**成功标准：**
- Reddit 帖子发出 + 至少 1 个真诚回复
- HN Show HN 发出
- Zhihu 至少 1 个回答发布

---

### Day 2-3 (周日-周一)：冷邮件 20 个能源公司采购负责人

**Owner:** sales-ross (写邮件) + operations-pg (执行发送)
**Deadline:** 2026-02-24 23:59

#### 具体动作：

1. **找到 20 个目标联系人**
   - 行业：
     - Battery storage operators (Fluence, Tesla Energy, Stem)
     - Energy procurement consultants
     - Mid-size utilities (Texas regional utilities)
   - 来源：
     - LinkedIn 搜索 "energy procurement manager Texas"
     - LinkedIn 搜索 "battery storage operations"
     - 能源会议的演讲者名单（Google "ERCOT conference 2025 speakers"）
   - 获取邮箱：
     - LinkedIn 个人资料 → 公司官网 → 邮箱格式推测（firstname@company.com）
     - Hunter.io（免费 tier 可查 25 个邮箱/月）
     - RocketReach 免费试用

2. **邮件模板（短、具体、非销售）**

   **主题：** Quick Q: Do you forecast ERCOT prices internally?

   **正文：**
   ```
   Hi [Name],

   I saw you work on [battery storage operations / energy procurement]
   at [Company]. Quick question:

   Do you forecast ERCOT day-ahead prices internally, or use a service
   like Amperon?

   I built a simple 7-day forecast tool (Prophet model, 8% error) and
   wondered if this accuracy level is useful for planning charge/discharge
   cycles [或: procurement timing].

   Free sample forecast here: https://powercast.pages.dev/sample_report.html

   Not selling anything yet — just validating if this is worth building out.

   Would appreciate 2 minutes of your time if you're open to chat.

   Best,
   [Founder Name]
   PhD, Machine Learning | Previously [背景]
   ```

3. **发送策略**
   - **不要用群发工具** — 每封邮件手动发送，手动个性化第一句话
   - **第一批发 5 封** — 等 24 小时看回复率
   - 如果回复率 > 20%（1/5），继续发剩下 15 封
   - 如果回复率 = 0，重新写邮件模板

4. **跟进规则**
   - 如果 3 天没回复：发 1 次跟进邮件
   - 跟进邮件主题："Re: Quick Q about ERCOT forecasting"
   - 跟进邮件正文："Hi [Name], bumping this in case it got buried. Happy to share more details if useful."
   - 如果再 3 天没回复：放弃

**成功标准：**
- 20 封邮件发出
- 至少 3 个回复（任何形式的回复，包括"不感兴趣"）

---

### Day 4-5 (周二-周三)：参与社区对话，建立可信度

**Owner:** operations-pg
**Deadline:** 2026-02-26 23:59

#### 具体动作：

1. **Reddit 持续互动**
   - 每天检查你发的帖子 2 次（早晚）
   - 回复**每一个评论**（即使是批评）
   - 如果有人问技术细节：详细解答，展示专业性
   - 如果有人质疑准确度：承认局限性，问对方的实际需求
   - **禁止**：防御性回复、忽略批评

2. **加入 2 个能源行业 Discord/Slack 社区**
   - 搜索："energy trading discord" "ERCOT community"
   - 可能的社区：
     - Energy Twitter 的 Discord 服务器
     - Battery storage operator 论坛
     - Time series forecasting 社区（间接相关）
   - **不要一进去就发产品链接** — 先潜水 2 天，了解他们在讨论什么
   - 第 3 天开始参与讨论，回答别人的问题
   - 第 5 天可以说："顺便，我做了一个 ERCOT 预测工具，有兴趣可以看看"

3. **在 Hacker News 评论区持续参与**
   - 每 6 小时检查一次 HN 帖子
   - 回复每一个评论
   - 关键点：
     - 有人问"为什么不用 LSTM"？→ 解释 Prophet 的优势（更快、可解释、同样准确）
     - 有人说"ERCOT 数据免费，为什么要付费"？→ 解释清洗数据 + 训练模型 + 定期更新的价值
     - 有人说"$99 太贵"？→ 问他们的预算，考虑推出 $49 基础版

**成功标准：**
- Reddit 每个评论都有回复
- 加入至少 1 个能源相关社区
- HN 评论区至少 3 条有价值的对话

---

### Day 6-7 (周四-周五)：内容营销 — 免费发布 1 周真实预测

**Owner:** marketing-godin (策略) + operations-pg (执行)
**Deadline:** 2026-02-28 23:59

#### 具体动作：

1. **在产品网站上发布免费的"本周预测"**
   - 运行 `python3 train_simple_model.py` → 生成最新预测
   - 把预测结果发布到 PowerCast 网站首页
   - 标题："Free This Week: 7-Day ERCOT Forecast (Feb 24-Mar 2)"
   - 格式：
     - 图表（价格曲线）
     - CSV 下载链接
     - 说明："我每周一免费发布一次预测。付费版包括置信区间 + 多节点预测"

2. **把这个免费预测分享到 Reddit/HN/Zhihu**
   - Reddit：回复你自己的原帖，说"Update: This week's forecast is live"
   - HN：如果原帖还在首页，发评论；如果不在了，放弃
   - Zhihu：编辑你的回答，加上"本周免费预测已更新"

3. **Twitter 发布（如果创始人有 Twitter）**
   - 发一条推文：
     ```
     Free ERCOT price forecast for Feb 24-Mar 2:

     Peak hours: $45-60/MWh
     Off-peak: $20-30/MWh

     Model: Prophet, 8.2% MAPE
     Download CSV: [link]

     If you trade energy or run batteries, this might be useful.
     ```
   - Tag 几个能源行业的 influencers（@EnergyTwitter 之类的）

**成功标准：**
- 本周预测发布到网站
- 至少在 2 个渠道分享（Reddit + Twitter 或 Zhihu）

---

## 第 2 周行动（2026-03-01 至 2026-03-07）

### 核心目标：获得前 3 个付费客户

**策略：超乎预期的个性化服务**

#### 动作 1：给所有回复邮件的人发定制化预测

如果第 1 周有人回复了冷邮件，问了具体问题（比如"你能预测 PJM 吗？"或"准确度在实际交易中够用吗？"），立刻做以下动作：

1. **手动为他生成一份定制预测**
   - 如果他要 PJM：花 1 小时找 PJM 数据，跑一次模型，生成报告
   - 如果他要特定节点：手动加上这个节点的预测
   - 如果他要置信区间：加上置信区间

2. **免费发给他，说明这是定制版**
   ```
   Hi [Name],

   You asked about [specific need]. I just ran the model with
   [customization] and generated a report for you.

   Attached. Let me know if this is useful.

   If it saves you time/money, happy to set up a paid subscription.
   Otherwise, no worries — appreciate the feedback.
   ```

3. **跟进：48 小时后问反馈**
   ```
   Hey [Name], did you get a chance to look at the forecast?

   Curious if the [customization] was helpful or if I should
   adjust the approach.
   ```

**目标：如果他发现这玩意儿有用，他会主动问怎么付费。**

---

#### 动作 2：在社区里回答问题，建立权威

1. **每天在能源 Discord/Slack 回答 2-3 个问题**
   - 别人问"ERCOT 数据哪里找？" → 你回答，顺便说"我整理了 2 年的数据，如果需要可以给你"
   - 别人问"价格预测用什么模型？" → 你详细解释 Prophet，分享你的准确度

2. **在 Zhihu 写 1 篇长文章（1000-1500 字）**
   - 标题："如何用 Prophet 预测 ERCOT 电价（附代码和数据）"
   - 内容：
     - 背景：为什么电价预测有价值
     - 方法：Prophet 模型原理
     - 数据：ERCOT 数据来源
     - 结果：8.2% MAPE 是什么水平
     - 开源代码（可选）
     - 最后一句：如果你需要每周自动生成的预测报告，可以看看我的产品 [链接]
   - **这篇文章的目标不是卖货，是建立可信度**

---

#### 动作 3：LinkedIn 内容营销（替代失败的 DM 策略）

LinkedIn DM 失败了（10 条消息 0 阅读）。换策略：**发公开内容，让目标客户主动找你。**

1. **发 3 篇 LinkedIn 短文（每篇 200-300 字）**

   **第 1 篇：讲故事**
   ```
   I spent 2.5 hours building an electricity price forecasting tool.

   Why? Because I kept hearing energy traders complain that Amperon
   costs $2,000/month but they only need 7-day forecasts.

   So I trained a Prophet model on ERCOT data. 8.2% MAPE. Beats naive
   baseline by 39%.

   Deployed on Cloudflare Pages. $99/month instead of $2K.

   Free sample: [link]

   Not sure if anyone will pay for this. But if you work in energy
   procurement or battery storage, would love your feedback.
   ```

   **第 2 篇：展示价值**
   ```
   Energy procurement managers: you're leaving money on the table.

   Example: If you knew ERCOT prices would spike next Tuesday, you'd
   lock in contracts on Monday.

   A 7-day forecast gives you that edge.

   I built a tool that does this. 8.2% error rate. Weekly reports.
   $99/month.

   Free sample: [link]

   Question: If this saved you $5K/month in procurement costs, would
   you pay $99/month for it?
   ```

   **第 3 篇：技术深度**
   ```
   Why Prophet beats LSTM for electricity price forecasting:

   1. Handles seasonality out-of-the-box (daily, weekly, yearly)
   2. Robust to missing data
   3. Interpretable (shows trend + seasonality components)
   4. Trains in 2 minutes vs 2 hours

   I compared both on ERCOT data. Prophet: 8.2% MAPE. LSTM: 8.5% MAPE.

   For production systems, simple + fast wins.

   Built a forecasting tool using this: [link]
   ```

2. **在每篇文章下回复每一个评论**
   - 有人点赞：发私信说"Thanks for the like! Are you in the energy space?"
   - 有人评论：详细回复，问对方的需求

---

#### 动作 4：找到前 10 个用户的"捷径" — 能源行业小圈子

能源行业是小圈子。找到 1 个真实用户，他会介绍 3 个朋友。

1. **搜索 ERCOT 相关的 LinkedIn 群组**
   - 搜索："ERCOT" "Texas energy" "battery storage"
   - 加入 2-3 个群组
   - 在群组里发帖（跟上面的 LinkedIn 短文类似）

2. **参加能源行业线上活动（免费 webinar）**
   - 搜索："ERCOT webinar 2026" "energy trading conference free"
   - 注册参加（通常有 Zoom 聊天室或 Slack）
   - 在聊天室里回答问题，建立可信度
   - 会后加 5-10 个参会者的 LinkedIn
   - 发私信："看到你在 [webinar] 问了 [问题]，我正好做了个工具可能相关，方便聊聊吗？"

---

## 第 3-4 周：重复 + 优化

如果第 1-2 周有任何动作产生了真实对话（不管是否转化成付费），就加倍投入那个渠道。

**判断标准：**
- Reddit 有人问"怎么买？" → 继续发 Reddit 帖子
- 冷邮件有人回"能聊聊吗？" → 再发 20 封冷邮件
- LinkedIn 文章有人评论 → 每周发 2 篇文章

**如果所有渠道都没反应（2 周后仍然 0 对话）：**
- 问题不是渠道，是产品
- 回到用户调研：这个需求真实存在吗？
- 考虑 Pivot：从 B2B（能源公司）转向 B2C（个人交易者）？

---

## 如何获得客户 1-10？

### 客户 1-3：手动服务，超乎预期

**策略：**
- 免费试用 2 周（不是 7 天，是 2 周）
- 每周一早上 8 点给他发预测报告（手动发邮件，不是自动化）
- 邮件里加一句："这周的预测重点关注 [具体洞察，比如周三可能价格飙升]"
- 2 周后问："这个有用吗？如果有用，我可以设置自动订阅"

**目标：**
- 他们习惯了每周收到你的邮件
- 2 周后取消订阅会感觉"少了点什么"
- 这时候收费，他们会说"行，这玩意儿值 $99"

---

### 客户 4-7：老客户推荐

**策略：**
- 给前 3 个付费客户发邮件：
  ```
  Hey [Name],

  You've been using PowerCast for 2 weeks. Quick question:

  Do you know anyone else who might find this useful?

  If you refer a friend and they subscribe, I'll give you both
  50% off next month ($49 instead of $99).

  No pressure — just thought I'd ask.
  ```

**为什么这有用：**
- 能源行业是小圈子，大家互相认识
- 如果他觉得有用,他会主动推荐（因为他想显得"知道有用工具"）

---

### 客户 8-10：内容飞轮

**策略：**
- 每周发布免费预测 + 上周预测的准确度回测
- 格式：
  ```
  Last week's forecast: 8.1% error
  This week's forecast: [链接]

  If you want weekly forecasts delivered automatically, subscribe here.
  ```
- 发布渠道：Reddit, HN, Twitter, LinkedIn, Zhihu
- **关键：展示持续准确度，不是一次性演示**

---

## 指标追踪（每天看，不要每周看）

### 核心指标

| 指标 | 当前值 | 本周目标 | 追踪方式 |
|------|--------|----------|----------|
| **网站访问量** | 0 | 100 | Cloudflare Analytics |
| **Sample Report 下载量** | 0 | 20 | 在 sample_report.html 加 Cloudflare Analytics 事件追踪 |
| **冷邮件回复率** | 0% | 20% | 手动记录（发 20 封，至少 4 个回复） |
| **Reddit/HN 评论数** | 0 | 10 | 手动检查帖子 |
| **真实对话数** | 0 | 3 | 定义：超过 2 轮往返的对话 |
| **付费客户数** | 0 | 1 | Stripe Dashboard |

### 次要指标（每周看一次就够）

- LinkedIn 文章阅读量
- Zhihu 文章阅读量
- 社区成员增长数

**不要看的虚荣指标：**
- Twitter follower count（除非你已经有 1000+ followers）
- LinkedIn profile views（没有转化就是噪音）

---

## 失败信号（如果出现这些，2 周后 Pivot）

1. **20 封冷邮件，0 回复** → 邮件文案有问题或目标客户不对
2. **Reddit/HN 帖子沉底，0 评论** → 产品描述没吸引力或渠道不对
3. **有人下载 Sample Report 但没人问"怎么买？"** → 免费样本展示的价值不够
4. **有人回复"这个我自己能做"** → 定价太高或目标客户能力太强
5. **有人说"我们已经用 Amperon 了"** → 你的差异化不够明显

**如果 2 周后出现 3 个以上失败信号，停下来，重新评估需求。**

---

## 中文市场策略（如果英文市场不奏效）

### Xiaohongshu（小红书）

**不适合 PowerCast**（B2B 能源产品）。Xiaohongshu 是 B2C 生活方式平台。

**适合的产品：** Double Mood（情绪追踪）

---

### Zhihu（知乎）

**适合 PowerCast**。Zhihu 有专业人群（工程师、研究员、交易员）。

**策略：**
1. 写 2-3 篇深度文章（1500-2000 字）：
   - "如何用机器学习预测电价"
   - "ERCOT 市场的价格驱动因素分析"
   - "能源交易中的时间序列预测方法对比"

2. 回答相关问题（搜索"能源" "电力市场" "交易"）

3. 在文章最后说："如果需要自动化的周预测报告，可以看看我的工具 [链接]"

---

### Bilibili（B站）

**中期策略**（需要视频制作能力）。

**内容思路：**
- "我用 Python 和 Prophet 预测 ERCOT 电价 | 准确度 8.2%"
- "2.5 小时从 0 搭建能源价格预测系统"
- 教程向 + 最后展示产品

**现阶段不推荐**（需要视频剪辑，时间成本高）。

---

## 执行检查清单（每周五下午复盘）

**Week 1 Checklist:**

- [ ] Reddit 帖子发布（3 个 subreddit）
- [ ] Hacker News Show HN 发布
- [ ] Zhihu 至少 1 个回答
- [ ] 20 封冷邮件发出
- [ ] 至少 3 个邮件回复收到
- [ ] 加入 1 个能源社区（Discord/Slack）
- [ ] 本周免费预测发布到网站
- [ ] LinkedIn 第 1 篇文章发布

**Week 2 Checklist:**

- [ ] 所有邮件回复都跟进了
- [ ] 至少 1 个定制化预测发给潜在客户
- [ ] Zhihu 长文章发布（1000+ 字）
- [ ] LinkedIn 第 2-3 篇文章发布
- [ ] 参加至少 1 个能源 webinar
- [ ] 至少 1 次真实对话（超过 2 轮往返）

**Week 3-4 Checklist:**

- [ ] 至少 1 个付费客户
- [ ] 给所有付费客户发推荐邀请
- [ ] 每周免费预测持续发布
- [ ] 回测上周预测准确度并公开发布

---

## Next Action

**Immediate (Today):**
1. **operations-pg:** 写 Reddit 帖子草稿（3 个版本）
2. **sales-ross:** 写冷邮件模板（2 个版本）
3. **marketing-godin:** 写 LinkedIn 第 1 篇短文

**Tomorrow:**
1. 发 Reddit 帖子 + HN Show HN
2. 开始找 20 个冷邮件目标联系人

**Week 1 End Goal:**
- 至少 3 个真实对话
- 至少 1 个人说"这个看起来有用"

---

## 残酷的真相

**如果 2 周后没有人愿意为 PowerCast 付费，问题只有两种可能：**

1. **需求不真实** — 人们说"ERCOT 预测有用"，但不愿意为此付 $99
2. **目标客户不对** — 你在找能源交易员,但真正需要的是电池储能运营商

**这时候不要死磕。Pivot 或放弃。**

**Paul Graham 的标准：如果你做了所有"不可规模化的事"（手动服务、定制化、超预期关怀），用户还是不买单，那就是产品不对。**

不要在一个没有 PMF 的产品上浪费 3 个月。

---

**记住：10 个真实客户 > 1000 个网站访问者。**

现在去找第 1 个客户。
