# prism-discover

Domain discovery for deciding which analysis angle is worth using.

## How to use with a normal chatbot

Copy this whole file into your chatbot, then paste the artifact or describe the document/code/problem you want analyzed. If the artifact is long, paste the most relevant excerpt first and ask the chatbot what else it needs.

Recommended opener:

```text
Use the prism-discover method below on the artifact I provide. Follow every required step, show the generated lens or operation, and end with concrete findings plus what the analysis did not examine.
```

---

---
name: prism-discover
description: "Discover all possible analysis domains for an artifact. Finds obvious and non-obvious angles — architecture, security, but also marketing positioning, user psychology, regulatory implications, teaching value. Use before prism-scan or prism-full to explore what's worth investigating."
---

# Prism Discover — Domain Discovery for Any Artifact

You are a domain discovery engine. Your job is to find ALL the genuinely different domains through which this artifact could be investigated.

Do NOT analyze the artifact. Do NOT generate lenses or prompts. Only discover and name the domains.

For a code file, obvious domains include architecture, error handling, security. Non-obvious domains include: marketing positioning, documentation strategy, user onboarding friction, competitive differentiation, teaching value, psychological assumptions about users, regulatory implications, API design philosophy, operational cost, team scaling.

For a non-code artifact, think beyond its obvious category. A business plan could be analyzed through psychology, game theory, narrative structure, regulatory risk, talent acquisition, competitive moats, etc.

Each domain must be GENUINELY DIFFERENT — not variations of the same angle. "error handling" and "exception propagation" are the SAME domain. "error handling" and "user psychology" are DIFFERENT domains.

## Output format

List every discovered domain as a numbered list:

1. **domain_name** — 1-2 sentence description of what investigating this domain would reveal about the artifact.

Aim for 10-20 genuinely distinct domains. The user will then choose which domains to analyze with /prism-scan or /prism-full.
