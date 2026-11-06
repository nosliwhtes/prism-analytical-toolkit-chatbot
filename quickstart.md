# Quickstart

## 60-second version

1. Copy [`prompts/prism-scan.md`](prompts/prism-scan.md).
2. Paste the whole file into a new message in Gemini, ChatGPT, Claude, or another chatbot. Add the request and artifact below before sending it.
3. Add this:

```text
Use the Prism Scan method on this artifact. Follow all steps. Do not give generic advice. End with a findings table and a short action list.
```

4. Paste your artifact, label its source/version and whether it is an excerpt, then send the message. If you have no artifact ready, try the [worked code review](examples/code-review-example.md).

For several documents, label them A1, A2, etc., include versions when known, and state whether each is complete or an excerpt. Start with the [review request template](templates/review-request.md). For local text files, `python3 scripts/compose.py --artifact your-file.txt --output review-bundle.md` prepares the full Scan prompt plus source line labels and a content hash; paste or upload the resulting file. See [bundle options and limits](README.md#review-multiple-sources-reproducibly).

## Good artifacts to analyze

- SOPs and work instructions
- emails or vendor proposals
- process maps
- project plans
- technical designs
- code snippets
- incident summaries
- policy drafts
- meeting notes

## How to get better output

Give the chatbot context:

```text
Context: This is for a food manufacturing operation. The goal is to find operational risk and handoff failure points, not rewrite the document.
```

Ask for evidence:

```text
For every finding, cite the exact sentence, step, or supplied line that supports it. Separate assumptions from evidence; give hypotheses a disconfirming test.
```

Ask for actionability:

```text
After the Prism findings, give me up to three next actions tied to finding IDs, with a checkable success condition. Prioritize evidence collection when a hypothesis is not established.
```

## If the chatbot gets vague

Reply with:

```text
Correct the output once using the selected prompt’s format and operating boundaries. For discovery, return only the domain list. For analysis, cite evidence, separate observations from hypotheses, allow unknown classification or no supported findings, and name what was not examined.
```

## If the table is hard to read

```text
Use one labeled block per finding instead of a wide table. Retain all seven Findings contract fields, in order, plus the actions and coverage gaps.
```

This changes presentation, not the evidence required. See the [linear example](examples/code-review-example.md#an-example-finding-in-a-linear-layout).

## Before acting on a finding

Open the cited source and check that it supports the claim. Supply missing context before treating a hypothesis as an established defect. For a revision, keep the source ID, identify its new version, and provide the old finding IDs for reconciliation. Use an applicable test to verify the proposed fix; a rewritten answer alone is not verification. Use an approved chatbot environment for sensitive work and review what you paste or upload.
