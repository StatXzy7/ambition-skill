# 参与贡献

感谢你愿意让这个模式库变得更好。最有价值的贡献有三种：一个真正改善过结果的新模式、某个模式的实战反馈，以及技能表现不对的问题报告。

English speakers: issues and pull requests in English are welcome. The skill's own instructions are kept in Chinese, so a maintainer may translate your pattern when merging it.

## 提一个新模式

先开一个 [新模式 issue](https://github.com/StatXzy7/ambition-skill/issues/new?template=new-pattern.yml) 讨论，再提 PR。一个好的模式需要：

- **一个真实的例子**：原来的提示词、用了这个模式之后的提示词，以及结果有什么变化。只有"听起来有道理"的模式，我们不收。
- **用和别用**：什么情况下该用它，什么情况下用了反而有害。
- **常见失败**：模型或人用这个模式时，最常见的走偏方式。

合并之前会查重。和已有模式重叠过半的，会合并进已有条目，比如补一个模板变体或一条实战记录，不另开新条目。

## 写进模式库

按 [`patterns.md`](skills/ambition/references/patterns.md) 里的"条目格式"写，并同时改三处：

1. 菜单表加一行；
2. 对应维度下加正文条目，标题写成 `### <ID> <名字>`，名字和菜单里的一字不差；
3. 文末"变更记录"加一行，写明日期和做了什么。

新 ID 取"维度字母 + 下一个序号"。已废弃的 ID 不复用。

如果模式总数变了，同步更新两份 README 里的 `patterns-N` 徽章和模式列表，以及 `assets/banner-*.svg` 里的"N 个提示词模式"。校验脚本会检查这几处是否一致。

## 反馈实战效果

用 [实战反馈 issue](https://github.com/StatXzy7/ambition-skill/issues/new?template=pattern-feedback.yml)，格式和技能里的 `note` 一样：日期、场景、好 / 一般 / 差、原因。某个模式连续两次反馈为"差"，我们会考虑修改或废弃它。

## 提交之前

```bash
python3 scripts/validate.py              # 检查仓库
python3 scripts/validate.py --self-test  # 植入已知错误，确认检查全部会失败
```

如果你新增了一项检查，请在 `PLANTED` 里补一个对应的植入错误：从来没失败过的检查不算检查（模式 V1）。

## 隐私

技能目录和示例里不要出现真实的项目名、本机路径、合作方信息、未发表的数字、邮箱或凭据。示例请用明显虚构的名字，并标明"虚构"。校验脚本会拦下邮箱地址和 `/Users/…`、`/home/…` 这类路径，其余的需要你自己检查。

## 许可

提交贡献即表示你同意按 [Apache-2.0](LICENSE) 许可发布你的贡献。
