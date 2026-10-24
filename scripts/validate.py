#!/usr/bin/env python3
"""Repository checks for ambition-skill (stdlib only).

    python3 scripts/validate.py              # check the repository
    python3 scripts/validate.py --self-test  # plant known errors, require all caught

The self-test follows pattern V1 of the skill: a check that has never failed
does not count, so every check below is shown failing on a planted error.
"""

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = "skills/ambition"
DOCS = ["README.md", "README.en.md", "CONTRIBUTING.md", "CHANGELOG.md"]
PRIVATE_SCAN = ["skills", "examples"]
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
HOME_PATH = re.compile(r"/(Users|home)/[A-Za-z0-9._-]+")


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields


def check_skill(root):
    errs = []
    path = root / SKILL / "SKILL.md"
    fm = frontmatter(path.read_text(encoding="utf-8"))
    if fm is None:
        return [f"{path.name}: missing YAML frontmatter"]
    name, desc = fm.get("name", ""), fm.get("description", "")
    if name != Path(SKILL).name:
        errs.append(f"SKILL.md: name '{name}' does not match directory '{Path(SKILL).name}'")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        errs.append("SKILL.md: name must be 1-64 lowercase letters, digits, or hyphens")
    if not desc or len(desc) > 1024:
        errs.append(f"SKILL.md: description must be 1-1024 characters (got {len(desc)})")
    body = path.read_text(encoding="utf-8")
    for ref in sorted(set(re.findall(r"`(references/[^`]+\.md)`", body))):
        if not (root / SKILL / ref).is_file():
            errs.append(f"SKILL.md: referenced file {ref} does not exist")
    return errs


def pattern_ids(root):
    """Return (menu rows, entry headings) from patterns.md, ignoring retired entries."""
    text = (root / SKILL / "references/patterns.md").read_text(encoding="utf-8")
    menu = re.search(r"^## 菜单\n(.*?)^## ", text, re.S | re.M)
    rows = re.findall(r"^\| ([A-Z]\d+) \| ([^|]+?) \|", menu.group(1) if menu else "", re.M)
    active = text.split("\n## 已废弃", 1)[0]
    heads = re.findall(r"^### ([A-Z]\d+) (.+)$", active, re.M)
    return rows, heads


def check_patterns(root):
    errs = []
    rows, heads = pattern_ids(root)
    if not rows:
        return ["patterns.md: menu table not found or empty"]
    for label, items in (("menu", rows), ("entries", heads)):
        ids = [i for i, _ in items]
        dup = sorted({i for i in ids if ids.count(i) > 1})
        if dup:
            errs.append(f"patterns.md: duplicate IDs in {label}: {', '.join(dup)}")
    menu, entries = dict(rows), dict(heads)
    for i in sorted(set(menu) - set(entries)):
        errs.append(f"patterns.md: {i} is in the menu but has no entry")
    for i in sorted(set(entries) - set(menu)):
        errs.append(f"patterns.md: {i} has an entry but is not in the menu")
    for i in sorted(set(menu) & set(entries)):
        if menu[i].strip() != entries[i].strip():
            errs.append(f"patterns.md: {i} is named '{menu[i]}' in the menu but '{entries[i]}' in its entry")
    return errs


def check_counts(root):
    """Pattern counts shown in the READMEs and banners must match patterns.md."""
    errs = []
    n = len(pattern_ids(root)[0])
    for doc in ("README.md", "README.en.md"):
        found = re.findall(r"patterns-(\d+)-", (root / doc).read_text(encoding="utf-8"))
        if not found:
            errs.append(f"{doc}: pattern-count badge not found")
        for k in found:
            if int(k) != n:
                errs.append(f"{doc}: badge says {k} patterns, patterns.md has {n}")
    for svg in sorted((root / "assets").glob("banner-*.svg")):
        if f"{n} 个提示词模式" not in svg.read_text(encoding="utf-8"):
            errs.append(f"assets/{svg.name}: does not show '{n} 个提示词模式'")
    return errs


def check_evals(root):
    errs = []
    path = root / SKILL / "evals/evals.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"evals.json: invalid JSON ({e})"]
    if data.get("skill_name") != Path(SKILL).name:
        errs.append("evals.json: skill_name does not match the skill")
    ids = [e.get("id") for e in data.get("evals", [])]
    if len(ids) != len(set(ids)):
        errs.append("evals.json: duplicate eval ids")
    for e in data.get("evals", []):
        if not e.get("prompt") or not e.get("expectations"):
            errs.append(f"evals.json: eval {e.get('id')} needs a prompt and expectations")
        for f in e.get("files", []):
            if not (root / SKILL / f).is_file():
                errs.append(f"evals.json: eval {e.get('id')} fixture {f} does not exist")
    return errs


def check_marketplace(root):
    errs = []
    path = root / ".claude-plugin/marketplace.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"marketplace.json: invalid JSON ({e})"]
    version = data.get("metadata", {}).get("version")
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    if version and f"## [{version}]" not in changelog:
        errs.append(f"CHANGELOG.md: no section for version {version}")
    for p in data.get("plugins", []):
        if p.get("version") != version:
            errs.append(f"marketplace.json: plugin {p.get('name')} version differs from metadata.version")
        for s in p.get("skills", []):
            if not (root / s / "SKILL.md").is_file():
                errs.append(f"marketplace.json: skill path {s} has no SKILL.md")
    return errs


def check_copies(root):
    errs = []
    for name in ("LICENSE", "NOTICE"):
        if (root / name).read_bytes() != (root / SKILL / name).read_bytes():
            errs.append(f"{SKILL}/{name} differs from the root {name}")
    return errs


def check_links(root):
    errs = []
    link = re.compile(r"\]\(([^)\s]+)\)|(?:src|srcset|href)=\"([^\"]+)\"")
    for doc in DOCS:
        text = (root / doc).read_text(encoding="utf-8")
        for m in link.finditer(text):
            target = (m.group(1) or m.group(2)).split("#", 1)[0]
            if not target or re.match(r"[a-z]+:", target):
                continue
            if not (root / target).exists():
                errs.append(f"{doc}: broken relative link {target}")
    return errs


def check_private(root):
    """Keep personal details out of the installable skill and the examples."""
    errs = []
    for top in PRIVATE_SCAN:
        for f in sorted((root / top).rglob("*")):
            if not f.is_file() or f.name in ("LICENSE", "NOTICE"):
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
            rel = f.relative_to(root)
            for m in EMAIL.finditer(text):
                errs.append(f"{rel}: contains an email address ({m.group(0)})")
            for m in HOME_PATH.finditer(text):
                errs.append(f"{rel}: contains an absolute home path ({m.group(0)})")
    return errs


CHECKS = [check_skill, check_patterns, check_counts, check_evals,
          check_marketplace, check_copies, check_links, check_private]


def run(root):
    errs = []
    for check in CHECKS:
        try:
            errs += check(root)
        except (OSError, AttributeError, KeyError) as e:
            errs.append(f"{check.__name__}: {type(e).__name__}: {e}")
    return errs


def edit(rel, old, new):
    def apply(root):
        p = root / rel
        text = p.read_text(encoding="utf-8")
        assert old in text, f"self-test mutation target not found in {rel}: {old!r}"
        p.write_text(text.replace(old, new, 1), encoding="utf-8")
    return apply


PLANTED = {
    "menu ID typo": edit(f"{SKILL}/references/patterns.md", "| F4 | 下一个问题 |", "| F9 | 下一个问题 |"),
    "entry renamed": edit(f"{SKILL}/references/patterns.md", "### H1 目标背后的目标", "### H1 目标背后的目标们"),
    "duplicate entry ID": edit(f"{SKILL}/references/patterns.md", "### H2 ", "### H1 "),
    "skill name mismatch": edit(f"{SKILL}/SKILL.md", "name: ambition", "name: ambitious"),
    "stale badge count": edit("README.en.md", "patterns-25-", "patterns-24-"),
    "invalid evals JSON": edit(f"{SKILL}/evals/evals.json", '"skill_name"', "skill_name"),
    "missing eval fixture": edit(f"{SKILL}/evals/evals.json", '"files": ["evals/files/compare.py"]', '"files": ["evals/files/missing.py"]'),
    "version without changelog": edit(".claude-plugin/marketplace.json", '"version": "1.0.0"\n  }', '"version": "9.9.9"\n  }'),
    "skill LICENSE drift": edit(f"{SKILL}/LICENSE", "Apache License", "Apache Licence"),
    "broken README image": edit("README.md", "assets/workflow-light.svg", "assets/workflow-lite.svg"),
    "email leaked into skill": edit(f"{SKILL}/references/contexts.md", "# 使用者语境", "# 使用者语境 someone@example.com"),
    "home path leaked into example": edit("examples/contexts.example.md", "`~/work/`", "`/Users/alice/work/`"),
}


def self_test():
    clean = run(ROOT)
    if clean:
        print("self-test needs a clean repository first:")
        print("\n".join(f"  - {e}" for e in clean))
        return 1
    missed = []
    for label, mutate in PLANTED.items():
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
            mutate(copy)
            caught = run(copy)
        print(f"  {'caught' if caught else 'MISSED'}  {label}" + (f"  ({caught[0]})" if caught else ""))
        if not caught:
            missed.append(label)
    print(f"self-test: {len(PLANTED) - len(missed)}/{len(PLANTED)} planted errors caught")
    return 1 if missed else 0


def main():
    if "--self-test" in sys.argv[1:]:
        return self_test()
    errs = run(ROOT)
    for e in errs:
        print(f"error: {e}")
    rows, _ = pattern_ids(ROOT)
    print(f"{'FAILED' if errs else 'ok'}: {len(CHECKS)} checks, {len(rows)} patterns, {len(errs)} errors")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
