# Static walkthrough — 2026-10-22

Evaluator: implementation agent. Method: source/instruction consistency review across all five main prompts and seven reference lenses, using [fixtures.json](fixtures.json). This is **not** an executed model evaluation. There are no sampled model answers or model/version results. Automated CLI checks are separate. Independent code-review findings are tracked in the pull request description.

| Fixture | Instruction-level review and evidence | Remaining uncertainty |
| --- | --- | --- |
| benign | Analysis boundaries allow no findings; Deep Scan now tests whether a trade-off exists. Findings contract prohibits filling rows just to meet a quota. | A model may still invent a concern; no response sampled. |
| known_bug | Code-review lenses allow a fixable empty-suffix bug, cite exact evidence, and request a next test. Performance costs remain unmeasured. The Python slicing behavior was separately checked locally. | Not all lenses focus on string semantics; no recall score claimed. |
| incomplete_context | Every prompt treats quoted vendor instructions as data. Analysis limits claims to available code; Optimize requires measured/derived costs or unmeasured status. | Prompt instructions cannot enforce injection resistance. |
| missing_artifact | Analysis asks for a usable artifact and stops; discovery expressly permits this exception to its domain-only list. A URL alone is not reviewed content. | No provider attachment behavior tested. |
| conflicting_sources | Evidence and scope keeps A1/A2 and versions distinct, requires explicit comparison, and forbids silently choosing authority. The worked example limits its observation to textual inconsistency. | Real authoritative versions and workflow effects are unknown. |
| partial_coverage | Analysis records partial coverage, accepts existing line labels, and does not equate an excerpt omission with system-wide absence. | Context-window loss across turns is not detectable by this pack. |
| retract_prior_claim | Findings contract preserves IDs through retraction; Full and Reflect exclude retracted claims from the final actionable table. Repetition and prior analysis do not add evidence. | Actual adherence requires model output evaluation. |

Discovery was checked separately: no findings contract is included, and its boundary no longer asks for hypotheses, tests, improvements, or constraints. All analysis formats retain the required evidence/status and next-test/action fields, including lenses with specialized details. Historical lens metadata remains attribution, not a new quality claim.

No saved model-quality score, comparative superiority claim, external API call, or automatic pass/fail rating of model responses is warranted by this walkthrough.
