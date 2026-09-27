# A0: Cross-Notes on Extracts A1–A4

**Sources compared**

| ID | Report | Drive ID |
|---|---|---|
| A1 | Systemic Examination Assessment Infrastructure & Operational Problem Discovery Report | `1_86p4vmAW2x34p9fG84YT3EsmoCLr7iM45RoFSSUFsE` |
| A2 | Bangladesh School and College Examination Workflow: process-mapping study | `1_IEEOzmRoSgTs_6bosW5pWOuv_Uwyb_lUUaDoc0SfRQ` |
| A3 | Assessment and Examination Ecosystem: customer discovery and user research | `1nhTEQGlS08p04MCXVfAHCz9AqEFwZVM8Cqi5GnyuZag` |
| A4 | Problem Space of Academic Operations and Assessment: B2B EdTech validation (PDF, older, LMS-framed) | `1MMF-DKxQk-282NC4W5Kyu92IWzromGb4` |

**Common baseline.** All four reports are AI-generated deep-research syntheses. **None contains primary research with Bangladeshi teachers, schools, boards or parents.** Each one proposes fieldwork as a next step:

| Report | Proposed fieldwork |
|---|---|
| A1 | 30 teachers, 10 principals, 5 board officers, 20 students/parents; shadow 15 teachers; audit 500 scripts |
| A2 | Time-motion data listed as "missing evidence" |
| A3 | 30 shadowing sessions; 15 ICT audits |
| A4 | 30 interviews; 10 observations; paid pilots |

The only independently checkable Bangladeshi evidence across the set is news reporting. The main items are:
- the SSC 2026 re-evaluation figures (A1)
- Noipunno's failures (A2, A3, A4)
- the curriculum rollback (A4)

Everything quantitative about schools (time, cost, error rates, WTP) is modeled or unsourced.

---

## Contradictions between sources

| # | Topic | Source A says | Source B says | Assessment: which is better supported |
|---|---|---|---|---|
| 1 | **Board re-evaluation policy** | **A1:** SSC 2026 introduced **full script re-evaluation**: 327,271 applications, 56,259 mark changes, 27,836 grade changes, 4,585 fail→pass. | **A2:** Board "Khata Punor Nirikkhon" is **clerical only** (re-summing, unmarked items) and "strictly prohibit[s]" re-evaluation of answer quality. A3 is silent. | **A1 is better supported.** It cites specific 2026 news (TBS, Views Bangladesh, Daily Sun, Prothom Alo); A2 cites no source on this point. **[Analyst note]** One A1 headline reads "*Failing* SSC scripts to undergo full re-evaluation", yet A1 also reports 3,079 new GPA-5s, which implies non-failing scripts were re-evaluated too. Scope (all applicants, or failing scripts only), board coverage and whether it carries over to HSC and later years must be verified from board notices. |
| 2 | **Time to grade one CQ script** | **A1:** 3.5–6 min for a 12–16-page SSC/HSC script (4.2 min used in its model). | **A2:** 6–10 min per 70-mark CQ script (8 min used); 2–3 min per MCQ sheet. | **Neither is measured.** Both are unsourced; A1's "field data" does not exist. A2's model roughly doubles grading labor compared with A1's. A time-motion study is required, and this number drives any ROI claim. |
| 3 | **Board examiner honorarium per script** | **A1:** BDT 15/script (≈BDT 274M total for SSC). | **A2:** BDT 25–45/script. **A3:** ৳130/script, self-rated "Strongly Supported". | **All weak.** A3's source is about **recruitment-exam** honorarium revisions, so it is likely misattributed. A1 and A2 give no source. Obtain the actual board circular before using any figure. |
| 4 | **Internal evaluation fee** | **A2 (Stage 8):** built into salary, or BDT 10–20/script in private schools. | **A2 (cost model):** BDT 6/script. | Contradiction inside A2. Treat internal grading as mostly unpaid salaried duty until verified. |
| 5 | **MPO/secondary teacher salary** | **A1:** BDT 12,500–16,000 base (10th/11th grade). | **A3:** persona ৳16,500–22,000; Output 02 says ৳5,000–12,000 base. **A4:** BDT 11,300–16,000 / 16,000–22,000 / 16,000–24,000. | **A1 is best sourced** (Daily Star and Prothom Alo pay-scale articles). The others are internally inconsistent. All may pre-date the new pay scale referenced by A1's own sources. Verify against the current national pay scale. |
| 6 | **ERP / software price anchor** | **A1:** local ERPs charge BDT 10–30/student/month. | **A2:** BDT 80/student/**year** (≈6.7/month). **A4:** BDT 5–12/student/month; BDT 30k–150k/yr; "sweet spot" 5–10. | **A4 is somewhat better** (cites Edufy, EduManager and Eduzone pricing pages), but these are vendor list prices. The range spans about 5x. Validate with real contracts. |
| 7 | **Viable price / kill threshold** | **A1:** kill the product if WTP < **BDT 15/student/year**. | **A4:** WTP BDT 5–12/student/**month** (60–144/year); below BDT 3/month is "too cheap to be reliable". | These are 4–10x apart and imply very different business models. A4's figures are unsourced assertions; A1's is a proposed floor, not a finding. **Unresolved. This is the top pricing question for fieldwork.** |
| 8 | **What is the #1 problem?** | **A1:** hasty, unmoderated **initial human evaluation** (judgment quality). | **A2:** transcription chain, single ICT operator, component pass-rule errors (costliest). **A3:** cover-page **arithmetic** and double entry. **A4:** exam **question-paper generation**, then tabulation. | **A1 has the only real outcome data**: the 2026 re-evaluation changes, which re-scrutiny arithmetic checks had not caught at that scale. That points to judgment errors in **board** exams. For **internal** school exams there is no evidence either way. A2, A3 and A4 rank by modeled labor or budget. Treat as competing hypotheses; A1's H2 audit (1,000 scripts: arithmetic vs judgment errors) is the right test. |
| 9 | **Cover-page summation error rate** | **A3:** 5–8% of scripts. | **A1:** school "2–4% uncorrected" (estimate); board 0.31% (mislabelled; 3.07% of candidates had marks changed). **A2:** no rate. | **All unsourced.** A1's board figure is the only one anchored to real data, and it covers all error types, not just arithmetic. |
| 10 | **Role of AI in grading** | **A1:** "An automated AI answer-script grader MUST NOT be built at this stage." **A3:** "must be abandoned". | **A3's own human-control matrix** allows "AI assisted / suggested" short-answer scoring with 100% teacher override. **A2:** Category 3 "potentially AI" = cover-sheet HTR, arithmetic, feedback; subjective grading stays human. **A4:** does not evaluate AI grading; says feedback has very low WTP. | **Consensus on autonomous grading is well founded** for high-stakes and board contexts: human-accountability statements, trust and Bangla HTR risk. **The docs do not actually test assistive AI** (suggested sub-part marks, page-coverage checks, answer transcription) with teacher confirmation. Their "don't build" verdicts argue against a strawman of full replacement. A3's matrix is the most precise and usable position. |
| 11 | **Curriculum in force** | **A4:** 2021/22 competency curriculum rolled back in late 2024; the 2012 CQ/MCQ syllabus restored for 2025/26. | **A3:** treats NCF 2021 continuous assessment (PI/BI, Noipunno) as the live regime and lists "continuous assessment data loss" as a current pain. **A2:** puts Noipunno in the current tech stack, but its CQ/MCQ/Practical structure matches the restored curriculum. **A1:** assumes CQ/MCQ; never mentions the rollback. | **A4 is correct** and matches the known rollback. A3's PI/BI pain points are outdated. Noipunno lessons remain valid only as a cautionary tale about cloud-dependent government apps. |
| 12 | **Scanning feasibility** | **A1:** full-script scanning (96,000 pages per cycle for 1,200 students) may cost more time than it saves; a named kill criterion. | **A2, A3, A1-Opp1:** scan only the **cover sheet** (one page per script) for arithmetic and HTR verification. | **Not contradictory once scoped.** Full-script digitization for AI grading carries A1's labor risk; cover-sheet capture largely avoids it. Product design should minimize pages captured, or capture pages only where AI assistance is actually used. |
| 13 | **Mobile vs desktop** | **A1:** must be mobile-first and offline on basic teacher smartphones. | **A3:** teachers say mobile is convenient but revert to desktop Excel or paper for mark matrices on small screens. **A4:** student and parent touchpoints must be mobile or SMS. | **Reconcilable:** use mobile for **capture** (photos, quick confirmation) and desktop or large layouts for **matrix editing and tabulation**. None of the claims is empirically tested. |
| 14 | **Recheck fee** | **A1:** BDT 150–300/paper. | **A2:** Board BDT 150/subject via Teletalk; internal BDT 100–300. | **A2 is more specific.** Plausible, but the 2026 fee for full re-evaluation may differ. Verify. |
| 15 | **SMS cost** | **A2:** BDT 0.25–0.40 (0.30 used). | **A4:** BDT 0.35–0.50. | Minor. A4 cites vendor pages. Low decision impact. |
| 16 | **Beachhead segment** | **A4:** commercial **coaching centers** first (fast decisions, high test cadence, OMR budgets). | **A3:** urban private Bangla/English-version schools (1–3-month sales cycle; the coordinator as champion). **A1:** boards or large school groups (moderation), plus schools (mark verification). **A2:** medium private and MPO schools. | **None validated.** A4 and A3 agree that private, owner-run institutions decide fastest and that government schools should be avoided. Coaching centers are unexamined in A1–A3. |
| 17 | **Teacher incentive / resistance** | **A3:** teachers resist automation for fear of losing **honorarium and private-tutoring income** and being monitored. | **A1:** teachers want relief from burnout and error anxiety, and examiners decline appointments because honoraria are low. **A4:** teachers run private coaching after hours. | Both plausible, and neither is evidenced. Honorarium fear applies mainly to board exams; internal exams are unpaid duty, where relief may dominate. Test both in interviews. |
| 18 | **"70%" statistics** | **A2:** >70% of non-government and MPO institutions depend on a single ICT operator. | **A4:** ~70% of schools lack integrated automation. | The same round figure is used for different claims with no source. **Likely hallucinated in both.** |
| 19 | **Rework and cost scale** | **A2:** a 1,000-student school spends BDT 982,700/yr on direct exam costs; rework is "12–15%" of hours (but its own 290 h is ~2.8%). | **A4:** a 1,200-student school wastes BDT 580k–1.19M/yr (much of it fee arrears, not assessment). | Different scopes, both modeled. Neither should appear in a business case without measurement. |
| 20 | **Who uses an OMR/MCQ tool** | **A1:** OMR is used by boards and large coaching centers; MCQ is <30% of weight. | **A3:** MCQ OMR should be 100% automated and is trusted. **A4:** coaching centers pay BDT 25k–75k for OMR and want smartphone OMR. | Consistent. MCQ auto-scoring is trusted and table-stakes, not a differentiator. |

---

## Top 15 most decision-relevant insights

Ranked by impact on PRD and strategy, with evidence strength noted.

1. **Autonomous AI grading of handwritten CQ scripts is not an acceptable product for high-stakes contexts. Assistive, teacher-in-the-loop AI remains untested, not disproven.** (A1, A2, A3; strength: Medium)
   - All three reject automated pass/fail grading, citing human-accountability directives for board exams, trust, and Bangla HTR risk.
   - A3's control matrix gives a workable policy: auto for arithmetic, OMR and GPA; *suggested* scores with 100% teacher override for short answers; no auto-scoring of essays or creative writing.
   - **PRD implication:** the teacher confirms every mark. The AI's role is to suggest, check and explain, never to decide.

2. **The 2026 SSC re-evaluation shock is the strongest real-world "why now".** (A1; news-sourced, analyst-unverified)
   - 327,271 applications; 56,259 marks changed; 27,836 grade changes; 4,585 fail→pass; 3,079 new GPA-5s; Dhaka Board grade changes rose from about 2,800 to 8,999.
   - It shows that first-pass human evaluation errors are large and publicly salient. Verify against official board releases before external use.
   - **Fix A1's errors before quoting:** the error rate is 3.07% of candidates, not 0.31%; the Dhaka increase is about 3x, not 8x.

3. **The structure of the CQ (creative question) format must be native to the data model and rubric engine.** (A1, A2, A4; strength: High)
   - Each CQ has sub-parts a/b/c/d = Knowledge 1, Comprehension 2, Application 3, Higher-Order 4 (Bangla labels: Gyan, Onudhabon, Proyog, Ucchotoro Dokkhota). A typical paper is 7 CQs = 70 marks plus 30 MCQ; science is 50 CQ + 25 MCQ + 25 Practical.
   - Sub-part-level marks enable the diagnostic feedback the docs identify as absent: A1 Opportunity 3.

4. **The restored 2012-style CQ/MCQ curriculum is the design baseline, not NCF 2021.** (A4 correct; A3 outdated)
   - Drop PI/BI continuous-assessment features and any Noipunno-style design assumptions.
   - Keep the Noipunno lessons: server fragility at peak times, offline need, teacher distrust, and parallel "shadow khatas".

5. **The deterministic result rules are table-stakes, and errors in them are the most costly.** (A2, A4; strength: High for existence of rules, Low for cost magnitude)
   - Rules to support:
     - independent pass marks for CQ, MCQ and Practical (the 33% rule applies per component, not only to the total)
     - 4th-subject rule (GP above 2.0 counts)
     - GPA 5.0 conversion
     - grace marks
     - absent ≠ zero
     - max-mark bounds (reject 85/70)
   - These belong in validated deterministic code with audit logs, not AI.

6. **The transcription chain is the clearest automatable waste.** (A1, A2, A3; strength: Medium, qualitative consensus)
   - Marks are hand-copied up to five times: script margins → cover grid → paper mark slip → Excel → ERP.
   - Capturing marks once, at sub-part level, and propagating them removes summation, keying, row-shift and missing-mark errors.
   - This is the most defensible MVP value even before any AI grading.

7. **Offline-first is non-negotiable.** (A2, A3, A4; strength: Medium-High)
   - Unreliable rural and semi-urban connectivity, load-shedding, and online ERPs that push staff into an "Excel shadow pipeline".
   - Requirements:
     - local storage with sync
     - instant, offline-safe "Submit Marks" confirmation (A3's moment of truth)
     - no dependency on peak-time servers
     - tolerance of low-end Android devices

8. **Capture scope decides feasibility.** (A1 vs A2/A3)
   - Full-script scanning (about 10–16 pages per script) may cost more staff time than it saves; this is A1's kill criterion.
   - Cover-sheet or selective capture is cheap.
   - Any AI-assisted grading of full answers must prove a net time saving in a time-motion pilot. Capture UX (phone batch-capture, page ordering, supplementary sheets) is a core product risk, not a detail.

9. **Physical-script realities must be designed for.** (A2; strength: Medium, plausible qualitative)
   - mixed Bangla/English/"Banglish" handwriting that degrades over 12–16 pages
   - crossed-out attempts (risk of double-counting)
   - detached supplementary "loose sheets" with unrecorded serial numbers
   - 45–55 GSM paper with bleed-through
   - skipped or stuck pages, plus diagrams and math derivations
   - A **page and question coverage check** ("every question and page has a mark?") is a low-risk AI or vision feature aimed directly at ERR-02, the skipped-page error.

10. **The Bangla encoding problem is real.** (A2, A4; strength: Medium-High)
    - Bijoy (legacy ANSI) vs Unicode breaks CSV imports and question files.
    - The product must import and convert Bijoy text, use Unicode throughout, and support Bangla math and science typography for rubrics and questions.

11. **Buyer ≠ user ≠ veto-holder.** (A3, consistent with A1 and A4; strength: Medium)
    - Exam Coordinator = operational champion (heaviest user and pain).
    - Owner/MD (private) or governing body/SMC (MPO) = buyer.
    - Subject teachers = passive-resistance veto; ICT admin = technical veto.
    - Government schools cannot buy directly: 12–24-month tenders, avoid.
    - **Rule:** never add net data-entry work for teachers.

12. **Sell institutional outcomes, not student feedback.** (A4, A1; strength: Medium)
    - A4 rates student feedback "Very Low" and homework grading "Low" for willingness to pay: students and teachers don't hold budgets.
    - Institutions pay for control, accuracy, speed, reputation and revenue protection.
    - Position AI as faster, more accurate, defensible results with fewer disputes. Feedback is a differentiating by-product for parents.

13. **Pricing is the biggest unknown.** The anchors conflict by up to 10x:
    - A1 kill threshold: BDT 15/student/**year**
    - A2: ERP at BDT 80/student/year
    - A1: ERPs at BDT 10–30/student/month
    - A4: BDT 5–12/student/month, "sweet spot" 5–10; coaching BDT 2,000–8,000/month flat; paid-pilot setup fee BDT 10,000–15,000
    - All are unsourced or vendor list prices. A4's paid-LOI gate (≥4 of 10 pilots pay a setup fee) is the best proposed test.

14. **Coaching centers are an unexplored but plausible wedge for a grading product.** (A4; strength: Low-Medium)
    - Coaching centers run daily and weekly tests (MCQ plus written) for 500–2,000+ students and need results within 24 hours.
    - They already pay for OMR and question banks, and owners decide quickly.
    - The docs discuss only OMR for them. **[Analyst note]** AI-assisted grading of weekly written tests (lower stakes than board exams, high volume, speed-sensitive) may fit better than schools, which have slow procurement and teacher veto. Needs interviews. Segment by size: large brands vs neighborhood centers.

15. **Incumbents and the do-nothing option set the bar.** (A2, A3, A4)
    - Excel, WhatsApp, paper registers and guidebooks cost nothing and need no training.
    - Local ERPs (Edufy, Pipilika Soft, Bidyaan, BDSchool, Bornomala, SMART Educare, PathshalaSoft, ShikkhaPlus, MMIT) already sell on tabulation and fees, and bundle-lock schools.
    - Strategy should be **integrate/export into ERPs + Excel** rather than replace them.
    - Sales timing must avoid exam windows. Pilot in a single mid-term cycle (A3).

---

## Cross-document credibility notes

- **Recurring AI deep-research artifacts:**
  - unresolved `[cite: N]` markers (A1, A2, A4)
  - uniformly templated sections with precise but unmeasured numbers
  - fictional named personas presented as "evidence-based" (A3)
  - self-assigned "Verified" evidence labels (A3)
  - duplicated source lists padded with vendor listicles, Quora, tutor sites and Facebook or YouTube videos (A2, A4)
- **Sources worth independently checking**, as the highest-value verifiable items:
  - SSC 2026 re-evaluation figures: TBS News, Views Bangladesh, Daily Sun, Prothom Alo, BSS; ideally official board press releases
  - board challenge fee and process for 2026
  - the official board examiner honorarium circular
  - the current MPO pay scale
  - the curriculum rollback notice (NCTB/MoE)
  - BANBEIS institution and teacher counts (A4's 24,000 institutions / 150,000 teachers)
  - ERP vendor pricing pages
- **Arithmetic and labeling errors found:**
  - A1: error rate 0.31% should be 3.07% of candidates; "8x" should be about 3x like-for-like
  - A2: rework 12–15% is actually about 2.8%; its cost model uses BDT 6/script against BDT 10–20 in its own text
  - A3: two conflicting salary ranges
  - A4: three salary ranges and three clerical-hours figures
- **Government-title inconsistency (A1).** The text refers to the "Education Adviser" (interim-government title), while the linked headlines say "Education Minister". Quotes may mix periods. Verify attribution.
