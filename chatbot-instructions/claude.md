# Using Prism with Claude

Claude is usually strong at Prism-style structural analysis. Paste the selected prompt first, then the artifact.

Recommended opener:

```text
Apply this Prism prompt exactly. Make the generated lens specific to my artifact, not generic. Distinguish fixable issues from structural trade-offs.
```

For high-stakes work, use `prism-full` because it includes an adversarial pass that retracts overclaims.
