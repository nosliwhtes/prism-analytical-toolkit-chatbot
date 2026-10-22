# Quickstart

## 60-second version

1. Copy [`prompts/prism-scan.md`](prompts/prism-scan.md).
2. Paste it into Gemini, ChatGPT, Claude, or another chatbot.
3. Add this:

```text
Use the Prism Scan method on this artifact. Follow all steps. Do not give generic advice. End with a findings table and a short action list.
```

4. Paste your artifact.

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
For every finding, cite the exact sentence, step, line, or assumption that supports it.
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
