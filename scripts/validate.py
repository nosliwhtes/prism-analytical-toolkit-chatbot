#!/usr/bin/env python3
"""Offline prompt-contract and local Markdown file-link checks; not model evaluation."""
import argparse
import json
import os
import re
import stat
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
WINDOWS_DEVICES = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"} | {
    f"{prefix}{digit}" for prefix in ("COM", "LPT") for digit in "123456789¹²³"
}
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
    """Ignore fenced/indented code in the supported Markdown subset."""
    lines = []
    fence = None
    paragraph = False
    for line in text.splitlines(keepends=True):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            lines.append("\n")
            paragraph = False
        elif marker:
            fence = marker[1]
            lines.append("\n")
            paragraph = False
        elif not line.strip(" \t\r\n"):
            lines.append(line)
            paragraph = False
        elif re.match(r"^(?: {4}| {0,3}\t)", line) and not paragraph:
            lines.append("\n")
        else:
            lines.append(line)
            # Indented code cannot interrupt a paragraph. Headings/thematic
            # breaks end it, so a following indented block is still excluded.
            stripped = line.rstrip("\r\n")
            paragraph = not (
                re.match(r"^ {0,3}#{1,6}(?:[ \t]|$)", stripped) or
                (paragraph and re.fullmatch(r" {0,3}(?:=+|-+)[ \t]*", stripped)) or
                re.fullmatch(r" {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})", stripped)
            )
    return "".join(lines)


def link_destination(text, start):
    """Read a destination and optional title following an inline link opener."""
    i = start
    if i < len(text) and text[i] == "<":
        start = i = i + 1
        while i < len(text) and text[i] not in ">\r\n":
            i += 2 if text[i] == "\\" else 1
        if i >= len(text) or text[i] != ">":
            return None
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
            return None
        target = text[start:i]
    # An optional title must be separated from the destination by whitespace.
    closing = re.match(r'''(?:\s+(?:"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\((?:\\.|[^)\\])*\)))?\s*\)''', text[i:])
    if closing:
        return re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])", r"\1", target), i + closing.end()
    return None


def inline_targets(text):
    """Extract ordinary inline destinations, including titles and balanced parentheses.

    This is intentionally not a full CommonMark parser (see evaluation/README.md).
    """
    opener = re.compile(r"\[(?:\\[^\n]|[^\]\\\n])*\]\(\s*")
    for paragraph in re.split(r"\n[ \t]*\n", prose_only(text)):
        # Resolve equal-length backtick runs in advance. Scan in source order so
        # a code span can hide a link, but a destination's backticks stay literal.
        next_run = {}
        code_ends = {}
        for run in reversed(list(re.finditer(r"`+", paragraph))):
            length = len(run[0])
            if length in next_run:
                code_ends[run.start()] = next_run[length]
            next_run[length] = run.end()
        i = 0
        while i < len(paragraph):
            if paragraph[i] == "\\":
                # Punctuation escapes; skipping a backslash pair leaves the
                # following opener active, unlike a single escaping backslash.
                i += 2
                continue
            if i in code_ends:
                i = code_ends[i]
                continue
            if paragraph[i] == "[":
                match = opener.match(paragraph, i)
                destination = link_destination(paragraph, match.end()) if match else None
                if destination is not None:
                    target, i = destination
                    yield target
                    continue
            i += 1


def local_link_parts(root, source, target):
    """Classify and bound a decoded destination without filesystem operations."""
    # Explicit external references never enter the filesystem path pipeline;
    # their percent-encoded bytes need not be UTF-8. A one-letter scheme may be
    # a Windows drive and must still pass the decoded local-path checks below.
    if target.startswith(("#", "//")) or (
            re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) and
            not re.match(r"^[a-z]:", target, re.I)):
        return None
    # Split URI delimiters before decoding: %23 and %3F are filename characters.
    local = unquote(target.split("#", 1)[0].split("?", 1)[0], errors="strict")
    if any(ord(char) < 32 or ord(char) == 127 for char in local):
        raise ValueError("control character in local destination")
    # A Windows drive is not an external URI scheme, including drive-relative C:x.
    if re.match(r"^[a-z]:", local, re.I):
        raise ValueError("drive-qualified destination")
    if re.match(r"^[a-z][a-z0-9+.-]*:", local, re.I):
        return None  # Encoded URI schemes also never enter the filesystem.
    if local.startswith("/") or "\\" in local:
        raise ValueError("absolute or backslash destination")
    parts = list(source.parent.relative_to(root).parts)
    depth = len(parts)
    for part in local.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            depth -= 1
            if depth < 0:
                raise ValueError("destination escapes pack root")
        else:
            # Prevent Windows device/stream and trailing-dot/space aliases even
            # when validating on POSIX. Decode exactly once, like the OS path.
            device = part.partition(".")[0].rstrip(" ").upper()
            if ":" in part or part.endswith((".", " ")) or device in WINDOWS_DEVICES:
                raise ValueError("nonportable destination component")
            depth += 1
        parts.append(part)
    return parts


def local_link_exists(root, parts):
    """Check bounded components without following symlinks or reparse points."""
    current = root
    for index, part in enumerate(parts):
        if part == "..":
            current = current.parent
            continue
        current = current / part
        try:
            metadata = current.lstat()
        except (FileNotFoundError, NotADirectoryError):
            return False
        if linked_metadata(metadata):
            raise ValueError("symlink or reparse point in destination")
        if not (stat.S_ISREG(metadata.st_mode) or stat.S_ISDIR(metadata.st_mode)):
            raise ValueError("destination is not a regular file or directory")
        if index < len(parts) - 1 and not stat.S_ISDIR(metadata.st_mode):
            return False
    return True


def linked_metadata(metadata):
    return (stat.S_ISLNK(metadata.st_mode) or
            getattr(metadata, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def source_metadata(path):
    """Check every component before traversing a local, stable source path."""
    path = path.absolute()
    if path.anchor.startswith(("//", "\\\\")):
        raise ValueError("pack sources must use local paths")
    current = Path(path.anchor)
    metadata = current.lstat()
    for part in path.parts[1:]:
        if linked_metadata(metadata) or not stat.S_ISDIR(metadata.st_mode):
            raise ValueError("unsafe source parent")
        current = current / part
        metadata = current.lstat()
    if linked_metadata(metadata):
        raise ValueError("symlink or reparse point in source")
    return metadata


def markdown_sources(root, errors):
    """Inventory sources without following linked files or directory entries."""
    files = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            if not stat.S_ISDIR(source_metadata(directory).st_mode):
                raise ValueError("source directory is not a directory")
            with os.scandir(directory) as entries:
                for entry in sorted(entries, key=lambda item: item.name):
                    if entry.name == ".git":
                        continue
                    path = directory / entry.name
                    name = path.relative_to(root).as_posix()
                    try:
                        # Non-Markdown regular files are not source inputs. Never
                        # follow entries to decide whether to descend into them.
                        if not (os.path.normcase(entry.name).endswith(".md") or entry.is_symlink() or
                                entry.is_dir(follow_symlinks=False)):
                            continue
                        metadata = path.lstat()
                        if linked_metadata(metadata):
                            raise ValueError("linked source entry")
                        if stat.S_ISDIR(metadata.st_mode):
                            pending.append(path)
                        elif stat.S_ISREG(metadata.st_mode):
                            files[name] = path
                        else:
                            raise ValueError("non-regular source entry")
                    except ValueError:
                        errors.append({"path": name, "rule": "unsafe_source"})
                    except OSError as exc:
                        errors.append({"path": name, "rule": "unreadable_file", "detail": str(exc)})
        except ValueError:
            errors.append({"path": directory.relative_to(root).as_posix(), "rule": "unsafe_source"})
        except OSError as exc:
            errors.append({"path": directory.relative_to(root).as_posix(),
                           "rule": "unreadable_file", "detail": str(exc)})
    return files


def read_markdown(path):
    """Recheck components, then validate the descriptor before reading content.

    POSIX also refuses a leaf symlink at open time. Windows relies on the
    pre-open reparse checks; the selected tree must remain local and stable.
    """
    expected = source_metadata(path)
    if not stat.S_ISREG(expected.st_mode):
        raise ValueError("source is not a regular file")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(path, flags | getattr(os, "O_BINARY", 0))
    try:
        actual = os.fstat(fd)
        if (linked_metadata(actual) or not stat.S_ISREG(actual.st_mode) or
                (actual.st_dev, actual.st_ino) != (expected.st_dev, expected.st_ino)):
            raise ValueError("source changed or is not a regular file")
        stream = os.fdopen(fd, "r", encoding="utf-8")
    except BaseException:
        os.close(fd)
        raise
    with stream:
        return stream.read()


def validate(root):
    root = Path(root).absolute()
    errors = []
    checked = 0
    texts = {}

    def read(path):
        name = path.relative_to(root).as_posix()
        if name not in texts:
            try:
                texts[name] = read_markdown(path)
            except UnicodeError:
                errors.append({"path": name, "rule": "invalid_utf8"})
                texts[name] = None
            except ValueError:
                errors.append({"path": name, "rule": "unsafe_source"})
                texts[name] = None
            except OSError as exc:
                errors.append({"path": name, "rule": "unreadable_file", "detail": str(exc)})
                texts[name] = None
        return texts[name]

    files = markdown_sources(root, errors)
    names = set(PROMPTS + LENSES) | {
        name for name in files if Path(name).parts[0] in ("prompts", "reference-prisms")
    }
    for name in sorted(names):
        if name not in files:
            errors.append({"path": name, "rule": "missing_prompt"})
            continue
        checked += 1
        text = read(files[name])
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
    for name, path in sorted(files.items()):
        text = read(path)
        if text is None:
            continue
        # Inline relative file links used by this pack. External URLs and anchors
        # are not fetched; reference-style links and heading anchors are not checked.
        for target in inline_targets(text):
            try:
                parts = local_link_parts(root, path, target)
                if parts is None or local_link_exists(root, parts):
                    continue
                rule = "broken_local_link"
            except ValueError:
                rule = "unsafe_local_link"
            except OSError:
                rule = "unreadable_local_link"
            errors.append({"path": str(path.relative_to(root)), "rule": rule, "detail": target})
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
