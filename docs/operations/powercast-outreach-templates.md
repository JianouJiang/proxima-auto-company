# PowerCast Outreach Templates

所有模板遵循 Paul Graham 原则：真诚、具体、非销售导向。

---

## Reddit 帖子模板

### 版本 1：展示型（推荐用于 r/datascience, r/MachineLearning）

**标题：**
```
I built a 7-day electricity price forecasting tool (ERCOT) — 8.2% MAPE with Prophet
```

**正文：**
```
## Background

PhD in ML here. I kept hearing energy traders complain that commercial
forecasting tools (Amperon, Platts) cost $2,000-$5,000/month, but most
teams only need simple day-ahead price predictions.

So I built a minimal version to see if simpler is better.

## Approach

- Model: Prophet (not LSTM — wanted interpretability)
- Data: 2 years of ERCOT LMP prices + weather features
- Training time: ~2 minutes
- Accuracy: 8.2% MAPE (vs 13.5% naive baseline)

## Results

7-day ahead forecasts, updated weekly. Free sample report:
https://powercast.pages.dev/sample_report.html

## Questions for the community

1. Is 8.2% MAPE good enough for real trading/procurement decisions?
2. Should I add confidence intervals, or is point forecast sufficient?
3. Worth expanding to PJM/CAISO, or is ERCOT-only fine for V1?

Not trying to sell anything — genuinely curious if this accuracy level
is useful in production.

Code + methodology: https://powercast.pages.dev

Happy to answer questions about the model or approach.
```

---

### 版本 2：问题导向（推荐用于 r/energy 或 r/investing）

**标题：**
```
How accurate do electricity price forecasts need to be for trading/procurement?
```

**正文：**
```
I'm working on an ERCOT price forecasting tool and trying to understand
the accuracy threshold that makes it useful vs useless.

Current model: Prophet-based, 8.2% MAPE on 7-day ahead forecasts.

Context:
- Commercial tools (Amperon) charge $2K-5K/month
- Most teams seem to use internal models or pay for these services
- I'm not sure if 8% error is "good enough" or "not even close"

Questions:

1. If you trade energy or manage battery storage, what error rate
   would you consider acceptable for day-ahead forecasts?

2. Do you need confidence intervals, or is a point forecast enough?

3. What's more valuable: higher accuracy or faster updates?

Sample forecast (free): https://powercast.pages.dev/sample_report.html

Not selling anything — trying to validate if this problem is worth
solving or if I'm solving the wrong thing.

Appreciate any feedback from people in the industry.
```

---

## Hacker News Show HN

**标题：**
```
Show HN: PowerCast – 7-day electricity price forecasts (ERCOT, $99/mo vs $2K tools)
```

**正文：**
```
I trained a Prophet model on 2 years of ERCOT data to predict day-ahead
electricity prices.

Accuracy: 8.2% MAPE. Beats naive baseline by 39%.

Commercial tools like Amperon charge $2,000-$5,000/month for similar
forecasts. I'm selling weekly reports for $99/month.

Tech stack: Python + Prophet + Cloudflare Pages. No backend. Built in
2.5 hours.

Free sample report: https://powercast.pages.dev/sample_report.html

## Why this exists

I kept hearing energy traders and battery storage operators complain
about the cost of commercial forecasting tools. Most teams only need
7-day ahead predictions, not real-time APIs or complex scenario analysis.

So I built the simplest version that could work: a static report,
updated weekly, delivered via email.

## Why Prophet > LSTM

Tried both. Prophet was faster to train (2 min vs 45 min), more
interpretable (shows trend + seasonality components), and nearly
identical accuracy (8.2% vs 8.5% MAPE).

For production, simple + fast wins.

## Questions for HN

1. Is this accuracy level useful for real trading/procurement decisions?
2. Should I expand to other markets (PJM, CAISO)?
3. Would you pay $99/month for this, or is that still too expensive?

Not sure if anyone will actually buy this, but figured I'd ship and
find out.

https://powercast.pages.dev
```

---

## Cold Email Templates

### 版本 1：Battery Storage Operators

**主题：**
```
Quick Q: Do you forecast ERCOT prices internally?
```

**正文：**
```
Hi [Name],

I saw you work on battery storage operations at [Company]. Quick question:

Do you forecast ERCOT day-ahead prices internally, or use a commercial
service like Amperon?

I built a simple 7-day forecast tool (Prophet model, 8% error) and
wondered if this accuracy level is useful for planning charge/discharge
cycles.

Free sample forecast: https://powercast.pages.dev/sample_report.html

Not selling anything yet — just validating if this is worth building out.

Would appreciate 2 minutes of your time if you're open to chat.

Best,
[Your Name]
PhD, Machine Learning | [Previous Background]
```

---

### 版本 2：Energy Procurement Managers

**主题：**
```
Do you use ERCOT price forecasts for procurement timing?
```

**正文：**
```
Hi [Name],

I noticed you manage energy procurement at [Company]. Random question:

Do you use day-ahead or week-ahead ERCOT price forecasts to time your
contract purchases?

I'm building a tool that predicts 7-day ahead prices (8% error rate)
and trying to understand if this accuracy is useful for procurement
decisions.

Sample forecast: https://powercast.pages.dev/sample_report.html

If you have 5 minutes to chat about your workflow, I'd love to hear
how you currently approach this.

Thanks,
[Your Name]
PhD, ML | Previously [Background]
```

---

### 版本 3：能源交易员

**主题：**
```
Question about ERCOT forecasting tools
```

**正文：**
```
Hi [Name],

Saw you're trading in ERCOT markets. Quick question:

What do you use for price forecasts — internal models, or commercial
tools like Amperon/Platts?

I built a simple 7-day forecast tool (8% MAPE) and I'm trying to
understand if this accuracy is useful for real trading decisions, or
if the threshold is much higher.

Free sample: https://powercast.pages.dev/sample_report.html

Happy to share more details if you're interested.

Cheers,
[Your Name]
```

---

## LinkedIn Post Templates

### 第 1 篇：Origin Story

```
I spent 2.5 hours building an electricity price forecasting tool.

Why?

Because I kept hearing energy traders complain that commercial tools
like Amperon cost $2,000-$5,000/month, but they only need simple
7-day ahead forecasts.

So I trained a Prophet model on 2 years of ERCOT data.

Result: 8.2% MAPE. Beats naive baseline by 39%.

Deployed on Cloudflare Pages. $99/month instead of $2K.

Free sample: https://powercast.pages.dev/sample_report.html

Not sure if anyone will pay for this. But if you work in energy
procurement, battery storage, or trading, I'd love your feedback.

Is 8% error good enough for real decisions?
```

---

### 第 2 篇：Value Proposition

```
Energy procurement managers: you're leaving money on the table.

Example scenario:

- Monday: ERCOT prices are $30/MWh
- Tuesday: Weather forecast shows heat wave coming
- Wednesday: Prices spike to $90/MWh

If you knew this on Monday, you'd lock in contracts at $30.

But most teams don't have forecasting tools (or pay $2K-5K/month for them).

I built a 7-day ahead forecast for $99/month:
- 8% error rate
- Weekly reports delivered Monday mornings
- Covers peak and off-peak hours

Free sample: https://powercast.pages.dev/sample_report.html

Question for the group:

If this saved you $5K/month in procurement costs, would you pay
$99/month for it?

Let me know if I'm solving the wrong problem.
```

---

### 第 3 篇：Technical Depth

```
Why Prophet beats LSTM for electricity price forecasting:

1. Handles seasonality out-of-the-box
   - Daily patterns (peak vs off-peak)
   - Weekly patterns (weekday vs weekend)
   - Yearly patterns (summer demand spikes)

2. Robust to missing data
   - ERCOT API sometimes has gaps
   - Prophet interpolates automatically

3. Interpretable
   - Shows trend + seasonality components separately
   - You can explain WHY prices are predicted to rise

4. Fast
   - Trains in 2 minutes vs 2 hours for LSTM
   - Matters when you're retraining weekly

I tested both on ERCOT data:
- Prophet: 8.2% MAPE
- LSTM: 8.5% MAPE

For production systems, simple + fast wins.

Built a forecasting tool using this approach:
https://powercast.pages.dev

If you're working on similar problems, happy to discuss methodology.
```

---

## Zhihu 回答模板

### 问题："如何预测电力市场价格？"

**回答：**

```
我最近做了一个 ERCOT（德州电力市场）的价格预测工具，分享一下方法和结果。

## 背景

电力价格预测是能源交易、储能运营、电力采购中的核心需求。商业工具（比如 Amperon）
通常收费 $2000-5000/月，但很多团队只需要简单的 7 天预测。

所以我尝试用最简单的方法实现一个可用的预测系统。

## 方法

**模型选择：Prophet（不是 LSTM）**

原因：
1. Prophet 自带季节性处理（日、周、年周期）
2. 对缺失数据鲁棒
3. 可解释性强（可以看到趋势和季节性分量）
4. 训练快（2 分钟 vs LSTM 的 45 分钟）

**数据：**
- 2 年 ERCOT LMP 历史价格（小时级）
- 天气特征（温度、风速、太阳辐射）
- 时间特征（小时、星期、季节）

**结果：**
- 7 天预测准确度：MAPE 8.2%
- 对比 naive baseline（上周同期价格）：提升 39%

## 示例

可以看这个免费的预测样本：https://powercast.pages.dev/sample_report.html

## 适用场景

1. **能源交易员**：提前 7 天预知价格趋势，规划交易策略
2. **储能运营商**：优化充放电时间（低价充电，高价放电）
3. **电力采购**：在价格飙升前锁定合同价格

## 商业化

目前做成了订阅服务（$99/月），每周一自动生成预测报告。

不确定市场需求如何，但至少技术上证明了"简单方法也能达到商业级准确度"。

## 开源

方法论和代码都在这里：https://powercast.pages.dev

如果你也在做类似的预测问题，欢迎交流。
```

---

## Twitter 模板

### 推文 1：Launch 公告

```
Built an ERCOT electricity price forecasting tool in 2.5 hours.

Prophet model, 8.2% MAPE, 7-day ahead predictions.

$99/month vs $2K for Amperon.

Free sample: https://powercast.pages.dev/sample_report.html

If you trade energy or run batteries, this might be useful.
```

---

### 推文 2：免费预测发布

```
Free ERCOT price forecast for Feb 24-Mar 2:

Peak hours: $45-60/MWh
Off-peak: $20-30/MWh

Model: Prophet, 8.2% MAPE

Download CSV: https://powercast.pages.dev/sample_report.html

If you're in energy trading or battery storage, let me know if this
accuracy is useful.
```

---

### 推文 3：Technical Deep Dive

```
Why Prophet > LSTM for electricity forecasting:

1. Handles seasonality (daily/weekly/yearly)
2. Robust to missing data
3. Interpretable (shows why prices rise)
4. Trains in 2 min vs 2 hours

Tested on ERCOT:
- Prophet: 8.2% MAPE
- LSTM: 8.5% MAPE

Simple wins.

Tool: https://powercast.pages.dev
```

---

## 跟进邮件模板

### 跟进 1（3 天后无回复）

**主题：** Re: Quick Q about ERCOT forecasting

**正文：**
```
Hi [Name],

Bumping this in case it got buried.

Happy to share more details about the forecasting approach or send
you a customized sample report if useful.

No pressure — just wanted to follow up once.

Best,
[Your Name]
```

---

### 跟进 2（有回复，但没下一步行动）

**主题：** Re: ERCOT forecasting

**正文：**
```
Hi [Name],

Thanks for the reply!

You mentioned [specific point they raised]. I actually just ran a
quick analysis on this and found [specific insight].

Would you be open to a 10-minute call to discuss your workflow?
I'm trying to understand if this tool actually solves a real problem
or if I'm building the wrong thing.

Let me know if [day/time] works, or suggest another time.

Cheers,
[Your Name]
```

---

### 跟进 3（有人说"有兴趣但现在没时间"）

**主题：** Re: ERCOT forecasting

**正文：**
```
Hi [Name],

No worries — I know you're busy.

I'll send you this week's forecast report anyway (on the house).
If it's useful, great. If not, no problem.

Attached.

Let me know if you have any feedback.

Best,
[Your Name]
```

---

## 社区讨论回复模板

### Reddit/HN 有人质疑准确度

**你的回复：**
```
Great question. 8.2% MAPE means the forecast is off by ~$3-5/MWh on
average (when actual price is $40/MWh).

For context:
- Naive baseline (last week same time) = 13.5% MAPE
- Commercial tools claim 5-7% MAPE (but cost $2K-5K/month)

So this is better than free/naive, but not as good as top-tier commercial.

Question for you: If you're making procurement decisions, is this
accuracy level useful, or do you need <5% to justify paying for it?

Genuinely trying to understand the threshold.
```

---

### Reddit/HN 有人说"我能自己做"

**你的回复：**
```
Absolutely — the tech isn't rocket science. Prophet is open-source,
ERCOT data is free.

The value isn't in the model. It's in:
1. Pre-cleaned data (no missing values, validated)
2. Weekly automatic updates
3. Formatted reports ready to use
4. You don't spend 2 hours/week doing this yourself

If your time is worth $50/hour, spending 2 hours/week = $400/month.
$99/month subscription pays for itself.

But if you're a student/researcher doing this for learning, then yeah —
build it yourself. That's what I did originally.
```

---

### Reddit/HN 有人问"为什么不用 LSTM？"

**你的回复：**
```
I tested both. Results:

Prophet:
- MAPE: 8.2%
- Training time: 2 minutes
- Interpretable (can see trend + seasonality)

LSTM:
- MAPE: 8.5%
- Training time: 45 minutes
- Black box (hard to explain why price is predicted to rise)

For production, Prophet wins on speed + interpretability with minimal
accuracy tradeoff.

LSTM might be better for <5% MAPE, but for $99/month product, Prophet
is good enough.

Happy to share the comparison code if you're curious.
```

---

## 定制化服务邮件模板

### 场景：有人回复冷邮件，问"能不能预测 PJM？"

**你的回复：**
```
Hi [Name],

Great question. PowerCast currently only covers ERCOT, but I can run
a quick PJM forecast for you manually.

Give me 24 hours — I'll pull PJM data, train the model, and send you
a sample report.

If it's useful, I can add PJM to the product. If not, no worries —
just trying to understand what you actually need.

Talk soon,
[Your Name]
```

---

### 场景：有人说"我需要特定节点的预测"

**你的回复：**
```
Hi [Name],

Good point — the current version covers 4 major ERCOT nodes. Which
specific node do you need?

I can generate a custom report with [Node Name] included and send it
to you this week.

If this is useful, I can make it a standard part of the product.

Let me know the node and I'll get it to you.

Best,
[Your Name]
```

---

## 成功标准

每个模板的目标不是"立刻成交"，而是：

1. **开始对话** — 收到真诚的回复（即使是"不感兴趣"）
2. **建立可信度** — 展示专业性和真诚
3. **收集反馈** — 了解真实需求是什么

**如果 20 封邮件发出，有 4 个人回复（任何形式的回复），这就是成功。**

**如果 Reddit 帖子有 10 个评论（即使是批评），这就是成功。**

**如果有 1 个人说"这个看起来有用，我想试试"，这就是巨大成功。**

---

现在去发第一封邮件。
