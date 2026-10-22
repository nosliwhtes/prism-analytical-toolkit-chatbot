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

## Review multiple sources reproducibly

Give each document or excerpt a label, version, and scope using the [review request template](templates/review-request.md). The analysis prompts track source coverage, cite exact evidence, distinguish conflicting versions, and keep finding IDs through corrections. See the [worked multi-source review](examples/multi-source-review.md). These instructions improve traceability; they do not guarantee a chatbot's compliance or correctness.

For local UTF-8 text files, an optional Python helper creates one paste/upload bundle containing the **complete selected prompt**, numbered source lines, and SHA-256 hashes of original source bytes:

```sh
python3 scripts/compose.py --prompt full --artifact proposal.md --artifact requirements.md --context review-context.txt --focus "handoff correctness" --output review-bundle.md
```

Repeat `--artifact` in citation order. Omit `--prompt` for Scan, `--context`/`--focus` when unnecessary, and `--output` to print to stdout. Run `python3 scripts/compose.py --help` for options. The helper only reads the named sources and the selected local prompt; it makes no network/model calls, executes no source code, and refuses to overwrite an existing output. It rejects symlinks in artifact/context paths (including parent directories), non-regular files, missing, empty, non-UTF-8, and NUL-containing inputs. Its default combined source limit is 200,000 bytes, adjustable with `--max-bytes`; oversize inputs fail without truncation. This is **not** a model token/context limit: select smaller excerpts for your chatbot and record omitted parts. PDF, office documents, URLs, and images need text extraction or the chatbot's own upload support.

Secure source reads require POSIX no-follow flags and directory-descriptor support (tested on Linux); unsupported systems fail with an error rather than follow links. Use real, non-symlink source paths. `--output` requires a filesystem supporting hard links: the helper writes and syncs a private staging file in the destination directory, then atomically creates the destination without replacement. Encoding, write, or close failures leave no incomplete destination and handled failures remove the staging file, so a corrected command can retry. Abrupt process termination may leave a private `.prism-bundle-*.tmp` staging file. The direct Markdown copy/paste workflow remains available on all platforms.

Hashes identify bytes, not truth, authority, or document dates. The numbered display normalizes CRLF/CR to LF and omits the final line separator; metadata records original ending counts and whether a final newline was present. This is a readable review copy, not a lossless file export; use original files for byte-sensitive questions. The bundle labels unknown versions as unspecified; supply known versions in context. Review the generated bundle before sharing it: it contains the source text. Use `--output` rather than shell redirection when you need overwrite protection. Keep private bundles outside this public repository; `review-bundle*.md` is ignored as a convenience.

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
python3 -m py_compile scripts/compose.py
```

The validator exits 0 on success and 1 on validation failures, with path/rule diagnostics, including malformed UTF-8. Use `--root PATH` to check a different pack. It checks known prompt-contract regressions and inline local file links (including optional titles, angle destinations, and encoded spaces), ignoring code examples. It is a documented Markdown subset, not a complete CommonMark parser or empirical model evaluation. See the [evaluation fixtures and rubric](evaluation/README.md), [implementation rationale](docs/functional-improvements.md), and [maintenance guidance](AGENTS.md). No runtime packages, lockfile, application build, or model API are needed.

CI uses the Python supplied on GitHub's Ubuntu 24.04 hosted runner and an immutable revision of [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1). The official [checkout documentation](https://github.com/actions/checkout) specifies Node 24 runner support inherited from v5; hosted runners meet this requirement. Dependency review: 2026-10-04. Preserve the pin and verify official release compatibility when updating it.
