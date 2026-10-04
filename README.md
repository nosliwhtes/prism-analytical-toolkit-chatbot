# Prism Analytical Toolkit for Chatbots

A plain-English, copy/paste-ready version of the Prism Analytical Toolkit for use with Gemini, ChatGPT, Claude, NotebookLM, and human colleagues.

Prism helps a chatbot do deeper structural analysis instead of ordinary surface review. It is useful for code reviews, process reviews, strategic decisions, policies, business plans, architecture proposals, and documents where you suspect hidden trade-offs or recurring failure patterns.

Original Journey kit: https://www.journeykits.ai/browse/kits/jeremy/prism-analytical-toolkit

## Quick start

1. Open one of the files in [`prompts/`](prompts/).
2. Copy the full prompt into your chatbot.
3. Paste the artifact, document excerpt, code, or problem you want analyzed.
4. Ask the chatbot to follow the selected format: domains for discovery, evidence-grounded findings for analysis. No supported findings is a valid result.

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

No install is required to use the Markdown prompts. Optional offline maintenance checks use only Python’s standard library.

## For Gemini

With Gemini, you can either:

- paste the full prompt file directly into the chat, or
- upload the prompt file and the document you want reviewed, then say: "Use the uploaded Prism prompt exactly."

See [`chatbot-instructions/gemini.md`](chatbot-instructions/gemini.md).

## Privacy and work-use notes

- Do not paste confidential work data into public chatbots unless your company permits it.
- For sensitive material, use your company-approved AI environment.
- Prism can surface security, operational, or compliance weaknesses. Share findings responsibly.
- History is optional in every prompt. No files are written without an explicit saving request and capability; otherwise the suggested entry is returned as text with “not saved” status.

## License

MIT. See [`LICENSE`](LICENSE).

## Attribution

Derived from the public Journey kit `jeremy/prism-analytical-toolkit`, adapted into a chatbot-friendly Markdown prompt pack.

## Reliable agent use and maintenance

Copy a complete prompt, including its operating boundaries. Slash names are labels, not installed commands. Supply the artifact and relevant context; no tools or filesystem are required. Discovery returns only domains. Analysis separates observations from hypotheses, permits empty findings, and stops after the specified passes. Hypothetical constructions are not authorization to execute code or edit files.

Reference lenses retain historical upstream metadata for attribution. Their scores and model recommendations are not independently verified benchmarks of this adaptation. Simulated experts and repeated in-chat perspectives do not provide independent evidence.

Run the offline checks from the repository root with Python 3.12 or newer:

```sh
python3 scripts/validate.py --json
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/validate.py
```

The validator exits 0 on success and 1 on validation failures, with path/rule diagnostics. It checks known prompt-contract regressions and inline local file links, not empirical model quality. See the [evaluation fixtures and rubric](evaluation/README.md) and [maintenance guidance](AGENTS.md). No runtime packages, lockfile, application build, or model API are needed.

CI uses the Python supplied on GitHub's Ubuntu 24.04 hosted runner and an immutable revision of [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1). The official [checkout documentation](https://github.com/actions/checkout) specifies Node 24 runner support inherited from v5; hosted runners meet this requirement. Dependency review: 2026-10-04. Preserve the pin and verify official release compatibility when updating it.
