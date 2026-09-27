# Bangladesh School and College Examination Workflow: End-to-End Operational Workflow Research and Process-Mapping Study

- **Drive ID:** `1_IEEOzmRoSgTs_6bosW5pWOuv_Uwyb_lUUaDoc0SfRQ` (Google Doc, about 92k characters, read in full including the source list)
- **Research topic:** A process map of **internal** (institution-run) examinations in Bangladeshi schools and colleges, contrasted with board exams (SSC/HSC). It covers stages, actors, tools, time, cost, errors, handoffs, bottlenecks, rework, exceptions, quality control, and suitability for AI or automation.
- **Apparent method:** Desk research and synthesis. There are about 20 cited web sources:
  - academic: ResearchGate paper on the BD examination system, BRAC University dspace thesis, NepJOL grading-controversy paper, IJISRT June-2026 "AI integration" review, arXiv 2606.11931 "Semantic Grading of Written Answers in Low-Resource Language"
  - vendor/marketing blogs: Vivago, Nextzen, ORDEVS/Bornomala, FEMS, BDSchool, Nibiz
  - an EdTech blog: ebtd.education
  - social video: Somoy TV, Centrist Nation TV and Kaler Kantho Facebook videos, and a YouTube "SSC 2026 board challenge" how-to
  - unresolved `[cite: 19-28]` markers remain in one table
- **Was primary research conducted?** **No.** Nothing shows interviews, site visits, shadowing, document collection or surveys. All stage timings, costs, headcounts and the "medium institution" model (1,000 students) are illustrative constructs. They are written in an authoritative register ("Active: 8 hours; Elapsed: 5 days") with no measurement behind them. The doc itself lists "empirical time-motion tracking of examiner evaluation speed" as missing evidence. Claimed sample size: **none**.

---

## Main findings

1. **Two operating models.** Internal exams run end-to-end inside the institution: class tests, monthly tests, term exams, Half-Yearly, Annual, Pre-Test and Selection Tests. Board exams (SSC/HSC) diverge after registration. For board exams:
   - boards supply question papers, OMR sheets and answer scripts
   - scripts are collected at district centers and coded by detaching a barcoded top sheet
   - scripts go to external examiners
   - marks are submitted to board servers by SMS or web portal
   - the institution's role shrinks to registration, venue preparation, Pre-Test selection screening, and facilitating post-publication board challenges ("Khata Punor Nirikkhon")
2. **32-stage internal lifecycle** (full list in Product-relevant specifics). It is detailed as 13 macro-stages, each with an objective, trigger, actors, inputs, activities, outputs, tools, documents, handoffs, approval, time, cost, effort, errors, bottlenecks and friction.
3. **Institutional archetypes:**
   - **Government secondary:** 1,000–3,000+ students, Bangla medium, stencils/Excel, 60–80 per section, severe teacher shortage
   - **MPO:** 500–2,000 students, Bangla medium or English version, local ERPs and SMS
   - **Private urban:** 500–4,000+ students, integrated ERP (Bornomala, SMART Educare), parent apps, complex multi-component weighting
   - **English-medium (CAIE/Edexcel):** 200–1,200 students, Google Classroom/LMS, double-marking
   - **Rural non-government:** 100–500 students, unreliable power, no ICT staff
   - **Madrasa (Dakhil/Alim):** 200–1,500 students, Arabic notation, high volume per examiner
4. **Scale effect.** A small school (100–300 students) is handled by one coordinator in 3–5 days. A 2,000-student school (5 grades × 10 subjects) produces **20,000 scripts per term**. Manual transcription of multi-component marks (CQ, MCQ, Practical, CA) then causes "catastrophic" backlogs.
5. **Assessment weighting examples:** 70% CQ / 30% MCQ, or 50% CQ / 25% MCQ / 25% Practical. For **science** subjects, the doc states CQ 50% + MCQ 25% + Practical 25%, and each component must be **passed independently**.
6. **Evaluation (Stage 8):**
   - **6–10 min per CQ script (70 marks)** and **2–3 min per MCQ sheet**
   - 7–14 days elapsed for a bundle of 200
   - honorarium: internal pay is built into salary, or **BDT 10–20/script** in private institutions; **board pay is BDT 25–45/script**
   - errors: unchecked pages or questions, cover-page addition errors, inconsistent partial marks, crossed-out answers mis-marked
7. **Mark entry (Stage 9).** Each value is re-entered by hand at four points (verbatim chain): "Teacher writes on script → Teacher writes on paper mark slip → Operator types into Excel → Operator copies into ERP". Entry takes 1–2 min per student per subject and 5–10 days elapsed. Error types:
   - transposition ("73 as 37")
   - row-shifting
   - missing marks entered as zero instead of absent
8. **Verification (Stage 10).** Excel formula errors (wrong VLOOKUP or AVERAGE range) and wrong pass rules (e.g. a student who failed CQ is marked pass because CQ+MCQ exceeded 33). Grace-mark policy is applied manually.
9. **Recheck (Stage 12), "Khata Punor Nirikkhon":**
   - fee of **BDT 100–300/subject internally** and **BDT 150/subject for board exams via Teletalk**
   - window of about 7 days after publication; resolution in 7–14 days; about 20 min per script audit
   - the doc states that public board rules restrict "recheck" to clerical re-summing and unmarked-item checks, **not re-evaluation of answer quality**
10. **Single points of failure.** "In over 70% of non-government and MPO institutions" one ICT operator or contract typist holds master access to the tabulator. The doc also describes a "Master Tabulator", often a retired senior teacher, as the only person who understands grace marks and subject pass combinations. Marking standards live in senior teachers' memory, not in written rubrics.
11. **Subject-specific evaluation:**
    - **Math:** step-checking; an early sign error propagates; partial credit is erratic
    - **Science:** tripartite components; software fails to apply sub-component pass rules
    - **English 1st/2nd paper:** impressionistic holistic grading with **10–15 marks of variance** across examiners for identical essay quality
    - **Bangla & BGS:** 7 CQ sets (70 marks) with 12–16 pages per script; fatigued examiners read sub-parts (a)/(b) closely, skim (c)/(d), and "arbitrarily" award 2–3 of 4
12. **Physical artifacts:**
    - **>90%** of assessment output is handwritten paper
    - handwriting degrades from page 1 to page 16 (7 CQs in 2.5 h)
    - crossed-out attempts are sometimes double-counted or the valid re-attempt is missed
    - supplementary sheets (2- or 4-page "L-sheets" added to an 8- or 12-page main booklet) detach because they are only stapled or cotton-tied, and their serial numbers go unrecorded
    - **45–55 GSM** newsprint causes bleed-through, tearing and stuck pages, so pages get skipped
13. **Technology landscape:**
    - **ERPs:** Bornomala, SMART Educare, BDSchool, PipilikaSoft, FEMS, Smart Academic
    - **productivity tools:** Excel/Sheets, Word with Bijoy/Avro
    - **messaging:** WhatsApp, Teletalk SMS
    - **national platform:** **Noipunno** (NCTB/MoE), which had server downtime, and teachers scored **2.87/10** on digital readiness
14. **"Excel shadow pipeline."** ERPs are slow or online-only, so staff export blank sheets, key marks offline in Excel, then bulk-upload CSV. Uploads fail through schema mismatches, **Bijoy vs Unicode encoding** errors and truncated roll numbers. ERPs accept impossible values (e.g. 85 in a paper out of 70) and have no audit logs.
15. **Cycle time.** Active work is **85.0 h (16.4%)** and queue time **433.0 h (83.6%)**, for about **21.5 calendar days** per term exam cycle. Evaluation has the largest queue: 150 h waiting against 18 h active, because "scripts sitting on teacher desks while regular classes continue".
16. **Annual labor for a 1,000-student school** (3 terms, 10 subjects): **10,230 human-hours**. Components:
    - script marking: 4,000 h (8 min × 30,000 scripts)
    - invigilation: 2,700 h
    - question typing and formatting: 1,800 h
    - bundling: 960 h
    - mark entry: 500 h
    - duplication: 144 h
    - report printing: 96 h
    - principal approval: 30 h
17. **Annual direct cash cost for a 1,000-student school: BDT 982,700** (about BDT 982.7 per student per year):
    - paper: 360,000
    - printing: 210,000
    - evaluation fees: 180,000 (at BDT 6/script)
    - stationery: 90,000
    - ERP: 80,000 (BDT 80/student/yr)
    - refreshments: 30,000
    - recheck: 30,000 (300 appeals × BDT 100)
    - SMS: 2,700 (BDT 0.30/SMS)
    Paper, printing and stationery together are more than 66% of the total.
18. **Error taxonomy (ERR-01 to ERR-06):**
    - ERR-01: question typo
    - ERR-02: skipped page
    - ERR-03: cover summation
    - ERR-04: row-shift, "catastrophic: entire class assigned wrong grades"
    - ERR-05: component-threshold miscalculation
    - ERR-06: detached supplementary sheet
    The worked propagation example is a cover sub-total of 58 written for a true 68. That gives an A (4.00) instead of A+ (5.00) and a GPA of 4.92 instead of 5.00. It triggers an appeal and about **4+ hours of rework**.
19. **Rework.** "12–15%" of exam-cycle hours, about **290 staff-hours per year** at 1,000 students:
    - 120 h fixing Excel errors
    - 80 h on recheck retrieval
    - 50 h reprinting
    - 40 h re-moderation
    Manual summation takes **45–60 s per script**, which the doc puts at **375 h per year**.
20. **Quality checkpoints:**
    1. moderation
    2. exam-day identity and loose-sheet serial logging
    3. examiner self-check
    4. Scrutiny Committee checking a **10% random sample** of scripts against the ledger
    5. Principal sanity check
    Deficits: unlogged database edits, and draft mark slips are destroyed or burned after publication.
21. **Student and parent journey.** A 14–21-day wait with zero visibility. Portals crash on result day. There is a 7-day dispute window, and recheck is clerical only, so resolution can take up to 14 more days.
22. **AI-suitability classification:**
    - **Cat 1, deterministic software:** component pass/fail, GPA, audit logs
    - **Cat 2, traditional automation:** SMS, PDF report cards, seat plans
    - **Cat 3, potentially AI/ML:** Bangla/English **cover-sheet handwriting recognition (HTR)**, cover arithmetic verification, formative feedback generation
    - **Cat 4, must remain human:** high-stakes subjective grading (creative composition, essays), grace marks, malpractice discipline
23. **Counter-evidence:**
    - schools see Excel as free and churn back to it
    - AI script grading faces newsprint bleed-through, handwriting variability and no training data, with a risk of "public outcry, parent lawsuits"
    - cloud-only products fail under load-shedding
    - Noipunno shows teachers abandon tools that add entry overhead
24. **Conclusions (Section 21):**
    - The workflow is hybrid and paper-heavy.
    - Evaluation is the biggest time sink; paper and printing are the biggest cost.
    - Evaluation and mark entry have the most errors.
    - Component pass/fail errors and row-shift errors are the most costly.
    - Recheck and entry verification cause the most rework.
    - The biggest bottleneck is the teacher evaluation queue.
    - Items worth product research:
      - (a) eliminate transcription between script covers and databases
      - (b) offline-first multi-teacher mark entry
      - (c) automated cover-page arithmetic
    - Next step: field-test offline smartphone cover-sheet scanning into a validated database.

---

## Quantitative claims table

| Claim | Value | Source cited in doc | Source type | Credibility (High/Med/Low) and why |
|---|---|---|---|---|
| Internal lifecycle stages | 32 | none | None | **Med.** A reasonable decomposition, not empirical. |
| Class size, government schools | 60–80 per section | none | None | **Med.** Consistent with other docs and general knowledge. |
| Scripts per term, 2,000-student school | 20,000 | derived (2,000 × 10) | Derived | **Med.** Arithmetic correct. The "5 grades" framing is irrelevant. |
| CQ/MCQ/Practical weighting (science) | 50/25/25, separate pass per component | none explicit | None | **High.** Matches the known SSC science structure. |
| CQ/MCQ weighting (other) | 70/30 | none | None | **High.** |
| Bangla/BGS CQ structure | 7 CQs × 10 = 70 marks; a1/b2/c3/d4 | none | None | **High.** Standard *srijonshil* format. |
| Time per CQ script | 6–10 min (8 used) | none | None | **Low-Med.** Conflicts with A1's 3.5–6 min. |
| Time per MCQ sheet (manual) | 2–3 min | none | None | **Low-Med.** |
| Evaluation elapsed for 200 scripts | 7–14 days | none | None | **Med.** |
| Internal evaluation honorarium | built into salary, or BDT 10–20/script (private) | none | None | **Low.** The cost model uses BDT 6/script, which is internally inconsistent. |
| Board evaluation honorarium | BDT 25–45/script | none | None | **Low.** Conflicts with A1 (BDT 15) and A3 (BDT 130). |
| Question moderation honorarium | BDT 100–300/paper (select private) | none | None | **Low.** |
| Invigilation honorarium | BDT 200–500/session | none | None | **Low.** |
| Paper cost | BDT 800–1,100/ream | none | None | **Med.** Plausible market price. |
| Printing cost | BDT 15–35/student/exam term | none | None | **Low-Med.** |
| SMS cost | BDT 0.25–0.40/SMS (0.30 used) | none (mentions Teletalk, Greenweb) | None | **Med.** A4 says 0.35–0.50. |
| Mark entry time | 1–2 min per student per subject | none | None | **Low-Med.** |
| Recheck fee (board) | BDT 150/subject via Teletalk | YouTube board-challenge video | Social video | **Med.** Plausible and commonly reported. Verify for 2026. |
| Recheck fee (internal) | BDT 100–300/subject | none | None | **Low.** |
| Recheck audit time | 20 min/script | none | None | **Low.** |
| Single-ICT-operator dependency | >70% of non-govt/MPO institutions | none | None | **Low.** Precise percentage with no basis; likely fabricated. |
| Handwritten paper share | >90% of assessment output | none | None | **Med.** Directionally plausible. |
| Answer-booklet paper | 45–55 GSM | none | None | **Low-Med.** |
| English essay examiner variance | 10–15 marks | NepJOL grading paper? (Nepal) | Academic (non-BD?) | **Low.** Not demonstrated for BD. |
| Noipunno digital readiness | 2.87/10 | IJISRT (2026) review | Academic (low-tier journal) | **Low-Med.** The source is weak and the scale is undefined. |
| Cycle time | 85 h active, 433 h waiting, 21.5 days, 83.6% queue | none | None | **Low.** Illustrative model presented as data. |
| Annual labor, 1,000-student school | 10,230 human-hours | derived | Derived | **Low-Med.** Arithmetic sums correctly; inputs are assumed. |
| Script marking share | 4,000 h (8 min × 30,000) | derived | Derived | **Low-Med.** |
| Direct exam cost, 1,000 students | BDT 982,700/yr (982.7/student) | none | None | **Low.** Illustrative model. Sums correctly. |
| ERP subscription | BDT 80/student/year | vendor blogs? | Vendor | **Low.** Conflicts with A1 (BDT 10–30/month) and A4 (5–12/month). |
| Paper + printing + stationery share | >66% of direct cost | derived | Derived | **Med** (internally). 660,000/982,700 = 67%. |
| Rework share | 12–15% of hours; 290 h/yr | none | None | **Low.** 290 h is only about 2.8% of the doc's own 10,230 h. |
| Manual summation | 45–60 s/script, 375 h/yr | derived | Derived | **Low-Med.** 375 h uses the 45-s lower bound. |
| Addition error rework | >4 h per incident | none | None | **Low.** |
| Scrutiny sample | 10% of scripts | none | None | **Low-Med.** |
| Student wait | 14–21 days | none | None | **Med.** |
| Report cards to sign | 1,000–3,000 per cycle | none | None | **Med.** Scales with enrollment. |
| Queue sizes | 200–500 scripts/teacher; 10k–30k mark fields; 1k–3k cards | none | None | **Med.** |
| Teaching load | 4–5 classes/day; 200–400 scripts per teacher | none | None | **Med.** |

---

## Product-relevant specifics

**Internal exam types (verbatim list):** Class Tests, Monthly Tests, Term Examinations, Half-Yearly, Annual, Pre-Test, Selection Tests. Board exams are SSC and HSC; the Madrasa board exams are Dakhil and Alim.

**The 32 internal stages (verbatim order):**
1. Examination Planning
2. Academic Calendar Integration
3. Exam Scheduling & Timetable
4. Subject/Course Registration
5. Question Paper Creation (CQ & MCQ)
6. Question Review/Moderation
7. Marking Scheme/Rubric Design
8. Printing & Duplication
9. Student Registration & Roll Allocation
10. Seating & Room Allocation
11. Invigilator Assignment
12. Examination Day Setup
13. Student Attendance Recording
14. Answer Script Collection
15. Script Counting & Packaging
16. Script Sorting & Bundling
17. Script Identification/Coding
18. Script Distribution to Examiners
19. Teacher/Examiner Evaluation
20. Marking & Annotation
21. Moderation/Secondary Checking
22. Mark Entry (Paper Registers)
23. Mark Consolidation (Digital)
24. Error Checking & Verification
25. Result Calculation (GPA Conversion, NCTB 5.0 scale)
26. Result Approval
27. Report Card/Marksheet Generation
28. Result Publication
29. Student/Parent Communication (PTM)
30. Recheck/Complaint Handling ("Khata Punor Nirikkhon")
31. Result Finalization & Amendment
32. Archival & Record Retention

**Marks structure**
- CQ items have sub-parts a/b/c/d worth 1/2/3/4 marks (Knowledge, Comprehension, Application, Higher Ability).
- Typical papers: **70 CQ + 30 MCQ**, or **50 CQ + 25 MCQ + 25 Practical** for science. Each component is passed separately.
- MCQ papers have 30 items. An internal CQ paper of 7 CQs = 70 marks. GPA is on a 5.0 scale. A total of 33 appears as the pass threshold in the error example.

**Pass rules to encode (Category 1 deterministic)**
- independent sub-component pass (CQ, MCQ, Practical)
- grace marks
- absent vs zero (absent must not be entered as 0)
- max-mark bounds (reject 85/70)
- GPA conversion

**Cover page mark table.** The teacher transfers per-question sub-scores to a grid on the cover, totals it, and signs. The doc describes this as the key digitization target: vision-based scanning of the cover plus verification of its arithmetic.

**Who grades**
- Internal exams: subject teachers. Juniors and substitutes sometimes grade without training.
- Moderation: HoD/department sampling.
- Scrutiny Committee: 10% sample against the ledger.
- Approval: Principal plus Exam Committee chair, with wet signatures. Class teacher and headmaster also sign each report card.

**Stakeholders and roles**

| Role | Duties | Pain point |
|---|---|---|
| Principal/Headmaster | Final authority | Signature load |
| Examination Controller | Logistics, security, halls, script distribution | Delays |
| Academic Coordinator | Syllabus, moderation, grace policy | Cross-section grading variance |
| Subject Teacher | Draft questions, invigilate, grade, fill mark slips | Evening grading, handwriting, fatigue |
| Office Clerk | Duplication, packets, desk slips, bundling | Physical workload |
| ICT/Data Entry Operator | Excel/ERP entry, printing, SMS | Single point of failure, transposition |
| Student/Parent | — | Delays, no feedback, rigid recheck |

**Handoffs (friction points)**
- Invigilator → Sorting: missing absentee slips
- Sorting → Teacher: unindexed bundles, lost scripts
- Teacher → ICT: illegible mark slips
- ICT → Principal: paper vs screen line-by-line audit

**Time**
- 21.5-day cycle per term exam.
- The evaluation queue is 7–10 days. Mark entry queue is 3–5 days. Sign-off queue is 2–3 days.
- Parents wait 14–21 days.

**Re-evaluation.** Clerical only, both internally and (per this doc) at board level. There is a 7-day window. A board challenge through Teletalk costs BDT 150 per subject.

**Result processing chain (verbatim lineage):** "physical script internal pages → script cover summary table → handwritten paper mark slips → MS Excel spreadsheets → School ERP databases" → GPA/letter grades → master tabulation PDFs → laser-printed report cards plus SMS through a gateway API (Teletalk, Greenweb) and a parent portal.

**Device and connectivity**
- Online-only ERPs fail in rural and semi-urban areas.
- Load-shedding hits duplicators and cloud access.
- Most local platforms do not support concurrent teacher logins, so everything goes through one office desktop.

**Languages and encoding**
- Scripts are mixed Bangla/English.
- Question creation uses **Bijoy (ANSI legacy) and Avro** keyboards and MathType.
- **Bijoy vs Unicode UTF-8** encoding breaks CSV imports.
- Madrasa exams need Arabic notation.
- Medium: Bangla medium, English version, English medium (CAIE/Edexcel).

**Personas implied.** No named personas. Roles as listed above.

**JTBD.** Not framed explicitly. Implied jobs are "publish accurate results within about 3 weeks" and "eliminate transcription and summation errors".

**Pain points ranked** (from Section 21)
- Time: evaluation (4,000 h), then invigilation (2,700 h), then question creation (1,800 h).
- Money: paper and printing, more than 66%.
- Errors: evaluation and mark entry.
- Costliest errors: component pass/fail rules and row-shifts.
- Rework: recheck and entry verification.
- Bottleneck: the teacher evaluation queue, then the single ICT operator.

**Willingness to pay**
- Negative signal: schools see Excel as costing $0, so SaaS subscriptions churn back to Excel.
- Only cost anchor for software: ERP at BDT 80/student/yr, which is 8.1% of direct exam cost.

---

## Assumptions (stated or implicit)

1. A "standard medium institution" of 1,000 students, 3 terms, 10 subjects and 30 teachers represents the market.
2. Every student sits 10 written subjects in each of 3 terms, and each subject produces one script.
3. Stage timings and costs apply uniformly across archetypes, even though the doc itself says they vary "dramatically".
4. Board-level recheck is still clerical-only in 2026. This conflicts with A1's report of full re-evaluation for SSC 2026.
5. Noipunno/NCF-era problems still describe current teacher attitudes. In Section 08 the doc places Noipunno in the current technology stack without noting that the curriculum was rolled back.
6. Handwriting recognition of the cover sheet (digits in a grid) is much more tractable than grading answers. This is implied, not stated, and it is reasonable.
7. Institutions will accept offline-first mobile capture on "low-cost smartphones".
8. Marking consistency depends on undocumented senior-teacher memory, with no written rubrics.

## Recommendations made by the doc

1. Product research priorities:
   - eliminate manual transcription between script covers and digital databases
   - build an **offline-first, multi-teacher mark entry interface** that removes the single-ICT-operator bottleneck
   - **automate cover-page arithmetic summation** to remove clerical recheck failures
2. Next investigation: field-test offline mobile capture interfaces, "optical cover-sheet scanning via low-cost smartphones", that feed cover summaries straight into a validated database and bypass paper mark slips and single-operator queues.
3. Keep high-stakes subjective grading (creative composition, essays), grace marks and malpractice decisions human-controlled.
4. Put pass/fail component rules, GPA conversion and audit logging in deterministic software, not AI.
5. Avoid cloud-only designs. Avoid tools that add data-entry overhead without instant relief.

## Open questions raised or implied

- Stated as missing evidence:
  - how often scripts are lost in transit, private vs government
  - error rates in board SMS mark submissions
  - empirical time-motion data on examiner speed per subject in rural schools
- Implied:
  - How much evaluation time is spent on arithmetic and page-checking (automatable) versus judgment?
  - Would teachers accept a per-sub-part digital mark grid instead of a paper cover sheet?
  - Can ERP vendors (Bornomala, SMART Educare, BDSchool, etc.) accept validated imports or APIs?
  - Which subjects are most amenable to AI assistance? Math step-checking and short CQ parts (a) and (b) seem more amenable than essays.
  - How do these workflows differ for colleges (HSC) and madrasas?

## Critical assessment

**The format creates false precision.** Every stage has exact hours, headcounts and BDT costs, but there is no fieldwork. The template (objective / trigger / actors / … / friction) is filled in uniformly, which is characteristic of a generated deep-research report. Figures such as "~20 total human-hours", "~120 human-hours per exam day" and "433.0 hours waiting" are modeled numbers and should not be cited as findings.

**Likely fabricated statistics**
- "Over 70% of non-government and MPO institutions" depend on a single ICT operator. No source.
- "Over 90%" of output is handwritten paper. Directionally true but unsourced.
- The 10–15 mark English essay variance is attributed loosely; the NepJOL source appears to be Nepal-focused.
- The 12–15% rework share contradicts the doc's own 290 h out of 10,230 h (about 2.8%).

**Internal inconsistencies**
- Evaluation fee is BDT 10–20/script (private) in Stage 8 but BDT 6/script in the cost model.
- Time per CQ script is 6–10 min in Stage 8 and 8 min in the model. A1 says 3.5–6 min.
- The doc says data is "transcribed across four redundant stages" but lists five media.
- Cycle time is 21.5 days, but the parent wait is "14-to-21 days".
- Science subjects are "Physics, Chemistry, Bio" with CQ 50%, but Bangla/BGS use a 70-mark CQ. That is fine, but the "70 marks" CQ script time is then applied to all 30,000 scripts, including science and MCQ-only components.

**Outdated or contested policy claims**
- The doc says public board rules "strictly prohibit any re-evaluation of answer quality". A1 reports that SSC 2026 introduced full script re-evaluation, citing TBS News and Views Bangladesh. A2 cites a YouTube "SSC 2026 board challenge" video but still describes the older clerical regime. **[Analyst note]** Either A2 is outdated or A1's reform applies only to failing or specific scripts. The Views Bangladesh headline cited in A1 reads "*Failing* SSC scripts to undergo full re-evaluation", which suggests a scope limited to failing scripts. Verify.
- **Curriculum.** The doc does not state that the NCF 2021 is current. It describes Noipunno formative tracking "under NCF 2021" in the past tense ("were required"), but lists Noipunno in the current technology stack and uses it as counter-evidence about teacher attitudes. It never notes that the competency curriculum and Noipunno were rolled back in late 2024/2025. The CQ/MCQ/Practical structure it describes matches the restored curriculum, so it is broadly correct for 2026, but the Noipunno framing mixes eras.

**Vendor claims.** The ERP names (Bornomala, SMART Educare, BDSchool, PipilikaSoft, FEMS, Smart Academic, Nibiz) come from vendor "best software" blogs, which are self-promotional listicles. Claims about ERP shortcomings (no validation, no audit logs, no concurrent logins) are generalized without product testing. **[Analyst note]** Some named ERPs probably do support multi-user web entry. Verify before positioning against them.

**AI treatment is sensible.** The doc does not hype AI. It places subjective grading in the "must remain human" category and places cover-sheet HTR and feedback in "potentially AI". It never analyzes assistive AI grading, such as suggested marks with teacher override or page-coverage detection, for short-answer CQ parts.

**Missing Bangladesh evidence.** No school budgets, no real mark sheets, no observed timings, no teacher quotes. Madrasa, English-medium and college specifics are one-line generalities.

**Credible content.** Several qualitative workflow details are highly specific and consistent with general knowledge of Bangladeshi schools, and are plausibly accurate:
- Bijoy/Unicode encoding breakage
- Riso duplicators
- desk roll slips
- stapled or cotton-tied loose sheets
- Teletalk board challenge
- "Khata Punor Nirikkhon"
- component pass rules
- 4-point transcription chain
- absent vs zero

## Confidence level

**Overall: Medium for the qualitative workflow map, Low for all quantities.**

The stage sequence, actors, artifacts, handoffs, error types and deterministic rules are coherent and useful as a *hypothesis* process map to validate in fieldwork. All time, cost and percentage figures are modeled or invented and must not appear in a PRD as facts. The board recheck policy statement may be out of date.

## Relevance to product decisions

| Decision | How this doc should inform it | Strength |
|---|---|---|
| Data model and rules engine | CQ sub-parts (a–d, 1/2/3/4); CQ/MCQ/Practical components with **independent pass rules**; absent vs zero; max-mark bounds; grace marks; GPA 5.0 conversion; 4th-subject rule (from A4). These are must-haves. | **Strong** |
| MVP scope | Single-entry capture that replaces the four-hop transcription chain; cover-sheet capture and sum check; validated mark entry; audit log; report cards and SMS. | **Strong** (as hypothesis) |
| AI boundary | AI for cover HTR, arithmetic checks and feedback drafts; humans for essays, creative composition, grace marks and discipline. Assistive grading of short CQ parts is unaddressed and needs its own validation. | Medium-Strong |
| Architecture | Offline-first; concurrent multi-teacher entry; Bijoy-to-Unicode handling; CSV/ERP import/export; low-end Android. | **Strong** |
| Integration strategy | Integrate with or export to incumbent ERPs rather than replace them. Excel is the real competitor. | Medium |
| Physical capture design | Handle supplementary sheets, crossed-out attempts, bleed-through and page-skipping. Page-coverage checks ("was every page and question marked?") are a candidate feature addressing ERR-02. | Medium-Strong |
| Business case / ROI | Use its models only as templates to fill with measured data (scripts × minutes, entry minutes, rework). | Weak |
| Segment choice | Archetype table useful for segmentation hypotheses (private urban and MPO as early targets; rural and government harder). | Medium |
