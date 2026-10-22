# Using Prism with Any Chatbot

If the chatbot supports file uploads, upload both the Prism prompt and the artifact. If not, paste the prompt, then paste the artifact.

If the chatbot skips steps, say:

```text
Your previous output missed the selected Prism prompt’s format. Correct it once using that prompt’s operating boundaries and output format. For prism-discover, return only the domain list; do not add a lens or findings. For analysis prompts, cite evidence and distinguish observations, hypotheses, and unknowns. Do not invent missing context.
```

For long artifacts, provide relevant excerpts with enough context to assess each claim.

Use the [review request template](../templates/review-request.md) to label sources, versions, and omitted sections. If local files are available, the optional [offline composer](../README.md#review-multiple-sources-reproducibly) prepares a single paste/upload bundle. It does not contact or configure any chatbot. If you revise an artifact, retain its source ID, identify the new version, and ask the chatbot to recheck affected finding IDs; a changed file alone does not prove a finding fixed.
