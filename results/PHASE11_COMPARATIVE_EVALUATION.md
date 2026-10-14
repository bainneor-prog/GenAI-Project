# Phase 11 — Comparative Evaluation of the BI Workflows

## Scope and evidence boundary

This evaluation compares the implemented traditional Excel/Power BI workflow with the implemented GenAI-assisted Python workflow. It is not a controlled experiment isolating the causal effect of GenAI. Differences may also reflect Python, expanded requirements, additional development effort, researcher experience and iterative verification.

The evidence inventory is [PHASE11_EVIDENCE_INVENTORY.csv](PHASE11_EVIDENCE_INVENTORY.csv), and the dimension-level matrix is [PHASE11_EVIDENCE_MATRIX.csv](PHASE11_EVIDENCE_MATRIX.csv). The traditional artifacts available are the assessment document, Excel workbook and PBIX file under `baseline/`. The binary PBIX and workbook can support artifact inspection, but their internal transformations were not converted into a complete machine-readable audit trail here.

## Executive answer

The GenAI-assisted workflow demonstrably expanded the implemented analytical scope and made the Python calculation, stored-output and evidence-linking chain more explicit. It also added independent audit, blind replication and formal human decision records. These are meaningful advantages in analytical depth, reproducibility, traceability and governance.

The evidence does not demonstrate that GenAI alone caused those improvements, reduced total effort, or produced universally more accurate results. Python, extra project scope and substantial human verification contributed. The available evidence is insufficient to quantify time savings. Reliability is mixed: many calculations were independently checked, but A4/A5 replication was partial, model rankings were configuration-sensitive, and F005 remains deferred under D017.

## Seven-dimension comparison

### 1. Analytical depth — advantage demonstrated for the revised workflow

The traditional artifacts document a conventional descriptive/statistical BI project. The revised workflow added crop-specific and pooled comparisons, interaction families, nonlinear sensitivity, predictive benchmarks, feature contribution analysis and a dedicated EDA workspace. This is broader implemented scope, not proof that GenAI itself caused every addition. The added depth produced useful supported patterns, especially aggregation differences and model-design sensitivity, while also identifying findings that had to be withheld.

### 2. Analytical efficiency — insufficient evidence

No comparable active-hours, task-duration or controlled productivity log was located. AI-assisted code and documentation are evident, but debugging, dependency issues, dashboard redesign and verification also required effort. The available evidence is insufficient to quantify time savings between the traditional and GenAI-assisted workflows.

### 3. Accuracy and reliability — mixed/context-dependent

Phase 7 recorded numerical checks and methodological warnings. Phase 8 reproduced several results directionally or within displayed precision, while A4/A5 were partial and predictive rankings differed under alternative seeds/configurations. Human review accepted six findings with qualifications and deferred F005. Passing checks support specific outputs; they do not prove every assumption or interpretation is valid.

### 4. Reproducibility — advantage demonstrated for available Python artifacts

The revised workflow provides a validated checksum, locked dependency files, executable scripts, fixed seeds, structured outputs, tests and evidence references. The traditional workbook and PBIX remain available and may contain additional traceability, but a complete machine-readable reconstruction of their formulas and transformations is not evidenced in this repository. This is a comparison of documented implementation, not a claim that Excel or Power BI cannot be reproducible.

### 5. Transparency and traceability — advantage demonstrated for the revised workflow

Finding IDs, Analysis IDs, deterministic outputs, evidence references, audit records, blind replication and human decisions form an explicit chain. F001, F003, F005 and F006 can be navigated through the Phase 9 explorer; F005 is explicitly incomplete/restricted. The chain is strongest for stored Python evidence and weaker where external/partial artifacts remain.

### 6. Stakeholder communication — mixed/context-dependent

The traditional workflow includes an assessment and Power BI dashboard. The revised dashboard adds results-first summaries, interactive EDA, business-question pages, qualifications and finding traceability. Phase 10 was human-approved, but no controlled usability study or comparable stakeholder outcome measure exists. Therefore improved communication is a documented design feature and expert-reviewed outcome, not a measured population effect.

### 7. Human oversight, governance and risk — advantage demonstrated for the revised workflow, with added verification cost

The revised workflow explicitly records independent audit, blind replication, evidence gaps, qualified acceptance and deferral. It also exposes GenAI risks: hallucinated interpretations, automation bias, statistical misuse, dependency/tool risk and provenance uncertainty. These controls reduce risk but do not eliminate it. Human decisions remain final, and technical statuses remain distinct from acceptance decisions.

## Effort and automation assessment

- Demonstrably automated: deterministic Python calculations, structured result generation, checksum validation, repeatable model evaluation, evidence-index construction and dashboard loading.
- Required substantial human intervention: governance decisions, method validation, interpretation restrictions, audit comparison, blind-replication unblinding, visual acceptance and final finding decisions.
- Not measurable from available evidence: comparative development time, total labour, time savings, productivity percentage and net verification cost.

## Reproducibility chain spot checks

| Finding | Chain assessment | Evidence basis | Remaining issue |
|---|---|---|---|
| F001 | Complete for stored Python evidence | A002, source checksum, Phase 7/8 checks, Phase 9 decision, dashboard reference | Provenance and units unknown |
| F003 | Complete with supplementary distinction | A016–A022, independent A7, C002, decision log | Pooled/centred statistics must not be substituted |
| F005 | Partially complete / unresolved | A029–A034, D017, partial A4/A5, deferred decision | Cotton specification warning unresolved |
| F006 | Complete for both distinct configurations | A056–A061, independent A1, C006, qualified decision | No universal best model or real-world generalisation |

## Central limitations

The data provenance and units remain UNKNOWN. Traditional artifact internals were not fully machine-extracted. The comparison is not randomized or controlled. Some independent replications were partial. Model performance is within-dataset. No causal agricultural claim, financial benefit or operational recommendation follows.

## Final conclusion

The most defensible conclusion is mixed but favourable to the revised workflow for analytical depth, reproducibility, traceability and governance documentation. No defensible conclusion can be made that GenAI reduced overall effort or universally improved accuracy. The workflow’s value came from GenAI assistance combined with Python, broader scope, independent checking and explicit human oversight. Its credibility depends on retaining those checks rather than treating AI output as authoritative.

Phase 12 and Phase 13 are not started.

