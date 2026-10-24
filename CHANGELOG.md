# 更新日志

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。模式库自身的逐条变更记在 [`patterns.md`](skills/ambition/references/patterns.md) 末尾的"变更记录"里。

## [1.0.0] - 2026-10-25

首个公开版本。

### 新增

- `ambition` 技能：五步改写流程，以及 `list`、`add`、`note` 三个命令。
- 25 个提示词模式，分为高度、深度、验证、广度、合作方、选题、追问七组。每个模式都写明什么时候用、什么时候别用、模板和常见失败。
- 使用者语境：按"项目 `.claude/ambition/` → `~/.claude/ambition/` → 自带模板"的顺序查找 `contexts.md`，你自己填的文件不会在升级时被覆盖。附一份虚构的填写示例。
- 4 个测试用例和小任务夹具 `compare.py`。
- Claude Code 插件市场清单，支持 `/plugin install`。
- `scripts/validate.py`：检查技能元数据、模式菜单与正文是否一致、README 和横幅里的模式数、测试用例、插件清单、相对链接，以及技能目录里有没有邮箱和本机路径；`--self-test` 会植入 12 种已知错误，要求全部抓住。
- 中英文 README、横幅、流程图和社交预览图，issue 与 PR 模板，GitHub Actions 校验。

[1.0.0]: https://github.com/StatXzy7/ambition-skill/releases/tag/v1.0.0
