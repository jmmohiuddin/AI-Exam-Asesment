# D0: Cross-Document Notes (D1 Product Architecture vs D2 Competitive Intelligence)

- **Inputs:**
  - **D1-late:** product architecture report, `1XlHNbHPLpgCwDU8FejqyR7uXgt7RmAdin21hk1no6W0`, 17:41.
  - **D1-early:** earlier version of the same report, `1Fv0n2nVySe4ZR7j_hWesHRYpK7sXMPNlkl7tREWJVIY`, 16:55.
  - **D2:** competitive intelligence blueprint, `10LW-OcDzVRLS0hAtBNmsEFeSjZyR4IGx2lS-3B6hPdo`.
- **Detailed extracts:** `D1-product-architecture.md` and `D2-competitive-intel.md` in this folder.
- **Caveat:** All three are AI-generated deep-research reports. None contains primary research (interviews, script samples, pilots, pricing surveys), and none gives any market-size figure. Treat every number as a hypothesis. Items marked **[Analyst note]** are my judgement.

---

## 1. Contradictions between the documents

| # | Topic | D1-late | D1-early | D2 | Why it matters |
|---|---|---|---|---|---|
| 1 | Time saved | "up to 70%"; also 60–80% and 60–70%; KPI ≥60% | 70%; KPI 65%+ | "up to 90%"; "80–90%" | The value proposition number is unanchored. Use none of these externally until a pilot measures it. |
| 2 | Current turnaround | 2–4 weeks internal; 6–8 weeks board; "3 weeks → 2 days" | "weeks to days" | 7–14 days; "10 days → 4 hours" | The baseline for ROI claims differs by 2–3×. Measure it in discovery. |
| 3 | Teacher review speed target | <25 s (target <12 s) **per multi-part creative paper** | <12 s **per answer block** | <2 min **per 10-page script** | These differ by roughly 10×. D1-late's figure implies rubber-stamping; D2's is realistic for real verification. This drives the ROI maths. |
| 4 | Confidence routing thresholds | High ≥0.85 → **batch auto-approve**, optional spot-check; Low <0.60 | High ≥0.88; Low <0.70; **random mandatory checks** against automation bias | Flags only; no thresholds | D1-late is the most permissive and drops the automation-bias safeguard. [Analyst note] Keep D1-early's safeguard. |
| 5 | Review paradigm | Script-by-script, with double-blind masking | **Question-wise (horizontal)** review as a core principle | One-tap per-script mobile verification | A core UX decision. Horizontal review has the strongest evidence (Gradescope) and helps consistency. |
| 6 | MCQ/OMR | Include; "Fully Automated" | Include; instant key match | **"Should NOT build"** generic OMR | Decide whether MCQ is in scope. [Analyst note] Scoring MCQ marks inside the same script is cheap and completes the total; standalone OMR products are commodity. |
| 7 | Capture channel | Mobile PWA with WASM compression in the MVP, plus flatbed; offline queue in **Phase 2** | Must list says mobile + desktop, but **roadmap puts mobile in V1** (desktop first) | **Native Android app**, offline-first, as a core differentiator; flatbed described as the outdated competitor norm | Platform choice (PWA vs native) and offline timing conflict. |
| 8 | Bangla OCR bar | "Custom OCR"; Phase 1 only "printed Bangla + **handwritten digits**" | Bangla HTR **TER <4.5%**; "isolated character accuracy 96%+"; GraDeT-HTR named | **~88% character accuracy** as target, "moat" and sufficient bar | That is 4.5% vs about 12% error. D2's bar is too low for prose grading, and D1-late's roadmap does not deliver handwritten Bangla at all in Phase 1. |
| 9 | Accuracy metric | ≥92% first-pass AI-teacher agreement | HAR >88% unedited acceptance | R² ≥0.90 vs board examiners | Three incompatible metrics. [Analyst note] Standardise on per-sub-question exact/±1 agreement, quadratic weighted kappa and MAE vs double-marked human ground truth, plus a human-human baseline. |
| 10 | Competitor set | Gradescope, LMS quiz engines, unnamed local ERPs | Gradescope, Eduman/ClassTune, generic LLM chatbots | About 20 players, including Indian AI graders (GradeFoundry, VedaAI, **Saraswati AI**, DeepGrade), Frizzle, CoGrader, BanglaOCR | D1's differentiation ("confidence-routed review with visual evidence", "template-free") ignores that D2's own tables show Saraswati, GradeFoundry, IntelGrader and Gradescope already offer confidence flagging, spatial overlays, one-tap override and audit trails. |
| 11 | Gradescope characterisation | "Requires strict fixed-template paper layouts"; "basic auto-grading" | "Industry Gold Standard" for review UX | Answer grouping on defined question regions | D1-late downplays the benchmark to manufacture a "blue ocean". |
| 12 | Differentiation / moat | Localisation + confidence routing + diagnostic intelligence | Bangla HTR + Srijonshil rubric engine + BD ERP connectors | Bangla ICR + NCTB CQ + red-ink overlay + mobile + Edufy/ClassTune connectors + data flywheel | No agreement. The features D2 calls "High defensibility" (overlays, mobile) are table stakes by its own tables. |
| 13 | ERPs named | Unnamed, V1 | **Eduman, ClassTune** (V1) | **Edufy (SoftifyBD), ClassTune, Pathshala Soft** as core; Eduman listed but not a target | The integration partner is unclear, and no document shows these ERPs have APIs. |
| 14 | ERP integration timing | Should/V1 (but the publish step "updates ERP records") | V1 | Core element and a GTM channel | Integration is either a V1 nicety or the distribution strategy. |
| 15 | Target segment | NCTB secondary/higher secondary, Grades 6–12 (Bangla and English medium in the test cohort) | Secondary/higher secondary, NCTB | Four segments: English-medium (Cambridge/Edexcel), NCTB private, admission coaching, universities; plus international expansion | Segment focus is undecided. English-medium schools are the highest-WTP segment in D2, but the Bangla/NCTB moat does not apply there. |
| 16 | Buyer | "School Management Committee, Principal, or **Regional Educational Board Officer**" | Principal / institutional board | Principal/trustees, headmaster/governing committee, coaching MD, university controller, **plus individual teachers (freemium)** | D1-late mixes in public board exams, a separate government market. D2 adds teacher-paid PLG, which D1 never considers. |
| 17 | Pricing | None | None | BDT 12–20 per booklet target; WTP BDT 10–15 (NCTB) and 20–30 (English-medium); COGS ~$0.04 per script | The only commercial hypotheses are in D2, and they conflict internally: the price ceiling (20) exceeds the NCTB WTP (15). |
| 18 | Parent / student channel | Student portal STU-01 (V1) | SMS on publish; student/parent portal | WhatsApp PDF reports (cited as most praised) | Delivery channel differs. [Analyst note] WhatsApp and SMS fit Bangladeshi parent behaviour better than a portal login. |
| 19 | Highest-risk workflow | Ingestion and student ID mapping | Bangla handwriting extraction and layout parsing | Bangla ICR (experiment #1) | Two of three say Bangla recognition. Both risks are real; ID mapping is solvable with QR/roster design. |
| 20 | Answer grouping | V1 (and already visible in REV-01 navigation) | V2 | Credited to Gradescope; not proposed | Priority unclear. [Analyst note] Grouping is high-leverage for short answers and low for CQ (c)/(d) prose. |
| 21 | Rubric authoring | AI draft rubrics in V2 | AI rubric co-pilot in V2 (but used in the usability test) | "Pre-loaded dropdown library of NCTB CQ rubrics" as a core UX | [Analyst note] Pre-built templates plus teacher-entered marking points is the realistic MVP; AI drafting is later. |
| 22 | Bias control | Double-blind header masking | Horizontal review ordering | Not addressed | Masking is questionable in school contexts (teachers know their students' handwriting). |
| 23 | Curriculum | Srijonshil 1+2+3+4 treated as fixed | Same, plus a "30 MCQ + 70 CQ" split; cites Bangladesh Post on CQ annual exams for grades 6–9 | Same; CQ presented as a structural moat | None of the three mentions the 2021 curriculum or its late-2024 rollback. See Insight 9. |

---

## 2. Where the documents agree (the weakly supported consensus)

These are directionally credible, but only as hypotheses:

1. **Human-in-the-loop is non-negotiable.** Never auto-publish, never market as "teacher replacement", and show evidence for every suggested mark.
2. **Paper stays.** CBT and online exams are not viable for Bangladeshi summative exams, so capture from paper is mandatory.
3. **CQ structure** (stimulus plus four sub-parts worth 1/2/3/4) is the core rubric unit for NCTB schools.
4. **Bangla (and mixed Bangla-English-maths) handwriting is the central technical risk.**
5. **Tabulation and transcription pain is real and deterministic.** Automated summation, audit logs and ledger export give value without AI risk.
6. **Local ERPs lack script-grading capability** and are more likely partners (or future competitors) than current competitors.
7. **The manual workflow plus DIY ChatGPT is the true incumbent.**

---

## 3. Top insights for product strategy, MVP and differentiation [Analyst note throughout]

### Strategy

1. **No evidence base exists yet.** Every number across the three documents (time saved, accuracy, WTP, turnaround, error rates) is unsourced or vendor-sourced, and market size is entirely absent. Before any build commitment, collect:
   - 200–1,000 real anonymised answer scripts across grades and subjects;
   - 15–30 teacher and controller interviews and observations of a marking cycle;
   - WTP conversations with 10–20 school owners or principals;
   - market sizing from official statistics (e.g., BANBEIS institution and enrolment counts; not in these documents).
2. **Run the feasibility gate first.** D2's experiment #1 (Bangla ICR on real scripts) and #2 (CQ step-marking vs double-marked humans) are the right first work. Change one thing: test **direct multimodal LLM grading from page images** against a separate OCR→LLM pipeline. Current models may make standalone Bangla ICR unnecessary, which both documents miss because they reason from 2024-era model assumptions. Also measure human-human agreement: the AI only needs to match teacher-teacher consistency, not perfection.
3. **The closest analogue is Saraswati AI (India), not Gradescope.** It is mobile capture, on-screen AI marks, one-tap teacher verification and WhatsApp reports to parents, for K-12 teachers and coaching centres at about $5/month. Study its flows, pricing and reviews in depth. Also assume that Indian players (Saraswati, GradeFoundry, VedaAI, DeepGrade) could add Bangla; West Bengal gives them a domestic reason to. The window may be shorter than D2 implies.
4. **Pick one segment.** D2's four segments pull in different directions:
   - English-medium schools pay more but need English and Cambridge-style schemes, where foreign competitors already fit.
   - NCTB private schools need Bangla and CQ (the actual differentiation) but pay less.
   - Coaching centres have the volume and a fast feedback loop (weekly model tests) but are price-sensitive and MCQ-heavy.

   A plausible sequencing hypothesis to test: **NCTB private secondary schools, or SSC-focused coaching centres running written CQ model tests**. Both use the CQ format, produce frequent script volume, and have a single decision-maker.

### MVP

5. **Both proposed MVPs are too broad.** D1-late's "MVP" bundles capture, ID resolution, trilingual handwriting OCR, calibrated LLM scoring, review and tabulation into 6 months. It also contradicts its own roadmap, which delivers only printed-text and digit OCR in Phase 1. D2 bundles four segments, three GTM motions, ERP and payment rails. A defensible MVP cut to evaluate:
   - **Grades:** 9–10 (SSC track) *or* one class level in one pilot school network.
   - **Subjects:** 1–2 where answers are more structured (e.g., Physics, Chemistry or Higher Maths CQ), with Bangla prose-heavy subjects (Bangla, social science) deferred until feasibility is proven.
   - **Question types:** CQ (a)/(b) short answers plus (c) numeric application, with (d) higher-order answers as suggest-only or human-only at first; in-script MCQ totals entered or OMR'd.
   - **Capture:** phone capture with a **printed answer-sheet template or cover** (QR roll ID, question boxes). This deliberately rejects D1-late's "template-free" claim; controlling the input is the cheapest accuracy gain.
   - **Review:** question-wise (horizontal) review with evidence highlights. **Every item reviewed** in the pilot (no auto-approve), plus instrumentation of the override rate to calibrate thresholds later.
   - **Output:** automatic summation, an Excel/PDF mark sheet in the school's format, and a per-student result slip shareable over WhatsApp.
   - **Deferred:** analytics dashboards, ERP APIs, student portal, AI rubric generation, payments, appeals, predictive modelling, multi-campus.
6. **Consider a low-AI wedge.** Digital mark capture and tabulation (teacher enters or confirms per-sub-question marks on a phone; the system handles totals, ledgers and report slips) removes a deterministic pain that all three documents agree on. It generates item-level data and builds trust before AI scoring is proven. AI suggestions can then be layered onto the same workflow.
7. **Borrow the good design assets.** From D1-late: state-machine invariants, override reason tags, prompt-injection handling, the offline edit cache, and the confidence-tier UX. From D1-early: horizontal review, random mandatory spot-checks against automation bias, an override-reason taxonomy feeding model improvement, loose-sheet (Othirikto Khata) handling and wrong-area answer remapping. From D2: the validation experiments and the WhatsApp parent report.

### Differentiation

8. **Features are not the differentiator.** Spatial overlays, confidence flags, mobile capture, one-tap override and audit trails already exist in competitors (per D2's own tables). Credible differentiation for Bangladesh is the combination of:
   - (a) measured accuracy on Bangla, mixed-script and maths CQ answers;
   - (b) exact fit to local exam logistics: CQ templates, roll numbers, loose sheets, school tabulation formats, Bangla UI, and GPA/grade rules;
   - (c) trust: audit, HITL, local data handling;
   - (d) distribution: school networks, coaching chains, possibly ERP partners;
   - (e) over time, proprietary labelled Bangla exam data, **provided consent and data rights are designed in from day one**. None of the documents addresses this.
9. **Curriculum volatility is a design constraint, not a moat.**
   - None of the documents mentions that the 2021 competency-based curriculum (which reduced traditional written exams) was **rolled back in late 2024**, restoring the CQ-based system from 2025.
   - The CQ assumption is therefore valid now, but policy has shifted twice in about four years.
   - Build a **configurable rubric engine**, with CQ 1+2+3+4 as one template, and do not market "NCTB CQ support" as a moat. The structure is trivial for competitors to copy.
10. **Foundation-model progress cuts both ways.** It erodes any OCR-based moat, which D2 concedes, but it also makes the product feasible sooner. Architect for **model-agnostic scoring**: swap providers, keep evaluation harnesses, and track cost per script. Put durable investment into workflow, evaluation datasets and distribution.
11. **Unit economics need real numbers.** D2's COGS of $0.04 per 10-page script and BDT 12–20 price are the only anchors. Recompute from actual token counts for page images at production quality. Model revenue per school as students × subjects × exams per year × price, and compare per-script vs per-student-per-year pricing. Include the teacher's review time, which is the cost the customer actually experiences.

---

## 4. Priority open questions (merged)

1. Can current multimodal models score real Bangla/mixed-script CQ answers within human-human agreement, and on which sub-parts and subjects?
2. What exactly do Bangladeshi scripts look like (booklets, loose sheets, roll-number conventions, cover sheets), and can a printed template be introduced for internal exams?
3. Who pays, how much, and in what unit (per script, per student per year, per teacher per month)? Who is the budget owner in private NCTB schools and coaching centres?
4. Is there really no Bangladeshi competitor? Check Amar School, softedu, BanglaOCR, ERP vendors' AI plans and university labs, all of which D2's sources touched but did not analyse. Are Indian players planning Bangla?
5. What are the data-protection, consent and residency requirements for minors' scripts processed by foreign LLM APIs?
6. Which review mode (horizontal vs per-script) and which confidence policy minimises total teacher time without automation bias? This needs measurement, not assertion.
7. Market size: the number of secondary schools, colleges and coaching centres in Bangladesh, and the share that is private and fee-paying. Not addressed by any document.
