# Prism Analytical Toolkit for Chatbots

A plain-English, copy/paste-ready version of the Prism Analytical Toolkit for use with Gemini, ChatGPT, Claude, NotebookLM, and human colleagues.

Prism helps a chatbot do deeper structural analysis instead of ordinary surface review. It is useful for code reviews, process reviews, strategic decisions, policies, business plans, architecture proposals, and documents where you suspect hidden trade-offs or recurring failure patterns.

Original Journey kit: https://www.journeykits.ai/browse/kits/jeremy/prism-analytical-toolkit

## Quick start

1. Open one of the files in [`prompts/`](prompts/).
2. Copy the full prompt into your chatbot.
3. Paste the artifact, document excerpt, code, or problem you want analyzed.
4. Ask the chatbot to follow every step and end with concrete findings.

Best default: [`prompts/prism-scan.md`](prompts/prism-scan.md)

## Which prompt should I use?

- **prism-scan**: default for most work. Use this first.
- **prism-discover**: use when you are not sure what kind of analysis would be useful.
- **prism-3way**: use when there are competing explanations or disagreement about the problem.
- **prism-full**: use for high-stakes reviews where the chatbot must challenge its own findings.
- **prism-reflect**: use when you want to know what the analysis itself missed or biased toward.

## Recommended work prompt

```text
I want you to use Prism Scan on the artifact below.

Goals:
- find hidden assumptions, structural trade-offs, and recurring failure patterns
- separate fixable problems from structural constraints
- avoid generic advice
- cite specific evidence from the artifact
- end with a short action list

Artifact:
[paste code, plan, policy, process, or decision here]
```

## For colleagues

Send them this repo and suggest starting with:

- [`quickstart.md`](quickstart.md)
- [`prompts/prism-scan.md`](prompts/prism-scan.md)
- [`examples/document-review-example.md`](examples/document-review-example.md)

No install is required. This repo is just Markdown prompts.

## For Gemini

Gemini usually works best if you either:

- paste the full prompt file directly into the chat, or
- upload the prompt file and the document you want reviewed, then say: "Use the uploaded Prism prompt exactly."

See [`chatbot-instructions/gemini.md`](chatbot-instructions/gemini.md).

## Privacy and work-use notes

- Do not paste confidential work data into public chatbots unless your company permits it.
- For sensitive material, use your company-approved AI environment.
- Prism can surface security, operational, or compliance weaknesses. Share findings responsibly.
- `prism-reflect` mentions a `.prism-history.md` growth log in the original agent version. For normal chatbot use, treat that as optional notes you keep privately, not something to publish.

## License

MIT. See [`LICENSE`](LICENSE).

## Attribution

Derived from the public Journey kit `jeremy/prism-analytical-toolkit`, adapted into a chatbot-friendly Markdown prompt pack.
