# 00 — Research Synthesis, Contradiction Register, Gap Analysis and Consolidated Evidence Base

| Field | Value |
|---|---|
| Document Name | Research Synthesis & Evidence Base |
| Version | 1.0 |
| Status | Baseline for product definition (supersedes the raw research reports as the source of truth for decisions) |
| Date | 2026-09-27 |
| Owner | Product (CPO) with Research, AI and Assessment leads |
| Purpose | Covers Steps 1–6 of the product-definition process. It inventories every research input, evaluates it critically, registers contradictions, identifies gaps, records the extra verification research, and consolidates what is actually known into an evidence base the other documents can trace back to. |
| Source Research | 14 reports in the Google Drive folder "AI Exam Answer Assesment", plus 1 older problem-space report and 1 adjacent ERP pricing report; independent verification V1 and V2 (this repo, `research/verification/`) |
| Dependencies | None. Every other document depends on this one. |

---

## 0. How to read this document

Every product decision in documents 01–11 must trace back to one of four things:

- **Verified facts (VF-xx):** confirmed against official or primary sources, or two independent reputable sources.
- **Evidence-based insights (EV-xx):** reasoned from research, with the confidence stated.
- **Assumptions (ASM-xx, in `10-registers.md`):** things we act on without proof, each with a validation method.
- **Open questions (OQ-xx):** things we do not know and must find out.

The research reports themselves are **inputs, not truth**. Each of the 14 reports is an AI-generated desk-research synthesis. None contains primary research with Bangladeshi teachers, students, schools or boards (§1.3). That single fact shapes the whole product plan: **Phase 0 of the roadmap is primary validation, not building** (see `01-PRD.md` §15).

**Legend for source codes** (used in all documents):

| Code | Report (Drive) | Extract file |
|---|---|---|
| S01 | Systemic Examination Assessment Infrastructure & Operational Problem Discovery Report | `research/extracts/A1-problem-discovery.md` |
| S02 | Bangladesh School & College Examination Workflow — Process-Mapping Study | `A2-exam-workflow.md` |
| S03 | Assessment & Examination Ecosystem — Customer Discovery & User Research | `A3-user-research.md` |
| S04 | Problem Space of Academic Operations & Assessment (older; B2B/LMS framing) | `A4-b2b-problem-space.md` |
| S05 | Comprehensive Technology Feasibility Research Report | `B1-tech-feasibility.md` |
| S06 | Technical Research Report: System Architecture & AI Model Selection | `B2-architecture-model-selection.md` |
| S07 | Technical Feasibility & System Risk Analysis | `B3-technical-risk.md` |
| S08 | Comprehensive Evaluation Framework (accuracy, psychometrics, gates) | `C1-evaluation-framework.md` |
| S09 | Architecture & Governance of HITL AI Assessment Systems | `C2-hitl.md` |
| S10 | Comprehensive Data Strategy & Governance Framework | `C3-data-strategy.md` |
| S11 | Comprehensive Product Architecture & Strategy Report (v2 17:41; v1 16:55 = S11a) | `D1-product-architecture.md` |
| S12 | Strategic Competitive Intelligence & Opportunity Blueprint | `D2-competitive-intel.md` |
| S13 | Business Model, Pricing & Unit Economics Blueprint | `E1-business-model.md` |
| S14 | Go-To-Market Strategy Research Report | `E2-gtm.md` |
| S15 | (Adjacent) Strategic Pricing Research for School & College ERP Platforms | `E3-erp-pricing-context.md` |
| V1 | Independent verification: Bangladesh education, exams, digital infrastructure, law (2026-09-27) | `research/verification/V1-bangladesh-education-regulatory.md` |
| V2 | Independent verification: Bangla HTR, math OCR, LLM grading, calibration, pricing, competitors (2026-09-27) | `research/verification/V2-ai-ocr-grading-state-of-art.md` |

`merged.pdf` (the file shared by the user) holds 569 pages containing S01–S03 and S05–S14. Its text matches the standalone reports exactly (`research/extracts/F0-merged-pdf-inventory.md`). S04 and S15 are separate files.

---

## 1. Step 1–2 — Research inventory and research matrix

### 1.1 Inventory matrix

| Code | Topic | Main findings (decision-relevant) | Important evidence | Key assumptions | Recommendations | Contradictions / outdated | Confidence | Relevance |
|---|---|---|---|---|---|---|---|---|
| S01 | Problem validation: board and internal exam evaluation | (1) The main failure is hasty, unmoderated first-pass human marking. (2) SSC 2026 full re-evaluation changed marks and grades at scale. (3) CQ = 1+2+3+4 marks. (4) Examiners mark 200–500 scripts in 10–15 days. | SSC 2026 re-evaluation figures (news-sourced). **V1 confirms the event, with different numbers.** | Fatigue drives the errors. Full-script scanning is needed. The AI grader was judged only as a *replacement*. | "Do NOT build an AI grader now." Build cover-sheet sum checks, a moderation portal and diagnostic feedback. Kill criteria. | Arithmetic errors (states 0.31%; the correct figure is 3.07% of candidates). Its "8×" should be about 3× like-for-like. Examiner fee of BDT 15 is wrong (V1: Tk 35/40). | Medium (board narrative); Low (all school-level numbers) | High: why-now, HITL stance, kill criteria |
| S02 | 32-stage internal exam lifecycle | (1) The transcription chain copies marks by hand up to 4–5 times. (2) Component pass rules and row-shifts cause the costliest errors. (3) Bijoy-vs-Unicode encoding breaks imports. (4) Supplementary sheets detach. (5) The evaluation queue is the main bottleneck. | Qualitative workflow details (plausible). All numbers are modelled. | A "standard 1,000-student school". Board recheck is clerical only (**outdated**; V1 shows full re-evaluation from 2026). | Offline multi-teacher mark entry; automatic cover arithmetic; keep essays human. | Uses Noipunno-era framing; internal cost inconsistencies. | Medium (qualitative); Low (quantitative) | High: deterministic rules, data model, edge cases |
| S03 | Stakeholders, personas, buying journey | (1) Owner = buyer, coordinator = champion, teacher = veto. (2) Human-control matrix: AI *suggests* short-answer marks and the teacher keeps 100% override; no auto-scoring of essays. (3) Offline-first "Submit Marks" moment of truth. | Noipunno failure (news). The personas are **fictional**. | NCF 2021 continuous assessment is current (**outdated**). | "Abandon AI grader; build offline orchestration + score verification." | Its ৳130/script figure comes from recruitment exams (misattributed). Salary ranges conflict. | Low–Medium | Medium–High: adoption model, control matrix |
| S04 | B2B problem ranking (LMS vs operations) | (1) The 2012 curriculum was restored after the 2024 rollback (correct). (2) Admin and revenue problems get budget; pedagogy does not. (3) Student feedback has "very low" WTP. (4) Coaching centres test at high frequency and pay for OMR. | Vendor ERP price pages (BDT 5–12 per student per month). | Price-sensitivity bands (unsourced). | Build an assessment operations engine (question bank, tabulation, OMR). Paid-LOI validation gate. | Salary and hours figures conflict internally. | Low–Medium | Medium: segment, WTP, curriculum |
| S05 | Technology feasibility (24 deliverables) | (1) Feasible **only** as AI-assisted HITL. (2) Bangla full-page HTR CER 12.8–18.7%, WER 36–48%, "unviable for autonomous grading". (3) Maths → CAS. (4) Go/No-Go gates. | Bangla baselines align with published literature (V2). | Fixed templates; self-hosted Qwen2.5-VL-72B. | STEM + English MVP, Grades 9–12; deterministic scoring; experiments before build. | Outdated models (Claude 3.5 Sonnet, GPT-4o). Over-built infrastructure (K8s, 32×H100). Residency claim contradicts use of US APIs. | Medium | High: MVP shape, gates |
| S06 | Architecture options A–F, model landscape, costs | (1) Specialised pipeline + HITL (option D) beats monolithic VLM. (2) Pass both the HTR transcript and the image crop to the LLM. (3) No RAG for small rubrics. (4) Pin model versions and run a regression set. (5) 300-script, 10-pipeline bake-off. | Price aggregator blogs (stale). No experiments were run, yet it reports "scorecard QWK ≥0.89". | Auto-accept ACS ≥0.88 with no human. Human review costs $0.15 per *script*. | Gemini 2.0 Flash as workhorse; fine-tune HTR only. | Its cited "BDPA" is India's DPDP Act. Threshold logic is inverted. Models outdated. | Medium–Low | High: bake-off design, provider abstraction |
| S07 | Risk-centred feasibility (40 sections) | (1) Anchored answer sheets with QR codes are the single biggest de-risking lever. (2) Every awarded mark must cite a text span and bbox. (3) Carry-forward partial credit. (4) RPN risk register. (5) Red-team plan for handwritten prompt injection. | Real references mixed with filler. | **Bangla CER <3% (1.9%) "feasible"**: unsupported and contradicted by V2. | Constrained hybrid, STEM only, SCOPE conformal gate, triple-LLM ensemble. | The most over-engineered report (Kafka, K8s, GNN, 14 POCs). SCOPE was designed for pairwise judging. | Low–Medium | High: risk register, grounding, templates |
| S08 | Evaluation framework and psychometrics | (1) "Accuracy" has six layers. (2) Errors compound across stages. (3) The target is measured human–human agreement, not perfection. (4) Absolute agreement (QWK, MAE), not correlation. (5) Risk–coverage curves. (6) Boundary proximity triggers review. (7) Release gates. (8) Show evidence before the score (automation bias). | Metric formulas are standard and correct. | Fixed thresholds (QWK 0.85/0.88) conflict with its own human-baseline principle. | Golden + Challenge datasets; version-tagged evaluation records. | Its own targets conflict (CER 3/5/8%, QWK 0.78/0.85/0.88). SSC/HSC 30–50% auto-accept is unsourced. | High (definitions); Low (numbers) | Very High: evaluation spec |
| S09 | HITL architecture and governance | (1) Operating mode depends on stakes (HOTL / HITL / Human-in-Command). (2) Six reviewer roles. (3) Correction taxonomy A–H with mandatory reason codes. (4) Instruction precedence. (5) Exception rules sandboxed and expiring. (6) No online learning. (7) 5% masked reviews. (8) Unconditional right to human regrade. | Arxiv preprints on calibrated grading (plausible). | Temperature-scaled verbalised confidence (methodologically muddled). | Routing matrix at C>0.90 / CRI<0.20. | Routing maths means only MCQs can auto-finalise (contradicts its own "35–65% automated"). Cost arithmetic error. Board QWK ≥0.95 exceeds human IRR. | Medium–High (design); Low (numbers) | Very High: HITL spec |
| S10 | Data strategy, privacy, governance | (1) PII isolated at the edge. (2) HMAC tokenisation. (3) Training opt-in kept separate from the service DPA. (4) Staged override hygiene. (5) Curriculum version tags. (6) Crypto-shredding deletion. (7) Gold annotation tiers. | Legal claims rest on Scribd, Facebook and paper titles. | FERPA/COPPA "school authorisation" transplanted to Bangladesh. | Institutional opt-in; local copy; 10→500 school pilot. | Retention tables contradict each other. Raw data purged at 30 days even though appeals can come later. "Eight boards" (there are nine). COPPA is miscited. | Medium–High (patterns); Low (law, numbers) | Very High: data and privacy spec |
| S11 | Product architecture, UX and state machine | (1) Option B chosen (ingestion + verification + tabulation). (2) REV-01 review console. (3) State machine with invariants. (4) Automation levels by item type. (5) Edge cases, including prompt injection. (6) Keyboard-first review. | S11a (the earlier version) had question-wise review, automation-bias spot checks and named Bangladeshi ERPs; **all lost in v2**. | Template-free parsing; batch auto-approve at C≥0.85. | North Star = teacher-verified scripts per term. | The MVP scope contradicts its own roadmap (Bangla HTR in or out?). Review targets of <12–25 s per whole paper are implausible. | Low–Medium (facts); Medium–High (UX patterns) | High: UX, state model |
| S12 | Competitive landscape | (1) No verified product grades handwritten Bangla. (2) Indian analogues exist (Saraswati AI, GradeFoundry, VedaAI, DeepGrade). (3) Foundation models are suppliers **and** a substitution threat. (4) Four validation experiments. | Vendor sites and listicles. | Its moat claims (red-ink overlays, mobile capture) are contradicted by its own tables. | Price BDT 12–20 per booklet; three GTM motions at once. | Outdated model names. Several listed local players were not analysed. | Low–Medium | High: positioning, threats |
| S13 | Business model, pricing, unit economics | (1) Value metric = evaluated script. (2) Annual prepaid allowance plus overage, because usage is seasonal (peaks 10–12× base). (3) **Human review is about 82% of COGS**, so the flag rate drives margin. | Arithmetic errors (revenue BDT 19.5M, not 22.5M; gross margin about 59%). | 4-page scripts; GPT-4o-mini prices; Textract for Bangla (**Textract does not support Bangla**, V2). | Coaching and O/A-level beachhead; free 200-script pilot. | LTV = 3 years with zero churn. | Low–Medium | High: economics structure |
| S14 | Go-to-market | (1) Relationship-led sales. (2) Live demo on the school's own scripts. (3) 14-day pilot with parallel manual marking. (4) Gates ≥90% agreement and >60% time saved. (5) ERP co-sell at 15–20%. | None (market sizes are assumed). | ACV BDT 0.75–1.2M; CAC BDT 150k. | Beachhead: Dhaka English-version and elite Bangla-medium schools plus coaching. | "~88% Bangla" is character recognition, not grading. | Low | Medium: sales motion, pilot design |
| S15 | (Adjacent) ERP pricing | Mainstream schools pay **BDT 42–60 per student per year for a whole ERP** (BDT 45–65k/yr). Institutions pay by annual cheque (invoice Dec, due Jan). MPO fee caps apply. Paid, credited pilots (BDT 5,000). Avoid freemium for variable-cost items. | Published vendor price points. | — | — | Institution counts conflict with S14. | Medium (structure) | High: price ceiling constraint |

### 1.2 Research coverage vs the areas the prompt enumerates

| Research area requested | Covered by | Coverage quality |
|---|---|---|
| Problem research | S01, S02, S04 | Desk-only; board-exam evidence good (news), school-level evidence absent |
| Bangladesh education workflow | S02, S01 | Qualitatively rich; quantities modelled |
| User, teacher, student, school research | S03 (fictional personas), S11 | **No primary research** |
| Curriculum | S04 (correct), others (partly outdated) | **Weak**. Verified in V1. |
| Assessment methodology / psychometrics | S08, S09 | Good definitions; thresholds unsourced |
| Mathematics evaluation | S05, S06, S07 (sections) | Moderate; V2 added SymPy pitfalls and HMER state of the art |
| Bangla language / "BLM" | S05, S06, S07 (sections) | Contradictory; V2 resolved it with published benchmarks |
| OCR / handwriting | S05, S06, S07 | Contradictory; V2 verified |
| AI model research | S05, S06, S07 | **Outdated** (2024-era models); V2 verified current models and prices |
| Technology feasibility, risks | S05, S07 | Good risk identification; over-engineered solutions |
| Evaluation metrics, accuracy | S08 | Good |
| Data strategy | S10 | Good patterns; legal content unreliable → V1 |
| Competitors | S12 | Moderate; V2 partially verified |
| Business model, pricing, GTM | S13, S14, S15 | No WTP evidence; S15 gives the most credible constraints |
| Human-in-the-loop | S09 | Good design |
| Product design | S11 | Good UX patterns; scope explosion |
| **Not present:** a dedicated curriculum ontology report, a dedicated "BLM" (Bangla language model) report, a UX research report with observation data, a legal opinion | — | Gaps (§3) |

### 1.3 Cross-cutting credibility finding

All 14 reports share the signatures of generated deep-research output:

- unresolved `[cite: N]` markers;
- precise numbers with no measurement behind them;
- personas presented as "evidence-based" that are fictional composites (S03);
- self-assigned "Verified" labels (S03);
- shared sources across reports (S08, S09 and S10 cite the same preprints), so agreement between reports is **not independent corroboration**;
- outdated model names in every technical report.

Consequences for this product definition:

1. **No number from the reports becomes a requirement unless it is verified (V1/V2) or explicitly labelled as an assumption or target to validate.**
2. Where reports agree only because they share sources, the agreement counts as one data point.
3. The reports' qualitative design patterns (HITL modes, correction taxonomy, rubric schema, state machine, PII isolation) are used as **design inputs**. Good practice does not need local proof to be adopted. Local *numbers* do.

---

## 2. Step 3 — Contradiction Register

Every entry follows the same structure: sources, conflict, evidence, investigation, resolution, remaining uncertainty.

| ID | Source A | Source B | Conflict | Evidence and investigation | Resolution | Remaining uncertainty |
|---|---|---|---|---|---|---|
| **CON-01** | S01, S03 ("do not build / abandon AI grader") | S05, S06, S07, S11, S12 (build HITL AI grading) | Should the product grade answers with AI at all? | S01 and S03 argue against **autonomous replacement**. Neither tests teacher-confirmed suggestions, and S03's own control matrix allows AI-*suggested* short-answer marks. V2: published deployments with mandatory human verification report 16–23% grading-time reduction (VUB, arXiv 2603.13083) and human-level accuracy when uncertain items are routed to humans (Kortemeyer 2025). Commercial analogues (Eklavvya, Graide, Gradescope) use draft-plus-human-confirmation. V1: the 2026 marking law and re-evaluation shock raise demand for consistency and evidence trails. | **Build AI-assisted, teacher-confirmed marking**, not autonomous grading. Build a deterministic mark-capture and tabulation core that delivers value even when AI is switched off (DEC-01). | Whether the time saved *net of capture effort* is large enough to pay for. Validated in Phase 0/2 (OQ-01). |
| **CON-02** | S07 (Bangla HTR CER <3%, "FEASIBLE") | S05 (CER 12.8–18.7%, "unviable for autonomous grading"); S06 (8–11%) | Is Bangla handwriting recognition production-ready? | V2 (verified): the best published system, GraDeT-HTR (EMNLP 2025), reaches **6.19% CER on BN-HTRd and 8.68% on Bongabdo**, on curated data. Gemini 2.5 Flash reaches 19.39% / 37.42%. No benchmark of current frontier models on Bangla HTR exists. No dataset of real Bangladeshi exam scripts exists. S07's 1.9% has no traceable source. | S07 is rejected. **Bangla handwritten prose is not assumed production-ready.** Bangla prose items launch at support level L1 (evidence only) and are promoted only by passing evaluation gates (DEC-04, DEC-21). | Actual CER of 2026 frontier VLMs on Bangladeshi exam pages. This is the first Phase 0 experiment (EXP-02). |
| **CON-03** | S06 (auto-accept at ACS ≥0.88, no human), S07 (conformal auto-commit), S09 (auto-finalise for term exams), S08 (30–50% SSC/HSC auto) | S05, S11 ("every mark confirmed"), S09 (Human-in-Command for high stakes), S03 (teacher keeps final override) | Can any constructed-response mark be finalised without a human? | V2: autonomous marking of high-stakes work is not supported by current evidence. V1: the Public Examinations (Offences) (Amendment) Act 2026 makes over- or under-marking of *public* exam scripts punishable, confirmed by a third examiner. The PDPA 2026 grants rights over automated decisions. Draft National AI Policy v2 treats education as **high-risk** and requires human review. S09's own routing maths prevents auto-finalisation of constructed responses. | **In MVP and Pilot, no mark becomes final without an identified teacher's confirmation** (DEC-05). Batch confirmation of high-confidence items is permitted only at level L3, with masked audits. Autonomous finalisation is *out of scope*, to be reconsidered only for low-stakes practice tests after evidence exists (revisit condition in DEC-05). | Whether schools will want low-stakes autonomy later (class tests). |
| **CON-04** | S08 (QWK ≥0.85 / 0.88), S09 (board ≥0.95, term ≥0.88), S06 (≥0.89 claimed) | S10 (≥0.75), S05 (≥0.80), V2 literature (human–human QWK 0.61–0.85; common automated-scoring bar ≥0.70 and within 0.10 of human–human) | What agreement is "good enough"? | S08's own principle, which is psychometrically sound, says the target must be relative to *measured* human–human agreement on the same items. Targets above human IRR are invalid. No Bangladeshi IRR baseline exists. | Adopt **relative-to-human-baseline gates per item type** with an absolute floor (QWK ≥0.70) and a non-inferiority margin. The numbers are in `06-ai-model-decision-and-evaluation.md` §4 (DEC-29). | Actual Bangladeshi teacher–teacher agreement on CQ sub-parts. Phase 0 baseline study (EXP-01). |
| **CON-05** | S13 (coaching + O/A-level first), S04 (coaching first) | S14 (Dhaka English-version and elite Bangla-medium schools), S03 (urban private schools), S12 (four segments at once) | Beachhead segment | None of these is validated. The documents agree only that private, owner-run institutions decide fast and that government schools should be avoided. V1: ~97% of secondary schools are non-government; school internal exams are teacher-set CQ papers with rubrics (NCTB 2024 guideline). English-medium schools use CAIE/Edexcel mark schemes (the Bangla moat is irrelevant there, and competitors already serve English). Coaching volume is often MCQ (S12, E0), which OMR already handles. | **Primary: urban private (non-government) secondary schools, Grades 9–10, Bangla-medium and English-version streams, in Dhaka.** **Secondary experiment:** 1–2 coaching centres, for *written* tests only (DEC-02). | WTP and adoption in each segment (EXP-06). |
| **CON-06** | S13 (BDT 5–8/script), S14 (BDT 8–15), S12 (BDT 10–30), S01 (kill if <BDT 15/student/yr), S04 (BDT 5–12/student/month) | S15 (mainstream schools pay BDT 42–60/student/yr for an entire ERP) | Price level | No primary WTP data exists anywhere. S15 is the most credible anchor (published vendor prices). V1: board examiners are paid **Tk 35 (SSC) / Tk 40 (HSC) per script**, which anchors the perceived market value of marking one script. V2: AI compute costs roughly $0.003–0.05 per page per model call. | Pricing is a **hypothesis to test**, not a requirement. The product must meter per page and per script and support prepaid allowances. Design-to-cost ceiling in DEC-18. | Real WTP (EXP-06). |
| **CON-07** | S13 (free 200-script pilot), S14 (free 500–1,500 scripts) | S15, S04 (paid, credited pilot; "if institutions demand free trials, stop") | Free or paid pilot | Neither is evidenced. A paid pilot is a stronger demand signal and is cheaper to run. | Default: **paid, credited pilot**. A free pilot is allowed only for 3–5 Phase 0 design partners who contribute consented data (DEC-19). | Conversion rates. |
| **CON-08** | S02 (board re-scrutiny is clerical only) | S01 (full re-evaluation in 2026) | Board re-evaluation policy | V1 (verified): SSC 2026 allowed **full re-evaluation for the first time**. 402,052 candidates challenged 1,056,458 written scripts. 56,259 candidates had marks changed, 27,836 grade changes, 4,585 fail→pass. The government plans a criteria-based policy limiting future re-evaluation. S01's "327,271 applications" does not match V1 (likely an early or partial figure). | S02 is outdated. V1's numbers are used. | Final re-evaluation policy for 2027+ (V1). Low impact on MVP (internal exams). |
| **CON-09** | S03, S02 (NCF 2021 continuous assessment, PI/BI, Noipunno current) | S04 (2012 curriculum restored) | Curriculum in force | V1 (verified): the competency curriculum was rolled back on 2024-09-01. Secondary uses revised 2012-based textbooks in 2026. Science, humanities and business groups are reinstated. **A new curriculum is planned for 2028**, phasing undecided. Interim changes arrive in 2027. | Design for the revised 2012 CQ/MCQ format, with a **versioned, data-driven curriculum and rubric model** so the 2028 change is a data change, not a code change (DEC-15, DEC-16). No PI/BI features. | The 2028 curriculum's assessment design (monitor; RSK-10). |
| **CON-10** | S01 (BDT 15/script) | S02 (BDT 25–45), S03 (৳130) | Examiner honorarium | V1 (verified): **Tk 35 SSC, Tk 40 HSC** per script, with a raise to Tk 45/50 approved in June 2025 (payment in 2026 unverified). S03's ৳130 is the *recruitment exam* rate. | Use V1. | Whether the raise is paid. |
| **CON-11** | S05 (law requires local residency), S06 ("BDPA" 7-year retention, local storage), S10 (localisation, "Act 2026 Law 63") | S07 (AWS/US APIs; silent on law) | Data residency and law | V1 (verified): the **Personal Data Protection Act 2026 (Act No. 63 of 2026)** was enacted 2026-04-10. A child is anyone under 18, and processing needs **parental or guardian consent** (s.9). Localisation was narrowed in 2026 to *restricted* data and designated CII. Cross-border transfer is allowed on consent, contract, or the data subject's interest (education is given as an example). Processing records must be kept ≥5 years. The Act gives rights over automated decisions. The 7-year retention claim is unsourced. S06's "BDPA" citation is India's DPDP Act. | Use V1 as the working legal baseline. **A legal opinion is a Phase 0 gate** (DEC-12, OQ-05). Design for portability to in-country hosting. | Whether exam scripts are classed as "confidential" or "restricted" (s.29); regulations under the Act; whether the children's profiling ban survived; AI-training legality (V1). |
| **CON-12** | S10 (raw scans deleted after 30 days) | S08, S09 (every mark links to the raw image; appeals and regrades) | Retention vs auditability | School results, disputes and re-checks run for weeks after marking. S10's 30-day purge would destroy evidence before appeals close. | Retention tied to the **exam lifecycle**: raw images are kept until *result finalisation + appeal window* (school-configurable, default 180 days after publication), then deleted. Marks and audit records are kept ≥5 years (PDPA processing record) (DEC-30). | School-level record-keeping expectations (OQ-12). |
| **CON-13** | S11 v2 (template-free parsing is a differentiator) | S07, S05 (anchored templates, QR codes) | Answer-sheet format | Template-free parsing of unconstrained booklets is much harder. S07's anchored-sheet lever is the strongest de-risking idea across all reports. Schools use their own booklets and supplementary sheets (S02, S11a). | **A platform-generated QR cover sheet is mandatory; the school's normal booklet stays.** An optional structured answer booklet (answer boxes, pre-printed question labels) is offered for class tests (DEC-07). | Whether schools will adopt a printed cover sheet (EXP-04). |
| **CON-14** | S11 v2 (script-by-script review) | S11a v1 (question-wise "horizontal" review) | Review paradigm | Question-wise review is the established pattern (Gradescope). It improves consistency (one rubric in the reviewer's head at a time) and fits phone screens. | **Question-wise review is the default**; the script view is used for completeness and totals (DEC-06). | Teacher preference (usability test). |
| **CON-15** | S06 (Gemini 2.0 Flash), S05 (self-hosted Qwen2.5-VL-72B), S07 (Claude 3.5 Sonnet + GPT-4o ensemble), S13 (GPT-4o-mini) | V2 (current models and prices, Sept 2026) | Model selection | All the models the reports name are outdated. V2 verifies the current families and prices: Anthropic (Opus 5.5, Sonnet 5, Haiku 4.5), OpenAI (gpt-5.6 sol/terra/luna), Google (Gemini 3.8 Flash, 3.1 Pro). No published benchmark covers them on Bangla handwriting. | **No model is pre-selected.** Selection goes through a provider-agnostic bake-off on local data. Cost, accuracy, Bangla quality and data terms decide (DEC-08). | Bake-off results (EXP-02, EXP-03). |
| **CON-16** | S13 (vendor-paid reviewers at BDT 15/review) | S14, S03 (the school's own teachers review) | Who does human review | S13's own model shows vendor review is 82% of COGS. The mainstream price ceiling (S15) cannot absorb it. Teachers are the accountable markers. | **The customer's teachers review. The vendor provides no marking labour** (DEC-26). | — |
| **CON-17** | S05 (deterministic deductions only) | S06 (LLM allocates partial credit from CAS diff); S07 (rule engine with carry-forward) | Maths partial credit | V2: CAS equivalence is undecidable in general and `simplify` drops domain restrictions. Multi-line handwritten maths recognition hallucinates corrections. | Rubric-defined step criteria. The LLM proposes which student step matches which criterion; CAS **verifies** equivalence where parseable; deterministic carry-forward (ECF) rules compute the marks; the teacher confirms. CAS never awards method marks alone (DEC-32). | CAS parse coverage on real student LaTeX (EXP-03). |
| **CON-18** | S05, S07 (K8s, Kafka, GPU clusters, microservices) | S06, S11 (single GPU / Celery–Redis) | Infrastructure | Pilot volume is thousands of scripts. The prompt forbids over-engineering. | Modular monolith, PostgreSQL, object storage, a simple job queue, managed AI APIs, no GPUs in the MVP (DEC-11). | — |
| **CON-19** | S12 (don't build OMR/MCQ) | S03 (MCQ fully automated, trusted), S04 (smartphone OMR for coaching) | MCQ handling | V1: school internal exams have **no separate OMR sheet**; objective answers are written inside the script (NCTB 2024 guideline). Board MCQ is OMR (not our market). | MCQ answers are captured through a **bubble grid printed on the platform cover sheet** (deterministic OMR). Inline handwritten MCQ letters are a fallback read by AI and confirmed (DEC-22). | Whether schools switch to the bubble grid. |
| **CON-20** | S14 (time saved >60%), S11 (60–80%), S12 (up to 90%) | S09 ("up to 40%"), V2 (16–23% with mandatory verification; Graide vendor −74%) | Achievable time saving | Only V2 contains measured numbers, and they are much lower than the reports' claims. | **Never promise more than measured.** Pilot target: ≥30% reduction in teacher minutes per script for marking + totalling + mark entry combined, and ≥80% reduction in transcription/tabulation time (DEC-31). | Measured in pilot (EXP-05). |
| **CON-21** | S08 (show evidence first, score later), S10 (hide marks until "Evaluate") | S09 (pre-filled one-click sign-off), S11 v2 (batch auto-approve at C≥0.85) | Automation-bias UX | S08 cites evidence (PNAS Nexus via PsyPost; secondary) that teachers over-accept AI errors. S11 v1 had random mandatory checks; v2 dropped them. | Criteria-first review, 5% masked items, no one-click batch approve below L3, and L3 needs evidence of calibration (DEC-33). | Effect sizes in the Bangladeshi context. |
| **CON-22** | S09 (immediate RAG injection of corrections) | S10 (staged, validated, opt-in before any training use) | Learning from corrections | Unvalidated corrections can poison behaviour across tenants. PDPA and AI-training legality are uncertain (V1). | Corrections take effect **only within their own scope** (the question, exam or school where they were made) after teacher confirmation. Cross-tenant or global use requires validation plus a data-use agreement. No model training in MVP/pilot (DEC-17, DEC-13). | — |
| **CON-23** | S13 (4-page script) | S01 (12–16 pages SSC/HSC), S02 (8–16), V2 cost arithmetic (assumed 12) | Pages per script | Drives cost and capture time. No measurement exists. | Model costs per page. Base case 10 pages for internal exams (range 6–16). Measure in Phase 0 (ASM-07). | Measured page distribution (EXP-04). |

---

## 3. Step 4 — Research Gap Analysis

Status legend: **Sufficient** (a decision can be made now); **Partial** (a decision is possible with explicit assumptions); **Insufficient** (a decision needs new evidence before commitment).

| Area | Research Status | Gap | Impact | Additional Research Required |
|---|---|---|---|---|
| Problem | Partial | Board-exam problem verified (V1). **The internal-exam problem is not measured**: time per script, error rate, how much marking is judgement vs arithmetic. | High: the ROI story depends on it | Time-motion study with 15–20 teachers; audit of 500 marked internal scripts (margin vs cover totals) (EXP-05, EXP-07) |
| Users | Insufficient | No interviews. Personas are fictional. | High | 30 interviews (teachers, coordinators, principals/owners), 10 observations (EXP-06) |
| Market | Partial | Institution counts verified (V1: ~16,600 secondary schools, ~97% non-government). Segment size by ability to pay unknown. | Medium | Build a target list of Dhaka private secondary schools with tuition bands |
| Curriculum | Sufficient for MVP | V1 verified the format (70 written + 30 MCQ; 75 + 25 practical; CQ ka/kha/ga/gha 1/2/3/4; 4th-subject bonus; GPA table). 2028 reform unknown. | Medium | Obtain the NCTB SSC 2026 mark-distribution PDFs; collect 20 real school question papers and rubrics |
| Assessment | Partial | Metric framework good (S08). **No Bangladeshi human–human agreement baseline.** | High: all AI gates depend on it | Triple-marking study (EXP-01) |
| Product | Partial | UX patterns good. MVP scope contradictory in the sources. | Medium | Resolved by decisions (PRD) and usability tests |
| AI | Partial | Current models unbenchmarked on Bangla handwriting, BD maths handwriting or CQ grading. | **Critical** | Model bake-off on 300–500 real scripts per subject (EXP-02, EXP-03) |
| Data | Partial | No exam-script dataset exists (V2). Consent process untested. | High | Consent kit and Phase 0 collection |
| Technology | Sufficient | Architecture patterns clear; over-engineering rejected. | Low | — |
| Security | Sufficient (patterns) | Prompt injection via *handwriting* is untested (V2: no study found). | Medium | Red-team set with handwritten injections (EXP-08) |
| Privacy | Partial | PDPA 2026 verified (V1). Regulations, children's profiling clause and AI-training legality unclear. | **Critical (gate)** | Legal opinion from Bangladeshi counsel (Bangla-literate) (OQ-05) |
| Business model | Insufficient | No WTP data. Unit economics in the reports are arithmetically flawed. | High | Price tests in interviews plus paid-pilot conversion (EXP-06) |
| Pricing | Insufficient | Anchors conflict by up to 10×. | High | As above |
| GTM | Partial | Sales motion plausible, unvalidated. | Medium | Design-partner recruitment is itself the test |
| Operations | Insufficient | Who scans, how long capture takes, whether it eats the time saved (S01 kill criterion). | **Critical** | Capture time-motion with phone stand vs ADF (EXP-04) |
| Human-in-the-loop | Sufficient (design) | Teacher acceptance of the review workflow untested. | High | Usability tests with 12–20 teachers (EXP-09) |
| Accuracy | Insufficient | See Assessment and AI. | Critical | EXP-01..03 |
| Evaluation | Sufficient (framework) | Gold data absent. | High | Built in Phase 0 |
| UX | Partial | No observation of teachers marking. | Medium | EXP-05, EXP-09 |
| Architecture | Sufficient | — | Low | — |
| Scalability | Sufficient | Peak seasonality known qualitatively (exam seasons). Peak volumes per school unknown. | Low–Medium | Collect exam calendars from design partners |
| Legal / regulatory | Partial | See Privacy. Plus: school-level record-retention duties; whether AI-assisted *internal* marking is regulated at all (V1: no rule found). | High | Legal opinion; NCTB/DSHE informal consultation |
| Deployment / hosting | Partial | No hyperscaler region in Bangladesh (V2: none of Anthropic, OpenAI or Google offers BD residency). | High | Legal opinion plus local data-centre quote (OQ-06) |

**Conclusion of gap analysis.** The research is **sufficient to design** the product: architecture, workflows, data model, HITL, evaluation framework. It is **insufficient to commit** to accuracy promises, pricing, segment or autonomy levels. The roadmap therefore has an explicit Phase 0 of experiments with kill/continue gates (`01-PRD.md` §15). The product is built so that each uncertain capability can be switched on per subject and question type **only when its gate passes** (DEC-04).

---

## 4. Step 5 — Additional research conducted

Two independent verification studies were run on 2026-09-27, using web sources and prioritising official Bangladeshi sources, peer-reviewed papers and vendor documentation. Full texts with URLs: `research/verification/V1-*.md`, `V2-*.md`.

### 4.1 Verified facts used in product decisions (VF register)

| ID | Verified fact | Source (in V1/V2) | Used by |
|---|---|---|---|
| VF-01 | The 2021/22 competency curriculum was rolled back on 2024-09-01. Secondary uses revised 2012-based textbooks in 2026. Science, humanities and business groups are reinstated. | V1 Q1 (Daily Star, FE, Dhaka Tribune 2024-09-01; Dhaka Tribune 2026-05-15) | DEC-15, DEC-16 |
| VF-02 | A new curriculum is planned for **2028** (not 2027), with phasing undecided. 2027 adds four new subjects. Textbook content (esp. History, Bangla, ICT) is revised yearly. | V1 Q1 (TBS 2026-07-01; Prothom Alo 2026-06-08) | RSK-10, DEC-16 |
| VF-03 | SSC 2026 format: 70 written (creative + short answer) + 30 MCQ; subjects with practicals 75 + 25. MCQ on OMR at board level. Written part includes short-answer items (e.g., Maths 50 CQ + 20 SA + 30 MCQ; Physics 40 CQ + 10 SA + 25 MCQ + 25 practical, per a 2025 school syllabus). | V1 Q2 (BSS 2025-01-03; CPSCS syllabus 2025) | Rubric templates, MVP subjects |
| VF-04 | CQ sub-parts ka/kha/ga/gha = Knowledge 1 / Comprehension 2 / Application 3 / Higher-order 4 = 10 marks. "Answer N of M" choice rules apply. | V1 Q2 implications; consistent across S01, S02, S04, S09, S10, S11 | Rubric engine |
| VF-05 | GPA scale: 80–100 A+ 5.0; 70–79 A 4.0; 60–69 A− 3.5; 50–59 B 3.0; 40–49 C 2.0; 33–39 D 1.0; <33 F. Pass mark 33%. Components (theory/MCQ/practical) must be passed separately. The 4th subject counts only above GP 2.0, and GPA is capped at 5.0. | V1 Q2 (teachers.gov.bd; results reporting) | Result engine |
| VF-06 | NCTB 2024 interim guideline for internal annual exams: **subject teachers write question papers**, following NCTB samples. Setters must provide **sample answers and rubrics**. **No separate OMR sheet**; objective answers are written in the script. 30% continuous + 70% written. In 2025–26, schools run class tests, half-yearly and annual exams in board format. | V1 Q3 (NCTB guideline copy; CPSCS 2025) | Segment (internal exams), MCQ design, rubric input |
| VF-07 | SSC 2026: 1,829,485 sat; 62.25% pass. First common question papers across boards since 2006. HSC 2026: 1,270,583 candidates. | V1 Q2 | Context |
| VF-08 | **Public Examinations (Offences) (Amendment) Act 2026** (gazetted 2026-07-09): over- or under-marking a public exam script is punishable by up to 2 years, if confirmed by a third examiner. **Full re-evaluation** was allowed for SSC 2026: 402,052 candidates, 1,056,458 scripts, 27,836 grade changes. | V1 Q2 | Why-now, audit trail requirement |
| VF-09 | Board examiner pay: Tk 35 (SSC) / Tk 40 (HSC) per script. Examiners mark 300–600 scripts in 10–20 days. Marking-quality actions: e.g., Jashore board, 1,684 examiners facing action. | V1 Q8 | Value anchor, positioning |
| VF-10 | ~16,570 secondary schools (2024), ~97% non-government. 4,876 colleges; 9,269 madrasahs; 293,289 secondary teachers. 34,129 non-government institutions, of which 6,179 are non-MPO. ~12,000 Cambridge candidates in 90 schools. | V1 Q4 | Market sizing, segment |
| VF-11 | Households: 75.1% own a smartphone, 58.2% have internet, 9.1% a computer. Secondary schools with a computer lab: 40.25%; madrasahs 13.23%. The best-selling phone band is Tk 15–25k. | V1 Q5 | Phone-first capture, offline, device targets |
| VF-12 | **PDPA 2026 (Act 63 of 2026)** enacted 2026-04-10. Child = under 18; a parent/guardian consents (s.9). Rights include access, correction, portability, and objection to **automated decisions**. Processing records ≥5 years. Breach reporting. Four-tier data classification. Cross-border transfer allowed on consent/contract/interest. Localisation limited to restricted data and CII. National Data Management Authority created. | V1 Q6 | Privacy architecture, consent, hosting |
| VF-13 | The draft National AI Policy 2026–2030 (v2, not adopted) lists **education as high-risk**, with rights to explanation, contestation and human review, Algorithmic Impact Assessments, and 5-year retention of high-risk AI logs. | V1 Q6 | HITL, audit, explainability |
| VF-14 | No board on-screen-marking or AI-grading pilot was found. An AI assessment/OMR startup ("Correct") received a PM startup grant. Rajshahi University is piloting coded anonymous scripts. | V1 Q7; V2 Q7 | Competition, positioning |
| VF-15 | Bangla HTR state of the art: GraDeT-HTR CER **6.19% (BN-HTRd), 8.68% (Bongabdo)**, word-level pipeline. Line-level CER 26–38%. Gemini 2.5 Flash CER 19.39% / 37.42%. No benchmark of current frontier models; **no BD exam-script dataset**. | V2 Q1 | CON-02, DEC-21 |
| VF-16 | Azure Document Intelligence: **no Bengali** handwriting (nor printed). AWS Textract: English alphabet only. Mathpix: printed Bengali only. Google lists Bengali OCR; whether Bengali *handwriting* is supported is unverified. | V2 Q2 | Build/buy (OCR) |
| VF-17 | Handwritten maths: fine-tuned Uni-MuMER 79.74% expression rate (CROHME); zero-shot Gemini 2.5 Flash 55.32%, GPT-4o 48.81%. Multi-line student work degrades sharply and models hallucinate corrections. | V2 Q3 | Maths engine (tolerate noise; human confirmation) |
| VF-18 | LLM grading of handwritten STEM: GPT-4o with rubric, 46.7% exact, r = 0.62. GPT-5 on calculus reached human-level only with ~70% routed to humans. A 2026 ensemble reached ~8-point MAD with a ~17% review rate. A mandatory-verification deployment saved 16–23% time. | V2 Q4 | Accuracy expectations, time-saving promise |
| VF-19 | Human–human QWK is typically 0.61–0.85 (ASAP) and 0.82 (TOEFL Junior). The common automated-scoring bar is QWK ≥0.70 and within 0.10 of human–human (partial verification). | V2 Q4 | Gates (DEC-29) |
| VF-20 | Confidence: verbalised confidence has better ECE, while multi-sample consistency better **ranks** errors (AUROC). Combining signals is safest; routing needs ranking. | V2 Q5 | Confidence design |
| VF-21 | Current API prices (per MTok, in/out): Claude Opus 5.5 $4/$20; Sonnet 5 $2/$10; Haiku 4.5 $1/$5. gpt-5.6-sol $5/$30, -terra $2.50/$15, -luna $1/$6. Gemini 3.8 Flash $0.75/$3.75 (to 2026-12-31, then $1.50/$7.50); Gemini 3.1 Pro preview $2/$12. Batch is −50%. Image tokens for a 1500×2000 page: Claude hi-res 3,888; OpenAI high 2,942; Gemini high 1,120. | V2 Q6 | Cost model |
| VF-22 | No LLM vendor offers Bangladesh data residency. Anthropic: global/US inference. OpenAI: India storage only. Google Document AI: asia-south1. API data is not used for training on paid tiers. Abuse-monitoring retention is 30 days (OpenAI/Anthropic) or 55 days (Gemini). ZDR is available on request. | V2 Q6 | Hosting, privacy |
| VF-23 | No commercial product verifiably grades handwritten Bangla. The dominant pattern is draft score + human accept/override (Eklavvya, Graide, Gradescope grouping). | V2 Q7 | Positioning, HITL |
| VF-24 | SymPy `==` is structural. `simplify(a−b)==0` is not infallible and silently drops domain restrictions (checked in a local run). Math-Verify parses LaTeX and compares asymmetrically, with timeouts. | V2 Q8 | Maths engine |
| VF-25 | Prompt-injection vulnerability of LLM graders is **model-dependent** (contradictory studies). No study covers *handwritten* injections. | V2 Q4 | Red-team, security |

### 4.2 Claims in the research that were refuted or corrected by verification

| Claim | In | Correction |
|---|---|---|
| Bangla HTR CER <3% achievable (1.9%) | S07 | Unsupported; best published 6–9% on curated data (VF-15) |
| AWS Textract as the Bangla OCR option | S13 | Textract does not support Bangla (VF-16) |
| "BDPA" citation (7-year retention, local storage) | S06 | The citation is India's DPDP Act; the Bangladesh PDPA 2026 is different (VF-12) |
| Examiner honorarium BDT 15 / BDT 130 | S01 / S03 | Tk 35/40 (VF-09) |
| Board recheck is clerical only | S02 | Full re-evaluation in 2026 (VF-08) |
| NCF 2021 / PI-BI / Noipunno current | S03, S02 | Rolled back (VF-01) |
| "Eight general boards" | S10 | Nine general boards plus Madrasah and Technical (S10 extract) |
| NCTB "regulates SSC/HSC exams" | S09 | NCTB sets curriculum; the education boards conduct exams |
| Current models = GPT-4o / Claude 3.5 Sonnet / Gemini 2.0 Flash | S05, S06, S07, S12, S13 | Superseded (VF-21) |

---

## 5. Step 6 — Consolidated Evidence Base (EV register)

Each insight carries: the statement, its support, its confidence, and the decision it drives. Confidence: **H** = verified or strongly converging, independent; **M** = plausible with partial support; **L** = hypothesis.

### 5.1 Problem and context

| ID | Insight | Support | Conf. | Drives |
|---|---|---|---|---|
| EV-01 | Marking quality is a **publicly salient problem in 2026**. Mass re-evaluation changed tens of thousands of grades, and mis-marking of public exams is now criminalised. Consistency and evidence trails have social and legal value. | VF-08, VF-09 | H | Positioning ("consistent, evidenced marking"), audit trail |
| EV-02 | For **internal** school exams, teachers set the papers and write the rubrics, mark in board CQ format, and marking is salaried duty (no per-script pay). The pain is time, arithmetic and transcription, and disputes; not income. | VF-06; S02, S03 qualitative | M | Segment = internal exams; value = time + accuracy |
| EV-03 | Marks are copied by hand several times (script margin → cover grid → mark slip → Excel → ERP). Summation, transcription, row-shift and component-rule errors cause re-work and disputes. | S01, S02, S03 converge qualitatively (not independent: same genre of source) | M | Deterministic mark capture and result engine (Must) |
| EV-04 | Internal-exam grading time per script, and the share of arithmetic vs judgement errors, are **unknown**. | CON-02/08 in A0; no measurement | — | EXP-05, EXP-07 |
| EV-05 | Physical realities: 8–16-page stitched or stapled booklets; loose supplementary sheets; thin paper with bleed-through; crossed-out attempts; answers out of order; mixed Bangla/English/maths; diagrams. | S02, S11a | M | Capture and segmentation requirements, edge cases |
| EV-06 | Curriculum and format are politically volatile (two changes in four years; next in 2028). | VF-01, VF-02 | H | Versioned, data-driven curriculum and rubric templates |

### 5.2 Users, buyers, adoption

| ID | Insight | Support | Conf. | Drives |
|---|---|---|---|---|
| EV-07 | Buyer = owner/MD (private) or SMC/Governing Body (MPO). Champion = exam coordinator or academic head. Primary user and veto = subject teacher. Technical veto = ICT staff. | S03, S13, S14, S15 converge | M | Personas, onboarding, permissions |
| EV-08 | Teachers reject black-box scoring, loss of authority, and tools that add data entry. They accept tools that remove arithmetic and transcription while leaving them in control. | S03, S12 (unsourced but consistent); Noipunno history (news) | M | Teacher-sovereignty principle; never net-add entry work |
| EV-09 | Government-run digital assessment (Noipunno) failed on server load, connectivity and UX. Teachers returned to paper ("shadow khatas"). | S03, S04 citing news | M | Offline-first; no peak-time server dependency for capture |
| EV-10 | Only ~40% of secondary schools have a computer lab, 9% of households have a computer, 75% have a smartphone. | VF-11 | H | Phone-first capture; responsive review; question-wise review works on a phone |
| EV-11 | Institutions pay for control, accuracy, speed, reputation and dispute reduction, not student feedback (student feedback WTP "very low"). | S04, S13, S15 | M | Value proposition; feedback is a by-product, not the product |
| EV-12 | Private owner-run schools decide in 1–3 months. MPO takes 3–6 months with governing-body approval. Government needs tenders (out of reach). | S03, S15 (unsourced) | L–M | Beachhead (DEC-02), sales cycle |
| EV-13 | Institutional payment is an annual prepaid invoice paid by bank transfer or cheque, with budgets Nov–Jan. The exam pain windows are half-yearly (≈Jun) and annual (≈Nov–Dec). | S15 (most credible), S13, S14 | M | Billing design; pilot timing |

### 5.3 AI capability

| ID | Insight | Support | Conf. | Drives |
|---|---|---|---|---|
| EV-14 | Bangla handwritten prose transcription is not production-grade. Even the best specialised systems show 6–9% CER on curated data, and VLMs show 19–37% (older generation). | VF-15 | H | Bangla prose at L1 at launch (DEC-21) |
| EV-15 | English handwriting and single-expression maths are far more mature. Multi-line derivations remain error-prone and VLMs hallucinate "corrections". | VF-17; S05 | H | MVP subjects = maths/physics; CAS as verifier; human confirmation |
| EV-16 | LLM grading **with reference answer and rubric** substantially beats no-reference grading. Without a reference, models over-score. | VF-18 (Caraeni; engineering-quiz study) | H | Rubric + model answer mandatory for AI suggestion |
| EV-17 | Human-level accuracy on handwritten STEM has been reached only by **routing a large share of items to humans**. The coverage-accuracy trade-off is the product lever. | VF-18 | H | Support levels, risk-coverage-based thresholds |
| EV-18 | Confidence needs multiple signals. Ranking quality (AUROC) matters for routing more than calibration (ECE). | VF-20 | M–H | Confidence design |
| EV-19 | Prompt-injection vulnerability is model-specific. Handwritten injection is untested. | VF-25 | M | Red-team set; model selection criterion |
| EV-20 | CAS equivalence is a verifier with false negatives and false positives. It needs timeouts and must never be the sole grader. | VF-24 | H | Maths engine design |
| EV-21 | Errors compound across pipeline stages. Semantic OCR errors (negation, numbers) are critical and hard to detect. | S08 (sound reasoning) | H | Evidence display (show image crop, not just transcript); per-stage metrics |
| EV-22 | Automation bias: reviewers over-accept pre-filled AI scores. | S08 (secondary citation), general HCI literature | M | Criteria-first UI, masked checks |
| EV-23 | Model choice is not settled. Current frontier and Flash-tier models from three vendors are plausible. Per-page cost ranges roughly 10× across them ($0.003–0.05). | VF-21 | H | Provider abstraction; bake-off; cost-tiered routing |

### 5.4 Economics and market

| ID | Insight | Support | Conf. | Drives |
|---|---|---|---|---|
| EV-24 | Human review, not AI compute, dominates cost if the vendor pays reviewers. With teachers reviewing, AI compute becomes the main variable cost. | S13 own numbers; VF-21 | H | Teachers review (DEC-26); metered pricing |
| EV-25 | A mainstream school's whole ERP budget is BDT 45–65k/yr. AI grading at BDT 5–15 per script × ~24–36 scripts per student per year implies BDT 120–540 per student per year, 2–10× an ERP. This is affordable mainly for premium private schools. | S15; arithmetic | M | Beachhead = premium private (DEC-02); allowance-based packaging; AI per selected questions |
| EV-26 | Exam volume is extremely seasonal (peaks in exam months). | S13, S15 | M | Batch processing; allowances; elastic compute |
| EV-27 | No product verifiably grades handwritten Bangla (a gap, and a warning that it is hard). Indian analogues (Saraswati AI, Eklavvya) show the HITL mobile pattern works commercially in India for English/Hindi. | VF-23; S12 | M | Differentiation = Bangladesh workflow + trust + CQ rubric + Bangla; not "AI" per se |
| EV-28 | Foundation models may commoditise OCR. Durable value is in workflow, rubric and curriculum data, trust and audit, school relationships and labelled local data. | S12 threat table; VF-21 trend | M | Moat strategy; provider-agnostic architecture |
| EV-29 | Time savings measured in real verified deployments are modest (16–23%; vendor claims up to 74%). The reports' 60–90% claims are unsupported. | VF-18; CON-20 | H | Honest value promise |

### 5.5 Legal and governance

| ID | Insight | Support | Conf. | Drives |
|---|---|---|---|---|
| EV-30 | Students are children under the PDPA and need parent/guardian consent, collected via the school. The school is the controller (fiduciary) and the vendor is the processor. | VF-12 | H | Consent flow, DPA |
| EV-31 | Training AI on children's exam data is legally uncertain. | VF-12 conflicts; V1 | M | No training by default; opt-in addendum after legal sign-off (DEC-13) |
| EV-32 | Automated-decision rights plus the draft AI policy's high-risk classification of education require human review, explanation and contestation, with ≥5-year logs. | VF-12, VF-13 | H (Act) / M (draft policy) | HITL, explainability, appeal flow, audit retention |
| EV-33 | Hosting: no in-country option exists from LLM vendors. Cross-border processing likely rests on consent/contract under s.29(3). The regulations are not yet issued. | VF-12, VF-22 | M | Hosting decision needs a legal opinion (DEC-12) |

---

## 6. Research-to-decision pipeline (illustrated)

The documents follow `Research → Evidence → Insight → Problem → Requirement → Product decision → Technical decision → UX decision → Implementation requirement`. Five worked chains:

| Research | Evidence | Insight | Problem | Requirement | Product decision | Technical decision | UX decision | Implementation |
|---|---|---|---|---|---|---|---|---|
| S02, S03 | Qualitative transcription chain | EV-03 | Marks copied 4–5×; errors | FR-MRK-03, FR-RES-01..06 | DEC-01 deterministic core | TR-RES-01 result engine in pure code with unit tests | Totals computed live; no manual sum field | `results` module, 100% rule test coverage |
| S05, S07, V2 | VF-15 | EV-14 | Bangla prose OCR unreliable | FR-AI-04, AI-REQ-03 | DEC-21 Bangla prose L1 | Support-level registry per cell | "Evidence only" badge; no suggested score | `capability_levels` table; gate job |
| S08, V2 | VF-18, VF-19 | EV-17 | AI good only on a subset | FR-AI-06, AI-REQ-07 | DEC-04, DEC-29 | Risk–coverage calibrated thresholds | Queue sorted by risk; "Why flagged" chips | `confidence` service; calibration job |
| V1 | VF-08, VF-12, VF-13 | EV-32 | Legal and social need for human authority and evidence | FR-HITL-01, FR-AUD-01 | DEC-05 | Append-only audit log; per-mark evidence record | Teacher identity on every confirmed mark | `audit_events` hash chain |
| S15, S13, V2 | VF-21 | EV-24, EV-25 | Price ceiling vs AI cost | NFR-COST-01 | DEC-18, DEC-34 | Batch/overnight mode; Flash-tier default; escalation only on risk | "Results ready by 7 am" expectation | Cost meter per page |

Full traceability matrix: `11-traceability-and-final-review.md`.
