# C0: Cross-Document Notes (C1 Evaluation Framework × C2 HITL × C3 Data Strategy)

- **Documents:**
  - C1 = "Comprehensive Evaluation Framework…" (1NorDRR7071Bwpy3zRQBXsjQEKEZsnIqCZBwtiHh5ZVA)
  - C2 = "Architecture and Governance of HITL AI Assessment Systems" (1AdZykV6boZ19Wrd781mmEgf5GEWKY1DBJ4DTjAnbKlo)
  - C3 = "Comprehensive Data Strategy and Governance Framework…" (1zo9Blx60j-pQ4B1hIOu_VW7RVy8_dcPROJ2ixdLsN54)
- **Corroboration caveat.** [Analyst note] All three are AI-generated deep-research reports in the same style, and they **share sources**:
  - ResearchGate 414037845 ("Responsible AI-Assisted Assessment…") appears in C1 and C2.
  - arXiv 2609.05143 appears in C1 and C2.
  - arXiv 2606.12422 appears in C1 and C3.
  - The Iowa generic-scorer thesis appears in C1 and C3.
  - The NAPLAN AES report appears in C1 and C3.

  Where the docs agree, that is **not independent corroboration**. Almost every numeric threshold in all three is un-sourced or carries unresolvable `[cite: N]` markers.

---

## 1. Contradictions between the docs

| # | Topic | C1 (Evaluation) | C2 (HITL) | C3 (Data) | Which is better supported? [Analyst note] |
|---|---|---|---|---|---|
| 1 | **Human review for high-stakes / board exams** | 30–50% *auto* coverage ("assisted mode") for SSC/HSC and entrance exams; "dual human-AI moderation" | **100% human review**, Human-in-Command; masked AI recommendations; no grade final without affirmative human sign-off | Implicitly every script goes through teacher verification; no auto-finalization discussed | **C2.** It fits C1's own warnings on boundary errors and automation bias, GDPR Art. 22 (for later expansion), and the reputational stakes of public board results in Bangladesh. C1's 30–50% has no source. |
| 2 | **QWK target (item scoring)** | Gate ≥ 0.85; table target 0.88, minimum 0.78, halt < 0.70; principle: target = measured human IRR | ≥ 0.80 (auto subset); ≥ 0.88 routing/term; **≥ 0.95 board**; ≥ 0.75 homework | CQ Parts B/C/D ≥ 0.75; halt < 0.70 | **C1's principle** (target relative to measured Bangladeshi human-vs-human QWK) is best supported psychometrically. C2's 0.95 exceeds the human κ 0.70–0.85 that C2 itself cites. C3's 0.75 is the most realistic as an initial bar for 2–4-mark CQ parts. |
| 3 | **Medium-stakes review rate** | Not specified (formative 5–15% review implied by 85–95% coverage) | Term exams 25–35% review; exec summary says 35–65% auto-processed; the routing math allows auto-finalize only for MCQ | Not specified | **None.** C2 is internally inconsistent: with r3 ≥ 0.2 for all constructed responses, CRI ≥ 0.20 always, so no CQ answer can auto-finalize. Rates must come from local risk-coverage curves. |
| 4 | **OCR CER target** | Stage ≤ 5%; table ≤ 3% target / ≤ 8% minimum / > 12% halt; cites **≈ 10.89%** CER for fine-tuned TrOCR on real Bangla handwriting | None | **< 2.5%** (Table 4 and Table 8), from 150k training lines | **C1's cited evidence (≈ 10.89%)** is the only empirical anchor, and it undermines both C1's ≤ 3–5% and C3's < 2.5%. Use tiered targets and measure semantic preservation (negations, numbers) rather than CER alone. |
| 5 | **Gold-standard definition** | Adjudicated senior-examiner consensus; discrepancy > ~1 mark triggers adjudication | Two raters within ≤ 1 point: **arithmetic mean** becomes gold candidate; > 1 point goes to Senior Subject Lead | Two blind raters, then adjudicator; batch gold at QWK ≥ 0.75 (elsewhere ≥ 0.85) | **C1/C3 (adjudication)** are better supported for benchmarks. C2's averaging produces non-integer "gold" labels and blurs rater variance. A fixed "1 point" is scale-dependent: total disagreement on a 1-mark CQ part A. |
| 6 | **Gold / eval dataset size** | ≥ 400 independently scored scripts **per subject stratum** (3 raters) | Rule sandbox = 1,000 historical papers; no gold size | Teacher calibration network 5k–20k scripts; calibration set 20k multi-rater; B/C/D 100k; OCR 150k lines | Not directly contradictory; they serve different purposes (eval vs training). C1's 400 is too small to verify its own rare-event gates (≤ 0.05–0.1% severe errors need thousands of scripts). C3's 20k multi-rater set is costly. **Suggest:** ≥ 400 adjudicated per subject × sub-part for acceptance; larger sets for training. |
| 7 | **Raw image retention vs audit/appeal** | Every mark must link to the original raw image; appeals go to a senior examiner with the evidence log | Immutable audit log with hash of raw script; guaranteed human regrade on request | **Raw scans purged after 30 days**; redacted kept contract (+2 years); **audit logs 365 days**; system logs 90 days | **Conflict.** C3's 30-day purge could precede result publication and re-scrutiny windows. C3's 365-day audit retention undercuts C2's reconstructibility. Resolve by retaining *redacted* images plus hashes through the full appeal window (set per board or school calendar) and keeping audit logs ≥ the institutional record period. |
| 8 | **When teachers must justify overrides** | "Critical correction" = edits > ±10%; severity: 6–20% moderate, > 20% major | **Every override** needs a primary reason code (optional text/voice) | Lifecycle table: mandatory reason dropdown; feedback section: structured justification only for **> 20% variance** | **C2** (reason code on every override, short list) is cheap and gives better data. C3 is internally inconsistent. |
| 9 | **Teacher-consistency threshold** | Not specified | Quarantine overrides from teachers with **Cohen's κ < 0.60** | Intra-teacher grading consistency **QWK ≥ 0.80** (calibration alert) | They measure different things (C2: agreement for training eligibility; C3: consistency monitoring). Neither is sourced. κ 0.60 as a quarantine floor is more conventional. |
| 10 | **Automation-bias UI** | Never present pre-selected final scores; evidence and rubric first; teacher input before the AI score is revealed | Quick-review cell shows **pre-filled scores with one-click sign-off**; masking only in **5%** of routine reviews and in the full-manual cell | Marks hidden until the teacher clicks "Evaluate Script" | **C1/C3** match the automation-bias evidence C1 cites (PNAS Nexus via PsyPost; itself secondary). C2's one-click pre-filled sign-off is exactly the pattern C1 warns against. Product choice: default hide-first for high stakes; allow pre-fill for low stakes with 5% random masking as a monitor. |
| 11 | **Learning from teacher corrections** | Appeal overrides go to the regression evaluation DB | **Immediate (< 100 ms) RAG injection** of corrections; rules < 24 h (or "< 1 s"); SFT/DPO monthly or quarterly after validation | Overrides are **staged, filtered and sample-audited** before fine-tuning; training use requires the institution's **opt-in addendum** | Partly contradictory. C2's immediate RAG exemplar injection bypasses C3's staging and possibly its opt-in rule, if exemplars cross tenants. **C3's gating plus C2's tenant-isolated L3 memory** is the defensible combination: immediate use only within the same exam or tenant; cross-tenant only after validation and opt-in. |
| 12 | **Teacher identity in feedback data** | — | Feedback events carry an **anonymized teacher ID**; audit logs carry the teacher ID | Schema stores a `teacher_id` UUID in assessment records | Minor. C2 needs identifiable teacher IDs for its own κ-quarantine and poisoning defence. Use pseudonymous IDs with a controlled re-identification key. |
| 13 | **Minimum scan quality** | Eval set deliberately includes **150 DPI** scans and mobile photos | — | Ingestion rejects **< 200 DPI** (300 recommended) | Complementary if C1's set is a stress test. Otherwise conflicting: the eval set should mirror the ingestion gate, and C1's low-DPI slice then measures the gate's rejection behaviour. |
| 14 | **Cost per script** | Target ≤ $0.08; minimum ≤ $0.25; halt > $0.50; LLM $0.02–0.25/script | $0.01 compute; HITL total $13,500 per 100k (**arithmetic error**; correct ≈ $5,000), i.e. $0.05–0.135/script | **$0.232 per 8-page script** ($0.064 OCR, $0.16 sampled review) | **C3** is the most itemized. C2's compute assumption is likely too low and its arithmetic is wrong. All use USD and unsourced labour rates ($10/h in C2); none uses Bangladeshi examiner remuneration. |
| 15 | **Time saving** | Target ≥ 60%, minimum ≥ 35% | "Up to 40%" instructor time reduction; override edit time 45 s → 12 s | — | **C2's "up to 40%"** is closer to reported studies. C1's ≥ 60% target is aspirational. |
| 16 | **Drift / halt triggers** | Guardrails: QWK < 0.70, severe error > 0.1%, hallucination > 1%, fairness Δ > 0.02; KL > 0.05 | **PSI > 0.25 halts auto-approval** | **QWK < 0.70 halts pipeline**; curriculum version triggers re-benchmark | Complementary. C1 and C3 agree on QWK < 0.70 (possibly shared generation). Combine: QWK/MAE guardrails on audited samples, PSI on score distributions, curriculum-version re-benchmark. |
| 17 | **Training-data strategy** | — | Lists centralized / tenant-isolated / federated without choosing | Recommends **institutional opt-in** (called Option C, and "Strategy B" in the summary); federated rated "very high" complexity | **C3** gives a clear recommendation with legal separation (DPA vs addendum). |
| 18 | **CQ higher-order Part D (4 marks)** | High stakes: strict tolerance | **Mandatory human approval** for the 4-mark part | Trains B/C/D models to QWK ≥ 0.75 | Compatible: C3 trains, C2 routes. **C2's routing** is the safer product rule until Part-D agreement is proven against a human baseline. |
| 19 | **Who administers SSC/HSC** | "Public boards" | "NCTB regulates SSC/HSC examinations" | "All **eight** general education boards" | [Analyst note] Both C2 and C3 contain errors. NCTB sets curriculum and textbooks; exams are run by education boards (nine general boards plus Madrasah and Technical). |
| 20 | **Legal treatment** | None | Platform-policy guarantees only (human final authority, regrade right, ZDR) | Heavy Bangladeshi and international claims; conflates PDP Ordinance 2025 with "PDP Act 2026 (Law 63 of 2026)"; CSA 2023 / Ordinance 2025 / CSA 2026 blended; COPPA § 312.8 mis-cited; EU AI Act omitted | Only C3 makes legal claims, and they are **Low credibility**. Commission independent verification against official gazettes. |

---

## 2. Consolidated metrics table

"—" means the doc gives no target. Targets are quoted as stated; contradictions within a doc are shown with a slash.

| Metric | Definition (as used) | C1 target(s) | C2 target(s) | C3 target(s) | [Analyst note] suggested PRD stance |
|---|---|---|---|---|---|
| Quadratic Weighted Kappa (QWK) | κ_w = 1 − ΣwO/ΣwE, w_ij = (i−j)²/(k−1)² | Gate ≥ 0.85; target 0.88 / minimum 0.78 / halt < 0.70; ≥ human IRR | Auto subset ≥ 0.80; routing/term ≥ 0.88; board ≥ 0.95; homework ≥ 0.75 | B/C/D ≥ 0.75; halt < 0.70 | Target = measured human-human QWK per subject × CQ part (non-inferiority margin, e.g. −0.05). Floor 0.70 halt. |
| Human inter-rater reliability | H–H QWK/κ on double-marked scripts | Example 0.82; measure H1–H2, H2–H3, H1–H3 | Cohen's κ ≈ 0.70–0.85 | Gold ≥ 0.85; training 0.70–0.85; adjudicate < 0.70; batch gold ≥ 0.75 | Run a Bangladeshi baseline study before fixing any AI target. |
| Exact agreement | Share with ŷ = y | Defined; no numeric target | — | Part A exact match > 98% | Report per item max mark; useful for 1–2-mark items. |
| Adjacent / tolerance agreement | Share with abs(ŷ − y) ≤ k | ±1 on 10-point, ±0.5 on 5-point "standard"; formative ±1.5 marks | — | — | Report ±1 for 3–4-mark parts; exact for 1-mark parts. |
| MAE (marks) | (1/N)Σabs(ŷ − y) | Gate ≤ 0.35; target 0.25 / minimum 0.45 / halt > 0.60; selective risk ≤ 0.25 | MASD (human delta) tracked, no target | Measured, no target | Use normalized error (÷ max marks) per item type. |
| RMSE (marks) | √mean(ŷ − y)² | Target 0.40 / minimum 0.65 / halt > 0.85 | — | — | Diagnostic only. |
| Normalized error | abs(ŷ − y)/M_q | Defined | — | — | Preferred cross-item metric. |
| Script total MAE | Mean abs(Ŝ − S) over scripts | Defined, no target | — | — | Needed for results; set after baseline. |
| Pass/fail concordance / FFR | F1; FFR = FN/(TP+FN) | F1 ≥ 0.99 / 0.96 / < 0.93; "near-zero FFR" | — | — | Boundary ±1 mark always goes to human review (C1). |
| Severe error rate | Share with error > 20% of item marks | ≤ 0.1% gate; table 0.05% / 0.20% / > 0.50% | — | — | Keep as a guardrail; size the test set to certify it. |
| CER | Character edits / reference chars | Stage ≤ 5%; table ≤ 3% / ≤ 8% / > 12% | — | < 2.5% | Baseline first (C1 cites ≈ 10.89% for Bangla); tier by script type. |
| WER | Word edits / reference words | Stage ≤ 10%; table ≤ 5% / ≤ 12% / > 18% | — | — | Secondary. |
| Semantic Preservation Index | Cosine similarity of transcript meaning | ≥ 0.98 / ≥ 0.90 / < 0.85 | — | — | Add explicit negation- and number-flip checks. |
| Layout / segmentation IoU | Overlap of predicted vs true regions | Page edge ≥ 0.95; mIoU ≥ 0.90; question IoU ≥ 0.92 (table 0.95 / 0.88 / < 0.80) | — | Layout IoU > 0.90 | ≥ 0.90 for MVP. |
| Q↔A mapping F1 | Correct answer-to-question assignment | P/R ≥ 0.99; table 0.99 / 0.95 / < 0.92 | — | — | Treat unmapped or ambiguous as a mandatory human flag. |
| Criterion F1 (rubric) | Per-criterion P/R/F1 (FP = hallucination, FN = omission) | P/R ≥ 0.90; F1 0.92 / 0.82 / < 0.75; omission ≤ 3% | — | — | Track per rubric; needed for explainability. |
| Rubric/feedback hallucination rate | Share of outputs asserting evidence not in the script | Stage ≤ 1%; table 0.5% / 1.5% / > 2.5%; guardrail > 1% | Ungrounded suggestions auto-flagged (no rate) | — | Enforce evidence-span grounding (substring match, C2). |
| Math expression accuracy | Exact LaTeX/SymPy tree match | CAS equivalence method | — | > 96% | Unproven; baseline first. |
| ECE | Σ(abs(B_m)/N)·abs(acc − conf) | Stage/gate ≤ 0.03; table 0.02 / 0.05 / > 0.08 | ≤ 0.03 for monitored tasks; achievable < 0.025 after scaling | < 0.03 (20k multi-rater set) | ≤ 0.03 per item type is the consensus; measure on the Bangladeshi set. |
| Brier score | Mean (p − y)² | Defined | — | — | Diagnostic. |
| AUROC of confidence | Ranking of correct vs incorrect | — | 0.58–0.72 by method | — | More important than ECE for routing. C2's 0.72-after-temperature-scaling claim is suspect. |
| Coverage / auto-finalize rate | Share auto-accepted at τ | Formative 85–95%; board 30–50% | Exec 35–65%; term review 25–35%; board 0% auto; homework 90–95% auto | — | Derive from risk-coverage curves; board 0% auto. |
| Confidence / risk thresholds | Routing cut-offs | τ* from risk-coverage (e.g. MAE ≤ 0.25) | C > 0.90 & CRI < 0.20 auto; batch C > 0.98 & CRI < 0.05 | — | Replace C2's fixed numbers with empirical τ*. |
| Escalation precision/recall | Quality of human routing | ≥ 0.85 / ≥ 0.98 | — | — | Measure via random audit of auto-accepted items. |
| Audit sample rates | Random human checks | — | MCQ 1%; masked review 5% | Staged overrides "sampled" | Define per stakes: e.g. ≥ 5% of auto-accepted items in formative mode. |
| Subgroup fairness Δ | E[ŷ − y given A] − E[ŷ − y given B] | Gate ≤ 0.02; table 0.01 / 0.03 / > 0.05 | — | Representativeness delta < 5% | Define units (normalized marks); include handwriting-legibility tiers. |
| Handwriting bias | Variance of scores on identical content across legibility tiers | p < 0.05 means bias | — | Handwriting balance in training | Keep as a pre-release audit. |
| Distribution shift | KL / K-S / PSI | KL > 0.05 alarm | PSI > 0.25 halts auto-approval | Curriculum version triggers re-benchmark | PSI (0.1 warn / 0.25 halt) plus version gating. |
| Teacher acceptance / override rate | Accepted ÷ suggestions; SOR = overrides/total | Acceptance ≥ 85% / ≥ 70% / < 55% | Override 13–15% expected | — | Monitor; very high acceptance may indicate automation bias. |
| Teacher consistency | Intra/inter-teacher agreement | — | κ < 0.60 quarantine | Intra-teacher QWK ≥ 0.80 | Define both. |
| Time saving | 1 − T_assisted/T_manual | ≥ 60% / ≥ 35% / < 15% | Up to 40%; 45 s → 12 s per edit | — | Measure in pilot; 30–40% is a realistic target. |
| Cost per script | All-in USD | ≤ $0.08 / ≤ $0.25 / > $0.50 | ≈ $0.05 (corrected) – $0.135 | $0.232 (8 pages) | Recompute in BDT with local examiner rates. |
| Data quality | Missing pages, schema, latency, lineage | Aggregation error 0%; page order 100% | — | 0% missing; 100% schema; < 300 s; 100% lineage | Adopt C3's table. |
| Image quality gate | Blur, DPI, skew | Laplacian > 100; skew estimation error < 0.5° | Image-quality thresholding | ≥ 200 DPI; Laplacian > 100; skew ≤ 5° | Calibrate Laplacian on local devices. |

---

## 3. Retention and governance consolidation (only C3 gives numbers)

| Data | C3 value(s) | Conflicts |
|---|---|---|
| Raw scans | 30 days | C1 lineage-to-raw-image; C2 appeals/regrade; board or school appeal windows unknown |
| Redacted scans | Contract term (T1) / contract + 2 years (T5, Q&A) | Internal |
| Extracted text | Contract + 2 years | — |
| AI outputs | Contract (T1) / contract + 2 years (T5) | Internal |
| Teacher marks/overrides | Contract + 1 year | Shorter than the AI outputs; training-data provenance |
| Audit logs | 365 days | C2 immutable reconstructible audit; C1 appeal logs |
| System logs / telemetry | 90 days / 365 days | — |
| Institutional metadata, contracts, teacher accounts | Contract + 7 years | — |
| Rubrics / questions | Indefinite (T1) / contract + 7 years (T5) | Internal |
| Identity vault | Contract (T1) / enrollment (T5) | Internal; plus "avoid collecting names/NIDs" vs schema storing them |

**Roles:** C2 defines the educational roles (Class Teacher, Senior Teacher/Dept Lead, SME, Assessment Admin, AI Quality Reviewer, MLOps with no PII access). C3 defines the corporate data roles (CDO, DPO, CISO, AI Ethics & Annotation Director, Lead Data Engineer; break-glass needs CISO + DPO). They are complementary; together they form a full RBAC/ABAC matrix.

**Third-party LLM exposure:** C2 and C3 agree: redact before any vision or LLM call; zero-data-retention enterprise contracts; never send raw unredacted images or identity records (C3). C1 is silent. [Analyst note] Neither addresses identifying handwriting inside answers, and neither addresses in-country residency for LLM calls. C3's localization clause could bar sending even redacted text abroad if scripts count as "restricted"; verify.

---

## 4. Overall judgement

- **Best-supported content across the three:** metric definitions (C1), HITL workflow and correction-capture design (C2), and PII-isolation and training-consent architecture (C3). Each is standard practice and internally coherent.
- **Weakest content:**
  - All numeric thresholds (un-sourced and mutually inconsistent).
  - C3's Bangladeshi legal claims: draft, ordinance and act status conflated, unofficial sources, possibly outdated cyber-law section numbers.
  - C2's routing math (constructed responses can never auto-finalize) and cost arithmetic.
  - C1's high-stakes auto-coverage.
- **Priority actions before the PRD fixes numbers:**
  1. Run a Bangladeshi human-IRR baseline (3 raters × ≥ 400 scripts per subject × CQ part).
  2. Run a Bangla handwriting OCR baseline.
  3. Get a legal verification of the PDP instrument and cyber law, from official gazettes, including minors' consent and localization.
  4. Map board and school result, re-scrutiny and appeal timelines to set retention.
  5. Adopt Human-in-Command for high-stakes use.
