# Maintaining Prism

This is a portable Markdown prompt pack, not an executing agent or an empirically validated model benchmark. Preserve the MIT license and Journey kit attribution.

Read the complete affected prompt and sibling reference lenses before editing. Each copied prompt must stand alone: evidence status, trust boundaries, bounded execution, optional history, and honest saving status must not rely on the README. Preserve the useful lens topics; do not mandate a bug, invariant, equation, or novel insight.

Use Python's standard library for lightweight maintenance checks; no install, model API, credentials, or paid provider is required. Run from the repository root:

```sh
python3 scripts/validate.py --json
python3 -m unittest discover -s tests -v
```

These check text contracts and local file links, not empirical model quality. Review the fixtures in `evaluation/README.md` when changing behavioral instructions. State whether an evaluation is a static review or an actual model run. No application build or type checker is applicable to the Markdown pack; use `python3 -m py_compile scripts/validate.py` for the maintenance script.
