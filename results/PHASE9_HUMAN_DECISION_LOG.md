# Phase 9 Human Decision Log

These are recorded human instructions, not AI approvals. The recording timestamp is when the instruction was entered; no reviewer identity, signature, or personal inspection date was supplied.

| Finding | Decision | Recorded wording/reason | Qualifications and outstanding issues | Evidence |
|---|---|---|---|---|
| F001 | ACCEPT_WITH_QUALIFICATIONS | Within the analysed dataset, mean yield differs between crop groups. These differences are descriptive and do not establish causal crop effects. | Provenance and units remain unknown. | E001–E003, E029 |
| F002 | ACCEPT_WITH_QUALIFICATIONS | Within the analysed dataset, fertiliser use shows positive crop-specific associations with yield. | Correlation is not evidence that increasing fertiliser causes a particular improvement. | E004–E007, E029 |
| F003 | ACCEPT_WITH_QUALIFICATIONS | Rainfall–yield association is substantially stronger within crop groups than in the pooled dataset. | Pooled, crop-specific and within-crop-centred statistics remain distinct; no causation. | E008–E010, E029 |
| F004 | ACCEPT_WITH_QUALIFICATIONS | Tested irrigation group comparisons did not show statistically significant yield differences after relevant corrections. | Failure to detect significance does not establish no irrigation effect; no management recommendations. | E011–E014, E029 |
| F005 | DEFER | Cotton RESET/specification warning unresolved; D017 remains active; coefficient interpretation withheld. | A4 partial; fit results remain technical evidence only. | E015–E019, E029 |
| F006 | ACCEPT_WITH_QUALIFICATIONS | Several tested models predicted crop yield accurately within this dataset, but the best model depended on evaluation design and configuration. | Preserve primary gradient-boosting and independent linear rankings; retain crop-mean comparator; no universal best model or real-world generalisation. | E020–E025, E029 |
| F007 | ACCEPT_WITH_QUALIFICATIONS | Under tested Random Forest configurations, crop type dominated, followed by fertiliser use and rainfall. | Predictive importance is not causal influence. | E026–E028, E029 |

**Decision source for every row:** explicit human instruction supplied for Phase 9 recording. Technical `Status` remains `UNVERIFIED`; `Human_Decision_Status=RECORDED` distinguishes this decision record from completion of all technical checks.

