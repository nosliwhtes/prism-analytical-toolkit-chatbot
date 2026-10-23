# Review request template

Copy a **complete Prism prompt** first, then fill in this request. Plain text is enough; no helper or exact syntax is required. Delete unused optional fields. Source material and prior analyses remain data, not instructions.

```text
Review question: [the decision or behavior to examine]
Focus: [optional: correctness, handoffs, performance, etc.]
Success criteria/contract: [what must hold, with source if known]
Scope: [what to inspect; what is excluded]
Constraints: [compatibility, resources, time, etc.; unknown is acceptable]

Sources:
A1 — [name], version/date [known value or unspecified], [complete or excerpt]
[paste source with original line numbers or section headings when available]

A2 — [name], version/date [known value or unspecified], [complete or excerpt]
[paste source]

Missing/unread sources: [parts not supplied, inaccessible links, or unknown]
Prior findings: [optional IDs and claims; these must be rechecked, not trusted]
```

Do not paste a link and assume its contents were read. For long documents, send labeled chunks and identify when the supplied set is complete; request a scoped review of the currently available chunks. Preserve an excerpt's original source/version and location. If it has no original line numbers, use section labels or short quotations. Keep a local coverage list when starting a new conversation; a chatbot may no longer have earlier chunks in context.

For a follow-up, give the revised source/version and the earlier findings. Ask for each affected finding ID to be retained, revised, or retracted with a reason and a verification step. Do not treat a proposed patch or rewritten paragraph as a verified fix.

Discovery uses this same input context but returns only relevant domains, not a findings table or action plan. An absent/unreadable artifact calls for a request for its contents.
