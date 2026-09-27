# 11 — Traceability Matrix, Cross-Document Consistency Audit, Final Architecture Review and Self-Review

| Field | Value |
|---|---|
| Document Name | Traceability & Final Review |
| Version | 1.0 |
| Status | Completed for package v1.0 (re-run at every gate) |
| Date | 2026-09-27 |
| Owner | Product lead + Engineering lead |
| Purpose | Proves every requirement traces to research and forward to design, implementation and tests. Records the consistency audit across documents. Challenges the architecture against failure scenarios. Reviews the package from each stakeholder's perspective. |
| Source Research | All (`00`) |
| Dependencies | Documents 00–10 |

---

## 1. Traceability chain

`Research finding (S/V) → Verified fact / Evidence (VF/EV) → Decision (DEC) → Requirement (FR/NFR/AI-REQ/SEC/PRV) → Technical requirement (TR) → Design (SD § / API) → Screen (SCR/CAP) → Test (09 §)`

### 1.1 Key chains (narrative examples)

| # | Research | Evidence | Decision | Requirement | Technical | Design | UX | Test |
|---|---|---|---|---|---|---|---|---|
| T1 | S02, S03 (transcription chain) | EV-03 | DEC-01, DEC-09 | FR-RES-01..03, FR-REV-07 | TR-RES-01, TR-SCO-01 | SD §10 | SCR-18, SCR-22 | 09 §3.1 fixture suite |
| T2 | S05, S07, V2 (Bangla HTR) | VF-15, EV-14 | DEC-21, DEC-04 | FR-AI-01, FR-AI-02 | TR-AI-01, TR-OCR-02/04 | SD §5 | SCR-16 level badges, SCR-17 | 09 §10–11; 06 §4.3 L1/L2 gates |
| T3 | V1 (marking law, PDPA, AI policy) | VF-08, VF-12, VF-13, EV-32 | DEC-05, DEC-23 | HITL-01, FR-APL-01..03, NFR-AUD-01 | TR-AUD-01, TR-AI-07 | SD §9, §14.5 | SCR-17, SCR-24 | 09 §8 (audit tamper), §3 re-check |
| T4 | S08, V2 (agreement, calibration) | VF-18..20, EV-17, EV-18 | DEC-10, DEC-29 | FR-AI-06, AI-REQ-06/07 | TR-AI-06, TR-MLOPS-02 | SD §15 | 05 §7 confidence UX | 09 §10 gate runs |
| T5 | S15, S13, V2 (economics) | VF-21, EV-24, EV-25 | DEC-18, DEC-34, DEC-26 | NFR-COST-01, FR-PRC-04 | TR-COST-01..03, TR-PIPE-02 | SD §14.4 | SCR-08 mode choice | 09 §9 SLA; cost monitors |
| T6 | V1, S10 (consent, minimisation) | VF-12, EV-30 | DEC-13, DEC-14 | FR-ORG-06, PRV-02/05 | TR-PRV-01/02, TR-AI-08 | SD §4, §17 | SCR-05, CAP-02 | 09 §8 planted-name test |
| T7 | S08, S11a (automation bias, horizontal review) | EV-22 | DEC-06, DEC-33 | FR-REV-01, FR-REV-05 | TR-REV-01, TR-REV-03 | SD §9 | SCR-16/17, 05 §5.3 | 09 §15 automation-bias probe |
| T8 | S07 (anchored sheets) | CON-13 | DEC-07, DEC-22 | FR-EXM-05, FR-CAP-02, FR-AI-07 | TR-OMR-01, TR-CAP-05 | SD §14.3 | SCR-12, CAP-02 | 09 §11 OMR set |
| T9 | S01 (kill criteria), S04 (paid LOI) | CON-01, CON-07 | DEC-19, G0 | PRD §36 roadmap | — | — | — | EXP-04..06 |
| T10 | V1 (curriculum volatility) | VF-01, VF-02, EV-06 | DEC-15, DEC-16 | FR-CUR-01..04, FR-RUB-08 | TR-CUR-01/02, TR-DB-04 | SD §11 | SCR-06 | 09 §3 (pack update regression) |

### 1.2 Requirement Traceability Matrix (all PRD functional requirements)

Priority from the PRD. "Research" lists the main source/evidence. "SD" gives the section or endpoint group. "Test" gives the `09` section, or a named suite.

| FR | Pri | Research / decision | TRD | SD / API | Screen | Test |
|---|---|---|---|---|---|---|
| FR-ORG-01 | M | S11; DEC-38 | TR-TEN-01, TR-DB-02 | §6; `/schools` | SCR-03 | §3 Org; §5 isolation |
| FR-ORG-02 | M | VF-01 | TR-DB-02 | §7.1; `/sections` | SCR-03 | §3 |
| FR-ORG-03 | M | S02, S04 | TR-BE-05, TR-BN-01 | `/roster-imports` | SCR-05 | §3; §4 |
| FR-ORG-04 | M | S09; DEC-39 | TR-AUTHZ-01 | §9; `/staff` | SCR-04 | §5 authz matrix |
| FR-ORG-05 | M | S02 | TR-REV-01 | `/teaching-assignments` | SCR-04 | §3 |
| FR-ORG-06 | M | VF-12; DEC-13 | TR-PRV-01 | `/consents` | SCR-05, CAP-02 | §3; §8 |
| FR-ORG-07 | S | S03 | TR-TEN-01 | §6 | SCR-26 | §3 |
| FR-CUR-01 | M | VF-01; DEC-16 | TR-CUR-01 | §11; `/curriculum-versions` | SCR-06 | §3 |
| FR-CUR-02 | M | VF-03, VF-04 | TR-CUR-02, TR-RES-01 | `/paper-templates` | SCR-06, SCR-08 | §3.1 |
| FR-CUR-03 | M | VF-06 | TR-CUR-01 | `/schools/{id}/paper-templates` | SCR-06 | §3 |
| FR-CUR-04 | M/S | VF-04 | TR-CUR-02 | §7.2 (Item) | SCR-09, SCR-25 | §3 |
| FR-EXM-01 | M | VF-06 | TR-BE-03 | `/exams` | SCR-08 | §6 UF-01 |
| FR-EXM-02 | M | VF-04 | TR-BE-03 | `/exams/{id}/structure` | SCR-09 | §3 |
| FR-EXM-03 | S | S04 | TR-AI-02 | `/paper-extractions` | SCR-09 | §3 |
| FR-EXM-04 | M | S02, S04 | TR-FE-06, TR-BN-01 | — | SCR-09 | §6 visual |
| FR-EXM-05 | M | DEC-07, DEC-14, DEC-22 | TR-BE-04, TR-OMR-01 | `/cover-sheets` | SCR-12 | §4 PDF; §11 OMR |
| FR-EXM-06 | M | S14 | TR-RES-02 | `/mcq-keys` | SCR-09 | §3 |
| FR-EXM-07 | M | S11 | TR-BE-03 (TR-WF-01) | §14.1 | SCR-07, SCR-21 | §1 property tests |
| FR-EXM-08 | S | — | TR-DB-04 | `/exams` (clone) | SCR-07 | §3 |
| FR-RUB-01..05 | M | EV-16; S07; DEC-32 | TR-RUB-01, TR-MATH-01..03 | `/rubric-draft` | SCR-10 | §3; §11 maths fixtures |
| FR-RUB-06 | S | — | TR-AI-02 | `/rubric-draft` | SCR-10 | §3 |
| FR-RUB-07 | M | — | TR-RUB-02 | `/rubric-lock` | SCR-10 | §3 |
| FR-RUB-08 | M | DEC-15 | TR-RUB-03, TR-DB-04 | `/rubric-versions` | SCR-10, SCR-17 | §3 |
| FR-RUB-09 | S | — | TR-PIPE-03 | `/rubric-dry-runs` | SCR-11 | §3 |
| FR-CAP-01..07 | M | DEC-28; VF-11; EV-05, EV-09 | TR-CAP-01..07 | §14.3 | CAP-01..05 | §6 device matrix; §9 chaos |
| FR-CAP-08 | M | DEC-28 | TR-PIPE-04 | `/pdf-imports` | SCR-14 | §3 |
| FR-CAP-09 | M | S02 | TR-OBS-02 | `/exams/{id}/processing` | SCR-15 | §3 |
| FR-CAP-10 | M | S02 | TR-RES-01 | `/attendance` | SCR-15 | §3.1 (absent) |
| FR-PRC-01 | M | — | TR-PIPE-01 | `/scripts/{id}/status` | SCR-15 | §3 |
| FR-PRC-02 | M | RSK-19 | TR-VIS-03 | §5 | SCR-16 (unmapped) | §11 mapping |
| FR-PRC-03 | M | DEC-14 | TR-AI-08, TR-PRV-02 | §17 | — | §8 planted-name |
| FR-PRC-04 | M/S | DEC-34 | TR-PIPE-02/03 | §14.4 | SCR-08, SCR-15 | §9 SLA |
| FR-PRC-05 | M | — | TR-KB-03 | `/resuggest` | SCR-17 | §3 |
| FR-AI-01 | M | DEC-04 | TR-AI-01 | §5 registry | SCR-16, SCR-28 | §10 |
| FR-AI-02 | M | EV-21 | TR-OCR-02/04 | `/transcript` | SCR-17 | §11 |
| FR-AI-03 | M | S07; AI-REQ-04 | TR-AI-04 | §5 | SCR-17 | §10 |
| FR-AI-04 | M | PP-4 | TR-SCO-01 | §10 | SCR-17 | §1 property |
| FR-AI-05 | M | DEC-32 | TR-MATH-01..04 | §5 | SCR-17 badges | §11 |
| FR-AI-06 | M | DEC-10 | TR-AI-06 | §5 | SCR-17 risk chip | §10 calibration |
| FR-AI-07 | M | DEC-22 | TR-OMR-01/02 | §14.4 | SCR-18 | §11 OMR |
| FR-AI-08 | S | VF-06 | TR-AI-02 | §5 | SCR-18 | §11 |
| FR-AI-09 | M | VF-25 | TR-SEC-07 | 06 §7 | SCR-17 banner | §12 red team |
| FR-AI-10 | M | EV-05 | TR-VIS-02 | §5 | SCR-17/18 | §11 |
| FR-AI-11 | S | EV-11 | TR-AI-03 | §16 | 05 §8 | §6 |
| FR-AI-12 | C | — | — | — | — | — |
| FR-AI-13 | M | DEC-10 | TR-AI-05 | §14.4 | — | §10 budget |
| FR-REV-01 | M | DEC-06 | TR-REV-01 | `/review-queues` | SCR-16 | §3 |
| FR-REV-02 | M | PP-2 | TR-FE-03 | `/card` | SCR-17 | §6; §9 latency |
| FR-REV-03 | M | S09 | TR-REV-02 | `/decisions`, `/flags`, `/remap` | SCR-17, SCR-19 | §3 |
| FR-REV-04 | M | S09 | TR-REV-02 | decisions `reason_code` | SCR-17 | §3; §15 |
| FR-REV-05 | M | DEC-33 | TR-REV-03 | §9 | SCR-17 (masked) | §3; §15 |
| FR-REV-06 | S | DEC-04 | TR-REV-04 | `/batch-confirmations` | 05 §5.3 | §3 |
| FR-REV-07 | M | EV-05 | TR-REV-02 | `/review-view` | SCR-18 | §3 |
| FR-REV-08 | M | — | TR-FE-03 | — | 05 §5.2 | §7 keyboard |
| FR-REV-09 | S | EV-09 | TR-FE-04 | — | 05 §10.1 | §6 offline |
| FR-REV-10 | M | PP-1 | TR-ERR-04 | — | SCR-17 | §9 chaos (AI off) |
| FR-REV-11 | S | — | TR-REV-01 | — | SCR-16 | §3 |
| FR-HITL-01 | M | DEC-17 | TR-REV-02 | §9, §14.8 | SCR-17 | §3 |
| FR-HITL-02 | M | US-13 | TR-KB-01..03 | `/alternatives`, `/clarifications` | SCR-19 | §3 scope isolation |
| FR-HITL-03 | S | S09 | TR-KB-01 | `/exception-rules` | SCR-19 | §3 |
| FR-HITL-04 | M | S09 | TR-REV-02 | `/flags` | SCR-19, SCR-20 | §3 |
| FR-HITL-05 | S | S09 | TR-KB-01/02 | `/instructions` | SCR-06 | §3 |
| FR-MOD-01 | M | DEC-27 | TR-REV-05 | `/moderation-samples` | SCR-20 | §3; §15 |
| FR-MOD-02 | M | S02 | TR-BE-03 | `/lock` | SCR-21 | §3 |
| FR-MOD-03 | M | — | TR-AUD-01 | `/lock` | SCR-21 | §8 audit |
| FR-RES-01..03 | M | VF-05 | TR-RES-01 | §10 | SCR-22 | §3.1 |
| FR-RES-04 | S | VF-06 | TR-RES-01 | `/result-sets` | SCR-22 | §3.1 |
| FR-RES-05 | M | — | TR-BE-05 | `/mark-imports` | SCR-22 | §3 |
| FR-RES-06 | M | S02 | TR-RES-01 | — | SCR-22 | §3.1 |
| FR-RES-07 | M | S02, S11 | TR-BE-04 | `/tabulation` | SCR-22 | §4 |
| FR-RES-08 | C | S02 | TR-RES-01 | — | SCR-22 | — |
| FR-RES-09 | M/S | P4 | TR-BE-04, TR-BE-06 | `/publish` | SCR-23 | §3 |
| FR-FBK-01 | M | DEC-35 | TR-BE-04 | §16 | SCR-23; 05 §8 | §4 PDF |
| FR-FBK-02 | S | — | TR-BE-04 | — | 05 §8 | §4 |
| FR-FBK-03 | S | — | TR-OBS-02 | `/item-analysis` | SCR-25 | §3 |
| FR-APL-01..03 | M | DEC-23 | TR-REV-02, TR-RES-02 | `/rechecks` | SCR-24 | §3 |
| FR-ANL-01 | M | S03 | TR-OBS-02 | `/progress` | SCR-02, SCR-15 | §3 |
| FR-ANL-02 | S | OQ-18 | — (read model) | §14.7 | SCR-26 | §3 |
| FR-ANL-03 | S | — | — (read model) | `/item-analysis` | SCR-25 | §3 |
| FR-ANL-04 | S | — | — (read model) | `/summary` | SCR-26 | §3 |
| FR-AIQ-01 | M | US-23 | TR-OBS-03 | `/ai-quality` | SCR-27 | §3 |
| FR-AIQ-02 | M | 06 §6 | TR-OBS-03, TR-MON-02 | §18 | SCR-28 | §10 |
| FR-AIQ-03 | M | DEC-04, DEC-29 | TR-MLOPS-02 | §15 | SCR-28 | §10 |
| FR-ADM-01 | M | — | TR-AUTHZ-01 | `/settings` | SCR-29 | §3 |
| FR-ADM-02 | M | PRV-02 | TR-PRV-01 | `/consent-forms.pdf` | SCR-05 | §3 |
| FR-ADM-03 | M | — | TR-AUD-02 | `/audit-events` | SCR-30 | §8 |
| FR-ADM-04 | M/S | DEC-36 | TR-BE-07 | `/usage` | SCR-30 | §3 |
| FR-ADM-05 | M | VF-12 | TR-PRV-05, TR-TEN-03 | `/data-requests` | SCR-30 | §3 |
| FR-ADM-06 | M | — | TR-AUTHZ-03 | `/internal/*`, `/support-grants` | SCR-28, SCR-30 | §5 |
| FR-EXP-01 | M | DEC-25 | TR-BE-05 | `/tabulation?format=xlsx` | SCR-22 | §4; EXP-11 |
| FR-EXP-02 | M | — | TR-BE-04 | reports | SCR-22, SCR-23 | §4 |
| FR-EXP-03 | C | — | TR-API-04 | partner API | — | — |

**Coverage result:**
- Every **M** requirement has at least one TRD requirement, a design element, a screen (or is backend-only) and a test.
- The Could items FR-AI-12, FR-RES-08 and FR-EXP-03 are intentionally not designed in detail.
- The Should analytics FRs are supported by read models (SD §14.7) without dedicated TRD rows. This is acceptable because they carry no special technical risk.

---

## 2. Cross-Document Consistency Audit (prompt §57)

| Check | Result | Evidence / fixes made during the audit |
|---|---|---|
| Every PRD feature has technical support | **Pass** (M and S) | RTM §1.2. The ID check found the dangling references `TR-SYNC-02`, `TR-CUR-01`, `FR-MRK-03` and `FR-AUD-01`. Fixed: added TR-CUR-01/02 to the TRD; PRD now points to TR-FE-04; the 00 pipeline table was corrected. |
| Every technical subsystem has a product purpose | **Pass** | Maths sandbox → FR-AI-05/FR-RUB-05. Eval harness → FR-AIQ-03. Metering → FR-ADM-04/NFR-COST-01. Audit chain → SEC-10/FR-ADM-03. Knowledge module → FR-HITL-02. Risk model → FR-AI-06. OMR → FR-AI-07. PDF → FR-EXP-02/FR-FBK-01. Identity schema → DEC-14/PRV-03. No orphan subsystem. |
| Every major workflow has a wireframe | **Pass** | UF-01..UF-09 (`04` §3) cover exam creation, capture, AI processing, review, score change, correction rule, results approval, feedback and AI performance review. Re-check and moderation have screens (SCR-24, SCR-20). |
| Every important screen has UX requirements | **Pass** | `05` covers review (§5), explanation (§6), confidence (§7), feedback (§8), forms, tables and dashboards (§4.6–4.8), capture (§10.2) and accessibility (§9). |
| Every AI capability has evaluation criteria | **Pass** | Region/mapping → L1-1. Transcription → L1-2 (CER, CTER). Criterion decisions → L2-1..5. Risk → L3-3 (AUROC/ECE). OMR → TR-OMR-01. Maths → TR-MATH-02 (false-equivalence). Injection → 06 §7.3. Rubric/paper drafting (S) → teacher confirmation plus EXM-03 acceptance (≥90% sub-parts). Feedback drafts (S) → teacher approval only. |
| Every high-risk AI capability has human oversight | **Pass** | DEC-05: every mark is teacher-confirmed. Batch only at L3 with masking and forced-open. Moderation. Appeals with AI hidden. Demotion monitors. |
| Every data requirement has architecture support | **Pass** | DATA-01 → `08` §3 + TR-PRV-03. DATA-02 → SD §4 identity schema. DATA-03 → eval project + TR-AIE-02. DATA-04 → TR-BE-07. DATA-05 → correction events (SD §7.2). DATA-06 → SD §14.7. |
| Every security requirement is represented technically | **Pass** | SEC-01 → TR-AUTHZ-01 + RLS. SEC-02 → TR-DB-02. SEC-03 → TR-SEC-03. SEC-04 → TR-AUTH-02. SEC-05 → TR-AUTHZ-03. SEC-06 → TR-SEC-02. SEC-07 → TR-CAP-06. SEC-08 → TR-SEC-04/05. SEC-09 → TR-SEC-07. SEC-10 → TR-AUD-01. SEC-11 → TR-AUTHZ-02. |
| Every major assumption is documented | **Pass** | ASM-01..22, each with a validation method (`10` §2) |
| No document contradicts another | **Pass after fixes** | Fixes applied during the audit: (1) consent model unified to CT-1/2/3 (PRD FR-ORG-06 updated to match `08` §6.1). (2) Transcripts on demand vs always shown: PRD FR-AI-02 aligned with the 06 §10 cost decision. (3) Margin claim corrected (PRD §35.2, DEC-18) after TRD §38 arithmetic. (4) DEC-05 clarified for deterministic MCQ. (5) AI cost estimates recalculated with explicit arithmetic (06 §10). Verified consistent across docs: moderation default (5%, min 3); masking 5%; second-opinion cap 35%; cost target/ceiling BDT 3/6; retention default 180 days (90–365); L3 batch ≤20 with 1-in-10 forced open; pilot volume ~20k pages/day. |

**Residual inconsistency risk:** numeric gates in `06` are provisional until EXP-01. When they change, `01` §30, `07` §11 and `09` §10 must be updated together (owner: AI lead).

---

## 3. Final Architecture Review: challenge scenarios (prompt §58)

| Scenario | Impact | Detection | Mitigation | Fallback |
|---|---|---|---|---|
| **Our core assumption is wrong: assisted marking doesn't save teachers net time** | Value proposition fails for AI grading | EXP-05 (prototype, Phase 0) and pilot telemetry vs baseline | Question-wise review, prefetch and auto-advance; deterministic totals/transcription removal (saves time even at L0); capture optimisation (spread capture, PDF import) | Kill criterion K1 → ship the deterministic core (mark capture, question-wise marking, results, tabulation) as the product. Phase 3 cover-sheet mark capture for paper-marked scripts. |
| **OCR/reading is much worse than expected** | Few cells reach L2; teachers see mostly evidence-only | EXP-02 CER/CTER; L2 gates fail | Grade from image + rubric (not transcript); structured booklet for class tests; specialist HTR second reader; cheaper on-demand transcripts | Cells stay L1/L0; value from workflow; re-run bake-off every 6 months as models improve |
| **Bangla handwriting cannot be reliably recognised** | Bangla-medium prose items never get suggestions; Bangla-medium maths may be limited | BM strata of EXP-02; subgroup gates | DEC-21 (L1 by design); maths/numeric items less dependent on prose; English-version stream as an early adopter | Product positioned honestly: AI for numeric and English-version items, workflow for everything else; revisit with the national Bangla LLM / specialist HTR |
| **Teachers disagree with AI frequently** | Low usefulness; trust erodes | Change rate per cell (>40% → demote), reason codes, masked gap | Rubric quality tooling (dry run, templates), clarifications re-suggest pending items, per-school rubric coaching | Auto-demotion to L1; school can lower levels; manual mode always available |
| **One model performs poorly (or is deprecated)** | Quality drop or outage | Validity/grounding monitors; version watch; PSI | Two qualified vendors; pinned versions; regression + gate before change | Fail over to the second vendor where it passed the gate; else items degrade to L1; manual marking continues (TR-ERR-04) |
| **AI costs become too high** | Margin loss | Cost-per-page monitor; monthly reconciliation | Batch mode default; Flash-tier; evidence-only outputs; second opinion capped; AI only on enabled cells | Restrict AI to high-value items; raise price for priority mode; K5 re-pricing; evaluate in-country open models if cheaper at volume |
| **Curriculum changes (2027 interim, 2028 new)** | Templates/rubrics outdated; AI cells change | NCTB monitoring; pack versioning | Data-driven packs and templates; generic rubric schema; re-gating on item-type change | Manual rubric authoring always works; affected cells at L1 until re-gated |
| **Students intentionally manipulate the system** | Inflated suggestions; reputational risk | Injection flags; red-team suite; anomaly on keyword stuffing | Data-only prompting; structured output; criteria require substantive evidence; instruction text disables quick confirm | Script flagged for full manual marking; school disciplinary process (outside the product) |
| **Schools don't trust AI grading** | Slow adoption | Interviews (EXP-06), pilot conversion, AI-off usage | Positioning (teacher confirms every mark), school AI view, evidence UI, audit trail, appeals | Sell the deterministic core with AI off by default; enable AI per question once trust exists |
| **AI is excellent at MCQ but poor at essays** | Expected, and designed for | Per-cell gates | MCQ is deterministic OMR (not AI); essays/creative writing out of scope; criterion-based short answers only | Keep essays at L0/L1 indefinitely; do not market essay grading |
| (added) **Legal opinion blocks cross-border AI processing** | AI unavailable until in-country solution | EXP-10 | Portable core; in-country open-weight VLM evaluation (O3 in `06` §3) | K4: pause AI features; deterministic core can run in-country |
| (added) **Capture is too slow in real schools** | Time saving negated | EXP-04 | Spread capture, auto-trigger, office staff/helpers, PDF import from ADF for unbound sheets | Paper marking + digital mark capture (Phase 3) |

**Architecture verdict:** the design **degrades gracefully**. Every AI component can fail or be switched off without blocking marking, results or publication. That is the strongest property of the architecture, and it directly answers the research's biggest uncertainty (CON-01, CON-02).

---

## 4. Final Self-Review (prompt §64)

| Reviewer lens | Question | Verdict | Notes / remaining gaps |
|---|---|---|---|
| CEO | Would I understand the business? | **Yes, with caveats** | PRD §3 and §35 plus TRD §38 explain buyer, pricing hypotheses and unit costs. **Gap:** no validated WTP or market size in money; EXP-06 is the first commercial proof. Fixed costs exceed pilot revenue (TRD §38.3). |
| Product Manager | Could I turn this into a roadmap? | **Yes** | PRD §36 phases with gates G0–G3, experiments in `10` §4, MoSCoW per FR. |
| Teacher | Would this actually solve my problem? | **Likely, to be proven** | Removes totalling and copying, organises marking question-wise, keeps authority, works on a phone. **Unproven:** net time saving after capture (EXP-04/05). |
| Student | Would the resulting system improve assessment? | **Yes, modestly** | Item-level feedback, consistent rubric application, moderation, a fair re-check with evidence. There is no student-facing app, by design. |
| AI Engineer | Can I implement the AI architecture? | **Yes** | Pipeline stages, output contracts, prompting rules, verification, risk model, gates, bake-off design, costs with arithmetic (`06`). **Decision pending:** default model (EXP-02). |
| Backend Engineer | Can I implement the system? | **Yes** | Modules, entities, APIs, events, state machines, queue lanes, security controls (`03`, `02`). **Pending:** hosting region (DEC-12), identity component (TR-AUTH-04). |
| Frontend Engineer | Can I build the interfaces? | **Yes** | Screen specs, wireframes, component states, keyboard map, performance budgets (`04`, `05`). |
| Designer | Can I design the product from these requirements? | **Yes** | Tokens, typography (Bangla specifics), colour semantics, review anatomy, confidence UX, microcopy glossary. Visual design is still to be produced and tested (EXP-09). |
| QA Engineer | Can I test every important behaviour? | **Yes** | `09`: fixture suites, isolation/authz matrices, AI gates, red team, device matrix, load/chaos/DR, human workflow tests. |
| Security Engineer | Can I identify and mitigate security risks? | **Yes** | Threat model, controls, identity isolation for AI, audit chain, pen test gates (`08` §5, TRD §18–23). **Pending:** legal confirmation of cyber-law obligations. |
| School Administrator | Would this work operationally? | **Probably** | Roster import with Bijoy conversion, consent kit, covers, capture roles, exports to ERP, settings. **Unproven:** who does capture in each school (OQ-07), and cover-sheet adoption (OQ-08). |

**Improvements made as a result of this review** (already applied): consent model unification; cost arithmetic correction and the transcript-on-demand decision; margin claims corrected; ID reference fixes; DEC-05 MCQ clarification.

---

## 5. What would change our mind (summary of revisit triggers)

| If we learn… | We will… |
|---|---|
| Net time saving <15% (EXP-05) | Drop AI grading from v1; ship the deterministic core (K1) |
| No MVP cell passes L2 (EXP-02/03) | Same as above (K2) |
| <3/10 schools sign paid-pilot LOIs (EXP-06) | Re-segment (coaching? mid-market with AI-off pricing?) (K3) |
| Legal opinion blocks cross-border AI (EXP-10) | In-country deployment study; pause AI (K4) |
| Gate-passing AI costs >BDT 6/script | Restrict AI scope or re-price (K5) |
| A current VLM reaches Bangla handwriting CER <3% on our GS at acceptable cost | Promote Bangla prose cells through gates; revisit DEC-21/DEC-37 (S06 switch rule) |
| Teachers prefer script-wise review strongly (EXP-09) | Make script-wise the default (DEC-06 revisit) |
| Two cycles of L3 evidence with severe error ≤0.1% and legal permission | Consider low-stakes autonomy for practice tests (DEC-05 revisit) |

---

## 6. Consolidated open questions
See `10-registers.md` §6 (Decision Required: DEC-12, OQ-18, OQ-19; Evidence Required: OQ-01, 02, 04, 07, 11; Experiment Required: OQ-03, 08, 09, 14, 15; Research Required: OQ-05, 10, 12, 13, 20; Product Decision Required: OQ-16, 21, 22) plus the AI-specific issues AI-OQ-1..4 in `06` §12.
