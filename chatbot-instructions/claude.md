# Using Prism with Claude

Use the selected prompt and verify its evidence on your artifact. Paste the selected prompt first, then the artifact.

Recommended opener:

```text
Apply this Prism prompt exactly. Use the selected prompt’s output format. For discovery, list domains only; for analysis, distinguish evidence from hypotheses and allow no supported findings.
```

For high-stakes work, use `prism-full` because it includes an adversarial pass that retracts overclaims.
