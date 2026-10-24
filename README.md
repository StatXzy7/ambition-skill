# Ambition

[中文说明](README.zh-CN.md)

A prompt-rewriting skill for Claude Code. Give it the task description you were about to send, and it rewrites it to aim **higher, deeper, and wider**, while pairing every aggressive goal with a **frozen external verifier**.

- **Altitude**: ask for the goal behind the goal, not the noun ("a deck") or the action ("fix this function").
- **Depth**: hand the model raw material instead of your summary, name the tools an expert would actually use, and set a target that is uncomfortably high.
- **Breadth**: borrow methods from fields that have been solving the same verb for a long time.

The constraint that comes with this: when a model is pushed hard, the cheapest way to "succeed" is to quietly change the ruler: loosen a threshold, switch the timing baseline, keep only the favourable samples. So wherever the rewritten prompt raises the bar, it also freezes the validator and lists what is forbidden. A second rule: be aggressive in the work and conservative in what you tell others. Numbers in partner-facing material are always quoted like-for-like and with their qualifiers.

The instructions and templates are in Chinese. The skill writes the rewritten prompt in whatever language you use.

## What it contains

- A rewrite workflow: classify the task, diagnose the one or two weakest dimensions, pull real paths and scripts from your working directory, pick 2–4 patterns, and return a copy-ready prompt.
- A library of 25 patterns in seven groups, each with when to use it, when not to, a template, and its most common failure.
- A universal skeleton for task prompts (verb-form task, target, reference case, raw material, method, frozen validation, forbidden moves, definition of done, what to hand back on failure).
- A `contexts.md` template where you register your own validators, raw material, partner rules, and workspace caveats, so rewrites can cite real files instead of placeholders.
- Commands to list the menu, add a pattern, and log how a pattern worked in practice.

| Group | Patterns | Example |
| --- | --- | --- |
| H Altitude | H1–H5 | H3: end every meeting with three decisions, each with pros and cons for both sides |
| D Depth | D1–D6 | D2: a 10x target with the validator, threshold, and timing script locked |
| V Verification | V1–V3 | V1: plant known bugs; the validator counts only after it catches all of them |
| R Breadth | R1–R4 | R1: replace "make a deck" with "in 30 minutes, get whom to believe and decide what" |
| P Partners | P1–P2 | P1: reconstruct the partner's situation from public primary sources |
| S Topic selection | S1 | S1: verification tier, frontier, unfair advantage, stop condition, extreme version |
| F Follow-ups | F1–F4 | F2: check whether the last few rounds stayed in the safe zone |

Small tasks stay small: a rename or a localized bug fix gets one pattern, usually a "behaviour unchanged before and after" check, and at most 15 lines.

## Install in Claude Code

Clone the repository and copy the skill directory into your personal skills folder:

```bash
git clone https://github.com/StatXzy7/ambition-skill.git
mkdir -p ~/.claude/skills
cp -r ambition-skill/skills/ambition ~/.claude/skills/
```

To share it with a project instead, copy it into that project's `.claude/skills/`. If you already have a skill named `ambition`, inspect it before replacing it.

Then fill in `~/.claude/skills/ambition/references/contexts.md` with your own projects. See [examples/contexts.example.md](examples/contexts.example.md) for a filled-in fictional example. The skill works without it, but rewrites will then leave `{需要你填：…}` placeholders where your real scripts and paths would go.

## Use

```text
/ambition 下周和合作方开会，帮我做一份 PPT 介绍我们项目的进展
/ambition list
/ambition list 验证
/ambition add <a prompt, an article excerpt, or something that worked>
/ambition note D2 <date | scenario | good/ok/bad | why>
```

It also triggers on plain requests such as "rewrite this prompt", "how should I ask Claude this", or "help me think bigger about this task".

The output has five parts: a two-sentence diagnosis, the patterns used and why, the rewritten prompt in one code block, at most three decisions only you can make, and an offer to run it.

### Example (abridged)

Original: "Next week we meet a partner. Make a deck on our progress; we want them to keep working with us."

Rewritten (R1, H3, V3, P1):

```text
Task: in a {30-minute} meeting, get {the partner's technical lead} to believe
{our implementation works on the cases they care about}, agree to {provide the
next batch of measured data}, and leave with {a delivery date and acceptance
test}.
First answer: what must they believe before they will do that? What is the most
convincing evidence for each, preferably something they can reproduce?
End with decisions: the three decisions this meeting should drive, each with the
options, pros and cons for both sides, the one we want, and why it is also best
for them.
Evidence audit: every number traces to a file, commit, or script, with its
validation scope and comparison basis; mark anything without a source.
Only then choose the format and length. Shorter is better.
{Fill in: who the partner is and what they must deliver this year.}
```

## Files

```text
skills/ambition/
├── SKILL.md                  Workflow, argument dispatch, list/add/note
├── references/patterns.md    Menu, skeleton, 25 patterns, anti-patterns, changelog
├── references/contexts.md    Template for your validators, materials, and rules
├── evals/evals.json          Four test prompts with checkable expectations
└── evals/files/compare.py    Fixture for the small-task eval
examples/contexts.example.md  A filled-in, fictional contexts file
```

## Inspiration and limits

The patterns adapt ideas from Felix Rieseberg's [How to be more ambitious: A tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/), Matthew D. Schwartz's [Claude-shaped science](https://www.anthropic.com/research/claude-shaped-science), and the [BootLoops protocols](https://github.com/BootLoops-ai/skills), plus the author's own practice porting scientific software, optimizing solvers, and preparing partner meetings. The source articles are not distributed here. See [NOTICE](NOTICE).

Evidence that the skill helps is thin. On four test cases from the author's private projects, responses with the skill met 27 of 28 expectations versus 22 of 28 without it. That is one small run, graded against expectations the author wrote. The evals in this repository are generic rewrites of those cases and have not been re-run in this form.

A stronger prompt does not make a result correct. The frozen validator is what does, and the skill can only ask for one; it cannot build or check it for you.

## Contributing

Issues and pull requests are welcome. For a new pattern, include a real prompt it improved and what changed in the result; follow the entry format in `references/patterns.md` and do not reuse retired IDs. Remove confidential project names, paths, partner details, unpublished numbers, and credentials from contributions.

## License

Original instructions, templates, and documentation are licensed under [Apache-2.0](LICENSE). The license does not grant rights to the source articles. See [NOTICE](NOTICE) for attribution.
