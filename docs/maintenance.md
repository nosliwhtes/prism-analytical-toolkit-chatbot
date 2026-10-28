# Validate and maintain the prompt pack

The product is Markdown; the two optional Python scripts use only the standard library. There is no application build, dependency installation, type-checker configuration, or model API. Read [AGENTS.md](../AGENTS.md) before changing the pack.

Run the offline checks from the repository root with Python 3.12 or newer:

```sh
python3 scripts/validate.py --json
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/validate.py
python3 -m py_compile scripts/compose.py
```

The validator exits 0 on success and 1 on validation failures, with path/rule diagnostics, including malformed UTF-8. Use `--root PATH` to check a different pack. It checks known prompt-contract regressions and inline local file links (including optional titles, angle destinations, and encoded spaces), ignoring code examples. It is a documented Markdown subset, not a complete CommonMark parser or empirical model evaluation. See the [evaluation fixtures and rubric](../evaluation/README.md), [implementation rationale](functional-improvements.md), and [maintenance guidance](../AGENTS.md). No runtime packages, lockfile, application build, or model API are needed.

Link checks decode the path once before filesystem access and reject absolute/UNC paths, Windows drive/device aliases, backslashes, and traversal outside the selected pack. Relative `../` links within the pack remain supported. Destination symlinks and Windows reparse points are refused; unsafe and unreadable destinations produce diagnostics. External URI schemes, explicit protocol-relative URLs, and anchors are skipped without fetching. The selected pack must be local and stable during validation; this tool does not isolate a concurrently modified filesystem.

Source discovery checks directory entries before descending and rejects symlinks/reparse points, including linked ancestors of the selected root. Only inventoried regular Markdown files can be read or contract-checked; non-regular Markdown sources receive diagnostics. Reads recheck path components and the opened file descriptor. POSIX additionally uses no-follow/nonblocking open flags where available; Windows relies on pre-open reparse checks under the same stable-tree requirement, not atomic isolation from concurrent replacement.

CI uses the Python supplied on GitHub's Ubuntu 24.04 hosted runner and an immutable revision of [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1). The official [checkout documentation](https://github.com/actions/checkout) specifies Node 24 runner support inherited from v5; hosted runners meet this requirement. Dependency review: 2026-10-04. Preserve the pin and verify official release compatibility when updating it.
