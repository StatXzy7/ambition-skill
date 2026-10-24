<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
    <img src="assets/banner-light.svg" alt="Ambition：把提示词往更高、更深、更广改写，每一个激进目标都配上冻结的外部验证器" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/StatXzy7/ambition-skill/actions/workflows/validate.yml"><img src="https://github.com/StatXzy7/ambition-skill/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/StatXzy7/ambition-skill/releases"><img src="https://img.shields.io/github/v/release/StatXzy7/ambition-skill?color=E0561B&label=release" alt="release"></a>
  <a href="skills/ambition/references/patterns.md"><img src="https://img.shields.io/badge/patterns-25-E0561B" alt="25 个模式"></a>
  <a href="https://code.claude.com/docs/en/skills"><img src="https://img.shields.io/badge/Claude%20Code-skill-D97757?logo=claude&logoColor=white" alt="Claude Code skill"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-24292f" alt="Apache-2.0"></a>
</p>

<p align="center"><b>简体中文</b> · <a href="README.en.md">English</a></p>

<p align="center">
  <a href="#快速开始">快速开始</a> ·
  <a href="#用法">用法</a> ·
  <a href="#它怎么工作">工作原理</a> ·
  <a href="#一个例子">例子</a> ·
  <a href="#模式库">模式库</a> ·
  <a href="#常见问题">常见问题</a>
</p>

<br>

给模型下任务时，人们通常问得太少：任务写成一个名词（"做一份 PPT"），给的是消化过的摘要，最后还让模型自己评价自己。

**Ambition** 是一个 Claude Code 技能。你把准备发出去的提示词交给它，它从高度、深度、广度三个方向把任务往上拉。凡是抬高了目标的地方，它都会同时冻结验证器、写明禁止项。

| | 常见写法 | Ambition 往哪拉 |
| --- | --- | --- |
| **高度** | "做一份 PPT""修这个函数" | 追问目标背后的目标：做完之后，你希望接着发生什么 |
| **深度** | 只给摘要，目标定得保守 | 给原始材料，点名专家真正用的工具，目标定得激进 |
| **广度** | 只在本领域里找办法 | 借用长期在解决同一个动词的其他领域的方法 |
| **验证** | 让模型自己说"完成了" | 冻结验证器、阈值和计时口径，写明不许做的事 |

> [!IMPORTANT]
> 模型被逼紧时，最省事的"达成"方式是悄悄改尺子：放宽阈值、换计时口径、只挑有利的样本。所以 Ambition 在哪里抬高目标，就在哪里把尺子锁死。对外则反过来：给合作方看的数字，一律用同口径、带限定的版本。

## 快速开始

**Claude Code 插件（推荐）**

```text
/plugin install ambition --marketplace StatXzy7/ambition-skill
```

Claude Code 2.1.275 之前的版本分两步装：

```text
/plugin marketplace add StatXzy7/ambition-skill
/plugin install ambition@ambition-skill
```

<details>
<summary><b>其他安装方式</b></summary>

<br>

**npx skills**：用 [vercel-labs/skills](https://github.com/vercel-labs/skills) 命令行安装，可以装到 Claude Code，也可以装到其他支持 Agent Skills 的工具。

```bash
npx skills add StatXzy7/ambition-skill
```

**手动复制**：适合打算用 `add`、`note` 长期扩充自己模式库的人。

```bash
git clone https://github.com/StatXzy7/ambition-skill.git
mkdir -p ~/.claude/skills
cp -r ambition-skill/skills/ambition ~/.claude/skills/
```

如果已经有一个叫 `ambition` 的技能，先看一下再决定是否覆盖。

</details>

装好以后，直接说"帮我改写这个提示词"就能用。想让改写结果直接引用你项目里的真实脚本和路径，再花几分钟填一份 [`contexts.md`](#让它认识你的项目)。

## 用法

| 命令 | 作用 |
| --- | --- |
| `/ambition <原始提示词>` | 诊断并改写这条提示词 |
| `/ambition` | 不带参数时，改写你在对话里刚描述的任务 |
| `/ambition list [关键词]` | 列出模式菜单，例如 `list 验证` |
| `/ambition add <内容>` | 把一句提示词、一段文章或一次好用的经历提炼成新模式 |
| `/ambition note <ID> <效果>` | 记录某个模式的实战效果，例如 `note D2 2026-10-25｜性能优化｜好｜…` |

通过插件安装时，命令带插件前缀，写作 `/ambition:ambition`；如果没有别的命令占用这个名字，直接打 `/ambition` 也可以。不用命令也行，说"这个 prompt 怎么写更好""帮我把这个任务想得更高一点"都会触发。

每次改写都按同一个结构输出：

1. **诊断**：两三句话，说明原提示词最缺什么。
2. **用到的模式**：每个一行，说明为什么用它。
3. **改写后的提示词**：一个可以直接复制的代码块。
4. **需要你定的**：最多三项，只列只有你能决定的事，例如目标数字、谁拍板。
5. **下一步**：问你要不要直接按改写后的提示词执行。

## 它怎么工作

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/workflow-dark.svg">
    <img src="assets/workflow-light.svg" alt="五步改写流程：读任务、诊断、取材、选模式、改写；输出诊断、用到的模式、改写后的提示词、需要你定的、下一步；执行后用 note 回收效果" width="100%">
  </picture>
</p>

- **读任务**：判断任务类型和大小。改名、修一个已定位的 bug 这类小任务，只配一条"改动前后行为不变"的检查，改写后不超过 15 行。
- **诊断**：从高度、深度、验证、广度四个问题里，找出最弱的一两处，不需要每一处都改。
- **取材**：花几分钟在工作目录里找真东西：验收脚本、冻结的基线、原始数据、以前的报告。路径和数字都从文件里读，读不到就写成 `{需要你填：…}`，不编。
- **选模式**：按短板挑 2–4 个模式。全部叠上去，提示词会又长又散，关键的那条要求反而被淹没。
- **改写**：激进目标只用于内部工作，而且同一个提示词里必须同时写上冻结项和禁止项。

## 一个例子

> 下周和合作方开会，帮我做一份 PPT 介绍我们项目的进展，希望他们继续合作。

改写后（节选，用到 R1、H3、V3）：

```text
任务：在 {30 分钟} 的会上，让 {合作方的技术负责人}
相信 {我们的实现在他们关心的用例上可用}，同意 {提供下一批实测数据}，
并在结束前定下 {交付日期和验收方式}。
先回答：要让他们做到这些，他们必须先相信哪几件事？
每件事最有说服力的证据是什么（优先选他们自己能复现的）？
会议以决策收尾：列出最该推动的三个决策，每个给出可选方案、对双方的利弊、
我们希望对方选哪个，以及为什么这个选项对他们也是最优的。
证据审计：材料里的每个数字都要能追到文件、提交号或脚本，
带上验证范围和对比口径；找不到出处的标"无出处"。
然后再决定 PPT 的形式和篇幅。越短越好。
{需要你填：合作方是谁、今年要交付什么。}
```

| 改写里的这一句 | 来自 |
| --- | --- |
| 在 30 分钟的会上，让谁相信什么、同意什么 | `R1` 名词换成动词 |
| 他们必须先相信哪几件事，再决定形式和篇幅 | `R1` 名词换成动词 |
| 会议以决策收尾，每个决策附双方的利弊 | `H3` 会议以决策收尾 |
| 每个数字都能追到出处，带上口径 | `V3` 证据审计 |
| `{需要你填：…}` | 改写规则：不确定的事实不编，留给你填 |

## 模式库

25 个模式分成 7 组。每个模式都写明什么时候用、什么时候别用、模板，以及最常见的失败方式。完整内容见 [`patterns.md`](skills/ambition/references/patterns.md)。

| 组 | 模式 | 举例 |
| --- | --- | --- |
| **H** 高度 | H1–H5 | `H3` 会议以决策收尾：找出最紧迫的三个决策，各附双方的利弊 |
| **D** 深度 | D1–D6 | `D2` 激进目标加冻结验证器：定 10 倍目标，同时锁死尺子和口径 |
| **V** 验证 | V1–V3 | `V1` 验证器先证明自己会失败：植入已知错误，全部抓住才算数 |
| **R** 广度 | R1–R4 | `R1` 名词换成动词："做 PPT"改成"在 30 分钟内让谁相信什么、决定什么" |
| **P** 合作方 | P1–P2 | `P1` 还原对方处境：从公开的原始材料还原合作方的目标、卡点和担心 |
| **S** 选题 | S1 | `S1` 选题五问：验证分级、前沿、不公平优势、止损条件、极致版本 |
| **F** 追问 | F1–F4 | `F2` 自我设限检查：最近几轮是不是一直停在安全区 |

不同类型任务的常见起点：

| 任务 | 常见起点 |
| --- | --- |
| 工程实现与优化 | `H2` · `D2` · `V1` · `D4` |
| 选题与调研 | `S1` · `H5` · `D6` · `R4` |
| 对外沟通 | `R1` · `H3` · `P1` · `V3` |
| 分析与决策 | `H1` · `D4` · `D5` · `V2` |

<details>
<summary><b>展开全部 25 个模式</b></summary>

<br>

| ID | 名字 | 一句话 |
| --- | --- | --- |
| H1 | 目标背后的目标 | 一直问"然后呢"，直到碰到真正想要的结果 |
| H2 | 从修一个到保持一个性质 | 不只修一个问题，而是让某个性质始终成立，并由模型来维护 |
| H3 | 会议以决策收尾 | 找出最紧迫的三个决策，各附正反理由 |
| H4 | 换掉机制本身 | 设计比现有流程更好的机制，用历史数据回测，再并行跑一段时间 |
| H5 | 从极致成功倒推 | 先写出 6 个月后最好的产出，再倒推第一周做什么 |
| D1 | 改深元提示词 | 先回答五个问题，再改写我的提示词 |
| D2 | 激进目标加冻结验证器 | 定 10 倍目标，同时锁死尺子和口径 |
| D3 | 把"做不到"拆成假设 | 把"不可能"拆成真下限和惯性两类，逐条做实验 |
| D4 | 从原始数据推翻已有结论 | 不复述结论，而是复现或推翻它；等价不等于正确 |
| D5 | 找新东西 | 问什么事现在新变得可能；新信号要在没见过的数据上验证 |
| D6 | 用专家的工具，不用专家的词 | 先点名具体的库、求解器、统计模型，再动手 |
| V1 | 验证器先证明自己会失败 | 植入已知错误，全部抓住才算数 |
| V2 | 独立审查 | 让没参与开发的 agent 专门找不成立的结论 |
| V3 | 证据审计 | 每个数字和断言都要有出处、带限定、给判定 |
| R1 | 名词换成动词 | "做 PPT"改成"在 30 分钟内让谁相信什么、决定什么" |
| R2 | 借别的领域的方法 | 找长期在解决同一个动词的领域，借它的方法，不借角色 |
| R3 | 尽调式审查 | 用尽职调查的方法，列出对方会查的地方和能当场做的复现实验 |
| R4 | 多视角并行 | 子 agent 各自带一个学科的方法，并给定搜索预算 |
| P1 | 还原对方处境 | 从公开的原始材料还原合作方的目标、卡点和担心 |
| P2 | 会后变成承诺 | 整理出承诺、日期、验收方式，以及对方没说出口的顾虑 |
| S1 | 选题五问 | 验证分级、前沿、不公平优势、止损条件、极致版本 |
| F1 | 要一个更好的 | 用同一个验证器、不改阈值，扩到更难的情形 |
| F2 | 自我设限检查 | 检查最近几轮是不是一直停在安全区 |
| F3 | 资源乘十 | 资源多 10 倍会改做什么，在现有资源下它最小的版本是什么 |
| F4 | 下一个问题 | 做完之后最自然的下一个问题是什么，能不能抢先 |

</details>

## 让它认识你的项目

不做任何配置也能用，只是改写结果里本该填你的真实脚本和路径的地方，会留成 `{需要你填：…}`。想让它直接引用真东西，就把自带的[模板](skills/ambition/references/contexts.md)复制一份，登记你的验证器、原始材料、对外口径和工作区规矩：

```bash
mkdir -p ~/.claude/ambition
curl -fsSL https://raw.githubusercontent.com/StatXzy7/ambition-skill/main/skills/ambition/references/contexts.md \
  -o ~/.claude/ambition/contexts.md
```

技能按这个顺序找 `contexts.md`，用第一个找到的：

1. 当前项目的 `.claude/ambition/contexts.md`：只对这个项目生效；
2. `~/.claude/ambition/contexts.md`：对你所有的项目生效；
3. 技能自带的空白模板。

前两份是你自己的文件，升级技能时不会被覆盖。填好的样子见 [`examples/contexts.example.md`](examples/contexts.example.md)（虚构项目）。

## 仓库结构

```text
skills/ambition/
├── SKILL.md                  改写流程、参数分派、list / add / note
├── references/patterns.md    菜单、通用骨架、25 个模式、反模式、变更记录
├── references/contexts.md    登记验证器、材料和口径的空白模板
└── evals/                    4 个测试用例和夹具文件
examples/contexts.example.md  填好的 contexts 示例（虚构）
scripts/validate.py           仓库校验，带植入错误的自测
.claude-plugin/               Claude Code 插件市场清单
```

## 常见问题

<details>
<summary><b>这和直接让模型"把提示词写好一点"有什么不同？</b></summary>

<br>

有两点不同。第一，每个模式都来自实际用过的做法，并且写明了什么时候别用，所以模型不会把所有招数都往上叠。第二，有一条硬约束：抬高目标的地方，同一个提示词里必须写上冻结的验证器和禁止项。没有这条，激进目标换来的往往是一次"改了尺子"的达成。

</details>

<details>
<summary><b>小任务会不会被写成长篇大论？</b></summary>

<br>

不会。改名、修一个已定位的 bug 这类任务只用一个模式，改写后不超过 15 行，不派子 agent，也不跑循环。测试用例里专门有一条检查这一点。

</details>

<details>
<summary><b>我手里还没有验证器怎么办？</b></summary>

<br>

先用 `V1`：在写解法之前先写验证器，再往一个正确的实现里植入几种已知错误，验证器全部抓住才算数。在有被证明过的验证器之前，不要定激进目标。

</details>

<details>
<summary><b>它会不会编造我的脚本路径或合作方信息？</b></summary>

<br>

改写规则要求路径和数字都从工作目录或 `contexts.md` 里读，并注明出处；读不到的写成 `{需要你填：…}`。合作方是谁、关心什么这类事实，它只会留空等你填。

</details>

<details>
<summary><b>能用英文吗？</b></summary>

<br>

能。技能的说明和模板是中文写的，但改写后的提示词使用你提问时用的语言。

</details>

<details>
<summary><b>用插件安装以后，用 add / note 改过的模式会不会丢？</b></summary>

<br>

会。插件更新时会覆盖技能目录，`patterns.md` 里的改动也在其中。如果打算长期扩充自己的模式库，建议 fork 这个仓库后手动安装；你的 `contexts.md` 放在 `~/.claude/ambition/` 下，不受影响。

</details>

## 来源与局限

模式改写自 Felix Rieseberg 的 [How to be more ambitious: A tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/)、Matthew D. Schwartz 的 [Claude-shaped science](https://www.anthropic.com/research/claude-shaped-science) 和 [BootLoops 协议](https://github.com/BootLoops-ai/skills)，再加上作者在科学软件移植、求解器优化和合作方会议准备中的实践。仓库里不包含原文，署名见 [NOTICE](NOTICE)。

关于这个技能有没有用，目前证据还很少。在作者私有项目的 4 个测试用例上，用技能的回答达成了 28 条期望中的 27 条，不用技能的达成 22 条。这只是一次小规模测试，期望也是作者自己写的。本仓库里的 4 个用例是那次测试的通用改写版，还没有按改写后的版本重新跑过。

提示词写得再好，也不能保证结果就对。让结果可信的是冻结的验证器；技能只能要求你准备一个，不能替你造出来，也不能替你检查。

## 参与贡献

欢迎提交新模式、实战反馈和问题。新模式请用 [issue 模板](https://github.com/StatXzy7/ambition-skill/issues/new/choose)，附上一个它真正改善过的提示词。提交 PR 之前，运行 `python3 scripts/validate.py`。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

原创的说明、模板和文档以 [Apache-2.0](LICENSE) 许可发布。这个许可不涉及来源文章的权利，署名见 [NOTICE](NOTICE)。

<br>

<p align="center">
  <img src="assets/logo.svg" width="44" alt="">
  <br>
  <sub>如果它帮你把某个任务想得更高了，欢迎点一个 Star。</sub>
</p>
