# Functional improvement rationale

Reviewed 2026-10-22 against main commit `07349de725702276a58e7e93722b2a68e960a829`. Prism is a portable prompt pack, not an executing chatbot. This work preserves its five main prompts, seven reference lenses, MIT license, Journey attribution, and direct copy/paste usage.

## Evidence and priorities

The full small repository, AGENTS.md, prompts, lenses, examples, fixtures, validator, tests, and CI were inspected. Baseline: 12 prompt contracts and 8 unit tests passed on Python 3.12.3. Four [PR #1 review concerns](https://github.com/nosliwhtes/prism-analytical-toolkit-chatbot/pull/1/files) were checked against source: incomplete finding-table fields, titled links skipped, discovery asking for analysis, and a forced trade-off instruction. These are source findings, not observed model failures. Additional local reproductions showed a UnicodeDecodeError on invalid UTF-8 and false broken links inside code samples.

Using Gary Klein's premortem method from the creative-ideation workflow, the useful failure cases were: a reviewer cannot locate the evidence; contradictory document versions get silently merged; a partial source is treated as a whole system; a corrected claim survives in the final table; a copied bundle omits its safety/analysis protocol. Cosmetic changes, more generic lenses, and a new chatbot application do not address these failures.

1. **Evidence and usable results:** source/version/coverage handling, complete findings tables, stable IDs, explicit retractions, scoped severity, and next actions with success conditions. Discovery receives its own output rules. Missing context and benign artifacts remain valid outcomes.
2. **Offline integration:** an optional standard-library CLI combines a full prompt with explicit UTF-8 sources, numbered citations, and byte hashes. Fail before output for invalid/oversize inputs; never truncate silently or overwrite existing output. No network, credentials, execution, or live installation.
3. **Reliable maintenance:** fix reproduced validator errors and titled links, check additional prompt files, add CLI/mutation regressions, and expand manual evaluation fixtures. Static contracts remain explicitly distinct from model compliance.

## Alternatives and references

- **Prompt-only changes:** least maintenance, but users must assemble and label every source manually. Still fully supported; this is preferable if the helper's tests and documentation become disproportionate to its use.
- **Prompts plus a small offline composer (selected):** reproducible handoff without a provider dependency. Costs: an optional Python command and longer, self-contained prompts. Byte limits cannot predict each model's context window, and Markdown framing cannot enforce prompt-injection resistance.
- **Provider-driven evaluation or chatbot runtime:** could measure outputs and automate runs, but introduces dependency/provider setup, cost, and an expanded product boundary. Deferred until explicitly wanted with approved evaluation inputs and budget.

Primary references inspected on 2026-10-22:

- [Fabric's standalone patterns](https://github.com/danielmiessler/Fabric#just-use-the-patterns) support keeping reusable prompts usable without adopting the full runtime. Its model/provider setup is not needed here.
- [Promptfoo test cases](https://www.promptfoo.dev/docs/configuration/test-cases/) illustrate explicit inputs, expectations, and per-prompt applicability. That separation informs the fixtures; no Promptfoo installation, runtime, or quality claim is imported.
- [CommonMark link syntax](https://spec.commonmark.org/0.31.2/#links) supports optional titles and angle destinations. The validator implements a documented subset, not CommonMark conformance.

These comparisons confirm the existing project direction; they are not competitive benchmarks. No new managed service is proposed, so pricing research is not relevant. Reconsider this scope if users need actual provider execution, automated outcome scoring, PDF extraction, or guaranteed machine-readable model output.

## Verification approach

Write failing CLI/mutation cases first, implement the bounded behavior, run the complete standard-library suite and compile both scripts, then inspect the diff independently. Review fixtures statically with explicit uncertainty; do not report hypothetical outputs as executed model evaluations. The composer must round-trip source text through its line labels, retain the complete selected prompt, and preserve existing files on error. See [evaluation guidance](../evaluation/README.md) for the distinction between instruction review and empirical testing.
