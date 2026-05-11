# Quickstart

## 60-second version

1. Copy [`prompts/prism-scan.md`](prompts/prism-scan.md).
2. Paste it into Gemini, ChatGPT, Claude, or another chatbot.
3. Add this:

```text
Use the Prism Scan method on this artifact. Follow all steps. Do not give generic advice. End with a findings table and a short action list.
```

4. Paste your artifact.

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
After the Prism findings, give me the three changes that would reduce the most risk this week.
```

## If the chatbot gets vague

Reply with:

```text
Rerun the analysis. Your last answer was too generic. Use specific evidence from the artifact, classify each issue as fixable or structural, and name what your analysis did not examine.
```
