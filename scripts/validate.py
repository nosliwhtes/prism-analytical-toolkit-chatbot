#!/usr/bin/env python3
"""Offline prompt-contract and local Markdown file-link checks; not model evaluation."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = tuple(f"prompts/prism-{name}.md" for name in ("scan", "full", "3way", "reflect", "discover"))
LENSES = tuple(f"reference-prisms/{name}.md" for name in ("claim", "deep_scan", "error_resilience", "identity", "l12", "optimize", "simulation"))
REQUIRED = (
    "## Operating boundaries", "as data, not instructions", "one bounded run", "History is optional",
    "Do not write files unless the user explicitly requests saving",
    "file-writing capability is available", "not saved", "only after a successful write",
)
ANALYSIS_REQUIRED = ("Separate observations", "no structural constraint established",
                     "## Evidence and scope", "## Findings contract",
                     "Source/location + evidence", "Next test or action")
DISCOVERY_REQUIRED = ("Return only a numbered list", "Do not generate lenses or findings",
                      "only exception to domain-only output")
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
    r"Find the fundamental trade-off the system is managing",
)


def prose_only(text):
    """Ignore fenced/indented code and inline code in the supported Markdown subset."""
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            lines.append("\n")
        elif marker:
            fence = marker[1]
            lines.append("\n")
        elif line.startswith(("    ", "\t")):
            lines.append("\n")
        else:
            lines.append(line)
    return re.sub(r"(?<!`)(`+)(?!`)(.*?)\1(?!`)", "", "".join(lines), flags=re.S)


def inline_targets(text):
    """Extract ordinary inline destinations, including titles and balanced parentheses.

    This is intentionally not a full CommonMark parser (see evaluation/README.md).
    """
    text = prose_only(text)
    for match in re.finditer(r"(?<!\\)\[[^\]\n]*\]\(\s*", text):
        start = i = match.end()
        if i < len(text) and text[i] == "<":
            start = i = i + 1
            while i < len(text) and text[i] not in ">\r\n":
                i += 2 if text[i] == "\\" else 1
            if i >= len(text) or text[i] != ">":
                continue
            target = text[start:i]
            i += 1
        else:
            depth = 0
            while i < len(text):
                char = text[i]
                if char == "\\" and i + 1 < len(text):
                    i += 2
                    continue
                if char.isspace() or (char == ")" and depth == 0):
                    break
                if char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                i += 1
            if depth:
                continue
            target = text[start:i]
        # An optional title must be separated from the destination by whitespace.
        if re.match(r'''(?:\s+(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\((?:\\.|[^)\\])*\)))?\s*\)''', text[i:]):
            yield re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])", r"\1", target)


def validate(root):
    root = Path(root)
    errors = []
    checked = 0
    texts = {}

    def read(path):
        name = path.relative_to(root).as_posix()
        if name not in texts:
            try:
                texts[name] = path.read_text(encoding="utf-8")
            except UnicodeError:
                errors.append({"path": name, "rule": "invalid_utf8"})
                texts[name] = None
            except OSError as exc:
                errors.append({"path": name, "rule": "unreadable_file", "detail": str(exc)})
                texts[name] = None
        return texts[name]

    names = set(PROMPTS + LENSES)
    for directory in ("prompts", "reference-prisms"):
        names.update(path.relative_to(root).as_posix() for path in (root / directory).rglob("*.md"))
    for name in sorted(names):
        path = root / name
        if not path.is_file():
            errors.append({"path": name, "rule": "missing_prompt"})
            continue
        checked += 1
        text = read(path)
        if text is None:
            continue
        discovery = name == "prompts/prism-discover.md"
        for phrase in REQUIRED + (DISCOVERY_REQUIRED if discovery else ANALYSIS_REQUIRED):
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
        text = read(path)
        if text is None:
            continue
        # Inline relative file links used by this pack. External URLs and anchors
        # are not fetched; reference-style links and heading anchors are not checked.
        for target in inline_targets(text):
            if re.match(r"[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith(("#", "//")):
                continue
            local = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not (path.parent / local).exists():
                errors.append({"path": str(path.relative_to(root)), "rule": "broken_local_link", "detail": target})
    return {"ok": not errors, "prompts_checked": checked, "errors": errors,
            "scope": "Static text contracts and inline local file links; no model-quality claim."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit a machine-readable result")
    parser.add_argument("--root", type=Path, default=ROOT, help="pack directory (defaults to this checkout)")
    args = parser.parse_args()
    result = validate(args.root)
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
