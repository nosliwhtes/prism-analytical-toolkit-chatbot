# Worked example: conflicting handoff instructions

This is an authored illustration, not a measured chatbot response. Paste a complete [Prism Scan prompt](../prompts/prism-scan.md) before the request.

```text
Review question: Do these instructions specify one clear release owner?
Scope: Only these two excerpts; no interviews or incident data.

A1 — Release SOP, version 2, excerpt
Step 4: The operations lead approves release after QA review.

A2 — Shift handover checklist, version unspecified, excerpt
Item 6: QA approves release; operations is informed afterward.

No document hierarchy, effective dates, or proof of current practice is supplied.
```

A useful final table can separate the observed inconsistency from any unverified operational harm:

| ID | Finding and trigger | Source/location + evidence | Status | Impact/severity + rationale | Classification | Next test or action |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | Release approval is assigned to different roles in the two excerpts | A1 Step 4: “operations lead approves”; A2 Item 6: “QA approves” | Observation: textual inconsistency | Unknown: which instructions govern practice is not supplied | Fixable documentation gap if both are current; otherwise unknown | Confirm applicable versions and document authority; success: one governing approval role is identified with a source |

Do not claim an actual unauthorized release, a regulatory violation, or that A1 supersedes A2. The absence of an authority rule in these excerpts does not prove none exists elsewhere. An action to reconcile the documents depends on confirming applicability. No structural constraint is established.

If later context establishes A2 is obsolete, retain F1's identity, revise its applicability, and remove any unsupported claim of a current conflicting workflow. Coverage stays limited to the supplied excerpts and that new context.
