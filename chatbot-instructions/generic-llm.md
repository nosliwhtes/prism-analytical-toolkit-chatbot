# Using Prism with Any Chatbot

If the chatbot supports file uploads, upload both the Prism prompt and the artifact. If not, paste the prompt, then paste the artifact.

If the chatbot skips steps, say:

```text
You skipped required Prism steps. Rerun from the beginning. First show the generated lens or operation, then execute it, then give findings with evidence, severity, and fixable-vs-structural classification.
```

Smaller models often need shorter artifacts and stronger reminders to cite evidence.
