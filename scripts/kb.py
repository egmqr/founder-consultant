#!/usr/bin/env python3
"""Checklist tool for the founder-consultant skill.

  python scripts/kb.py check                       validate the checklist and insights
  python scripts/kb.py next-id                     print the next free insight id
  python scripts/kb.py summary                     rebuild README summary + SKILL.md description
  python scripts/kb.py session start|end [--publish]
                                                   check + summary; --publish also sets the
                                                   GitHub repo description (needs gh)
  python scripts/kb.py selftest                    run the built-in self-check
"""
import re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK_RE = re.compile(r"^- \*\*([A-Z]+-\d+)\*\* (.+)$", re.M)
AREA_RE = re.compile(r"^## (.+?) \(([A-Z]+)\)[ \t]*$", re.M)
SHORT_RE = re.compile(r"^<!-- short: (.+?) -->", re.M)  # optional line under an area heading
START, END = "<!-- kb-summary:start -->", "<!-- kb-summary:end -->"


def front_matter(path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError(f"{path.name}: missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        key, _, val = line.partition(":")
        val = val.strip()
        meta[key.strip()] = [v.strip() for v in val[1:-1].split(",") if v.strip()] if val.startswith("[") else val
    return meta


def load(root=ROOT):
    checklist = (root / "knowledge/checklist.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    checks = CHECK_RE.findall(checklist)  # [(id, text)]
    areas = AREA_RE.findall(checklist)  # [(name, code)]
    shorts = {}
    for m in AREA_RE.finditer(checklist):
        s = SHORT_RE.match(checklist, m.end() + 1)
        shorts[m.group(2)] = s.group(1).strip() if s else ""
    insights = [front_matter(p) for p in sorted((root / "knowledge/insights").glob("R*.md"))]
    return checks, areas, insights, shorts


def check(root=ROOT):
    checks, areas, insights, shorts = load(root)
    ids = [c for c, _ in checks]
    errors = [f"duplicate check id {c}" for c in sorted({c for c in ids if ids.count(c) > 1})]
    codes = {code for _, code in areas}
    errors += [f"{c}: no '## Name ({c.split('-')[0]})' heading" for c in ids if c.split("-")[0] not in codes]
    for i in insights:
        errors += [f"{i.get('id', '?')}: missing {k}" for k in ("id", "date", "title", "areas", "checks") if not i.get(k)]
        errors += [f"{i.get('id')}: unknown check {c}" for c in i.get("checks", []) if c not in ids]
        errors += [f"{i.get('id')}: unknown area {a}" for a in i.get("areas", []) if a not in codes]
    return errors


def next_id(root=ROOT):
    _, _, insights, _ = load(root)
    return f"R{max([int(i['id'][1:]) for i in insights] or [0]) + 1:03d}"


def first_sentence(text):
    text = re.sub(r"_From [^_]*_", "", text).strip()
    return re.split(r"(?<=[.!?])\s", text, maxsplit=1)[0]


def descriptions(root=ROOT):
    checks, areas, insights, shorts = load(root)
    lower = lambda n: n if n[:2].isupper() else n[0].lower() + n[1:]  # keep "AI ..." capitalized
    names = [lower(name) for name, _ in areas]
    updated = max([i["date"] for i in insights] or ["never"])
    counts = f"{len(checks)} checks in {len(areas)} areas (updated {updated})"
    skill = (f"Product-agnostic audit of what you're building (web app, API, mobile app, agent or automation) "
             f"against a checklist for robust, reliable, secure AI products, covering {', '.join(names)}. Use to audit "
             f"the current project or system and get ranked findings with fixes. {counts}.")
    labels = [shorts.get(code) or lower(name) for name, code in areas]
    head = "Product-agnostic AI skill that audits the app or system you're building: "
    for n in range(len(labels), 0, -1):  # GitHub caps repo descriptions at 350 characters
        listed = ", ".join(labels[:n]) + ("" if n == len(labels) else " and more")
        repo = f"{head}{listed}. {counts}."  # counts = "N checks in K areas (updated D)"
        if len(repo) <= 350:
            break
    return skill, repo


def summary(root=ROOT):
    checks, areas, insights, shorts = load(root)
    skill_desc, repo_desc = descriptions(root)
    lines = [START, repo_desc, ""]
    for name, code in areas:
        lines.append(f"**{name} ({code})**")
        lines += [f"- `{cid}` {first_sentence(text)}" for cid, text in checks if cid.startswith(code + "-")]
        lines.append("")
    lines += ["Why each check matters:", ""]
    lines += [f"- [{i['id']}](knowledge/insights/{i['id']}.md) {i['title']}" for i in insights]
    lines.append(END)
    readme = root / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = re.sub(re.escape(START) + ".*?" + re.escape(END), lambda _: "\n".join(lines), text, flags=re.S)
    readme.write_text(text, encoding="utf-8", newline="\n")
    skill = root / "SKILL.md"
    stext = skill.read_text(encoding="utf-8")
    stext = re.sub(r"^description: .*$", lambda _: "description: " + skill_desc, stext, count=1, flags=re.M)
    skill.write_text(stext, encoding="utf-8", newline="\n")
    return repo_desc


def session(publish, root=ROOT):
    errors = check(root)
    if errors:
        sys.exit("kb check failed:\n  " + "\n  ".join(errors))
    desc = summary(root)
    if publish:
        subprocess.run(["gh", "repo", "edit", "--description", desc], cwd=root, check=True)
    return desc


def selftest():
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "knowledge/insights").mkdir(parents=True)
        (t / "knowledge/checklist.md").write_text(
            "## Data ownership (DATA)\n\n- **DATA-1** Own it. More text. _From R001._\n- **DATA-2** Back it up.\n",
            encoding="utf-8")
        (t / "knowledge/insights/R001.md").write_text(
            "---\nid: R001\ndate: 2026-01-02\ntitle: T\nareas: [DATA]\nchecks: [DATA-1]\n---\nbody\n", encoding="utf-8")
        (t / "README.md").write_text(f"x\n{START}\nold\n{END}\ny\n", encoding="utf-8")
        (t / "SKILL.md").write_text("---\nname: t\ndescription: old\n---\n", encoding="utf-8")
        assert check(t) == [], check(t)
        assert next_id(t) == "R002"
        desc = session(False, t)
        assert "building: data ownership." in desc and "2 checks in 1 areas (updated 2026-01-02)" in desc, desc
        assert "covering data ownership" in (t / "SKILL.md").read_text(encoding="utf-8")
        readme = (t / "README.md").read_text(encoding="utf-8")
        assert "- `DATA-1` Own it." in readme and "More text" not in readme and "old" not in readme
        assert readme.startswith("x\n") and readme.endswith("y\n")
        assert "2 checks in 1 areas" in (t / "SKILL.md").read_text(encoding="utf-8")
        long = "".join(f"## AI area number {i} with a long name (A{chr(65 + i)})\n- **A{chr(65 + i)}-1** x\n" for i in range(20))
        (t / "knowledge/checklist.md").write_text(long, encoding="utf-8")
        (t / "knowledge/insights/R001.md").write_text(
            "---\nid: R001\ndate: 2026-01-02\ntitle: T\nareas: [AA]\nchecks: [AA-1]\n---\nbody\n", encoding="utf-8")
        _, repo = descriptions(t)
        assert len(repo) <= 350 and repo.endswith("(updated 2026-01-02).") and "and more" in repo, repo
        assert "AI area number 0" in repo, repo
        (t / "knowledge/checklist.md").write_text(long.replace("(AA)\n", "(AA)\n<!-- short: tiny -->\n"), encoding="utf-8")
        _, repo = descriptions(t)
        assert repo.startswith("Product-agnostic AI skill that audits the app or system you're building: tiny, "), repo
        (t / "knowledge/insights/R002.md").write_text(
            "---\nid: R002\ndate: 2026-01-01\ntitle: T\nareas: [NOPE]\nchecks: [NOPE-1]\n---\n", encoding="utf-8")
        errs = check(t)
        assert any("unknown check NOPE-1" in e for e in errs) and any("unknown area NOPE" in e for e in errs), errs
    print("selftest ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    cmd = args[0] if args else ""
    if cmd == "check":
        errs = check()
        print("\n".join(errs) or "ok")
        sys.exit(1 if errs else 0)
    elif cmd == "next-id":
        print(next_id())
    elif cmd == "summary":
        print(summary())
    elif cmd == "session" and len(args) > 1 and args[1] in ("start", "end"):
        print(session("--publish" in args))
    elif cmd == "selftest":
        selftest()
    else:
        sys.exit(__doc__)
