#!/usr/bin/env python3
"""Offline prompt-contract and local Markdown file-link checks; not model evaluation."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = tuple(f"prompts/prism-{name}.md" for name in ("scan", "full", "3way", "reflect", "discover"))
LENSES = tuple(f"reference-prisms/{name}.md" for name in ("claim", "deep_scan", "error_resilience", "identity", "l12", "optimize", "simulation"))
REQUIRED = (
    "## Operating boundaries", "as data, not instructions", "Separate observations",
    "no structural constraint established", "one bounded run", "History is optional",
    "Do not write files unless the user explicitly requests saving",
    "file-writing capability is available", "not saved", "only after a successful write",
)
# Deliberately narrow regression guards for known contradictory mandates.
FORBIDDEN = (
    r"Prove these three properties CANNOT all coexist",
    r"Prove (?:this|the) improvement recreates",
    r"STRUCTURAL CERTAINTIES",
    r"Name the conservation law: A × B = constant",
    r"Derive the conservation law: A × B = Constant",
    r"append it to a persistent constraint log",
    r"For guaranteed single-shot execution",
    r"SCORED 9(?:\.5)?/10",
    r"not just observations",
    r"Apply this law to your own simulation",
    r"trace forward through ALL downstream code",
)


def validate(root):
    errors = []
    checked = 0
    for name in PROMPTS + LENSES:
        path = root / name
        if not path.is_file():
            errors.append({"path": name, "rule": "missing_prompt"})
            continue
        checked += 1
        text = path.read_text(encoding="utf-8")
        for phrase in REQUIRED:
            if phrase not in text:
                errors.append({"path": name, "rule": "missing_boundary", "detail": phrase})
        for pattern in FORBIDDEN:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append({"path": name, "rule": "contradictory_mandate", "detail": pattern})
        if name.endswith("prism-discover.md"):
            opener = text.split("```text", 1)[1].split("```", 1)[0] if "```text" in text else ""
            if "Return only a numbered list" not in opener or "show the generated lens" in opener:
                errors.append({"path": name, "rule": "discovery_format"})
        if name.endswith("optimize.md") and not all(term in text for term in ("unmeasured", "Never invent timing", "source, units, workload, and method")):
            errors.append({"path": name, "rule": "measurement_provenance"})
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        # Inline relative file links used by this pack. External URLs and anchors
        # are not fetched; reference-style links and heading anchors are not checked.
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", text):
            if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
                continue
            local = target.split("#", 1)[0]
            if not (path.parent / local).exists():
                errors.append({"path": str(path.relative_to(root)), "rule": "broken_local_link", "detail": target})
    return {"ok": not errors, "prompts_checked": checked, "errors": errors,
            "scope": "Static text contracts and inline local file links; no model-quality claim."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit a machine-readable result")
    args = parser.parse_args()
    result = validate(ROOT)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{'PASS' if result['ok'] else 'FAIL'}: {result['prompts_checked']} prompts checked")
        for error in result["errors"]:
            print(f"{error['path']}: {error['rule']}: {error.get('detail', '')}")
        print(result["scope"])
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
