# Maintaining Prism

This is a portable Markdown prompt pack, not an executing agent or an empirically validated model benchmark. Preserve the MIT license and Journey kit attribution.

Read the complete affected prompt and sibling reference lenses before editing. Each copied prompt must stand alone: evidence status, trust boundaries, bounded execution, optional history, and honest saving status must not rely on the README. Preserve the useful lens topics; do not mandate a bug, invariant, equation, or novel insight.

Use Python's standard library for lightweight maintenance checks; no install, model API, credentials, or paid provider is required. Run from the repository root:

```sh
python3 scripts/validate.py --json
python3 -m unittest discover -s tests -v
```

These check text contracts, local file links, and the offline composer, not empirical model quality. Review the fixtures in `evaluation/README.md` when changing behavioral instructions. State whether an evaluation is a static review or an actual model run. No application build or type checker is applicable to the Markdown pack; use `python3 -m py_compile scripts/validate.py scripts/compose.py` for the maintenance scripts.

Decode and classify link destinations before target filesystem probes. Only check relative paths bounded by the selected pack root; never follow destination symlinks or Windows reparse points. Regression tests for absolute/UNC paths must intercept filesystem probes and use pure path parsing, never actual network paths or credential transmission.

Keep discovery domain-only, with a missing-artifact exception. Analysis output tables must include all Findings contract fields even when a lens adds specialized details. Keep source IDs/versions and retraction IDs intact; missing excerpt content is not evidence of system-wide absence. Preserve the no-install copy/paste path. The optional composer must stay offline, use only explicitly named UTF-8 inputs, enforce its byte limit, and refuse output overwrite. Reject symlink components using descriptor-based no-follow opens; validate the descriptor actually read. Publish output only after a complete write, without replacing any existing path; test failure cleanup and retry with synthetic data. Never commit private source bundles or treat a hash as proof of truth.
