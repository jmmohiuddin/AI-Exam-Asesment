# Comprehensive Evaluation Framework for AI-Powered Examination Assessment: Accuracy Definitions, Psychometric Metrics, End-to-End Pipeline Decomposition, and System Governance

- **Drive ID:** 1NorDRR7071Bwpy3zRQBXsjQEKEZsnIqCZBwtiHh5ZVA
- **Topic:** How to define, measure, and gate "accuracy" for an AI pipeline that grades handwritten exam scripts (image, OCR, segmentation, mapping, rubric matching, scoring, calibration, routing, feedback), with psychometric metrics, fairness audits, release gates, and cost modelling.
- **Method (as stated / inferred):** AI-generated deep-research synthesis (Gemini-style "Opens in a new window" link list; stray `[cite: N]` markers left in the master table). No original data. It cites about 27 unique URLs: psychometrics (Frontiers in Psychology 2026 on agreement metrics, NCME *Educational Measurement* 5th ed. ch. 8, ITC Technology-Based Assessment guidelines 2025), state technical reports (NH, NJ, NAPLAN automated essay scoring), arXiv preprints (2603–2609 series), a Scribd upload on Bangla TrOCR, PsyPost coverage of a PNAS Nexus study, and vendor or blog posts (accelate.ai, Arthur AI, Graveiens AI, Oxford Review). The extraction covers 100% of the doc text (about 71k characters).

---

## Main findings

1. **Accuracy has six layers** and cannot be a single number. The layers are: (a) Model accuracy (isolated sub-task models), (b) Pipeline accuracy (compounded across stages), (c) Assessment accuracy (psychometric validity/reliability of marks versus the construct), (d) Human-agreement accuracy (concordance with reference raters), (e) Operational usefulness (review reduction, correction latency, teacher cognitive load, escalation precision), (f) Business and institutional usefulness (cost/script, turnaround, scalability, legal defensibility, auditability). The doc says "95% accurate" is "psychometrically meaningless" unless decision boundary, dataset distribution, reference standard, granularity and tolerance are specified.

2. **There are seven decision nodes, each with its own metric family:**
   - OCR/HTR: CER, WER, semantic preservation.
   - Question segmentation: IoU, bounding-box P/R.
   - Answer mapping: Top-1 mapping accuracy, categorical F1.
   - Rubric matching: criterion P/R/F1.
   - Grading and partial credit: QWK, MAE, exact/adjacent agreement.
   - Confidence and abstention: ECE, risk-coverage curves.
   - Feedback: factual correctness, rubric alignment, actionability, hallucination rate.

3. **Global metrics hide catastrophic local failures.** Worked examples: 98% character accuracy can still drop a negation ("not exothermic" becomes "exothermic") and zero a high-value item. 92% exact agreement can put all 8% of errors on pass/fail boundary cases (40 becomes 38 of 100).

4. **Metrics are organized along nine evaluation units:** character/symbol (CER, symbol accuracy), word (WER, term P/R), sentence/line (sentence accuracy, Semantic Preservation Index), criterion (P/R/F1), answer/item (exact agreement, QWK, MAE, RMSE, tolerance agreement), page/document (segmentation IoU, QA mapping accuracy), student script (total-score MAE, pass/fail accuracy), cohort (Spearman ρ, distribution difference), institution/district (group offset bias, disparate impact ratio).

5. **The pipeline has 13 stages, each with a target.** These are the most PRD-relevant numbers in the doc:

   | # | Stage | Targets stated |
   |---|---|---|
   | 1 | Image Quality Assessment | Laplacian variance > 100; contrast/brightness distributions; usability threshold |
   | 2 | Page layout detection | Page-edge IoU ≥ 0.95; skew-angle estimation error < 0.5°; page-sequence accuracy 100% |
   | 3 | Page segmentation (printed vs handwriting vs stamps vs bleed-through) | mIoU ≥ 0.90; region P/R |
   | 4 | Question detection / answer region | Question boundary IoU ≥ 0.92; bbox recall ≥ 0.98; line-level segmentation accuracy |
   | 5 | Question↔answer mapping | Mapping precision ≥ 0.99, recall ≥ 0.99, F1 |
   | 6 | OCR/HTR | CER ≤ 5%, WER ≤ 10%, Semantic Preservation Index |
   | 7 | Content understanding/parsing | Dependency parsing accuracy, concept extraction F1 (no numbers) |
   | 8 | Rubric interpretation | Criterion detection P/R ≥ 0.90; omission rate ≤ 3%; hallucination rate ≤ 1% |
   | 9 | Evaluation & partial credit | Score MAE ≤ 0.35; QWK ≥ 0.85; partial-credit concordance |
   | 10 | Score aggregation (caps, optional-question selection, rounding, negative marking) | Aggregation error rate 0%; exact total concordance |
   | 11 | Confidence estimation | ECE ≤ 0.03; Brier score |
   | 12 | Verification & routing | Escalation precision ≥ 0.85; escalation recall ≥ 0.98; automation coverage rate |
   | 13 | Result generation | End-to-end pass/fail accuracy; grade-band concordance; audit-trace completeness |

6. **Errors compound.** With 10 independent stages at 98%, end-to-end accuracy is 0.98^10 ≈ 81.7% (arithmetic checks). The doc says real compounding is worse because upstream errors corrupt downstream inputs. It proposes an **Error Propagation Matrix** with five failure types:
   - IQA blur/shadow: high detectability, high recoverability via re-scan.
   - Segmentation fault: moderate detectability, medium recoverability; major impact.
   - Question-mapping error: low detectability, low recoverability; *critical*, item score inversion.
   - Semantic OCR corruption: very low detectability, because the output is grammatical; *critical*.
   - Rubric hallucination: low detectability, since the model is confident; major, score inflation.

7. **Ground truth has four reference standards:** official answer key (objective items only); single examiner (operational but noisy); double-scored independent average (the "standard operational baseline" in high-stakes testing); adjudicated senior-examiner consensus, used when raters differ by more than about 1 mark. The last is the **definitive gold standard for benchmarks**.

8. **The target should be the human-vs-human baseline.** AI is acceptable when AI-vs-H_consensus concordance is statistically equivalent to or better than H1-vs-H2 concordance under identical conditions. Measure all pairs (H1–H2, H2–H3, H1–H3); the average human IRR sets T_target. Example: if humans reach QWK 0.82, demanding AI QWK 0.98 against a single rater is "psychometrically invalid".

9. **Metric definitions (verbatim in substance):**
   - Exact agreement: A_exact = (1/N) Σ I(ŷᵢ = yᵢ). This depends on scale granularity and is near 0% on a 100-point continuous scale.
   - Tolerance/adjacent agreement: A_tol(±k) = (1/N) Σ I(|ŷᵢ − yᵢ| ≤ k). The "standard practice" for high stakes is **±1 mark on a 10-point scale or ±0.5 on a 5-point scale**.
   - Normalized error: E_norm = |ŷᵢ − yᵢ| / M_q. A 1-mark miss on a 1-mark item = 1.0 (total failure); on a 20-mark essay = 0.05.
   - MAE = (1/N) Σ|ŷᵢ − yᵢ|. RMSE = √((1/N) Σ(ŷᵢ − yᵢ)²). RMSE ≫ MAE signals rare large errors.
   - QWK: κ_w = 1 − (Σ w_ij O_ij)/(Σ w_ij E_ij), with w_ij = (i − j)²/(k − 1)². This is the "primary psychometric metric" for ordinal constructed response.
   - ICC(A,1): two-way random effects, absolute agreement. Krippendorff's α handles missing data and multiple raters.
   - Mean directional bias: B̄ = (1/N) Σ(ŷᵢ − yᵢ). Positive means over-marking. Also audit variance compression and floor/ceiling effects.
   - Handwriting bias: Bias_hw = Var(Ŷ_pristine, Ŷ_average, Ŷ_poor) on identical content rewritten in five legibility tiers (pristine, average cursive, poor/messy, small/dense, varying slant). Significant at p < 0.05 means the vision model is corrupting assessment.
   - Fairness: Δ_Fairness = E[Ŷ − Y_ref | A] − E[Ŷ − Y_ref | B], conditional on proficiency. DIF is also used.
   - ECE = Σ (|B_m|/N)·|acc(B_m) − conf(B_m)|. Brier = (1/N) Σ(pᵢ − yᵢ)².
   - Coverage C(τ) = (1/N) Σ I(Confᵢ ≥ τ). Selective risk R(τ) = Σ Errorᵢ·I(Confᵢ ≥ τ) / Σ I(Confᵢ ≥ τ). Choose τ* such that selective risk stays below an institutional threshold (example: **MAE ≤ 0.25**).
   - Script-level MAE_total over summed item scores. False Pass Rate = FP/(FP+TN). False Fail Rate = FN/(TP+FN). High-stakes systems enforce "near-zero FFR".
   - Grade-band concordance: exact agreement plus nominal κ (mentions the Bangladesh GPA 5.0 scale). Ranking: Spearman ρ, top-k overlap (for example the top 5%), mean rank displacement.
   - Distribution shift: K-S test; KL divergence D_KL(P‖Q) = Σ P log(P/Q). **D_KL > 0.05** is "significant".
   - Workflow: Teacher Acceptance Rate = accepted / total suggestions. Correction rate = 1 − acceptance. Critical Correction Rate = edits greater than ±10%. Efficiency Gain % = (1 − T_assisted/T_manual) × 100. NASA-TLX for workload.
   - Feedback hallucination rate H_rate = N_hallucinated / N_total_feedback. Actionability is rated on a 1–5 scale.

10. **Correlation is not agreement.** Human [2,4,6,8,10] vs AI [4,6,8,10,12] (+2 shift) or [1,2,3,4,5] (50% compression) both give Pearson r = 1.00, but exact agreement is 0% and MAE is 2.0 and 3.0 respectively. So absolute-agreement metrics (QWK, ICC, MAE) must be primary.

11. **Rater protocol:** double-blind, with scripts anonymized and stripped of prior marks, comments and AI metadata. The panel is H1, H2, H3, AI_A, AI_B, and a hybrid H+AI.

12. **Domain-specific requirements:**
    - Criterion-level TP/FP/FN, where FP = "rubric hallucination" and FN = "rubric omission".
    - Maths: Error-Carried-Forward (ECF) partial credit; CAS equivalence check (Equivalent(A,B) ⇔ Simplify(A − B) = 0); LaTeX expression-tree comparison.
    - Diagrams: component P/R, topology via graph matching, label-to-component distance. The doc states text-only metrics are invalid for diagrams.
    - Essays: 512-token limit of BERT-class models; lost-in-the-middle in LLMs; multi-trait output (content, argument, evidence, grammar, coherence).
    - **Bangla:** more than 500 visual shapes (juktakkhor conjuncts, kars, matra). Fine-tuned TrOCR reaches **CER ≈ 10.89%** on real handwritten samples. Matra joins break line and word segmentation. Code-switching (English technical terms inside Bangla sentences in SSC/HSC Srijonshil answers) needs token-level language detection.

13. **Severity matrix (4 tiers):**
    - Minor: ≤ ±5% of item marks, no grade or rank change; acceptable.
    - Moderate: 6–20% of item marks, no boundary crossing; optional teacher verification.
    - Major: > 20% or a grade-band shift; mandatory human escalation.
    - Critical: pass/fail inversion or unmapped question; **automatic system halt plus senior adjudication**.

14. **Escalation triggers:** OCR uncertainty; structural anomaly (missing labels, crossed-out text, unmapped blocks); out-of-distribution input; ensemble or multi-prompt disagreement; **score within ±1 mark of a pass/fail or grade boundary**.

15. **Stakes profiles:**
    - Low-stakes/formative: auto-coverage **85–95%**, tolerance **±1.5 marks**.
    - High-stakes public exams (SSC/HSC, university entrance): coverage **30–50% (assisted mode)**, strict exact/adjacent tolerance, "dual human-AI moderation".

16. **Automation bias:** a PNAS Nexus study (via PsyPost) found teachers accepted harsh AI errors more than identical human errors, giving a **22% larger fairness gap**. Mitigation is "calibrated trust design": do not show pre-selected final scores; show evidence and rubric first; require active teacher input before revealing the AI score.

17. **Dataset stratification:**
    - Urban, semi-urban and rural; public board and private.
    - English, Bangla and mixed medium.
    - **Handwriting mix 20% pristine / 50% average / 20% poor / 10% extreme-cursive.**
    - Scans including mobile photos and **150 DPI** low-resolution, perspective distortion, uneven light.
    - Score range from zero to top-percentile.

    Leakage controls: contamination audits (test items, prompts and keys must not appear in training *or prompt context*), student-level splits, temporal splits on future sessions.

18. **Statistics:**
    - Sample size to detect ΔQWK = 0.03 at power 0.80, α = 0.05: N = ((Z₁₋α/₂ + Z₁₋β)/(δ/σ_κ))². The doc concludes **N ≥ 400 independently scored scripts per subject stratum**.
    - Tests: paired t / Wilcoxon for MAE/RMSE; McNemar for pass/fail.
    - Report QWK with a 95% bootstrap CI, **B = 1,000** resamples (example QWK 0.84 [0.81, 0.87]).

19. **MLOps release gates** (PROMOTE / HOLD / ROLLBACK). All gates must pass:
    - **QWK ≥ 0.85, MAE ≤ 0.35**
    - **Major/Critical error rate ≤ 0.1%**
    - **Subgroup bias Δ ≤ 0.02**
    - **ECE ≤ 0.03**
    - Cost per script within budget

    Each evaluation record logs {model version, prompt version, pipeline version, dataset version, question, student answer, reference answer, reference score, AI score, confidence, latency, cost}. Regression runs cover the full Golden Dataset and a Challenge Dataset.

20. **Cost model:** Cost_script = Cost_AI + (1 − C)·Cost_human_review. Example: a frontier LLM at $0.25/script with 85% coverage vs a fine-tuned compact model at $0.02/script with 70% coverage. The frontier model *can* cost more overall.

21. **Audit and appeals:** every mark links to raw image, crop bbox, transcript, rubric version, confidence and prompt trace. On an appeal, the script goes to an **independent senior examiner** together with the AI evidence log. An override is logged as a correction event and **added to the regression evaluation database**.

22. **Goodhart safeguards:** guardrail metric sets (severe error rate, distribution variance, subgroup bias) must pass alongside any primary metric. Optimizing exact agreement alone pushes the model toward conservative mean scores.

23. **Six-level metric hierarchy:** L1 component, L2 task, L3 assessment, L4 system, L5 human-workflow, L6 business. Metrics are classified as Primary (QWK ≥ 0.85, MAE ≤ 0.35), Secondary (CER, mapping F1, ECE) and Guardrail. Guardrail breaches halt deployment: **severe error > 0.1%, rubric hallucination > 1.0%, disparate impact Δ > 0.02**.

24. **Master Evaluation Matrix (target / minimum acceptable / guardrail):**

    | Metric | Target | Min acceptable | Guardrail (halt) |
    |---|---|---|---|
    | CER | ≤ 3.0% | ≤ 8.0% | > 12.0% |
    | WER | ≤ 5.0% | ≤ 12.0% | > 18.0% |
    | Semantic Preservation Index (cosine) | ≥ 0.98 | ≥ 0.90 | < 0.85 |
    | Question boundary IoU | ≥ 0.95 | ≥ 0.88 | < 0.80 |
    | QA mapping F1 | ≥ 0.99 | ≥ 0.95 | < 0.92 |
    | QWK | ≥ 0.88 | ≥ 0.78 | < 0.70 |
    | MAE (marks) | ≤ 0.25 | ≤ 0.45 | > 0.60 |
    | RMSE (marks) | ≤ 0.40 | ≤ 0.65 | > 0.85 |
    | Criterion F1 | ≥ 0.92 | ≥ 0.82 | < 0.75 |
    | Rubric hallucination rate | ≤ 0.5% | ≤ 1.5% | > 2.5% |
    | ECE | ≤ 0.02 | ≤ 0.05 | > 0.08 |
    | Severe error rate (> ±20%), % scripts | ≤ 0.05% | ≤ 0.20% | > 0.50% |
    | Subgroup bias Δ | ≤ 0.01 | ≤ 0.03 | > 0.05 |
    | Pass/fail concordance F1 | ≥ 0.99 | ≥ 0.96 | < 0.93 |
    | Teacher acceptance rate | ≥ 85% | ≥ 70% | < 55% |
    | Time-to-correct gain | ≥ 60% | ≥ 35% | < 15% |
    | Cost per script (USD) | ≤ $0.08 | ≤ $0.25 | > $0.50 |

25. **Stakeholder matrix:** teacher (time, acceptance, NASA-TLX), student (rubric alignment, clarity, appeal rate, subgroup bias), parent (consistency, pass/fail accuracy, auditability), administrator (turnaround, cost, scalability), policy researcher (QWK, DIF, NCME alignment), developer (CER/WER, latency, ECE).

---

## Quantitative claims table

| Claim | Value | Source cited | Source type | Credibility H/M/L + why |
|---|---|---|---|---|
| End-to-end accuracy of 10 stages at 98% | ≈ 81.7% | None (arithmetic) | Derivation | H: arithmetic is correct. The independence assumption is acknowledged as optimistic. |
| Fine-tuned TrOCR CER on real Bangla handwriting | ≈ 10.89% | Scribd upload "Bangla Handwritten Word Recognition Using Fine-Tuned TrOCR" | Unreviewed document on Scribd | L–M: plausible order of magnitude for word-level Bangla HTR, but the venue, dataset and split are unknown. |
| Bangla has > 500 distinct visual shapes | > 500 | Implied (ResearchGate Bengali HWR) | Academic paper | M: commonly cited range; the count depends on the conjunct inventory used. |
| Harsh-AI-error fairness gap | 22% larger | PNAS Nexus via PsyPost | Pop-science write-up of a peer-reviewed study | M: primary paper not cited directly; effect magnitude not checked. |
| Human QWK example | 0.82 | None | Illustrative | L: illustrative only. |
| Adjacent agreement "standard" | ±1 on 10-pt, ±0.5 on 5-pt | NCME / state technical reports (implied) | Professional standard | M: adjacent agreement is standard in the ETS/NAPLAN tradition; the ±0.5-on-5 rule is not standard wording. |
| Sample size for ΔQWK = 0.03 | N ≥ 400 scripts per stratum | Formula, no σ_κ given | Derivation without inputs | L: the result depends on σ_κ and on a paired design. Detecting 0.03 κ between two models usually needs a paired bootstrap; 400 may be insufficient. |
| Bootstrap CI example | QWK 0.84 [0.81, 0.87], B = 1,000 | None | Illustrative | M: the method is standard; the numbers are illustrative. |
| Laplacian blur threshold | > 100 | None | Folk heuristic (OpenCV tutorials) | L: depends on resolution and scale; must be calibrated locally. |
| Stage CER/WER targets | ≤ 5% / ≤ 10% | None | Author judgement | L–M: contradicts its own master table (≤ 3% / ≤ 5%). |
| QWK release gate | ≥ 0.85 | None stated for the gate; table cites `[cite: 1, 3]` | Unresolvable citation markers | L: the `[cite: N]` markers point to no reference list. |
| MAE release gate | ≤ 0.35 marks | None | Author judgement | L: MAE in raw marks is not comparable across 1-mark and 20-mark items (the doc's own E_norm point). |
| ECE gate | ≤ 0.03 (table target ≤ 0.02) | None | Author judgement | M: achievable with post-hoc calibration on large validation sets (C2 reports 0.013–0.024). |
| Severe error gate | ≤ 0.1% (table target 0.05%) | None | Author judgement | L: verifying ≤ 0.05% needs roughly 6,000+ zero-error scripts for a 95% upper bound (rule of three). Not discussed. |
| Rubric hallucination | ≤ 1% (stage) / ≤ 0.5% target | `[cite: 12]` | Unresolvable | L. |
| Subgroup Δ | ≤ 0.02 gate; ≤ 0.01 target | `[cite: 7]` | Unresolvable | L: units undefined (marks? normalized?). |
| Teacher acceptance | ≥ 85% target | `[cite: 8]` | Unresolvable | L: a high acceptance rate can also indicate automation bias, which the doc itself warns about. |
| Time saved | ≥ 60% target | `[cite: 8]` | Unresolvable | L–M: C2 reports "up to 40%". |
| Cost per script | ≤ $0.08 target, ≤ $0.25 min | `[cite: 10]` | Unresolvable | L: no Bangladesh labour-cost basis. |
| Frontier vs compact LLM cost | $0.25 vs $0.02/script | None | Illustrative | L–M: plausible 2026 ranges, not sourced. |
| High-stakes coverage | 30–50% auto (assisted) | None | Judgement | L: conflicts with C2 (100% human review for boards). |
| Low-stakes coverage | 85–95%, ±1.5 marks | None | Judgement | L–M. |
| Handwriting strata | 20/50/20/10% | None | Judgement | L: not derived from any Bangladeshi population estimate. |
| KL divergence alarm | > 0.05 | None | Judgement | L: KL depends on binning; no justification. |
| Critical correction threshold | > ±10% edits | None | Judgement | L: inconsistent with the 6–20% "moderate" tier. |

---

## Frameworks/processes proposed (step by step)

**A. Evaluation engine pipeline (§9.1):**
1. Ingest raw script plus metadata.
2. Run the versioned pipeline (Model_v, Prompt_v, Pipeline_v).
3. Capture outputs (text, score, rubric logic, confidence).
4. Compare against the Ground Truth DB (adjudicated scores, rubric criteria).
5. Compute metrics (QWK, MAE, CER, ECE, bias, hallucination).
6. Release gate decision: PROMOTE / HOLD / ROLLBACK.

**B. Release gating (§9.2):**
1. Rerun the Golden and Challenge datasets.
2. Evaluate accuracy, severe-error, fairness, calibration and economic gates.
3. All pass means PROMOTE; any fail means HOLD or ROLLBACK.

**C. Human baseline protocol (§3.2, §3.5):**
1. Anonymize and strip prior marks.
2. Have three independent humans score.
3. Compute pairwise IRR.
4. Adjudicate discrepancies greater than about 1 mark to a senior examiner, which creates the gold standard.
5. Score with AI_A, AI_B and hybrid H+AI.
6. Declare AI acceptable if AI-vs-consensus ≥ H1-vs-H2 (equivalence test).

**D. Selective automation (§6.2):**
1. Compute calibrated confidence.
2. Sweep τ to build the risk-coverage curve.
3. Choose τ* where selective risk ≤ the institutional limit (example MAE ≤ 0.25).
4. Auto-accept above τ*.
5. Abstain or escalate below τ*, or on any trigger (OCR uncertainty, structural anomaly, OOD, model disagreement, ±1 mark of a boundary).

**E. Severity handling (§6.4):** minor accepted; moderate highlighted for optional verification; major goes to mandatory review; critical triggers system halt and senior adjudication.

**F. Handwriting-bias audit (§5.2):**
1. Rewrite identical content in five legibility tiers.
2. Score each version.
3. Test variance across tiers (p < 0.05 flags bias).

**G. Appeal loop (§9.4):**
1. Dispute is raised.
2. Route to an independent senior examiner with the AI evidence log.
3. Log the override as a correction event.
4. Add it to the regression evaluation DB.

**H. Six-level metric hierarchy** with Primary / Secondary / Guardrail classes (§10).

---

## Specifics a PRD/TRD needs

- **Primary scoring metrics and targets:** the doc offers two inconsistent sets.
  - Release gate: QWK ≥ 0.85 and MAE ≤ 0.35.
  - Master table: QWK target 0.88 / min 0.78 / halt < 0.70; MAE 0.25 / 0.45 / > 0.60; RMSE 0.40 / 0.65 / > 0.85.
  - Adjacent agreement: ±1 mark on a 10-point scale. No numeric target is given for exact or adjacent agreement percentages.
  - [Analyst note] The PRD should pick one set, state it per item type and max mark (for example per CQ sub-part: 1/2/3/4 marks), and use E_norm or per-mark-scale targets rather than a global MAE.
- **OCR:** CER ≤ 3% target, ≤ 8% minimum, halt > 12%; WER ≤ 5% / 12% / 18%; Semantic Preservation ≥ 0.98 / 0.90 / < 0.85. The stage section says CER ≤ 5%, WER ≤ 10%. The Bangla SOTA it cites is about 10.89% CER. [Analyst note] That is already above the "minimum acceptable" 8%, so for Bangla handwriting the targets are aspirational unless scoped to line-level printed-like hands or backed by teacher-verified transcripts.
- **Layout/mapping:** page-edge IoU ≥ 0.95; skew error < 0.5°; page order 100%; segmentation mIoU ≥ 0.90; question boundary IoU ≥ 0.92 (≥ 0.95 in the table); bbox recall ≥ 0.98; mapping P/R ≥ 0.99; aggregation error 0%.
- **Rubric:** criterion P/R ≥ 0.90; criterion F1 target 0.92 / min 0.82 / halt < 0.75; omission ≤ 3%; hallucination ≤ 1% at stage level, 0.5% / 1.5% / > 2.5% in the table.
- **Calibration and routing:** ECE ≤ 0.03 (table 0.02 / 0.05 / > 0.08); escalation precision ≥ 0.85, recall ≥ 0.98; boundary proximity ±1 mark forces review. Coverage: formative 85–95%, board 30–50%.
- **Safety and fairness:** severe (> 20% of item) error ≤ 0.1% at the gate (table 0.05% / 0.20% / > 0.50%); subgroup Δ ≤ 0.02 at the gate (table 0.01 / 0.03 / > 0.05); pass/fail F1 ≥ 0.99; "near-zero" false-fail rate; KL divergence alarm > 0.05.
- **Workflow:** teacher acceptance ≥ 85% (min 70%, halt < 55%); time saved ≥ 60% (min 35%, halt < 15%); critical correction defined as > ±10% edits.
- **Cost:** ≤ $0.08/script target, ≤ $0.25 minimum, > $0.50 halt.
- **Gold dataset size:** ≥ 400 independently scored scripts **per subject stratum**, adjudicated with 3 human raters. Include a Golden set and a Challenge set. Stratify by handwriting (20/50/20/10), medium, geography, scan quality (including 150 DPI and mobile photos) and score range. Split by student, and temporally.
- **Audit sampling rates:** none given for post-deployment audit sampling. [Analyst note] This gap must be filled from C2 (MCQ 1% audit, 5% masked review) or set in the PRD.
- **Confidence thresholds:** method only (τ* from the risk-coverage curve). No numeric τ.
- **Which corrections feed which store:** only one route. Appeal overrides feed the **regression evaluation database**. Nothing on the rubric, rules or training stores (see C2).
- **Logging and lineage:** evaluation record fields (§9.1). Every mark links to the image, crop, transcript, rubric version, confidence and prompt trace.
- **UI rule:** evidence and rubric before the AI score; active teacher input before the score is revealed.
- **Retention, access control, anonymization, third-party LLM rules:** *not covered* beyond "scripts anonymized" for rater experiments and fairness analysis "where ethically approved and legally governed".

---

## Assumptions

1. Model confidence can be calibrated well enough that ECE ≤ 0.02–0.03 is achievable per item type, including for LLM scorers.
2. Adjudicated senior-examiner consensus is the gold standard. It assumes senior examiners are available at scale for Bangladeshi subjects and at a sensible cost.
3. Human IRR is measurable per item and stable enough to set targets.
4. Handwriting legibility can be manipulated experimentally (the same content rewritten), which needs recruited writers.
5. Demographic attributes (gender, urban/rural, medium) are available and lawful to process for fairness audits.
6. CAS equivalence can be applied to transcribed maths. This assumes LaTeX OCR is accurate enough.
7. Costs are in USD and inference prices of about $0.02–0.25/script.
8. A "Golden Dataset" and "Challenge Dataset" exist before the first release.

---

## Recommendations (from the doc)

1. Evaluate against human IRR, not perfection. Primary metrics should be absolute agreement (QWK, MAE, ICC), not correlation.
2. Monitor error propagation per stage. Add semantic preservation to catch low-WER, high-consequence OCR errors such as negation and numbers.
3. Use calibrated selective automation with an explicit abstention state and boundary-proximity escalation.
4. Use UI designs that force engagement (evidence first, score later) to counter automation bias.
5. Use version-controlled release gates with guardrail metrics. Any guardrail breach means HOLD or ROLLBACK.
6. Stratify datasets and prevent leakage (student-level and temporal splits, contamination audits including prompt context).
7. Report CIs (bootstrap, B = 1,000) and use paired tests.
8. Add appeal overrides to the regression suite.

---

## Open questions

1. What is the empirical human-vs-human QWK for Bangladeshi SSC/HSC CQ sub-parts (1/2/3/4 marks)? The doc offers no Bangladeshi baseline.
2. How is "confidence" defined for an LLM scorer: logit, verbalized, ensemble variance? C1 is silent; C2 addresses it.
3. What are the units of "Subgroup Bias Δ ≤ 0.02"? Raw marks, normalized, or QWK difference?
4. What is the severe-error threshold at script level versus item level? "> ±20%" is applied to "% total scripts" in the table but to "item marks" in the severity matrix.
5. How many scripts are needed to certify severe-error ≤ 0.05%, given the statistical power needed for rare events?
6. Is the "dual human-AI moderation" for board exams compatible with how Bangladeshi boards actually use head examiners and examiners? The doc does not describe the board process.
7. How should an optional-question selection rule ("answer any 5 of 8") be handled? The aggregation stage mentions it only as a failure mode.
8. What is the escalation-recall ≥ 0.98 measured against, given that the escalation ground truth depends on knowing the true error?

---

## Critical assessment

- **Internal contradictions in targets:**
  - CER ≤ 5% (stage) vs ≤ 3% target / ≤ 8% minimum (table).
  - WER ≤ 10% vs ≤ 5% / 12%.
  - QWK ≥ 0.85 (stage and gate) vs 0.88 / 0.78 (table).
  - MAE ≤ 0.35 (gate) vs ≤ 0.25 target / 0.45 minimum (table), and "MAE ≤ 0.25" as a selective-risk example.
  - ECE ≤ 0.03 vs 0.02.
  - Severe error ≤ 0.1% (gate and guardrail) vs ≤ 0.05% target, ≤ 0.20% minimum, > 0.50% guardrail. The guardrail limit in §10.2 (0.1%) is stricter than the table's "minimum acceptable" (0.20%).
  - Hallucination ≤ 1% (stage), halt > 1.0% (§10.2), vs 0.5% / 1.5% / > 2.5% (table).
  - Fairness Δ halt > 0.02 (§10.2) vs minimum acceptable ≤ 0.03 and halt > 0.05 (table).

  [Analyst note] These cannot all be true at once. A PRD must choose one set.
- **The human-baseline principle contradicts the fixed thresholds.** §3.2 says targets come from measured human IRR, but §9–10 hard-code QWK ≥ 0.85–0.88 regardless of item type. If Bangladeshi examiners agree at QWK 0.70 on a 4-mark higher-order CQ part, a 0.88 target is unattainable and invalid by the doc's own logic.
- **MAE in raw marks** is used as a global gate even though the doc itself shows raw error is meaningless across item maxima (E_norm section).
- **Unresolvable citations.** The master table carries `[cite: 1, 3]`, `[cite: 4]`, `[cite: 7, 12]`, `[cite: 8]`, `[cite: 10]`, `[cite: 12]` markers that do not map to the reference list. They are artefacts of another generation step. [Analyst note] Treat every number in that table as un-sourced author judgement.
- **Source quality is mixed.** The Bangla OCR number comes from a Scribd upload. Automation bias comes from PsyPost (secondary coverage). Release-gate practice comes from vendor blogs (Arthur AI, accelate.ai, Graveiens AI). Stronger sources (NCME ch. 8, ITC TBA guidelines 2025, NH/NJ technical reports, NAPLAN AES report) are cited but not tied to specific numbers.
- **Unrealistic targets:**
  - QA mapping F1 ≥ 0.99 and page sequence 100% on unnumbered loose pages and supplementary sheets.
  - Escalation recall ≥ 0.98 (needs perfect knowledge of true errors).
  - Aggregation error 0% is appropriate (deterministic code) but must be enforced by unit tests, not ML.
  - Bangla CER ≤ 3% vs cited state of the art about 10.89%.
- **Sample-size claim is weak.** "N ≥ 400 per stratum" is stated without σ_κ. For paired model comparisons and rare-event gates (0.05–0.1%), far larger sets are needed. The doc does not reconcile its gold-set size with its severe-error gate: 400 scripts cannot certify a 0.1% rate.
- **High-stakes coverage.** 30–50% auto-acceptance for SSC/HSC contradicts C2 (100% human review for board exams). It is also legally and politically risky in Bangladesh, where board results are public and contested. [Analyst note]
- **Over-engineering for an MVP:** ICC, Krippendorff's α, DIF, K-S, KL, top-k overlap, NASA-TLX and 13 stage gates are all good for mature programs. An MVP needs about 6–8 core metrics.
- **Legal claims:** the doc makes **no Bangladesh-law claims**. Its only legal-adjacent statements are "legal defensibility" and fairness analysis "where ethically approved and legally governed".
- **Domain framing:** GPA 5.0, SSC/HSC and Srijonshil are named correctly. The doc does not describe how Bangladeshi boards currently mark (head examiner, examiner, re-scrutiny). [Analyst note]

---

## Confidence level + Relevance to product decisions

- **Confidence in the doc's content:**
  - **Metric definitions and formulas: High.** QWK, MAE, RMSE, ECE, Brier, coverage/risk, FPR/FFR and KL are standard and correctly stated.
  - **Architecture and gating concepts: Medium–High.**
  - **Numeric targets: Low.** They are un-sourced, internally inconsistent, and not grounded in Bangladeshi baselines.
- **Relevance: Very high** for the Evaluation/QA section of the TRD, the gold-dataset spec, the release-gate process, the escalation-trigger spec and the reviewer-UI principle (evidence before score). Use the metric vocabulary and the stage decomposition directly. Treat thresholds as placeholders until a Bangladeshi human-IRR baseline study (3 raters × ≥ 400 scripts per subject/sub-part) is run. Borrow the high-stakes coverage numbers only after reconciling them with C2's human-in-command stance.
