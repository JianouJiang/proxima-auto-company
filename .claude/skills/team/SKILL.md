---
name: team
description: "根据任务快速组建临时 AI Agent 团队协作。自动从 .claude/agents/ 中选择最合适的成员组队。"
argument-hint: "[任务描述]"
disable-model-invocation: true
---

# 组建临时团队

你需要根据下面的任务，从公司现有的 AI Agent 中挑选最合适的成员，组建一支临时团队来协作完成。

## 任务

$ARGUMENTS

## 可用 Agent

以下是公司所有 Agent，定义在 `.claude/agents/` 目录下：

| Agent | 文件 | 职能 |
|-------|------|------|
| CEO | `ceo-bezos` | 战略决策、商业模式、PR/FAQ、优先级 |
| CTO | `cto-vogels` | 技术架构、技术选型、系统设计 |
| 逆向思考 | `critic-munger` | 质疑决策、识别致命缺陷、Pre-Mortem、防止集体幻觉 |
| 产品设计 | `product-norman` | 产品定义、用户体验、可用性 |
| UI 设计 | `ui-duarte` | 视觉设计、设计系统、配色排版 |
| 交互设计 | `interaction-cooper` | 用户流程、Persona、交互模式 |
| 全栈开发 | `fullstack-dhh` | 代码实现、技术方案、开发 |
| QA | `qa-bach` | 测试策略、质量把控、Bug 分析 |
| DevOps/SRE | `devops-hightower` | 部署流水线、CI/CD、基础设施、监控运维 |
| 营销 | `marketing-godin` | 定位、品牌、获客、内容 |
| 运营 | `operations-pg` | 用户运营、增长、社区、PMF |
| 销售 | `sales-ross` | 销售漏斗、转化策略 |
| CFO | `cfo-campbell` | 定价策略、财务模型、成本控制、单位经济 |
| 调研分析 | `research-thompson` | 市场调研、竞品分析、行业趋势、机会发现 |
| 编年记录 | `editor-chronicler` | 记录工作、每日报告、邮件摘要、编年史 |

## 执行步骤

### 1. 分析任务，选择成员

根据任务性质，选择 2-5 个最相关的 Agent 作为团队成员。选人原则：
- **只选必要的**：不是人越多越好，精准匹配任务需求
- **考虑协作链**：如果任务涉及从设计到开发，确保链路上的关键角色都在
- **避免冗余**：职能重叠的不要同时选

向创始人简要说明你选了谁、为什么选他们，然后立即开始组建。

### 2. 组建 Agent Team（串行执行，节省 Token）

⚠️ **重要：Agent 必须串行执行，不要并行 spawn 多个 agent！** 并行运行 14 个 agent 会消耗大量 token。

执行方式：
- 创建团队，team_name 基于任务简短命名（英文、kebab-case）
- 为每个成员创建具体的任务（TaskCreate），任务描述要包含足够上下文
- 用 Task 工具 **逐个（串行）** spawn teammate，`subagent_type` 选 `general-purpose`，在 prompt 中注入对应 agent 文件的完整内容作为角色设定
- **一个 agent 完成后再 spawn 下一个**，这样后续 agent 可以看到前面 agent 的产出
- spawn teammate 时通过 prompt 告知：你的角色设定、要完成的任务、产出文档存放在 `docs/<role>/` 目录下

### 2b. 模型分级使用（节省成本）

不是每个 agent 都需要最贵的模型。按角色分级：

| 模型等级 | Agent | 理由 |
|---------|-------|------|
| **opus**（仅战略决策） | `ceo-bezos`, `critic-munger` | 需要深度推理和判断 |
| **sonnet**（大部分工作） | `cto-vogels`, `product-norman`, `fullstack-dhh`, `research-thompson`, `cfo-campbell`, `editor-chronicler` | 需要较好的推理能力但不需要最强 |
| **haiku**（简单任务） | `qa-bach`, `devops-hightower`, `ui-duarte`, `interaction-cooper`, `marketing-godin`, `operations-pg`, `sales-ross` | 执行性任务，按照明确指令操作 |

spawn teammate 时在 prompt 中指定建议模型：
- 使用 `model: "opus"` 参数 spawn 战略 agent
- 使用 `model: "sonnet"` 参数 spawn 中层 agent
- 使用 `model: "haiku"` 参数 spawn 执行 agent

### 3. 协调与汇总

- 作为 team lead 协调各成员工作
- 收集各成员产出，汇总为统一的结论或方案
- 如有分歧，列出各方观点供创始人决策
- 完成后清理团队资源

## 注意事项

- 所有沟通使用中文，技术术语保留英文
- 每个成员产出的文档按约定存放在 `docs/<role>/` 下
- 团队是临时的，任务完成后即解散
- 创始人是最终决策者，Agent 提供建议但不替代决策
