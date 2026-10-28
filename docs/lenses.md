# Choose a reference lens

Start with [Scan](../prompts/prism-scan.md) unless you already know the question to investigate. These seven lenses offer a specific analytical approach. Copy the **entire selected file**, including its boundaries and findings contract, then add the artifact and scope. No main prompt or tool installation is needed alongside it.

| Lens | Useful question | Limit to keep in view |
| --- | --- | --- |
| [Claim](../reference-prisms/claim.md) | Which empirical assumptions could change the conclusion if false? | An inverted assumption is a hypothesis, not contrary evidence. |
| [Deep Scan](../reference-prisms/deep_scan.md) | Do boundaries, error handling or composition hide a code defect? | A suspicious pattern is not a bug without a failing contract or behavior. |
| [Error Resilience](../reference-prisms/error_resilience.md) | Does lost error context lead to a wrong decision downstream? | Stop at unavailable implementations; information loss alone is not harm. |
| [Identity](../reference-prisms/identity.md) | Does an interface's actual behavior match its promises? | A difference may be intentional, accidental or unknown. |
| [L12](../reference-prisms/l12.md) | Does a proposed structural constraint survive a counterexample? | No constraint is a valid result; a recurring pattern is not a theorem. |
| [Optimize](../reference-prisms/optimize.md) | Which boundaries might conceal a measurable cost? | Costs remain unmeasured without supplied measurements or a transparent derivation. |
| [Simulation](../reference-prisms/simulation.md) | How might the artifact behave through maintenance and growth? | Scenarios are conditional; success and inapplicable cycles are valid. |

Use one relevant lens for a focused review. More perspectives do not supply more evidence. If a lens is inapplicable, choose another or return to Scan. Historical metadata in these files is attribution, not a verified quality score or current model recommendation.
