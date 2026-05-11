# Using Prism with Gemini

## Option A: paste directly

1. Open [`../prompts/prism-scan.md`](../prompts/prism-scan.md).
2. Copy the entire file.
3. Paste it into Gemini.
4. Add your artifact below it.

Suggested message:

```text
Use the Prism Scan method I pasted below. Follow every required step. If the artifact is too long, analyze the excerpt and tell me what additional context would change your conclusions.
```

## Option B: upload files

Upload:

- the Prism prompt file you want to use
- the document/code/problem artifact

Then say:

```text
Use the uploaded Prism prompt exactly as the analysis method. Analyze the uploaded artifact. End with concrete findings, severity, fixable-vs-structural classification, and what the analysis did not examine.
```

## Best default for work use

Use `prism-scan` first. Use `prism-full` only when the conclusion matters enough to justify a longer answer.

## Privacy reminder

Use your company-approved Gemini/Workspace environment for work-sensitive documents. Do not paste confidential or regulated content into a personal/public chatbot.
