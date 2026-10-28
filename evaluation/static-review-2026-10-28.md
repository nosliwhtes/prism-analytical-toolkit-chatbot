# Review and verification — 2026-10-28

Base: `ddc58b0769b89c808401fc03fdede408d4d6f4a9`. Evaluator: implementation agent. Environment: Linux, Python 3.12.3. The source and instruction review below is **static**, not an executed chatbot evaluation. Local CLI checks are identified separately. No private sources, paid providers, model APIs or new runtime dependencies were used.

## Purpose and scope

Prism is a portable Markdown pack for colleagues reviewing code, SOPs, policies and decisions. Its five main methods and seven reference lenses guide structural analysis with evidence, uncertainty, bounded passes and optional history. The optional offline composer packages explicit text sources; the validator checks text contracts and a documented subset of local Markdown links. The no-install copy/paste path, existing prompt choices, license and Journey attribution remain intact.

Using the creative-ideation skill's spine method (Twyla Tharp), the design constraint was: make evidence-based structural review easier to use without requiring a chatbot application or provider integration. Minimizer's first fitting implementation was to reuse the secure file reader and existing output contract, not introduce another file-access layer or output schema.

Priorities and observed evidence:

1. **Secure and reliable inputs:** the selected prompt used direct `read_text()`, bypassing the composer's no-follow file reader. An isolated synthetic leaf link and parent link could replace the protocol with a harmless external marker; a FIFO blocked until the test timeout. Prompt reads now use the same descriptor checks as artifacts/context and reject malformed text before output. No actual private disclosure was observed.
2. **Faithful handoff:** discovery bundles appended a citation instruction inconsistent with domain-only output. The wrapper now preserves discovery's format. Source text containing terminal or bidirectional controls now displays visible escapes; hashes, byte counts and line labels still describe original bytes. This display is explicitly not lossless or a general sanitization boundary.
3. **Usable analysis:** seven-column findings tables had no explicit linear alternative. All eleven analysis prompts/lenses now permit labeled blocks with the same fields and order. Scenario questions in Scan, 3-Way and Simulation no longer presume something must break. The front page routes readers to the right prompt, a complete worked request and the helper/reference/maintenance guides.
4. **Maintenance and performance:** unmatched `[` characters caused repeated scans of the same suffix. Excluding raw nested openers from the supported label pattern fixes this case without claiming nested-label support. The validator now checks the complete findings header, so removing impact or classification fails a mutation test.

The work does not introduce a frontend, provider runner or new analysis method. A frontend design system is therefore not applicable. No application UI, build or type checker exists in this repository.

## Static fixture walkthrough

Reviewed the complete changed prompts and sibling lenses against all nine [fixtures](fixtures.json), with discovery's format checked separately. These observations concern instructions, not sampled model answers.

| Fixture | Instruction evidence and expected behavior | Limit |
| --- | --- | --- |
| benign | Operating boundaries and Findings contract permit no findings; scenario wording now also permits success. | A model may still invent a defect. |
| known_bug | Evidence and scope supports exact code citations; the worked example identifies the empty-suffix error without requiring an invariant. | Lens applicability varies; no recall score is measured. |
| incomplete_context | Supplied vendor instructions remain data; no execution, fake timing or saving is authorized. | Text instructions do not enforce prompt-injection resistance. |
| missing_artifact | All methods request readable contents and stop; discovery retains this explicit exception. | Provider attachment reading is untested. |
| conflicting_sources | Source IDs, versions and uncertain authority remain separate; format changes do not remove evidence fields. | Actual applicable authority is not supplied. |
| partial_coverage | Excerpt omissions do not establish whole-system absence; Simulation now repeats that caution in its knowledge-loss scenario. | The pack cannot detect a provider's silent context truncation. |
| retract_prior_claim | Full/Reflect and the shared contract keep IDs, record retractions and exclude them from actionable findings. | Actual model reconciliation is unmeasured. |
| scenario_safeguards | 3-Way and Simulation explicitly consider existing safeguards, no-failure outcomes and inapplicable scenarios. | Hypothetical growth cannot establish a measured capacity limit. |
| linear_format | Every analysis prompt/lens permits labeled blocks containing all seven fields in order, overriding later table references for presentation only. Discovery remains domains-only. | No screen-reader session or model-format compliance test was performed. |

## Executed verification

Baseline: static validator passed all 12 contracts; 64 unit tests passed; both scripts compiled.

New regressions were exercised before implementation: linked prompt acceptance, the prompt FIFO timeout, raw source control characters, discovery citation instructions, unmatched-bracket timeout and missing findings fields were reproduced. The final suite retains the original checks for byte limits, UTF-8, symlinks, reparse-point simulations, atomic no-overwrite output, failed-write cleanup, concurrent writers and link safety.

Final commands:

```sh
python3 scripts/validate.py --json
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/validate.py scripts/compose.py
git diff --check
```

Final results: **12 prompt contracts and all local file links passed; 69 tests passed; both scripts compiled; `git diff --check` passed.** The test run completed in 2.341 seconds on this machine. The five additional tests contain multiple input cases, including linked prompt parents, FIFOs, invalid UTF-8, empty and NUL-containing protocol files.

A separate end-to-end CLI smoke check used temporary synthetic proposal, requirements and context files with all five prompt choices. Each saved bundle retained its complete selected prompt, A1/A2/C1 line labels, original hashes and unchanged inputs, used mode 0600, and refused a second write without modifying the first output. The worked example's original empty-suffix error was reproduced locally; its candidate fix passed five explicit cases (empty suffix, present suffix, absent suffix, repeated suffix, empty text). All nine evaluation fixtures parsed with distinct IDs. These checks did not send a bundle to a chatbot.

Live chatbot/provider evaluation, native Windows execution and assistive-technology testing remain unrun. No application build or configured type checker applies.

### Targeted timing experiment

On the same Linux/Python process, each parser was called three times per input; the table gives median wall time. Inputs were repeated unmatched `[` characters followed by an ordinary `[valid](README.md)` link. Both versions returned that link. The baseline implementation was loaded from the base Git commit; nothing was fetched or installed for this experiment.

| Unmatched brackets | Baseline seconds | Revised seconds |
| --- | --- | --- |
| 1,000 | 0.007905 | 0.000130 |
| 5,000 | 0.167352 | 0.000622 |
| 10,000 | 0.653594 | 0.001235 |

The regression uses 100,000 brackets and a five-second subprocess timeout to catch the stall. These observations support this input-specific improvement, not a general linear-time or CommonMark-conformance claim.
