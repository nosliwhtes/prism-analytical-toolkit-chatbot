# Using Prism with Any Chatbot

If the chatbot supports file uploads, upload both the Prism prompt and the artifact. If not, paste the prompt, then paste the artifact.

If the chatbot skips steps, say:

```text
Your previous output missed the selected Prism prompt’s format. Correct it once using that prompt’s operating boundaries and output format. For prism-discover, return only the domain list; do not add a lens or findings. For analysis prompts, cite evidence and distinguish observations, hypotheses, and unknowns. Do not invent missing context.
```

For long artifacts, provide relevant excerpts with enough context to assess each claim.
