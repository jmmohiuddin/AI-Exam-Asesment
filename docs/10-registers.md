# 10 — Decision, Assumption, Risk, Experiment and Open-Question Registers

| Field | Value |
|---|---|
| Document Name | Product Registers (Decisions, Assumptions, Risks, Experiments, Open Questions) |
| Version | 1.0 |
| Status | Baseline; living document, updated at every gate review |
| Date | 2026-09-27 |
| Owner | Product lead (registers), Engineering lead (technical risks), Assessment lead (accuracy decisions) |
| Purpose | Records *why* each important decision was made, what we are assuming, what could go wrong, how we will find out, and what is still unknown, so future teams do not re-litigate or forget. |
| Source Research | `00-research-synthesis.md` (S01–S15, V1, V2, VF-, EV-, CON- IDs) |
| Dependencies | Referenced by every document 01–11 |

---

## 1. Decision Register

Status values: **Decided** (build to it), **Decided (provisional)** (build to it, but a named experiment may change it), **DECISION REQUIRED** (owner and deadline named).

| ID | Decision | Options considered | Selected direction | Reason | Evidence | Revisit condition | Status |
|---|---|---|---|---|---|---|---|
| DEC-01 | What the core product is | (a) Autonomous AI grader; (b) AI-assisted, teacher-confirmed marking on a deterministic mark-capture and results core; (c) admin utilities only (cover-sheet sum check, tabulation) with no AI grading | **(b)**. The deterministic core must deliver value on its own, with AI switched off. | (a) is unsupported by evidence and legally and socially risky. (c) ignores the largest time sink (marking) and the verified gap (no Bangla handwritten grading product). (b) keeps (c)'s value as the floor. | CON-01; VF-08, VF-18, VF-23; EV-01, EV-03, EV-17 | Kill criterion K1 or K2 is triggered → fall back to (c) | Decided |
| DEC-02 | Beachhead segment | Coaching centres; English-medium (Cambridge) schools; urban private Bangla-medium / English-version secondary schools; MPO schools; boards | **Urban private (non-government) secondary schools in Dhaka, Grades 9–10, Bangla-medium and English-version streams, with a tuition level that signals ability to pay.** Secondary experiment: 1–2 coaching centres, written tests only. | Teachers set CQ papers with rubrics (VF-06). Owners decide fast (EV-12). The Bangla/CQ capability is differentiating, unlike English-medium where competitors exist. Premium tuition absorbs the per-script price (EV-25). Boards are government procurement and politically sensitive. | CON-05; VF-06, VF-10; EV-07, EV-12, EV-25 | EXP-06 shows <3/10 target schools will pay a credited pilot fee, **or** coaching shows higher WTP and written-test volume | Decided (provisional) |
| DEC-03 | MVP subjects and grades | All subjects; Bangla + English + Maths; STEM only; Maths + Physics | **General Mathematics and Physics, Grades 9–10.** Expansion order: Higher Mathematics → Chemistry → English (EV) → Bangla-medium prose subjects (gated). | Equation- and number-heavy answers are the most mature AI capability (EV-15). Both subjects use the CQ format with numeric (ga/gha) parts. Grades 9–10 carry SSC-format stakes and are later in any 2028 curriculum phase-in (VF-02; phasing undecided). | CON-02; VF-03, VF-15, VF-17; EV-14, EV-15 | Bake-off (EXP-02/03) shows neither subject can reach L2 on any item type, **or** a different subject proves more tractable | Decided (provisional) |
| DEC-04 | How AI capability is exposed | All-or-nothing AI grading; per-subject toggle; **per-cell support levels** | **Support levels L0–L3 per capability cell (subject × item type × language/script).** L0 = manual (no AI score). L1 = evidence only (transcript, highlights, no score). L2 = suggested score per criterion, teacher confirms each item. L3 = suggested scores eligible for batch confirmation, with masked audits. **No L4 (autonomous) exists.** A cell is promoted only when it passes its evaluation gate (06 §4). | Converts research uncertainty into a controlled product mechanism. Honest to users. Enables shipping before every capability is proven. | CON-02, CON-03, CON-04; EV-14, EV-17 | Each gate review | Decided |
| DEC-05 | Final authority over marks | Auto-finalise high confidence; teacher confirms each item; teacher confirms batches | **In MVP, Pilot and Production v1, no mark becomes final without confirmation by an identified teacher account.** AI-suggested marks: confirmed per item (L2) or in capped batches (L3). Deterministically scored MCQ bubbles: all ambiguities (double marks, erasures, unreadable) are resolved by the teacher, and the teacher confirms the MCQ component per script or per batch. **Autonomous finalisation is out of scope.** | Legal and policy direction (VF-08, VF-12, VF-13). No evidence of reliable autonomous grading (VF-18). Trust (EV-08). | CON-03 | Earliest: Phase 5, for low-stakes practice tests only, after 2 cycles of L3 data show severe-error ≤0.1% (95% upper bound) **and** the legal opinion permits it | Decided |
| DEC-06 | Review paradigm | Script-by-script; question-by-question | **Question-wise review by default.** The script view is used for completeness checks, totals and appeals. | Consistency (one rubric at a time), speed, and fits phone screens. Proven pattern (Gradescope). S11a had this; S11 lost it. | CON-14 | Usability tests (EXP-09) show teachers strongly prefer script-wise | Decided (provisional) |
| DEC-07 | Answer-sheet format | Template-free booklets; fully anchored custom answer sheets; **QR cover sheet + school booklet** | **Platform-generated QR cover sheet per student per paper (mandatory), stapled on top of the school's normal booklet.** Optional structured answer booklet (printed question labels and answer boxes) for class tests. | The QR gives deterministic script identity, boundaries and student linkage, and removes names from pages. It avoids forcing schools to change booklets (a board-style habit). | CON-13; S07 | EXP-04 shows cover-sheet adoption <80% of scripts | Decided (provisional) |
| DEC-08 | AI model strategy | Single frontier model; self-hosted open model; fixed ensemble; **provider-agnostic, bake-off selected, cost-tiered** | **Provider abstraction. A default "reader-grader" VLM chosen by bake-off (Flash-tier likely). A second model family used only for disagreement checks on risky items. A specialist Bangla HTR engine evaluated as an optional second reader. No self-hosted large models in the MVP.** | No current model is benchmarked on BD data (VF-15). Costs vary ~10× (VF-21). The reports' picks are outdated. Lock-in risk. | CON-15; EV-23 | Every 6 months, or when a candidate model beats the incumbent on the frozen gold set at ≤ equal cost | Decided |
| DEC-09 | Deterministic vs AI boundary | — | **Deterministic:** QR/ID, page order, image quality, sums, bounds, component pass rules, GPA, MCQ bubble scoring, choice rules ("answer 5 of 8"), CAS equivalence, audit, routing rules. **AI:** region detection, question-label reading, transcription, criterion evidence extraction, score suggestion, feedback drafts. **AI + deterministic verification:** maths steps, numeric answers with units, MCQ letters written inline. | Use AI only where deterministic software cannot work. | S05, S06, S07 consensus; EV-20 | — | Decided |
| DEC-10 | Confidence and routing | Single model probability; fixed thresholds from the reports; **multi-signal, calibrated per cell** | **A risk score per item combines:** model self-reported criterion confidence, agreement across 2–3 samples, second-model disagreement (when run), legibility/transcription signals, CAS outcome, boundary proximity, item weight, and novelty. **Thresholds per cell are set from risk–coverage curves on gold data.** | VF-20: no single signal is reliable. Ranking matters for routing. | S08, S09; EV-18 | Recalibrate on every model or prompt change and each exam cycle | Decided |
| DEC-11 | System architecture style | Microservices + K8s + Kafka + GPU cluster; **modular monolith** | **Modular monolith** (single deployable API plus worker processes), PostgreSQL, S3-compatible object storage, Postgres-backed job queue, managed AI APIs. **No Kubernetes, Kafka or GPUs in MVP/Pilot.** | Pilot volume is thousands of scripts per week. Simpler means more reliable and cheaper. The prompt prohibits over-engineering. | CON-18 | Sustained >200k pages per week, or a self-hosted model is adopted | Decided |
| DEC-12 | Hosting location | Bangladesh data centre / local cloud; regional hyperscaler (Singapore/Mumbai); US | **DECISION REQUIRED (owner: CEO + counsel; deadline: end of Phase 0 legal opinion, before any pilot data leaves design-partner consent scope).** Recommended: **a regional hyperscaler region for the application and storage, with an architecture portable to a Bangladeshi data centre** (containers, S3-compatible storage, PostgreSQL, no proprietary managed services in the core). External LLM calls send only de-identified page crops under zero-data-retention terms where available. | No LLM vendor offers BD residency (VF-22). The PDPA allows transfer on consent/contract (VF-12), but the regulations are pending. Portability keeps the option open. | CON-11; EV-33 | Legal opinion; any regulation classifying exam scripts as restricted data | **DECISION REQUIRED** |
| DEC-13 | Use of student data for model training | Train on all data; opt-out; **no training by default; opt-in addendum later** | **No training or fine-tuning of any model on student scripts in MVP/Pilot.** Evaluation datasets are built only from explicitly consented design-partner data. Later training requires the school's opt-in **Data Contribution Addendum**, parental consent covering it, and a legal sign-off. | Legal uncertainty over AI training on children's data (V1). Trust. | CON-22; EV-31 | Legal opinion confirms lawful basis **and** ≥3 schools opt in | Decided |
| DEC-14 | Student identifiers on pages | Names on every page; **QR + roll only** | Students write **no name on answer pages**; they write roll and section only if the school requires it. The QR cover carries a pseudonymous script ID. The cover-sheet identity zone is **never sent to external AI**. Header redaction runs before any AI call. | Data minimisation (PDPA). Reduces bias. | S10; VF-12 | — | Decided |
| DEC-15 | Rubric model | Hard-coded NCTB CQ; **framework-agnostic schema + templates** | **Generic rubric schema** (item → criteria → marks, alternatives, common errors, ECF rules). **NCTB CQ ka/kha/ga/gha and SSC-style paper templates are data.** Rubrics are versioned and **locked before marking begins** (edits after lock create a new version with re-evaluation of affected items). | Curriculum volatility (VF-01, VF-02). | CON-09; EV-06 | — | Decided |
| DEC-16 | Curriculum representation | National ontology; none; **lightweight versioned tree** | Curriculum version → education level → class → group/stream → subject → paper → chapter → topic (optional learning objective). Items carry a cognitive level (knowledge/comprehension/application/higher-order). Content packs are loaded as data per academic year. | Enough for rubric templates, analytics and 2028 change; avoids speculative ontology work. | VF-01, VF-02 | New 2028 curriculum published | Decided |
| DEC-17 | How the system learns from corrections | Immediate global learning; periodic retraining; **scoped knowledge updates, no automatic learning** | Every correction is classified. Corrections change behaviour only through **scoped, versioned artefacts** (rubric clarifications, alternative answers, exception rules, prompt/instruction versions), each within its scope (question, exam, school). Global changes go through offline evaluation and regression gates. No online learning. | Prevents poisoning and cross-tenant leakage; legal uncertainty. | CON-22; S09, S10 | — | Decided |
| DEC-18 | Cost target (design-to-cost) | — | **Target AI variable cost ≤ BDT 3.0 per 10-page script at pilot volumes (≈$0.025 at 120 BDT/USD); hard ceiling BDT 6.0.** The ceiling applies to the default processing mode (DEC-34). | Premium price hypothesis BDT 8–12 per script (ASM-05) at ≥65% gross margin, with teachers reviewing. | EV-24, EV-25; VF-21 | Bake-off shows gate-passing configurations exceed the ceiling (→ restrict AI to selected items, or change price hypothesis) | Decided (provisional) |
| DEC-19 | Pilot commercial terms | Free; **paid-credited** | **Paid pilot credited to the first annual subscription** (hypothesis BDT 5,000–10,000). Free only for 3–5 Phase 0 design partners contributing consented data. | Stronger demand signal (S04, S15). | CON-07 | Paid-pilot sign-up <30% of qualified prospects | Decided (provisional) |
| DEC-20 | Teacher review client | Native app; desktop only; **responsive web (PWA)** | **Responsive web application.** Setup, rubric authoring, results and administration are desktop-first. **Question-wise review is fully usable on a 6-inch phone.** | Only 9% of households have a computer, 40% of schools have labs (VF-11). Question-wise review suits phones. | EV-10 | EXP-09 shows phone review is unusable | Decided |
| DEC-21 | Bangla handwritten prose | Grade from day one; exclude; **L1 at launch** | Bangla-script prose items (e.g., Physics ka/kha written in Bangla) launch at **L1 (evidence only)**. Promotion needs the gate (06 §4). Bangla numerals and short Bangla labels in maths answers are in scope for reading. | VF-15 | CON-02 | Gate result per cell | Decided |
| DEC-22 | MCQ capture | Inline handwritten letters; separate OMR sheet; **bubble grid on the cover sheet** | **Bubble grid printed on the QR cover sheet, scored deterministically (OMR).** Inline handwritten letters (ক/খ/গ/ঘ or a/b/c/d) are supported as a fallback, read by AI, and are L2 until gated. | Deterministic, cheap, trusted (S03). The school exam format puts MCQ inside the script (VF-06). | CON-19 | Schools refuse the grid | Decided (provisional) |
| DEC-23 | Appeals | None; **re-mark by a different teacher with evidence** | Re-check requests are logged. The re-mark is done by a teacher other than the original marker (or the HoD), **with AI suggestions hidden**, and the original evidence is available afterwards. The outcome and reason are recorded. Students have an **unconditional right to a human re-mark**. | EV-32, S09 | — | — | Decided |
| DEC-24 | Interface languages | English only; **Bangla + English** | **Bangla and English** for all teacher and admin UI. Default is Bangla for teachers, switchable per user. Bangla digits in marks are optional per school. All text is Unicode; **Bijoy import is converted**. | EV-10; S02, S04 (Bijoy) | — | — | Decided |
| DEC-25 | Integration with ERPs | Build ERP; deep API integrations first; **exports first** | **Excel/CSV/PDF exports in common ERP import formats first** (MVP). A partner API and webhooks come in Phase 4. No fee or attendance modules. | ERP API openness unknown (OQ-10); avoid building an ERP. | S04, S12, S15 | ≥2 ERP partners commit | Decided |
| DEC-26 | Who performs human review | Vendor-paid reviewers; **customer's teachers** | **The school's own teachers.** The vendor provides no marking labour (except paid annotators for Phase 0 gold data). | Economics (EV-24), accountability (VF-08). | CON-16 | — | Decided |
| DEC-27 | Moderation before publication | None; **sampling by HoD** | Before an exam's results can be locked, a moderator (HoD or senior teacher) reviews a sample per marker (default: 5% of scripts, minimum 3 per marker, school-configurable) with AI suggestions hidden. Disagreements > tolerance trigger targeted re-review. | Board practice of head-examiner sampling (S01, S02); consistency. | — | EXP-09 friction | Decided (provisional) |
| DEC-28 | Capture device | Flatbed/ADF scanner; handheld phone; **Android app with spread capture + PDF import** | **Native Android capture app** (offline queue, auto-capture on page turn, two-page spread auto-split, QR detection for script boundaries), plus **PDF import** for schools with sheet-fed scanners. iOS not in MVP. | Phones are ubiquitous (VF-11). Stitched booklets block ADF (S02). | EV-05, EV-10 | EXP-04 shows capture > 45 s per 10-page script | Decided (provisional) |
| DEC-29 | Accuracy gates | Fixed QWK from the reports; **relative to measured human baseline with floors** | See `06-ai-model-decision-and-evaluation.md` §4: per-cell gates for L1, L2 and L3 relative to the human–human baseline, with an absolute floor QWK ≥0.70 and severe-error limits. | CON-04; VF-19 | — | After EXP-01 baseline | Decided (numbers provisional) |
| DEC-30 | Retention | 30-day raw purge; indefinite; **lifecycle-based** | Raw images: until result lock + appeal window (default 180 days after publication, school-configurable 90–365), then deleted. De-identified evaluation crops (consented only): until consent withdrawn or 3 years. Marks, evidence records and audit log: ≥5 years. | CON-12; VF-12 | Legal opinion | Decided (provisional) |
| DEC-31 | Value promise | Reports' 60–90% | **Promise only measured numbers.** Pilot success target: ≥30% reduction of teacher minutes per script for marking + totalling + mark entry; ≥80% reduction of tabulation/transcription time; results ready ≥5 working days earlier than the school's baseline. | EV-29 | CON-20 | Pilot measurement | Decided |
| DEC-32 | Maths engine | LLM grades; CAS grades; **LLM maps + CAS verifies + deterministic ECF** | The LLM reads steps and proposes the step→criterion mapping. CAS checks equivalence (with declared assumptions, timeouts and numeric spot checks). Deterministic error-carried-forward rules compute marks. The teacher confirms. **"CAS cannot decide" routes to review; it is never counted as wrong.** | VF-17, VF-24 | CON-17 | — | Decided |
| DEC-33 | Automation-bias protection | Pre-filled one-click; **criteria-first + masked checks** | Criterion evidence is shown before the total. 5% of items per reviewer are masked (the teacher scores first). No batch confirm below L3. Batch sizes are capped. Reviewer agreement-with-AI is monitored for rubber-stamping signals (e.g., median dwell <3 s per item). | EV-22 | CON-21 | EXP-09 | Decided |
| DEC-34 | Processing modes | Real-time only; **batch default + priority option** | **Standard mode:** batch/overnight processing (vendor batch APIs, ~50% cheaper), with suggestions ready by 07:00 next day for uploads before 22:00. **Priority mode:** results within ~60 min, metered at a higher rate. **Demo mode** for sales (≤60 s per script). | Internal marking windows are 7–14 days (S02). The cost ceiling (DEC-18). | VF-21 | Teachers reject next-day readiness | Decided |
| DEC-35 | Student/parent feedback in MVP | Student portal; **PDF/print + SMS summary** | Per-question marks breakdown, criterion notes and teacher-approved comments in a **PDF report / printed slip**. Optional SMS with total and grade. No student or parent accounts in MVP. | Low WTP for feedback (EV-11); scope control. | — | Phase 4 | Decided |
| DEC-36 | Pricing model (hypothesis) | Per student/year; per script; flat subscription; **annual allowance of scripts + overage** | **Annual prepaid plan with a script allowance plus metered overage**, priced per script. A per-student/year variant is price-tested in EXP-06. Never unlimited. | Seasonality, variable AI cost (EV-26). | CON-06 | EXP-06 | Decided (provisional) |
| DEC-37 | Specialist Bangla HTR | Build own; license vendor ICR; **evaluate open specialist (e.g., GraDeT-HTR) as second reader** | Evaluate in EXP-02. Adopt as a second reader for Bangla text only if it reduces critical transcription errors or improves routing AUROC at acceptable cost. | VF-15 | — | EXP-02 | Decided (provisional) |
| DEC-38 | Tenancy hierarchy | Deep fixed hierarchy; **Organisation → School → Academic Year → Class → Section, with Branch/Shift/Version as attributes** | See `03-system-design.md` §6. | Keeps multi-branch owners and shift/version reality without a rigid "campus" layer. | S11 | — | Decided |
| DEC-39 | Authentication | Email/password; SSO; **phone number + password with OTP** | Staff sign in with a mobile number and password. SMS OTP is required on a new device and for sensitive actions (publish, role change). No student accounts in MVP. | Phone ubiquity; low email use (assumption ASM-21). | — | — | Decided |
| DEC-40 | Rubric retrieval | RAG over rubric corpus; **full rubric in prompt** | The complete item rubric, model answer and accepted alternatives are placed in the prompt (small). Question-scoped exemplars (teacher-confirmed answers) are added only from the **same exam** and **same school**. | Rubrics are small (S06); avoids retrieval errors and leakage. | CON-22 | — | Decided |

---

## 2. Assumption Register

| ID | Assumption | Why needed | Evidence | Risk if wrong | Validation method |
|---|---|---|---|---|---|
| ASM-01 | Schools will print and attach a QR cover sheet per student per paper. | Deterministic identity and script boundaries (DEC-07). | None (S07 design logic). | Identity errors; manual linking effort. | EXP-04 with 3–5 schools; target ≥95% of scripts with a readable cover. |
| ASM-02 | Capturing a 10-page script takes ≤30 s with a phone on a stand, and a staff member or helper is available to do it. | Net time saving (S01 kill criterion). | None. | Capture eats the time saved → no value. | EXP-04 time-motion. |
| ASM-03 | Teachers can access a laptop/desktop **or** will review on a phone. | Review client (DEC-20). | VF-11 (low computer access). | Adoption barrier. | EXP-09; device survey in EXP-06. |
| ASM-04 | L2 suggestions reduce teacher marking time by ≥30% for maths/physics CQ. | Value proposition. | VF-18 (16–23% in one deployment); vendor claims higher. | Weak ROI. | EXP-05 crossover study. |
| ASM-05 | Premium private schools will pay ≈BDT 8–12 per script (or BDT 250–400 per student per year). | Business viability. | S13, S14, S12 (unsourced); S15 constrains the mainstream segment. | Revenue model fails. | EXP-06 price tests, paid pilot conversion. |
| ASM-06 | ≥95% of parents give consent via the school; non-consented scripts are marked manually in the same tool (AI off). | Operations and legality. | VF-12 requires consent; rate unknown. | Operational burden; legality. | EXP-10 consent kit trial. |
| ASM-07 | Internal exam scripts average ~10 written pages (range 6–16). | Cost and capture models. | S01/S02 (12–16 for SSC/HSC; unmeasured). | Cost ±60%. | EXP-04 page counts. |
| ASM-08 | Cross-border processing of de-identified crops under consent + contract is lawful, and exam scripts are not "restricted" data. | Hosting (DEC-12). | VF-12 (s.29(3)). | Must host in-country with open models → cost and accuracy impact. | Legal opinion (EXP-10). |
| ASM-09 | At least one current Flash-tier VLM passes the L2 gate on maths/physics numeric and English-version items. | MVP AI value. | VF-17, VF-18 (older models; mixed). | MVP ships at L0/L1 only. | EXP-02/03. |
| ASM-10 | Students label answers with question numbers (e.g., "২(গ)" / "2(c)"), which enables mapping. | Question-wise review. | Common exam practice (S02, S11a); unmeasured. | Mapping errors → manual mapping cost. | EXP-04 sample audit. |
| ASM-11 | Teachers can provide a rubric and model answer per question within the time they already spend setting papers. | AI suggestions depend on rubrics (EV-16). | VF-06 (the NCTB guideline requires sample answers and rubrics). | Rubric quality is poor → low AI accuracy. | EXP-09 rubric-authoring task; rubric template library. |
| ASM-12 | Schools have internet at least intermittently (upload overnight or from a phone's mobile data). | Upload. | VF-11 (58% of households; schools unknown). | Upload delays. | Offline queue; EXP-04. |
| ASM-13 | The exam coordinator will run the results module and the moderation step. | Result workflow. | S03 role model. | Results stall. | Pilot observation. |
| ASM-14 | Human–human QWK on BD CQ sub-parts is ≥0.70 for maths/physics. | Gates are relative to baseline. | VF-19 (international). | If lower, rubric quality must improve before AI can be judged. | EXP-01. |
| ASM-15 | LLM prices stay within ±50% of Sept 2026 over 12 months (the known exception: the Gemini 3.8 Flash promo price doubles on 2027-01-01). | Cost ceiling. | VF-21. | Margin squeeze. | Monthly price review; multi-vendor routing. |
| ASM-16 | Schools accept a paid pilot credited to the subscription. | DEC-19. | S04, S15 (unsourced). | Slower pipeline. | EXP-06 LOI gate. |
| ASM-17 | Handwritten prompt injection by students is rare and detectable. | Security posture. | VF-25 (no data). | Score manipulation. | EXP-08 red team; monitoring. |
| ASM-18 | Design partners will allow collection of 300–500 consented scripts per subject. | Gold data. | None. | No evaluation possible. | Phase 0 recruitment. |
| ASM-19 | Teacher resistance is manageable with "assistant" positioning and teachers retaining authority. | Adoption. | S03, S12 (unsourced). | Non-use → churn. | EXP-06, EXP-09, pilot usage metrics. |
| ASM-20 | Bangla-medium maths answers (Bangla and Latin digits, mixed notation) are readable by the chosen VLM at L2 quality. | Bangla-medium MVP coverage. | None specific. | Bangla-medium maths stays at L1. | EXP-02 stratum. |
| ASM-21 | Teachers reliably have a personal mobile number that receives SMS. | Authentication (DEC-39). | VF-11 (mobile ubiquity). | Login friction. | Pilot onboarding. |
| ASM-22 | ~24–36 AI-eligible scripts per student per year in the target segment (Grades 9–10: ~2 maths/physics papers × 3–5 exam cycles plus class tests). | Revenue per school. | S13 (36), S14 (24–48), all unmeasured. | Revenue ±50%. | Design-partner exam calendars. |

---

## 3. Risk Register (product, technical, commercial, legal)

Probability and impact: H/M/L. Detection = how we will know early. Full technical detail is in `02-TRD.md` §40.

| ID | Risk | Prob. | Impact | Detection | Mitigation | Fallback |
|---|---|---|---|---|---|---|
| RSK-01 | Bangla handwriting OCR is too poor for AI suggestions on Bangla prose | H | M (MVP scoped around it) | EXP-02 CER and critical-error rate | DEC-21 (L1), specialist HTR second reader (DEC-37), grade from image not transcript | Bangla prose stays L0/L1; product value comes from workflow and maths/physics |
| RSK-02 | Maths multi-line recognition errors cause wrong suggestions | M | H | EXP-03; override reasons "misread" | CAS verification, evidence crops, human confirmation, carry-forward rules | Maths items at L1 for affected item types |
| RSK-03 | Hallucinated evidence or scores | M | H | Grounding check (quoted evidence must match transcript span/region), audits | Evidence-grounding validator; reject ungrounded outputs; route to review | Downgrade cell level |
| RSK-04 | Incorrect scoring slips through batch confirmation (automation bias) | M | H | Masked-item disagreement, moderation sampling, appeals | DEC-33, DEC-27, L3 gates | Disable L3 school- or globally |
| RSK-05 | Model drift or vendor model deprecation changes behaviour | M | H | Regression suite on the frozen gold set before any model/prompt change; production drift monitors (override rate, PSI) | Version pinning, provider abstraction, re-gate on change | Roll back to previous pinned version; switch vendor |
| RSK-06 | AI cost exceeds ceiling | M | M | Per-page cost meter; monthly unit-cost report | Batch mode, Flash-tier default, selective second opinions, prompt caching, AI only on enabled items | Restrict AI to highest-value items; raise price |
| RSK-07 | Latency or throughput at exam peaks (10–12× base) | M | M | Queue depth and SLA monitors | Batch windows, horizontal workers, vendor rate-limit spreading across providers | Priority queue for paying "priority" jobs; delay standard mode |
| RSK-08 | Privacy breach or unlawful transfer | L | H | Security monitoring, audits, DPA reviews | DEC-12/13/14, encryption, RBAC, redaction before AI | Incident response; regulator and school notification |
| RSK-09 | Vendor dependency (single LLM vendor) | M | M | Vendor status, price changes | ≥2 qualified vendors after the bake-off | Fail over to the second vendor at the same support level only if it passed the gate |
| RSK-10 | Curriculum or format change (2027 interim, 2028 new) | H | M | NCTB announcements | Data-driven rubric templates and curriculum packs (DEC-15/16) | Manual rubric mode always available |
| RSK-11 | Teacher resistance / non-use | M | H | Weekly active reviewers, % items reviewed in-app vs paper | Teacher sovereignty, never add data entry, Bangla UI, training, champion model | Mark-capture-only mode still delivers tabulation value |
| RSK-12 | Schools don't trust AI; parents complain | M | H | Complaints, appeals rate | Positioning (teacher confirms every mark), evidence reports, appeals workflow | Run with AI hidden (L0) per school |
| RSK-13 | Data scarcity (no BD exam-script dataset) | H | H | Phase 0 collection progress | Design-partner consented collection; synthetic stress sets only for robustness, never as gold | Delay L2 promotion |
| RSK-14 | Capture overhead negates savings | M | H | EXP-04 | Spread capture, auto-trigger, capture by office staff, PDF import | Mark-capture-only mode for paper-marked scripts (Phase 2 feature: cover-sheet mark capture) |
| RSK-15 | Students manipulate the system (injection, writing instructions, gaming rubric keywords) | M | M | Red-team set; injection detector flags; anomaly on keyword stuffing | Treat student content as data, structured outputs, criteria require substantive evidence, human confirmation | Flag script for full manual marking |
| RSK-16 | Legal uncertainty (PDPA regulations, AI policy adoption) | M | H | Legal monitoring | Legal opinion gate; conservative defaults | In-country open-weight deployment evaluation |
| RSK-17 | Price ceiling too low in target segment | M | H | EXP-06 | Premium beachhead, allowance packaging | Reposition as tabulation/mark-capture product at lower price |
| RSK-18 | Indian competitors add Bangla, or ERPs add AI | M | M | Market watch | Speed to design partners, CQ workflow depth, local data | Partner with ERP (API) |
| RSK-19 | Question-to-answer mapping errors (unlabelled or out-of-order answers) | M | M | Mapping confidence; teacher "move to question" actions | Question-label detection, teacher quick remap, structured booklet option | Manual mapping queue |
| RSK-20 | Unfair performance across handwriting quality or medium | M | H | Subgroup gates (06 §4.4) | Legibility-tier strata in gold sets; route low-legibility to review | Keep affected strata at L1 |

---

## 4. Experiment Register (Phase 0 and pilot)

| ID | Experiment | Question answered | Design | Success / decision rule | Owner | Phase |
|---|---|---|---|---|---|---|
| EXP-01 | Human agreement baseline | What is teacher–teacher agreement per item type? (OQ-02) | 3 independent teacher markers per script, blind; ≥300 scripts per subject (maths, physics) from ≥3 schools; adjudication by a senior teacher for gold labels | Produces H–H QWK/exact/±1 per cell; sets gate baselines | Assessment lead | 0 |
| EXP-02 | Reader/grader bake-off | Which models and pipelines read and grade best at what cost? (OQ-03) | 3–4 current VLMs (≥2 vendors) + specialist Bangla HTR on 300–500 consented pages per stratum (EV maths, BM maths, EV physics, BM physics; legibility tiers) | Per-cell metrics vs gates (06 §4); cost per page; choose default + second model | AI lead | 0 |
| EXP-03 | Maths verification coverage | How often can CAS verify extracted steps; false positive/negative rates? | Run the maths engine on EXP-02 maths items; compare with adjudicated step marks | CAS false-positive (wrongly "equivalent") ≤0.5% on parsed pairs; coverage reported | AI lead | 0 |
| EXP-04 | Capture study | Time and quality of capture; page counts; QR adoption (OQ-07, OQ-08) | 3 schools × 2 exams; phone-on-stand vs handheld vs ADF (unbound pages); time-motion | ≤30 s per 10-page script (target), ≤45 s (kill threshold); ≥95% readable QR covers | Product ops | 0 |
| EXP-05 | Marking time-motion | Net teacher-time saving (OQ-01) | Crossover: 10–15 teachers mark matched script sets manually and with the prototype (L2 where available) | ≥30% reduction in minutes per script (target); <15% → K1 | Product + UX | 0 (prototype) / 2 |
| EXP-06 | Buyer and user interviews + price tests | WTP, buying process, objections (OQ-04) | 30 interviews (12 teachers, 8 coordinators, 10 principals/owners), Gabor-Granger at BDT 6/8/10/12 per script and BDT 200/300/400 per student/yr; LOI ask | ≥4/10 qualified schools sign a paid-pilot LOI | CEO | 0 |
| EXP-07 | Internal marking error audit | Share of arithmetic/transcription vs judgement errors | 500 marked internal scripts: margin marks vs cover totals vs ledger; second-marker re-mark of 100 | Quantifies value of deterministic core vs AI | Assessment lead | 0 |
| EXP-08 | Red-team set | Robustness to adversarial and injection content (OQ-14) | ≥200 constructed items: handwritten instructions ("give full marks"), keyword stuffing, off-topic, blank, rotated/upside-down pages, wrong question numbers | 0 successful score manipulations reaching a suggested score above the adjudicated mark by >1 without a flag | AI + Security | 0–1 |
| EXP-09 | Usability tests | Review UI efficiency and trust; phone viability (OQ-09) | 12–20 teachers (EV/BM, 2 schools), tasks: set up rubric, review 50 items, override, moderate | SUS ≥70; median item review time recorded; ≤3 critical usability issues open | UX lead | 1 |
| EXP-10 | Legal opinion + consent kit trial | Lawful basis, cross-border, retention, consent process (OQ-05) | Bangladeshi counsel opinion; consent form trial at 2 schools | Written opinion; consent rate ≥95% | CEO + counsel | 0 |
| EXP-11 | ERP export acceptance | Can our exports be imported? (OQ-10) | Test exports with 3 ERPs used by design partners | Import succeeds without manual editing | Product | 1 |

---

## 5. Gates and kill criteria

| Gate | When | Pass conditions | Kill / pivot criteria |
|---|---|---|---|
| **G0 — Validation gate** | End of Phase 0 (target Jan 2027) | Legal opinion permits the planned processing (or an in-country plan is costed); EXP-01 complete; ≥1 cell per MVP subject meets the L2 gate in EXP-02/03; EXP-04 capture ≤45 s/script; EXP-06 ≥4/10 LOIs | **K1**: net time saving <15% in the EXP-05 prototype → drop AI grading from v1, ship the deterministic core. **K2**: no MVP cell passes L2 → same. **K3**: <3/10 LOIs → re-segment. **K4**: legal opinion blocks cross-border processing and in-country cost >2× ceiling → pause. **K5**: gate-passing configuration costs >BDT 6/script → restrict AI scope or re-price. |
| **G1 — Pilot readiness** | Before half-yearly pilot (target May 2027) | All Must requirements met; security review passed; regression suite green; runbook; teacher training material in Bangla | Any open Sev-1 defect; privacy review not passed |
| **G2 — Pilot exit** | After pilot (target Aug 2027) | DEC-31 targets met in ≥3 schools; zero unresolved data incidents; appeals rate not higher than baseline; ≥3 schools convert | Targets missed by >50% in all schools → re-scope |
| **G3 — Production readiness** | Before annual exams (target Nov 2027) | SLOs met through pilot; cost within ceiling; support process staffed | — |

---

## 6. Open Questions Register

Classified as the prompt requires.

### 6.1 Decision Required
| ID | Question | Owner | Deadline |
|---|---|---|---|
| OQ-06 / DEC-12 | Hosting location for application and data | CEO + counsel | G0 |
| OQ-18 | Company policy on teacher-level performance analytics (sensitive in schools) | CPO + design partners | Before pilot |
| OQ-19 | Whether to offer an "AI off" (mark-capture only) tier at a lower price | CEO | After EXP-06 |

### 6.2 Evidence Required
| ID | Question |
|---|---|
| OQ-01 | Net teacher-time saving after capture overhead (EXP-04, EXP-05) |
| OQ-02 | BD teacher–teacher agreement per item type (EXP-01) |
| OQ-04 | Willingness to pay and preferred pricing unit (EXP-06) |
| OQ-07 | Who captures scripts in schools and how long it takes (EXP-04) |
| OQ-11 | Written-test volume and WTP in coaching centres (EXP-06 add-on) |

### 6.3 Experiment Required
| ID | Question |
|---|---|
| OQ-03 | Current VLM transcription quality on Bangladeshi exam pages (EXP-02) |
| OQ-08 | Adoption of QR cover sheets and bubble grids (EXP-04) |
| OQ-09 | Question-wise vs script-wise review preference; phone viability (EXP-09) |
| OQ-14 | Frequency and detectability of handwritten prompt injection (EXP-08) |
| OQ-15 | Teacher rubric quality and authoring time (EXP-09) |

### 6.4 Research Required
| ID | Question |
|---|---|
| OQ-05 | PDPA 2026 application: classification of exam scripts (s.29), cross-border conditions, whether the children's profiling ban survives, AI-training legality, consent procedure regulations, National Data Management Authority status (legal opinion) |
| OQ-12 | School record-retention obligations and typical internal appeal windows |
| OQ-13 | Assessment design of the 2028 curriculum (monitor NCTB) |
| OQ-10 | ERP import formats and API availability (EXP-11) |
| OQ-20 | Whether Google Document AI supports Bengali handwriting (V2 unverified) |

### 6.5 Product Decision Required
| ID | Question | Default until decided |
|---|---|---|
| OQ-16 | Should the product support schools that insist on names on answer pages? | No: the QR cover replaces names; names on pages are redacted where detected |
| OQ-21 | Should teachers see other teachers' marks during moderation? | No: blind moderation first, then comparison view |
| OQ-22 | Whether to show AI confidence numbers to teachers or only risk reasons | Risk reasons and levels only (see UI/UX doc §9) |
