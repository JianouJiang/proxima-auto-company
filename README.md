# Auto Company

一个 24/7 自主运行的 AI 公司。14 个 AI Agent 组成完整团队，自主构思产品、做出决策、编写代码、部署上线。人类只需要观察和偶尔引导方向。

## 原理

```
launchd (崩溃自重启)
  └── auto-loop.sh (永续循环)
        ├── 读 PROMPT.md + consensus.md
        ├── claude -p (驱动一个工作周期)
        │   ├── 读 CLAUDE.md (公司章程 + 安全红线)
        │   ├── 读 .claude/skills/team/SKILL.md (组队方法)
        │   ├── 组建 Agent Team (3-5 人)
        │   ├── 执行任务，产出文档/代码/部署
        │   └── 更新 memories/consensus.md (传递接力棒)
        ├── 失败处理: 限额等待 / 熔断保护 / consensus 回滚
        └── sleep → 下一轮
```

每个周期是一次独立的 `claude -p` 调用。`memories/consensus.md` 是唯一的跨周期状态——记录了上次做了什么、下次做什么。类似接力赛传棒。

## 快速开始

```bash
# 前提: 已安装 Claude Code CLI 并登录
# https://docs.anthropic.com/en/docs/claude-code

# 前台运行 (可直接看输出)
make start

# 或者安装为守护进程 (开机自启 + 崩溃自重启)
make install
```

## 常用命令

```bash
make help       # 查看所有命令
make start      # 前台启动循环
make stop       # 停止循环
make status     # 查看状态 + 最新共识
make monitor    # 实时日志
make last       # 上一轮完整输出
make cycles     # 历史周期摘要
make install    # 安装 launchd 守护进程
make uninstall  # 卸载守护进程
make pause      # 暂停守护 (不自动拉起)
make resume     # 恢复守护
```

## 团队阵容 (14 人)

### 战略层

| 角色 | 专家 | 职能 |
|------|------|------|
| CEO | Jeff Bezos | 战略决策、PR/FAQ、飞轮效应 |
| CTO | Werner Vogels | 技术架构、API First、为失败而设计 |
| 逆向思考 | Charlie Munger | 质疑一切、Pre-Mortem、防集体幻觉 |

### 产品层

| 角色 | 专家 | 职能 |
|------|------|------|
| 产品设计 | Don Norman | 用户体验、可供性、以人为本 |
| UI 设计 | Matias Duarte | 视觉语言、Material Design |
| 交互设计 | Alan Cooper | 用户流程、Goal-Directed Design |

### 工程层

| 角色 | 专家 | 职能 |
|------|------|------|
| 全栈开发 | DHH | 代码实现、Majestic Monolith |
| QA | James Bach | 探索性测试、质量把控 |
| DevOps/SRE | Kelsey Hightower | 部署、CI/CD、监控运维 |

### 商业层

| 角色 | 专家 | 职能 |
|------|------|------|
| 营销 | Seth Godin | 紫牛、许可营销、最小可行受众 |
| 运营 | Paul Graham | Do Things That Don't Scale、PMF |
| 销售 | Aaron Ross | 可预测收入、销售漏斗 |
| CFO | Patrick Campbell | 定价策略、单位经济学 |

### 情报层

| 角色 | 专家 | 职能 |
|------|------|------|
| 调研分析 | Ben Thompson | 市场调研、Aggregation Theory |

## 项目结构

```
auto-company/
├── CLAUDE.md                  # 公司章程 (使命 + 安全红线 + 团队 + 流程)
├── PROMPT.md                  # 每轮工作指令 (周期逻辑 + 收敛规则)
├── Makefile                   # 常用命令
├── auto-loop.sh               # 主循环脚本
├── stop-loop.sh               # 停止 / 暂停 / 恢复
├── monitor.sh                 # 监控面板
├── install-daemon.sh          # launchd 安装/卸载
├── memories/
│   └── consensus.md           # 共识记忆 (跨周期接力棒)
├── docs/                      # Agent 产出
│   ├── ceo/                   # CEO 的文档 (PR/FAQ, 战略备忘录)
│   ├── cto/                   # CTO 的文档 (ADR, 系统设计)
│   ├── critic/                # 逆向分析报告
│   ├── research/              # 市场调研, 竞品分析
│   ├── product/               # 产品 spec, 用户画像
│   ├── ui/                    # 设计系统, 视觉规范
│   ├── interaction/           # 交互流程, Persona
│   ├── fullstack/             # 技术方案, 代码文档
│   ├── qa/                    # 测试策略, Bug 报告
│   ├── devops/                # 部署配置, Runbook
│   ├── marketing/             # 定位, 内容策略
│   ├── operations/            # 增长实验, 指标
│   ├── sales/                 # 销售漏斗, 转化分析
│   └── cfo/                   # 财务模型, 定价分析
├── projects/                  # 所有新建项目的工作空间
├── logs/                      # 循环日志
└── .claude/
    ├── agents/                # 14 个 Agent 定义
    ├── skills/team/SKILL.md   # 团队编排技能
    └── settings.json          # 权限 + Agent Teams 开关
```

## 工作流程

### 自动收敛 (防止无限讨论)

| 周期 | 动作 |
|------|------|
| Cycle 1 | Brainstorm，每个 agent 提一个想法，排出 top 3 |
| Cycle 2 | 选 #1，Munger 做 Pre-Mortem，Thompson 验证市场，Campbell 算账 → GO / NO-GO |
| Cycle 3+ | GO → 建 repo 写代码。NO-GO → 试下一个。纯讨论禁止 |

### 六大标准流程

1. **新产品评估**: 调研 → CEO → Munger审查 → 产品 → CTO → CFO
2. **功能开发**: 交互 → UI → 全栈 → QA → DevOps
3. **产品发布**: QA → DevOps → 营销 → 销售 → 运营 → CEO
4. **定价变现**: 调研 → CFO → 销售 → Munger → CEO
5. **每周复盘**: 运营 → 销售 → CFO → QA → CEO
6. **机会发现**: 调研 → CEO → Munger → CFO

## 安全红线

以下操作**绝对禁止**，写入 CLAUDE.md 对所有 Agent 生效:

- 不得删除 GitHub 仓库 (`gh repo delete`)
- 不得删除 Cloudflare 项目 (`wrangler delete`)
- 不得删除系统文件 (`rm -rf /`, `~/.ssh/` 等)
- 不得进行非法活动
- 不得泄露凭证到公开仓库
- 不得 force push 到 main/master
- 所有新项目必须在 `projects/` 目录下创建

## 配置

环境变量覆盖，在启动时传入:

```bash
MODEL=sonnet ./auto-loop.sh                  # 换模型
LOOP_INTERVAL=60 ./auto-loop.sh              # 60秒间隔
CYCLE_TIMEOUT_SECONDS=3600 ./auto-loop.sh    # 1小时超时
MAX_CONSECUTIVE_ERRORS=3 ./auto-loop.sh      # 3次错误熔断
```

## 如何引导方向

AI 团队自主运行，但你可以随时介入:

1. **修改 `memories/consensus.md` 的 "Next Action"** — 下一轮会按你的指示行动
2. **`make pause`** — 暂停循环，手动 `claude` 进入交互模式沟通
3. **`make resume`** — 恢复自主运行
4. **查看 `docs/*/`** — 审查各 Agent 的产出

## 依赖

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) (已登录)
- macOS (launchd 守护进程，Linux 需改用 systemd)
- `jq` (可选，用于解析 JSON 日志)
- `gh` (可选，GitHub CLI)
- `wrangler` (可选，Cloudflare CLI)

## License

MIT
