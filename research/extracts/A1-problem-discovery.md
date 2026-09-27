# Systemic Examination Assessment Infrastructure and Operational Problem Discovery Report

Full title in doc: *"Systemic Examination Assessment Infrastructure and Operational Problem Discovery Report: Evaluating Evaluation Lifecycles, Institutional Workflows, and Market Readiness in Bangladesh"*

- **Drive ID:** `1_86p4vmAW2x34p9fG84YT3EsmoCLr7iM45RoFSSUFsE` (Google Doc, ~65k characters, read in full including the source list)
- **Research topic:** Problem validation for software (specifically AI grading) in Bangladesh exam evaluation. Covers public board exams (SSC/HSC) and internal school exams at MPO, government and private institutions. The doc asks whether there is a commercially viable problem that justifies building software.
- **Apparent method:** Desk research only. The sources are about 20 web links: Bangladeshi English-language news (Prothom Alo, TBS News, Daily Sun, Daily Star, BSS, Dhaka Tribune, bdnews24, Views Bangladesh, Dainik Shiksha), a government teachers' portal blog (teachers.gov.bd), a Facebook video, two university Gradescope evaluations (UBC, CU Boulder), a ResearchGate Gradescope paper, and vendor/blog reviews (Teachfloor, Notie AI). Unresolved `[cite: 1, 3]` markers remain in one table, a sign of an AI deep-research tool.
- **Primary research conducted?** **No.** The doc interviewed or observed no Bangladeshi teachers, schools or board officials. Phrases such as "Field data reveals…" (3.5–6 min per script) and "Field trials of academic platforms reveal…" (teacher resistance) cite no study, sample or source. Section 20 *proposes* primary research: 30 teachers (15 MPO, 15 private), 10 principals, 5 board officers, 20 students/parents, 15-teacher time-motion shadowing, and an audit of 500 scripts. This confirms that none of it was done. Claimed sample size: **none**.

---

## Main findings

1. **Headline thesis.** The main failure point is **hasty, unmoderated initial human evaluation** of physical scripts. Transcription or tabulation is secondary. The drivers are workload compression and low examiner pay. Grading workload causes burnout, but "the primary institutional failure points reside in initial evaluation accuracy, cover-sheet mark arithmetic, and manual transcription pipelines."
2. **SSC 2026 re-evaluation evidence (central data point).** After a full-script re-evaluation mandate across all boards:
   - **56,259 mark changes**. The text also says "56,259 candidates saw their marks changed", so it is unclear whether the unit is marks or candidates.
   - **27,836 grade changes**
   - **4,585 fail→pass reversals**
   - **3,079 candidates newly secured GPA-5**
   - **327,271 re-evaluation applications**, which the doc gives as a 17.89% re-evaluation rate
   - Dhaka Board grade changes went from an average of about 2,800 under the old re-scrutiny rules to **8,999 in 2026**.
   - The Education Adviser is quoted saying that "over 2,000 students" who initially failed later passed, and describing a "mental ordeal".
3. **Historical Dhaka Board grade changes under legacy "arithmetic-only" re-scrutiny:** 2022: 723; 2023: 3,085; 2024: 2,723; 2025: 2,946. Total mark changes are "Unreported" for those years, and fail→pass and GPA-5 reversals are "Minimal".
4. **Legacy re-scrutiny scope.** Before the reform, re-scrutiny did **not** re-read answers. It checked only that all answers carried marks, that marks were correctly transferred to the cover sheet, and that the cover-sheet arithmetic was right. The Ministry then introduced full **re-evaluation**, meaning re-grading of the original script.
5. **Ecosystem structure.** There are three tiers:
   - public boards: 11 Intermediate & Secondary Education Boards, including the Madrasa and Technical boards, with more than 1.8M candidates per cycle
   - government and MPO schools
   - non-MPO private institutions, including English-medium schools and prep bodies
   The Ministry of Education sets the mandate and NCTB sets the curriculum.
6. **NCTB assessment format.** Papers are split into MCQ and Creative Questions (CQ). Each CQ has four sub-parts: **Knowledge 1 + Comprehension 2 + Application 3 + Higher-Order 4 = 10 marks**. Internal school exams mirror this format: **Pre-test, Test, Half-Yearly, Annual**.
7. **Staffing.** MPO institutions face chronic staff shortages. One teacher may oversee **200–500 students per subject cohort** and teach **4–6 classes daily**.
8. **60-day publication window.** The doc says a "mandatory" 60 days runs from exam completion to publication of results, and calls this the root timing constraint.
9. **14-stage board workflow** (see Product-relevant specifics for the full table). Evaluation takes **10–15 days** and is rated "Extreme" labor intensity. Mark transcription takes **5–10 days** at "Very High" intensity. Re-evaluation takes **15–30 days**.
10. **Examiner appointment and logistics.** Examiners are appointed through the **eTIF (electronic Teacher Information Form)** system and collect bundles of **200–500 scripts** from board depots. "Thousands" fail to collect on time because of distance, other duties or low pay. Boards then issue show-cause notices and reallocate bundles.
11. **Head Examiner moderation** re-checks **5–10%** of graded scripts. Anomalies are only discovered after a whole bundle has been returned, so there is no real-time visibility.
12. **Double mark entry.** Teachers write marks per question on the script cover sheet, then again on tabulation sheets or board web portals.
13. **Sub-contracting misconduct.** Some examiners hand evaluation to family members or university students.
14. **Micro-workflow per script:**
    1. unpack and check the secret code, and check for detached supplementary pages
    2. read Bangla, English or "Banglish" handwriting and match it to CQ sub-parts, checking math steps and diagrams
    3. make subjective partial-credit decisions without standardized rubrics
    4. write red-ink marks per sub-part and circle sub-totals in the margin
    5. copy question totals into the cover-sheet grid, add them up manually, and write the total in figures and words
    6. fold, sort by mark order and re-tie the bundle
15. **Time per script:** **3.5–6 minutes** for a 12–16-page SSC/HSC CQ script. Examiners grade **30–40 scripts/day** alongside teaching. After about **script 25** in a session, speed drops and teachers switch to heuristics such as answer length, neatness and introductory sentences. The doc calls this "the root operational cause" of missed pages, wrong sums and arbitrary deductions.
16. **Result-processing failure modes:**
    - cover-sheet addition errors
    - tabulation keying errors ("37 as 73", row transposition)
    - OMR glitches on MCQ (bad bubbles, misaligned heads)
17. **No feedback to students.** Students receive aggregate grades or totals with no breakdown or commentary. Parents cannot see a graded script without filing a formal application.
18. **Bangla-specific technical barriers:**
    - conjunct characters (*juktoborno*)
    - variable *matra* (top-line)
    - highly cursive handwriting
    - Bangla–English code-mixing in STEM and social science answers
    - hand-drawn diagrams and circuits, and math derivations mixed into prose
19. **Question moderation failures happen at board level.** In **2026 HSC Physics**, four moderators received show-cause notices after CQs with mathematical inconsistencies were published, and scoring rules were adjusted mid-evaluation.
20. **Economics:**
    - "technology-based education market" of **$16B**, against **$18M** cumulative EdTech VC/PE
    - MPO entry-level basic salaries of **BDT 12,500–16,000/month** (10th/11th grade of the pay scale)
    - The doc concludes that per-student SaaS in the Western style is "economically non-viable".
21. **Workload model** (formula: N_students × N_subjects × N_exams × P_pages × t_page / 60):
    - **Board (SSC 2026):** 1,829,485 candidates × 10 papers × 1 exam × 12 pages × 0.35 min/page gives **18,294,850 scripts** and **1,280,639.5 labor hours**, compressed into a 15-day window. With an assumed **40,000 examiners**, that is about **32 hours each**.
    - **Model urban MPO school:** 1,200 students (grades 6–10) × 8 subjects × 3 cycles (Half-Yearly, Pre-Test, Annual) × 10 pages × 0.40 min/page gives **28,800 scripts** and **1,920 teacher-hours/year**.
    - **Cost:** board honorarium of about **BDT 274M** (at BDT 15/script). School teacher-time equivalent of about **BDT 432,000**.
    - **Re-evaluation rate:** board 17.89% (327,271 applications); school 3–5% "internal disputes".
    - **Error rate:** board given as "0.31% total candidates (56,259 changes)"; school "estimated 2%–4% uncorrected".
22. **Existing alternatives:**
    - pen and paper with cover sheets (no audit trail)
    - Excel or basic local ERP. Offline Excel templates are merged by formula; this removes GPA arithmetic but keeps the transcription risk.
    - OMR hardware for MCQ, which covers **"less than 30%" of NCTB assessment weight**
23. **Competitors:**
    - **Gradescope (Turnitin):** "1–3 per student/course" or enterprise pricing; the doc says it "fails on Bangla OCR". Cited as reaching **99.91% exact agreement** with manual grading and **20–35%** time reduction in STEM. **CU Boulder** dropped its central enterprise license because of cost against usage outside STEM.
    - **Crowdmark:** 3–8/student/year; no CQ support; needs high bandwidth.
    - **CodeGrade:** not applicable.
    - **Local BD ERPs:** fixed setup plus **BDT 10–30/student/month**, with zero evaluation assistance.
24. **Unsolved gaps named:**
    - handwritten Bangla and code-switched OCR
    - NCTB CQ rubric automation (Knowledge / Comprehension / Application / Higher-Order)
    - ultra-low-cost mobile, offline scanning
    - formative diagnostic reporting
25. **Contradictory evidence against an AI product (Section 15):**
    - Education Adviser directives enforce human accountability and reject machine pass/fail
    - scanning **96,000 pages per exam cycle** (1,200 students × 8 exams × 10 pages) "often exceeds the time saved"
    - principals "consistently reject per-student recurring software fees"
    - teachers resist complex setup and phone scanning
26. **Conclusion (explicit).** "Product development of an automated AI grading platform should be paused… **An automated AI answer-script grader MUST NOT be built at this stage.**" The doc recommends pivoting to lower-overhead admin utilities.

---

## Quantitative claims table

| Claim | Value | Source cited in doc | Source type | Credibility (High/Med/Low) and why |
|---|---|---|---|---|
| SSC 2026 mark changes after full re-evaluation | 56,259 | [cite: 1,3]; Daily Sun "Rechecking SSC Exam Scripts Reveal Serious Gap", Prothom Alo | News | **Med.** Specific, and traceable to named news. The unit (marks vs candidates) is inconsistent in the text. Not independently verified by analyst. |
| SSC 2026 grade changes | 27,836 nationwide | [cite: 3] news | News | **Med.** Same as above. |
| Fail→pass reversals | 4,585 | [cite: 3,7] news | News | **Med.** Conflicts with the Adviser's "over 2,000" quoted in the same doc, possibly a different stage or board subset. |
| New GPA-5 after re-evaluation | 3,079 | news | News | **Med.** |
| Re-evaluation applications | 327,271 (17.89%) | news / "official Ministry figures" | News (claims official) | **Med.** Arithmetic is consistent with 1,829,485 candidates. |
| SSC 2026 candidates | 1,829,485 | implied news | News | **Med-High.** Plausible magnitude. |
| Dhaka Board grade changes 2022–2025 | 723 / 3,085 / 2,723 / 2,946 | none specific | None | **Low-Med.** The "Minimal" reversal labels are unsupported. |
| Dhaka Board grade changes 2026 | 8,999 | news | News | **Med.** |
| "8x surge" in grade changes | 8x | derived | Derived | **Low.** Compares nationwide 2026 (27,836) with Dhaka-only prior years (about 2,800–3,000). A Dhaka-to-Dhaka comparison gives about 3x. |
| Error rate (board) | "0.31% total candidates" | derived | Derived | **Low.** 56,259 / 1,829,485 = **3.07%** of candidates. 0.31% is only correct per *script* (56,259 / 18.3M). Mislabelled. |
| Education boards | 11 | none | None | **High.** Well-known structure. |
| Candidates per cycle | >1.8M | news | News | **High.** |
| CQ sub-part marks | 1/2/3/4 = 10 | none | None | **High.** Matches the known NCTB *srijonshil* format. |
| Publication window | 60 days "mandatory" | none | None | **Low-Med.** A customary target, not shown to be a legal mandate. |
| Scripts per examiner | 200–500 | Dhaka Tribune (examiners increased), Dainik Shiksha | News | **Med.** |
| Evaluation deadline | 10–15 days | none | None | **Med.** Plausible, unsourced. |
| Head Examiner sample | 5–10% | none | None | **Low-Med.** |
| Time per CQ script | 3.5–6 min (4.2 used) | "Field data" (none) | None | **Low.** No field data exists in the doc. |
| Fatigue inflection | ~script 25; 30–40 scripts/day | none | None | **Low.** Reads as invented. |
| Teacher load | 4–6 classes/day; 200–500 students/subject cohort | none | None | **Low-Med.** |
| Board examiners | 40,000 (assumption) | Dhaka Tribune? | News / assumption | **Low.** Labelled "assuming". |
| Board evaluation labor | 1.28M hours | derived | Derived | **Low-Med.** Only as good as the 0.35 min/page and 12-page inputs. |
| Board honorarium | BDT 15/script, BDT 274M total | none | None | **Low.** Conflicts with A2 (BDT 25–45) and A3 (BDT 130). |
| School model labor | 1,920 teacher-h/yr (1,200 students) | derived | Derived | **Low-Med.** Hypothetical school. |
| School re-check rate | 3–5% | none | None | **Low.** |
| School uncorrected error | 2–4% | none | None | **Low.** Labelled "estimated". |
| MCQ/OMR share of assessment weight | <30% | none | None | **Med-High.** Consistent with the typical 70/30 CQ/MCQ split. |
| BD EdTech market | $16B | teachers.gov.bd blog | Gov portal blog (teacher-authored) | **Low.** Implausibly large and undefined; a teacher blog is not a market source. |
| Cumulative EdTech VC/PE | $18M | TBS News (Adviser speech) | News | **Low-Med.** Figure likely dated; scope unclear. |
| MPO entry basic salary | BDT 12,500–16,000/mo (10th/11th grade) | Prothom Alo / Daily Star / Daily Campus pay-scale articles | News | **Med.** Plausible for the old pay scale. The doc also cites a "9th pay scale" article, so the figures may be outdated. |
| Re-evaluation fee | BDT 150–300/paper | none | None | **Med.** A2 says BDT 150/subject. |
| Local ERP price | BDT 10–30/student/month | none | None | **Low.** Conflicts with A2 and A4. |
| Gradescope agreement | 99.91% exact agreement | ResearchGate Gradescope paper | Academic (vendor founders) | **Low-Med.** Metric context unclear; likely refers to a narrow task. Authors had a conflict of interest. |
| Gradescope time saving | 20–35% (STEM) | UBC report | Academic / institutional | **Med.** |
| Gradescope price | "1–3 per student/course" (no currency) | Teachfloor, Notie AI | Blog / vendor review | **Low.** |
| Crowdmark price | 3–8 per student/year | none | None | **Low.** |
| CU Boulder discontinued Gradescope license | Yes (cost) | oit.colorado.edu | Institutional | **Med-High.** |
| Pages to scan per school cycle | 96,000 | derived | Derived | **Med.** Arithmetic correct. Assumes full-script scanning. |
| Kill threshold WTP | < BDT 15/student/year | none | None (analyst-proposed) | n/a. A proposed criterion, not a finding. |
| Kill threshold AI accuracy | ±10% grading variance on Bangla CQ | none | None | n/a. Proposed. |
| 2026 HSC Physics moderators show-caused | 4 | bdnews24 | News | **Med.** |

---

## Product-relevant specifics

**Exam types and formats**
- Public exams are **SSC** and **HSC**, run by 11 boards (general, Madrasa, Technical).
- Internal exams: **Pre-test, Test, Half-Yearly, Annual**. The school model uses Half-Yearly, Pre-Test and Annual.
- The paper format is **MCQ + CQ**. Each CQ has 4 sub-parts worth **1/2/3/4 marks (10 total)**, testing Knowledge, Comprehension, Application and Higher-Order Thinking.
- MCQ is graded by OMR at board level and in large coaching centers, and makes up **<30% of weight**.
- Scripts run to **12–16 pages** at SSC/HSC and about 10 pages internally. They consist of a main booklet plus supplementary sheets attached with string.

**Who grades and how long**
- Board exams: appointed assistant examiners (through eTIF) grade bundles of 200–500 scripts in 10–15 days, alongside teaching. Head Examiners sample 5–10%.
- Internal exams: subject teachers grade. HoDs do informal quality control.
- Time: 3.5–6 min per CQ script (unsourced); 30–40 scripts/day; accuracy degrades after about 25.

**Board workflow (14 stages; stakeholder / time / failure modes):**

| # | Stage | Owner | Time | Key failure modes |
|---|---|---|---|---|
| 1 | Question creation | Item writers / teachers | 2–5 days/paper | ambiguity, formatting, misalignment |
| 2 | Question moderation | Moderation committee | 1–2 days | overlooked conceptual errors, leakage |
| 3 | Exam preparation | Exam Controller | 1–3 weeks | printing / packaging errors |
| 4 | Exam execution | Invigilators | 2–3 h/exam | missing IDs, swapped roll numbers |
| 5 | Script collection | Center head | 2–4 h | miscounts, damage, transit risk |
| 6 | Sorting & coding | Board scrutinizers | 3–7 days | masking errors (fictitious roll numbers / secret codes) |
| 7 | Distribution | Board officers (eTIF, buses, depots) | 2–5 days | late pickup |
| 8 | Evaluation | Examiners | 10–15 days | haste, bad partial marking, sub-contracting |
| 9 | Head Examiner moderation | Head Examiners | 3–5 days | small, superficial samples |
| 10 | Return | Examiners / depots | 1–3 days | late or lost scripts |
| 11 | Mark transcription | Data entry clerks (OMR + manual keying) | 5–10 days | keying errors, transpositions |
| 12 | Result calculation | Board computer section | 2–4 days | grace-mark edge-case bugs |
| 13 | Publication | MoE / boards (web, SMS) | 1 day | server crashes, SMS failures |
| 14 | Re-scrutiny / re-evaluation | Review committees | 15–30 days | volume, manual re-addition |

**Re-evaluation process**
- The legacy process was clerical only: all answers marked, marks correctly transferred, correct addition.
- In 2026 (per the doc), full script re-evaluation was introduced for SSC.
- Students pay **per subject** (BDT 150–300/paper per the severity table).

**Result processing**
- Cover sheet → tabulation sheet or board portal → board software (GPA, merit lists, grace-mark rules) → web portal, SMS and school lists.

**Stakeholders and roles**
- Teachers/examiners: motivated to finish without penalty; low honorarium.
- Exam Coordinators/Controllers: measured on timeliness and zero leaks.
- HoDs/Head Examiners: standardization.
- Principals/owners: reputation, pass rate, **GPA-5 yield**. They buy only if software cuts cost or burnout, or improves enrollment optics.
- ICT admins/data clerks: cautious, resist complex integrations.
- Students: want fairness, speed and explanation of deductions.
- Parents: financial sponsors who file re-scrutiny applications.

**JTBD**
- **Teacher/Examiner.** Functional: evaluate about 300 scripts accurately, total without error, submit on time. Emotional: avoid burnout and error anxiety. Social: be seen as competent and fair.
- **Principal.** Functional: smooth term exams, no disputes, rising GPA-5 yield. Emotional: confidence, no protests. Social: top-tier regional reputation.
- **Student.** Functional: understand where marks were lost and fix weaknesses. Emotional: fair grading. Social: peer and parent standing.

**Pain points ranked (Section 18 severity table)**
1. Initial evaluation errors: Critical, with a "Poor" workaround
2. Lack of formative feedback: High, with a "Very Poor" workaround
3. Transcription/keying errors: High
4. Script transit and collection delays: Moderate

**Willingness-to-pay signals** (mostly negative)
- "Weak evidence" of WTP for AI grading among MPO and public institutions.
- MPO budgets are locked, and SaaS "cannot be contracted without Ministry approval" (unsourced).
- Principals reject per-student recurring fees (unsourced).
- Private English-medium schools and top private colleges do buy tech platforms (positive, unsourced).
- The proposed kill threshold is WTP < BDT 15 (~$0.12) per student per year.

**Device and connectivity constraints**
- Schools lack scanning hardware, so the workflow must be mobile-first and offline-capable on basic teacher smartphones.
- Crowdmark-type tools require high bandwidth.

**Language**
- Scripts may be Bangla, English or mixed "Banglish". Bangla handwriting OCR is unsolved per the doc.
- The doc does not discuss the English-version vs Bangla-medium split.

**Curriculum**
- NCTB MCQ + CQ. The doc implicitly assumes the pre-2021 (2012) CQ framework is in force. That is consistent with the 2025 rollback, but the doc never mentions the rollback or the 2021 competency curriculum.
- Grades are secondary (6–10) and higher secondary (SSC, HSC). GPA is on a 5.0 scale with GPA-5 as the top grade.

**Opportunity areas proposed (non-AI-grading)**
1. **Mark audit and sum verification app.** The teacher photographs the cover sheet; the app parses handwritten sub-scores, sums them and flags discrepancies.
2. **Head Examiner QC / moderation suite.** Sample scripts are scanned at regional centers for statistical leniency/strictness auditing during the evaluation window.
3. **Diagnostic feedback generator.** Teacher-entered CQ sub-scores by cognitive level (K/C/A/H) become parent reports.

---

## Assumptions (stated or implicit)

1. Evaluation error in 2026 is mostly caused by fatigue and haste. Rubric ambiguity, question errors (such as the HSC Physics case) and examiner competence are not separated out.
2. The 60-day publication target is binding and "mandatory".
3. The 0.35–0.40 min/page grading speed and the 10–12 page script length represent reality.
4. 40,000 board examiners.
5. Grading AI is judged against "complete replacement" (Hypothesis 4). The doc never assesses assistive AI such as suggested marks or page-coverage checks, except as the cover-sheet OCR utility.
6. Full-script scanning is necessary for any digital evaluation. The 96,000-page argument assumes this even though Opportunity 1 only needs the cover sheet.
7. Low EdTech VC ($18M) implies low institutional WTP. This is a non-sequitur.
8. MPO schools cannot buy SaaS without Ministry approval (unsourced).
9. Internal school exams mirror board opacity and error patterns. Extrapolated with no school data.
10. Education authorities' stance on human accountability extends to *internal* school assessments. The directives cited concern public exams.

## Recommendations made by the doc

1. **Pause** automated AI grading development. "MUST NOT be built at this stage."
2. Pivot research to lower-overhead admin utilities:
   - mobile-first mark entry verification (cover-sheet OCR plus sum check)
   - Head Examiner moderation portal
   - diagnostic feedback generation from sub-scores
3. Run field trials on willingness to pay and scanning logistics before building.
4. Run the primary research program:
   - 30 teacher interviews (15 MPO / 15 private), 10 principals, 5 board officers, 20 students/parents
   - non-leading interview questions, e.g. "Walk me through step-by-step how you handled evaluation for your last mid-term examination."
   - time-motion shadowing of 15 teachers, measuring seconds per page for reading vs annotating, tally time, arithmetic error frequency before vs after 2 hours, and bundle handling time
   - audit of 500 graded internal scripts, comparing margin sub-scores against the cover sheet
5. Validate the hypotheses:
   - H1 fatigue: time-motion study with 50 teachers
   - H2 transcription vs evaluation error: audit of 1,000 scripts
   - H3 budgets: procurement records at 30 institutions
   - H4 AI accuracy: VLM benchmark on 500 real Bangla CQ scripts
6. **Kill criteria.** Stop if any of these is found:
   - WTP < BDT 15/student/year
   - scanning adds more staff time than it saves
   - VLM grading variance > ±10% on handwritten Bangla CQs vs expert committees
   - regulatory ban on scanning or software-assisted evaluation

## Open questions raised or implied

- What share of internal exam papers are informally re-checked or adjusted?
- Will teachers scan with their own phones without a hardware allowance?
- What admin software budget do mid-tier private schools have, and who holds final purchase authority?
- What are the word error rate and grading variance of vision-LLMs on handwritten Bangla CQ scripts across handwriting quality?
- How much of the 2026 change volume is arithmetic/transcription error and how much is judgment error? (The H2 audit is proposed.)
- *Implied:* Does the 2026 re-evaluation regime persist for HSC and later cycles? What do the board or Ministry allow for software-assisted evaluation?
- *Implied:* Does scanning only the cover sheet (1 page per script) avoid the scanning-overhead kill criterion?

## Critical assessment

**Unsupported or likely fabricated specifics**
- The "field data" of 3.5–6 min per script, the fatigue threshold at script 25, 30–40 scripts per day, and "field trials" showing teacher resistance have no source. They are presented as empirical but the doc conducted no fieldwork. **[Analyst note]** Treat them as plausible hypotheses, not findings.
- The school-level figures (2–4% uncorrected error, 3–5% internal disputes) are invented estimates for a hypothetical school.
- "MPO schools cannot contract B2B SaaS without Ministry approval" and "principals consistently reject per-student recurring fees" are unsourced assertions presented as established.

**Arithmetic and labeling errors**
- The "0.31% total candidates" error rate is wrong. It is 3.07% of candidates, or about 0.31% of scripts.
- The "8x surge" compares nationwide 2026 data with Dhaka-only historical data. Like-for-like Dhaka numbers give about 3.2x (8,999 vs about 2,800).
- The same 56,259 figure is called both "mark changes" and "candidates saw their marks changed".
- The Education Adviser's "over 2,000" fail→pass figure conflicts with 4,585 elsewhere in the doc, and the doc does not reconcile them.

**Title inconsistency.** The linked source titles say "Education **Minister**" (Views Bangladesh, TBS News), but the body repeatedly says "Education **Adviser**" (the interim-government title). **[Analyst note]** The doc may be mixing statements from different government periods. Verify who said what, and when, before quoting in a PRD or pitch.

**Weak market data**
- The "$16B technology-based education market" comes from a teachers.gov.bd blog. It is implausible and undefined.
- $18M cumulative VC is used as proof of weak institutional willingness to pay. That is a logical leap: VC funding measures investor appetite, not school budgets.

**Vendor or academic claims presented as fact**
- Gradescope's "99.91% exact agreement" is cited from the tool's own authors' paper without context. It is likely a narrow metric, not overall grading agreement.
- Competitor prices are missing currency units and come from blogs.

**Overgeneralization**
- Board-exam dynamics (eTIF, depots, secret coding, 60-day window, honorarium) are extrapolated to internal school exams. Internal exams have different incentives, e.g. no honorarium or small ones, and they are the likely B2B market.
- Hypothesis 4 argues against a strawman ("completely replace human evaluation") and then generalizes to "no AI grader at all". Assistive, teacher-in-the-loop AI marking is never evaluated.

**Internal tension**
- The doc argues that scanning full scripts costs more than it saves (96,000 pages).
- Its own Opportunity Area 1 needs only the cover sheet, and its Opportunity Area 2 needs only a sample of scripts. The scanning objection is therefore specific to full-script AI grading, but the doc applies it generally.

**Curriculum currency**
- The doc assumes the CQ/MCQ (2012-style) framework, which is correct after the 2024/2025 rollback.
- It never mentions the 2021 competency curriculum or the rollback, so it cannot say whether class 6–9 internal assessments in 2025/2026 fully follow CQ/MCQ.
- It does not assume the NCF is current, so there is no error here, only a gap.

**Missing Bangladesh evidence**
- No data on internal school exams, school budgets, device ownership or teacher attitudes.
- All Bangladeshi evidence concerns board exams, from news reports.

**Date sensitivity.** The central 2026 SSC statistics are recent news claims. The analyst has not verified them. They need confirmation from board press releases (e.g. Dhaka Board / Inter-Education Board Coordination Committee).

## Confidence level

**Overall: Medium-Low.**
- **Medium** for the board-exam problem narrative and the 2026 re-evaluation numbers. They are specific, traceable to named Bangladeshi news outlets and internally coherent in magnitude.
- **Low** for everything about school-level operations, time per script, fatigue dynamics, willingness to pay, scanning economics and competitor pricing. These are either unsourced or derived from invented inputs.
- **The strategic conclusion (don't build an autonomous AI grader first) is reasonable but weakly evidenced.** It rests on regulatory statements about *public* exams, a strawman hypothesis, and an unvalidated scanning-cost argument.

## Relevance to product decisions

| Decision | How this doc should inform it | Strength |
|---|---|---|
| Autonomous vs assistive AI grading | Strong signal that fully autonomous pass/fail grading is politically unacceptable for **board** exams (human accountability). Does not rule out teacher-in-the-loop AI for internal exams. | **Strong** (for board exams), **Weak** (internal) |
| Target segment (board vs school) | Board exam market is gated by the Ministry. The doc's own opportunities point to schools and large school groups. | Medium |
| MVP wedge | Cover-sheet capture + arithmetic verification + mark-entry validation, low-overhead and aligned with the 2026 error narrative. Head Examiner moderation analytics (for board or school-group) is a secondary option. | Medium |
| Rubric model | The CQ 1/2/3/4 K/C/A/H structure must be native in the data model; sub-part scoring enables diagnostic feedback. | **Strong** |
| Capture architecture | Mobile-first, offline-capable; minimize pages scanned; scanning labor is a named kill risk. | Medium-Strong (as a risk to test) |
| Pricing | Kill threshold of BDT 15/student/year conflicts with A4's 5–12 BDT/student/*month*. Pricing must be validated directly. | Weak |
| Validation plan / kill criteria | Interview protocol, time-motion metrics, the 500-script Bangla CQ VLM benchmark and the ±10% variance threshold are directly reusable. | **Strong** |
| Messaging | Error reduction, fairness and transparency after the 2026 re-evaluation shock are a credible "why now" narrative, subject to verifying the figures. | Medium |
