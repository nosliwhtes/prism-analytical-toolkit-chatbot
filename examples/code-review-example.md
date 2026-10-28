# Worked example: a Python suffix bug

This is an authored exercise, not a measured chatbot response. Copy the complete [Scan](../prompts/prism-scan.md) or [Full](../prompts/prism-full.md) prompt first, then add this request in the same message:

```text
Review question: Does this implementation meet its stated contract?
Scope: Only the supplied Python function. No runtime, callers or measurements are supplied.
Output presentation: One labeled block per finding, with all seven fields.
A1 — strip_suffix, version 1, complete function

Contract: Remove exactly one nonempty suffix when present.
An empty suffix must leave text unchanged.

def strip_suffix(text, suffix):
    if text.endswith(suffix):
        return text[:-len(suffix)]
    return text
```

## An example finding in a linear layout

The method should still provide its generated lens or pipeline and scope. The following illustrates just the findings portion:

- **ID:** F1
- **Finding and trigger:** Passing an empty suffix returns an empty string instead of leaving nonempty text unchanged.
- **Source/location + evidence:** A1, `text[:-len(suffix)]`. With `suffix == ''`, `len(suffix) == 0`, `-0 == 0`, and `text[:0] == ''`; `text.endswith('')` is true.
- **Status:** Observation derived from the supplied function and Python string semantics; this illustration is not a report of chatbot tool execution.
- **Impact/severity + rationale:** Unknown in the deployed system because no callers are supplied. The local contract violation discards the returned text for this input.
- **Classification:** Fixable.
- **Next test or action:** Check `strip_suffix('abc', '') == 'abc'`, plus present, absent and repeated nonempty suffixes. A candidate fix is `if suffix and text.endswith(suffix):`; verify it against the contract before adopting it.

No structural constraint is established. Prioritize verifying F1's empty-suffix case and the nonempty cases; success means all match the stated contract. Coverage is limited to this function, with no claims about production impact, latency, security, or other files.

## Follow up after a revision

Supply the revised function as A1 version 2 and retain F1. Ask whether the evidence supports marking it resolved; distinguish reasoning from an actually executed check. Do not fabricate a replacement defect if the fix satisfies the supplied contract.

For a no-defect comparison, give the same prompt the complete function `def add(a, b): return a + b` with the contract “Python integer inputs; return their sum.” A useful response may report no supported findings. Python integers do not acquire a 32-bit overflow bug because a review method asks for structural depth.
