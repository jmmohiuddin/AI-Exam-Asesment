# The Problem Space of Academic Operations and Assessment in Bangladesh: A B2B EdTech Problem Discovery and Validation Report

- **Drive ID:** `1MMF-DKxQk-282NC4W5Kyu92IWzromGb4` (PDF, 42 pages, about 786 KB, in a different Drive folder). It was read in full twice:
  - once through the Drive text export, where the tables came out garbled
  - once by decoding the PDF and extracting its tables with PyMuPDF, which recovered the full top-20 table, top-5 table, cost, WTP, segment and opportunity-map tables
- **Scope of this extract:** The report is mainly about whether to build an LMS. Per instructions, only the parts relevant to **exam assessment** are extracted in depth: exam authoring, grading, tabulation, OMR, feedback, WTP, segments and validation. LMS, fee-gating and communications content is summarized only where it affects assessment-product decisions such as bundling, WTP and beachhead.
- **Research topic:** B2B EdTech problem discovery across K-12, colleges, coaching centers and universities in Bangladesh. The core question is whether to build an LMS. The answer is no; instead it recommends an "Academic Assessment and Operations Engine".
- **Apparent method:** Desk research only. There are about 80 unique source URLs, many repeated 3–5 times, including:
  - vendor sites: BDSchool, ShikkhaPlus, PathshalaSoft, MMIT, Edufy pricing, Eduzone pricing, EduManager pricing, Fleek ExamPro, Genius Edusoft question-paper generator, qbankbd, Chorcha, Udvash
  - app-store pages
  - Scribd documents and a Quora thread
  - tutor-listing sites (teacheron, dhakatutors)
  - OECD Education at a Glance 2025, World Bank EdTech report, ILO, BTI country report
  - academic papers (MDPI, T&F, ResearchGate, BanglaJOL, BUET library)
  - Daily Star and Prothom Alo
  Unresolved `[cite: N]` markers appear throughout the tables. Emoji traffic-light glyphs are corrupted.
- **Primary research conducted?** **No.** The top-20 ranking is described as reflecting "empirical frequency, time-cost destruction…", but no survey or interview data is presented. Section 21 *proposes* 30 interviews (10 coaching centers, 10 private MPO schools, 10 English-medium schools), 5 exam-controller shadowing sessions, 5 teacher observations, concierge prototypes at 5 schools and paid pilots. Claimed sample size: **none**.

---

## Main findings (assessment-relevant)

1. **Curriculum context: explicit and correct.** The report says: "With the interim government rolling back the 2021/2022 competency-based curriculum in late 2024 and restoring the **2012** examination-centric syllabus for the 2025/2026 academic cycles, institutions are locked into paper-based Creative Question (CQ) and Multiple Choice Question (MCQ) frameworks." It is the only one of the four docs that states the rollback. The CQ tiers are named in Bangla: **Gyan** (Knowledge), **Onudhabon** (Comprehension), **Proyog** (Application), **Ucchotoro Dokkhota** (Higher-Order Thinking).
2. **Teacher load and pay** (inconsistent across sections):
   - base salaries of **BDT 11,300–16,000/month** (executive summary)
   - **BDT 16,000–22,000** (Problem 5)
   - **BDT 16,000–24,000** (Persona 1)
   Teachers are "overwhelmed by **25 to 35 hours** of manual clerical assessment and tabulation per examination cycle" (executive summary). Elsewhere the report says about 20 h per cycle writing and formatting papers plus **30–45 h** hand-entering marks, and **50–70 h** in the one-page map. **More than 180 h** of instructional time is lost per teacher per year.
3. **Class density.** 55–80 per section (60–80 in several places). A teacher sees **250–450 students/day** across 4–6 periods. Reviewing daily homework "would require **20 to 30 hours** of labor outside of school hours every week". Formative homework evaluation is therefore "largely abandoned": perfunctory tick-marks or no written tasks.
4. **Top-20 problem ranking.** Assessment-related items (Frequency / Frustration / Severity / Commercial viability):

   | Rank | Problem | Freq | Frust | Severity | Commercial viability |
   |---|---|---|---|---|---|
   | #1 | Manual CQ/MCQ question-paper formatting, chapter-weight balancing, leak risk | 4 | 5 | Critical | "Very High (willingness to spend exists)" |
   | #2 | High-volume exam mark entry, 4th-subject rules, tabulation-sheet processing | 3 | 5 | Critical | High (bundled into ERP) |
   | #5 | Grading bottleneck of paper-based homework in 60–80-student classes | 5 | 4 | High | **"Low (Teachers lack personal software budget)"** |
   | #6 | Coaching-center model test distribution, tracking and ranking | 5 | 4 | High | "Very High (High ARPU, strong budgets)" |
   | #10 | No pre-exam visibility of learning regression | 3 | 4 | High | Moderate ("analytical luxury") |
   | #14 | Bijoy vs Unicode typography | 4 | 3 | Medium | Moderate |
   | #15 | Slow, unstandardized subjective feedback on essays | 4 | 3 | Medium | **"Very Low (Students lack purchasing autonomy)"** |
   | #17 | Lab, continuous-assessment and practical marks tracking | 2 | 3 | Medium | Low |

   Non-assessment items in the top 20 include fee reconciliation and admit-card gating (#3), parent absence notices (#4), content fragmentation (#7), plagiarism (#8), teacher churn (#9), messaging encroachment (#11), hybrid learning (#12), printing costs (#13), device storage (#16), DSHE reporting (#18), timetabling (#19), and peer collaboration (#20, a "False Problem").
5. **Scoring formula.** Opportunity Score = 0.25 Financial Impact + 0.20 Frustration + 0.15 Frequency + 0.15 Existing Spend + 0.15 Switching Pressure + 0.10 Urgency. The formula "intentionally penalizes pedagogical complaints that lack institutional purchasing power". Component scores other than frequency and frustration are **not shown**.
6. **The #1 problem is exam-paper generation** under the reinstated 2012 NCTB curriculum. Four phases, about 12–19 days:
   - syllabus parsing and weight balancing across the four cognitive levels for CQ and MCQ, done by hand (**3–5 days**)
   - question sourcing from guidebooks (**Panjeree, Anupam, Lecture**) and drafting in Word (**5–7 days**)
   - moderation and re-formatting (**2–3 days**)
   - production on unencrypted USB sticks taken to print shops or risographs (**2–4 days**), which creates leak risk
   Each exam means hand-picking **10–15 CQs and 30 MCQs**.
7. **Tabulation (#2):**
   - terminal exams run **3 times a year** across all grades
   - GPA is on a 5.0 scale
   - the **4th-subject rule**: grade points above 2.0 count toward the overall score
   - continuous-assessment weightings apply
   - "**mandatory separate pass marks for written and MCQ papers**"
   About **70% of schools** lacking automation use paper ledgers or brittle Excel. Report cards are delayed by **2–3 weeks**. "Entire academic operations pause for **10–15 days** while staff cross-tabulates marks." Local ERPs close contracts at **BDT 5–12/student/month** "primarily on the strength of this module". Contracts are "routinely canceled" when tabulation is wrong.
8. **Coaching centers:**
   - Named brands: Udvash, Unmesh, Retina, Medico, plus "thousands" of neighborhood centers.
   - Test cadence: daily 20-minute MCQ tests, and daily 25-mark MCQ quizzes in Persona 2; weekly written papers; full mock exams.
   - Operations: daily OMR scanning, sorting written scripts, manual score entry, percentile calculation across three shifts.
   - Results must go out by SMS within **24 hours**, or students churn.
   - Persona: branch manager with **500–2,000 students**.
   - They pay vendors **BDT 15,000–50,000 upfront** for question-bank generators and OMR engines. OMR hardware and software cost **BDT 25,000–75,000**.
9. **Commercial readiness tiers:**
   - **Tier 1 (immediate spend):** fee reconciliation with gated exam entry; exam tabulation and grade processing
   - **Tier 2 (replacement spend):** automated CQ/MCQ authoring and printing
   - **Tier 3 (marginal or unpaid):** LMS, social, discussion
10. **Market sizing** (Problem 1): about **24,000** secondary and higher-secondary schools and colleges, and about **15,000** commercial coaching centers. The one-page map adds about **150,000 secondary teachers** and "millions of students across 24,000 institutions".
11. **Exam-related spend:**
    - institutions spend **BDT 20,000–100,000/yr** on guidebooks, typing, paper and press
    - exam paper printing and composing costs **BDT 50,000–250,000/yr**
    - SaaS at **BDT 1,500–3,500/month** "falls comfortably within" discretionary exam spend
12. **Price sensitivity thresholds** (per student per month):

    | Price | Reaction |
    |---|---|
    | < BDT 3 | Seen as "too cheap to be reliable" |
    | **BDT 5–10** | "Sweet spot" for private and MPO schools |
    | BDT 15–25 | Only elite English-medium schools and large coaching centers |
    | > BDT 35 | Rejected; school commissions a custom build instead |

    Overall WTP: **BDT 5–12/student/month**, or **BDT 2,000–8,000/month flat** for coaching centers. Current solution satisfaction is **1.5/5**.
13. **Cost of the problem** for a 1,200-student school, **BDT 580,000–1,190,000/yr**:
    - clerical and teacher overtime: 180k–300k
    - composing and printing: 60k–120k
    - fee arrears: 250k–600k
    - SMS waste: 40k–80k
    - paper and stationery: 50k–90k
    Clerical staff spend **about 250 person-hours per term** on fee checks, admit cards and tabulation fixes.
14. **Opportunity map** (annual institutional waste): exam generation BDT 80k–150k; tabulation 100k–250k; fee gating 200k–600k; coaching OMR 50k–180k; SMS 40k–100k; LMS BDT 0 ("False Market Opportunity").
15. **Why existing solutions fail:**
    - Google Classroom lacks NCTB CQ formatting, OMR parsing, tabulation, bKash/Nagad and Bangla SMS.
    - Moodle is too complex to host.
    - Local ERPs (MM IT, BDSchool, ShikkhaPlus, Edufy) treat academics as "superficial add-ons" with no question banks or rubrics.
    - Noipunno failed: outages, poor UI, rural connectivity, minimal training.
16. **Do-nothing competitor.** WhatsApp + Facebook + Google Drive + paper registers + print shops + guidebooks. It wins on zero cost, zero training and low bandwidth, and because paper allows "discretionary grade changes … retrospectively" while databases remove that flexibility.
17. **Strongest segments:**
    - **Primary beachhead:** commercial coaching centers (high tech maturity, very high WTP, low sales friction)
    - **Secondary:** private English-medium schools (tuition BDT 4k–15k/month; want homework tracking, report cards, parent portal)
    - **Scale target:** high-enrollment private and MPO Bangla-medium schools (budget locked at BDT 5–10/student/month; managing-committee sign-off; need an ERP core)
    - **Unattractive:** universities (6–12-month tenders)
    - **Avoid:** rural government schools (zero WTP)
18. **JTBD (assessment):**
    - **Assessment authoring.** Functional: "Generate a balanced, NCTB-compliant, typo-free examination paper in **under 15 minutes**, exportable to print-ready PDF with complete answer keys." Emotional: moderation-proof. Social: efficiency, no late-night typing.
    - **Result processing.** Functional: raw marks become a validated master ledger and report cards with zero discrepancies.
19. **Recommended product.** An "Academic Assessment and Operations Engine" with four modules:
    - **(1) Smart Question Bank and Exam Paper Builder:** NCTB CQ/MCQ across Science, Business Studies and Humanities; balances chapter weights and cognitive tiers; Bangla typography
    - **(2) Marks Ingestion and Tabulation Engine:** column-level validation, 4th-subject rules, board-compliant ledgers, *smartphone OMR for coaching centers*
    - **(3) Fee gating and QR admit cards** with bKash/Nagad
    - **(4) Transactional Bangla SMS**
20. **What NOT to build:** discussion boards, video conferencing, SCORM modules, desktop-only student portals, and **generic conversational AI chatbots** ("Schools will not pay for generalized AI tutoring tools").
21. **Decision.** "VALIDATE". Terminate the LMS. Proceed to paid pilots with coaching centers and private secondary schools. The biggest risk named is building an accurate, trusted **Bangla Unicode question repository** and handling tabulation edge cases. The claimed upside is that the platform "cuts teacher exam preparation time by **80%**".

---

## Quantitative claims table

| Claim | Value | Source cited in doc | Source type | Credibility (High/Med/Low) and why |
|---|---|---|---|---|
| Curriculum rollback | 2021/22 curriculum rolled back late 2024; 2012 syllabus restored for 2025/26 | Daily Star etc. | News | **High.** Consistent with known events. |
| Teacher base salary | BDT 11,300–16,000 / 16,000–22,000 / 16,000–24,000 | ResearchGate pay paper, OECD EAG 2025 | Academic / intergovernmental | **Low.** Three inconsistent ranges in one doc. OECD EAG does not cover BD pay scales in this way. |
| Clerical assessment hours per teacher per cycle | 25–35 h (also 20 + 30–45 h; 50–70 h) | none | None | **Low.** Internally inconsistent. |
| Instructional time lost | >180 h/teacher/yr | derived | Derived | **Low.** |
| Class size | 55–80 (60–80) per section | none | None | **Med.** Consistent across docs. |
| Students assessed per teacher per day | 250–450 | none | None | **Low-Med.** |
| Homework review labor | 20–30 h/week | none | None | **Low.** |
| Schools without integrated automation | ~70% | none | None | **Low.** Same suspicious "70%" figure as in A2, used for a different claim. |
| Report card delay | 2–3 weeks | none | None | **Med.** Consistent with A2's 21.5 days. |
| Operations pause during tabulation | 10–15 days | none | None | **Low-Med.** |
| CQs and MCQs per paper | 10–15 CQs, 30 MCQs to choose | none | None | **Med.** Plausible (e.g. 11 CQs offered, 7 answered; 30 MCQs). |
| Exam paper generation timeline | 3–5 + 5–7 + 2–3 + 2–4 days | none | None | **Low-Med.** |
| Target paper-generation time (JTBD) | < 15 min | none | Aspirational | n/a |
| Secondary and higher-secondary institutions | ~24,000 | none | None | **Med.** Order of magnitude is plausible. **[Analyst note]** Verify against BANBEIS. |
| Coaching centers | ~15,000 | none | None | **Low.** |
| Secondary teachers | ~150,000 | none | None | **Low.** **[Analyst note]** Appears low relative to BANBEIS-reported secondary teacher counts. Verify. |
| Exam-related materials spend | BDT 20k–100k/yr; printing/composing BDT 50k–250k/yr | [cite: 16] unresolved | None visible | **Low.** |
| Coaching software spend | BDT 15k–50k upfront; OMR BDT 25k–75k | [cite: 14] unresolved | Vendor? | **Low-Med.** |
| SaaS price that fits exam budget | BDT 1,500–3,500/month | none | None | **Low.** |
| ERP contract price | BDT 5–12/student/month; BDT 30k–150k/yr | [cite: 9,21,42]; Edufy / EduManager / Eduzone pricing pages | Vendor | **Med.** Vendor pricing pages are a real anchor. Conflicts with A1 (10–30) and A2 (≈6.7/month). |
| Price-sensitivity bands | <3 / 5–10 / 15–25 / >35 BDT per student per month | none | None | **Low.** Plausible but unsourced. |
| Coaching flat WTP | BDT 2,000–8,000/month | none | None | **Low.** |
| SMS cost | BDT 0.35–0.50/SMS | [cite: 11,13,21] | Vendor | **Med.** |
| Tuition arrears | 5–12% (top-5 table) vs 5–15% (Problem 3) | [cite: 9,17] | None visible | **Low.** Internally inconsistent. |
| Annual waste, 1,200-student school | BDT 580k–1.19M | [cite: …] unresolved | None visible | **Low.** Sums check out but inputs are unsourced. |
| Clerical hours | ~250 person-hours/term | none | None | **Low.** |
| Parent communication gap | 15–25% | none | None | **Low.** |
| Current solution satisfaction | 1.5/5 | none | None | **Low.** No survey exists. |
| Teacher prep time saved | 80% | none | None | **Low.** Aspirational claim. |
| Paid-pilot success gate | ≥4 of 10 sign LOI; BDT 10,000–15,000 setup fee | proposal | n/a | n/a (a proposed criterion) |
| English-medium tuition | BDT 4k–15k/month | none | None | **Med.** |

---

## Product-relevant specifics

**Exam types**
- Schools: terminal exams (3 per year), class tests (weekly), model tests, term tests.
- Coaching centers: daily 20-minute MCQ tests or 25-mark MCQ quizzes, weekly written tests, full mock exams, admission batches.
- Board exams: SSC and HSC, with university entrance exams as the target for coaching.

**Marks structure and rules**
- CQ in four tiers (Gyan, Onudhabon, Proyog, Ucchotoro Dokkhota) plus MCQ. Chapter-wise mark distributions.
- GPA on a 5.0 scale.
- **4th subject:** grade points above 2.0 count toward the overall score.
- **Separate pass marks for written (CQ) and MCQ**; continuous-assessment weighting; practicals.
- Tabulation sheets must be "board-compliant". Cambridge and Edexcel are also mentioned for English-medium schools.

**Who grades.** Subject teachers grade scripts and hand-enter marks. Exam controllers and head clerks tabulate. In coaching centers, branch staff scan OMR and enter written scores.

**Grading time**
- Not measured for scripts.
- Homework review would take 20–30 h/week, so it is abandoned.
- Teachers spend 30–45 h per cycle hand-entering marks (inconsistent figures).

**Re-evaluation.** Not covered.

**Result processing.** Handwritten scorecards are typed cell-by-cell into Excel, checked manually and printed as a master register. SMS goes out through GSM modems or web gateways.

**Stakeholders and personas**
- **P1 Subject Teacher:** math or physical science; urban or semi-urban MPO; 5 periods of 65–80 students; BDT 16k–24k; runs private coaching batches after hours.
- **P2 Coaching Branch Manager:** 500–2,000 students across 3 shifts; SMS percentiles within hours; staff run desktop OMR late at night.
- **P3 Private School Principal/Exam Controller:** worried about leaks, delayed report cards, grading-error disputes and fee arrears; direct purchasing authority with the School Managing Committee (SMC).

**Buyers**
- **Schools:** Principal, Head Teacher or SMC Chair. The money comes from the exam fees collected from students each semester (for authoring) or the general ICT/admin fund (for tabulation).
- **Coaching centers:** MD or Academic Head.

**Pain points ranked (assessment subset).** Exam paper generation, then tabulation, then (coaching) test operations, then homework evaluation collapse, then subjective feedback.

**WTP signals (the strongest numeric WTP guidance in the four docs, though unsourced):**
- BDT 5–10/student/month is the sweet spot.
- BDT 1,500–3,500/month SaaS fits exam budgets.
- Coaching centers pay BDT 2,000–8,000/month.
- Setup fee of BDT 10,000–15,000 as the paid-pilot gate.
- Explicit **negative** WTP for homework grading (teachers have no budget) and for student feedback (students lack purchasing autonomy).
- Schools won't pay for generic AI chatbots.

**Device and connectivity**
- Students rarely have laptops, so student and parent touchpoints must be mobile, SMS or PDF.
- Consumer apps win on low bandwidth.
- Smartphone-based OMR is proposed for coaching centers.
- Moodle-type complexity fails.

**Language and encoding**
- **Bijoy (ANSI) vs Unicode** conflicts corrupt files.
- Science and math typography in Bangla is hard.
- The question bank must be in **Bangla Unicode**.

**Medium.** Bangla medium; English version is implied; English medium (Cambridge/Edexcel).

**Curriculum.** NCTB restored 2012 framework; CQ/MCQ; streams are Science, Business Studies and Humanities.

**Competitors in the assessment space**
- Question-bank and OMR vendors for coaching (unnamed apart from the cited Fleek ExamPro, Genius Edusoft, qbankbd, Chorcha)
- ERPs: BDSchool, ShikkhaPlus, PathshalaSoft, MM IT, Edufy
- Commercial guidebooks: Panjeree, Anupam, Lecture

---

## Assumptions (stated or implicit)

1. Institutions buy administrative control, revenue protection and risk mitigation, not pedagogy. This underlies the low scores for feedback and homework grading.
2. Coaching centers are digitally proficient and decide "instantly without committees".
3. The 2012 curriculum restoration is stable for 2025/2026 and beyond.
4. A syllabus-aligned CQ/MCQ question bank can be built and trusted, and guidebook dependence can be displaced despite copyright and quality issues.
5. Tabulation is already partly solved by ERPs (it is the module ERPs sell on). A new entrant must therefore beat ERPs on tabulation accuracy or bundle it.
6. Pricing thresholds generalize across private and MPO schools.
7. Grading of written scripts is *not* treated as a product opportunity. Only OMR, tabulation and authoring are.

## Recommendations made by the doc

1. Kill the LMS. Build an "Academic Assessment and Operations Engine" with four modules: question bank and paper builder; marks ingestion and tabulation (plus smartphone OMR); fee gating and QR admit cards; Bangla SMS.
2. Beachhead: **commercial coaching centers**, then private English-medium schools, then high-enrollment private and MPO Bangla-medium schools. Avoid universities and rural government schools.
3. Price at BDT 5–12/student/month, or BDT 2,000–8,000/month flat for coaching.
4. Validation plan:
   - **Weeks 1–3:** 30 interviews (10 coaching, 10 MPO, 10 English-medium)
   - **Weeks 4–5:** shadow 5 exam controllers and 5 teachers
   - **Weeks 6–8:** concierge CQ/MCQ papers for 5 schools
   - **Weeks 9–12:** paid pilot with a BDT 10,000 setup fee
5. Interview prompts (verbatim):
   - Teachers: "Walk me through how you set your last terminal physics examination. Show me the draft files…"
   - Exam controllers: "Show me the register or spreadsheet where last term's marks were compiled. What happened when a teacher entered an incorrect score?"
   - Principals: questions about fee arrears.
6. Observation metrics:
   - minutes to format a 50-mark paper
   - typos found during moderation
   - clerical hours transcribing marks
   - parent complaints about calculation errors
7. Kill gate: at least 4 of 10 pilots sign a paid LOI and deposit BDT 10,000–15,000. "If institutions demand free trials, the problem lacks sufficient commercial urgency, and development must stop."
8. Do not build generic AI chatbots, forums, video or SCORM.

## Open questions raised or implied

- Can a trusted Bangla Unicode CQ/MCQ repository be built, and with what content rights? Guidebook publishers (Panjeree etc.) hold the categorized banks.
- Which tabulation edge cases (4th subject, separate pass marks, grace marks) must be supported at launch?
- *Implied for our product:* Coaching centers run **weekly written tests** at high volume with a 24-hour turnaround requirement. Is that a better wedge for AI-assisted *written-answer* grading than schools? The report only discusses OMR for coaching.
- *Implied:* If feedback and homework grading have "Very Low" or "Low" WTP, who pays for AI script-feedback features? Possibly bundled into coaching or private-school packages, or sold B2C to parents. The report does not examine this.
- *Implied:* Does the paper-register "flexibility" (retrospective grade changes) mean schools will resist audit trails? A2 and A3 treat audit logs as a benefit.

## Critical assessment

**Relevance to our product is indirect.** The report's frame is "LMS vs operations". It never evaluates AI grading of handwritten answer scripts. Its signals about grading are:
- homework grading has low WTP
- essay feedback has very low WTP because students don't buy
- OMR and tabulation have real budgets
This is an important *negative* signal for pure "AI feedback" positioning. It is not evidence against AI-assisted exam-script marking sold to coaching centers or private schools as a time or accuracy tool, which the report does not analyze.

**Unsupported numbers**
- The WTP bands, price-sensitivity thresholds, 70% no-automation figure, 1.5/5 satisfaction, 15–25% communication gap, 80% time saving and the market counts (24k institutions, 15k coaching centers, 150k teachers) have no visible source.
- Many table cells carry **unresolved `[cite: N]` markers**, so claims cannot be traced.
- The source list is padded with duplicated URLs and off-topic items (tutor listings, Quora, a Pakistani ERP blog, an Aalto thesis, procurement slides).

**Internal contradictions**
- Teacher salary appears as three different ranges (11.3k–16k, 16k–22k, 16k–24k).
- Clerical assessment time appears as 25–35 h, 50–65 h and 50–70 h per cycle.
- Arrears are 5–12% in one place and 5–15% in another; fee waste is 250k–600k in one place and 200k–600k in another.
- The top-20 ranking cannot be reproduced. Only frequency and frustration scores are shown, while the formula weights financial impact and existing spend more heavily. For example, #2 tabulation (freq 3) ranks above #4 (freq 5, frust 4) with no visible justification.
- "Coaching centers" are the "primary target (beachhead)", while the one-page map lists both coaching centers and Tier-1/2 private schools as "best initial segment".

**Vendor bias.** ERP prices and capabilities come from vendor pricing pages and "best software" listicles. The claim that ERP contracts are "routinely canceled" over tabulation errors is unsourced.

**Curriculum: correct.** This is the only doc that explicitly accounts for the late-2024 rollback and the restored 2012 CQ/MCQ framework. **[Analyst note]** Some sources it cites (formative assessment under "National Curriculum 2022", Noipunno) are NCF-era. The report correctly treats Noipunno as a past failure.

**Overgeneralization.** Coaching centers are treated as a uniform, tech-proficient, high-WTP segment, based on large brands (Udvash, Unmesh, Retina). Most of the "15,000" neighborhood centers are likely small and price-sensitive. **[Analyst note]** Segment them by size.

**Age and positioning.** The file sits in a different folder and was framed as older and LMS-oriented. Its WTP bands are the only concrete pricing anchors across the four docs, but they are unsourced and should be validated, not adopted.

## Confidence level

**Overall: Low-Medium.**
- **Medium** for qualitative market structure: admin and revenue problems get budget and pedagogy doesn't; coaching centers have high test cadence and spend on OMR; Bijoy/Unicode pain; the do-nothing competitor; the curriculum context.
- **Low** for all numbers (pricing, costs, market sizes, hours), which are unsourced or internally inconsistent.
- Assessment-grading insights are thin because grading was out of scope.

## Relevance to product decisions

| Decision | How this doc should inform it | Strength |
|---|---|---|
| Curriculum assumptions | Build on the restored 2012 NCTB CQ/MCQ framework: four cognitive tiers with Bangla labels, separate CQ/MCQ pass marks, 4th-subject rule, GPA 5.0. | **Strong** |
| Positioning of AI feedback | Don't sell "student feedback" as the primary value; WTP is very low. Sell teacher time saved, accuracy and results turnaround to the institution. | Medium-Strong |
| Beachhead | Test **coaching centers** (high test cadence, 24-hour turnaround, existing OMR spend, fast decisions) alongside private schools. Consider AI-assisted grading of written weekly tests as a wedge; unvalidated. | Medium |
| Pricing hypotheses | Start with BDT 5–10/student/month (schools) and BDT 2,000–8,000/month flat (coaching). Paid pilot setup fee of BDT 10,000–15,000 as the commitment test. Conflicts with A1's BDT 15/student/**year** kill threshold, so validate. | Medium (as hypotheses) |
| Adjacent modules / bundling | Tabulation (deterministic) is table-stakes and the ERP incumbents' selling point; the grading product must feed into or include validated tabulation. Question-paper generation is a possible adjacent wedge. | Medium |
| Validation gates | Adopt the paid-LOI gate (≥4/10) and the interview/observation prompts. | **Strong** |
| Technical risks | Bangla Unicode handling (Bijoy conversion), typography, low-bandwidth mobile. | Medium-Strong |
