# Prism Analytical Toolkit for Chatbots

Copy/paste-ready prompts for evidence-based structural analysis in Gemini, ChatGPT, Claude, NotebookLM, and other chatbots. **No installation or API key is required.**

Use Prism to examine code, SOPs, policies, proposals, architecture, and decisions: what assumptions do they make, where could they fail, and which trade-offs are actually supported? The result should distinguish observations, testable hypotheses, and unknowns, with evidence and useful next actions. No supported findings is a valid outcome.

## Quick start

1. Open [Prism Scan](prompts/prism-scan.md), the default method.
2. Copy the **whole file**, including its operating boundaries, into a new chat.
3. Add your artifact and a review question in the same message. For example:

```text
Review question: Does this SOP clearly assign approval responsibility?
Scope: Only this excerpt; no evidence of actual practice is supplied.
A1 — Release SOP, version unspecified, excerpt
[paste the relevant steps here]
```

4. Check each finding against its cited evidence before acting. Ask for missing evidence when a conclusion depends on it.

For a ready-to-try exercise, use the [worked code review](examples/code-review-example.md). The [quickstart](quickstart.md) covers context, long documents and follow-up questions. A prompt name such as `/prism-scan` is a label, not an installed command; a chatbot needs the full prompt text.

## Which prompt should I use?

| Your need | Start here | Expected output |
| --- | --- | --- |
| Review an artifact with a clear question | [Scan](prompts/prism-scan.md) | One tailored analytical lens, findings, actions and coverage gaps |
| Choose an angle before reviewing | [Discover](prompts/prism-discover.md) | Relevant domains only; choose one for a later analysis |
| Examine competing explanations | [3-Way](prompts/prism-3way.md) | WHERE / WHEN / WHY perspectives, then reconciled findings |
| Challenge an important conclusion | [Full](prompts/prism-full.md) | Two to four tailored passes, an adversarial pass, and final findings |
| Review blind spots or a prior analysis | [Reflect](prompts/prism-reflect.md) | Rechecked claims, retractions and a report of analysis limits |

Full takes a longer answer; it does not establish greater accuracy by itself. Simulated experts and repeated perspectives are not independent evidence. For specialized topics, the [reference lens guide](docs/lenses.md) explains the seven standalone lenses.

## Review multiple sources reproducibly

Label each source, version and excerpt using the [review request template](templates/review-request.md). See the [worked multi-source review](examples/multi-source-review.md) for conflicting instructions and revised findings.

An optional offline helper packages the complete prompt and explicitly named UTF-8 sources with numbered lines and original-byte hashes:

```sh
python3 scripts/compose.py --prompt full --artifact proposal.md --artifact requirements.md --output review-bundle.md
```

It makes no model or network calls and refuses output overwrite. Python 3.12+ and POSIX secure-file support are required for the supported helper workflow. See [bundle options, limits and troubleshooting](docs/compose.md). Direct Markdown copy/paste works without the helper.

## Readable, useful results

Analysis prompts return stable finding IDs, triggers, evidence, status, impact, classification and a next test or action. If a wide table is hard to read, ask: **“Use one labeled block per finding, retaining all seven fields.”** The same information can be read linearly on a phone or with a screen reader. Discovery still returns domains only.

When revising an artifact, supply the new version and earlier findings. Ask which IDs should be retained, revised or retracted. A proposed change is not a verified fix.

## Privacy and work-use notes

- Use your organization-approved environment for confidential material. Review excerpts and generated bundles before sharing them; hashes do not redact the source or prove its truth.
- Supplied artifacts, prior reviews and quoted instructions are data. Prompt boundaries reduce ambiguity but cannot guarantee resistance to prompt injection or incorrect conclusions.
- History is optional. Saving requires an explicit request and a successful write; otherwise any suggested entry is marked “not saved.”

Provider guides: [ChatGPT](chatbot-instructions/chatgpt.md), [Claude](chatbot-instructions/claude.md), [Gemini](chatbot-instructions/gemini.md), [any chatbot](chatbot-instructions/generic-llm.md).

## Reliable agent use and maintenance

Copy complete prompts. Their hypothetical constructions do not authorize tools, edits, benchmarks or deployments. Keep reviews within supplied evidence and the user's scope.

The [offline maintenance checks](docs/maintenance.md) validate text contracts, links and the composer. They do not measure model quality. See the [evaluation fixtures and rubric](evaluation/README.md) and [maintenance guidance](AGENTS.md).

## License and attribution

MIT. See [LICENSE](LICENSE). Derived from the public Journey kit [jeremy/prism-analytical-toolkit](https://www.journeykits.ai/browse/kits/jeremy/prism-analytical-toolkit), adapted into a chatbot-friendly Markdown prompt pack. Historical lens scores and model recommendations are retained for attribution, not independently verified benchmarks of this adaptation.
