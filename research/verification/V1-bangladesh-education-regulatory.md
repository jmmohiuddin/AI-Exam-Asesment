# V1 — Bangladesh Education and Regulatory Verification (for an AI exam-script assessment product)

**Prepared:** 2026-09-27 · **Scope:** Bangladesh secondary (Grades 6–10) and higher secondary (Grades 11–12), including SSC/HSC board exams, internal school assessment, digital readiness, and data/AI regulation.

**Method.** I used web search (WebSearch plus Exa search and fetch). The priority order was official sources (NCTB, the Ministry of Education and its Secondary and Higher Education Division (SHED), education boards, BANBEIS, BBS, BTRC, Bangladesh Bank, bdlaws, the ICT Division), then peer-reviewed or legal analysis, then major news outlets. Direct fetches from nctb.gov.bd, bdlaws.minlaw.gov.bd, thedailystar.net and tbsnews.net were blocked by the network proxy, so I read those pages through Exa's crawler. A few bdlaws pages came back in a legacy Bangla font encoding. I decoded them myself, and I mark those readings as needing legal review. Dates in brackets are publication dates. "Accessed" means the page carried no date and I read it on 2026-09-27.

**Status labels.** Verified = confirmed in an official source, or in at least two independent reputable sources. Partly = one reputable source only, a secondary source, or some details missing. Unverified = I could not find it. Contradicted = sources disagree, or a later source overrides an earlier one.

---

## Q1. Curriculum status, 2025–2026

### Verified facts
- **The 2021/2022 competency-based curriculum was rolled back on 1 Sep 2024.** A SHED circular called the National Curriculum 2022 "unfeasible". It cited teachers who were not prepared, unclear or negative views of the content and assessment methods, and weak institutional capacity. The circular reinstated the science, humanities and business groups at secondary level, restored assessment "as per the National Curriculum 2012 as much as possible", and ordered revised 2012-based textbooks for 2025. Sources: The Daily Star [2024-09-01] https://www.thedailystar.net/news/bangladesh/education/news/secondary-edn-science-arts-commerce-groups-return-3692371 ; The Financial Express [2024-09-01] https://thefinancialexpress.com.bd/national/science-arts-and-commerce-streams-to-be-reinstated-in-secondary-education ; Dhaka Tribune [2024-09-01] https://www.dhakatribune.com/bangladesh/education/356925/science-commerce-arts-segregation-returns-to
- **How the transition was sequenced:**
  - Students entering Class 10 in 2025 got 2012-based group textbooks and a shortened syllabus to finish in one year. They sat the 2026 SSC.
  - Students entering Class 9 in 2025 follow the full two-year 2012-based syllabus and sit the 2027 SSC.
  - The DSHE ordered all schools to reinstate the groups in Classes 9 and 10 on 16 Oct 2024. Source: BSS [2024-10-16] https://www.bssnews.net/news/216669
- **Primary level still uses the 2022 curriculum; secondary uses the revised 2012 curriculum.** Source: Dhaka Tribune [2025-07-17] https://www.dhakatribune.com/bangladesh/education/386691/nctb-to-launch-new-curriculum-in-2027-based-on
- **2026 school year.** Secondary classes still use revised 2012-based textbooks. In May 2026 the NCTB chairman said: "We are currently following a curriculum from 14 years ago (2012)." About 320 experts are revising 97 secondary and 36 primary books for 2027. In all, 601 textbooks will be revised, including English-version books up to Grade 9. The ICT textbooks for Grades 6–10 are being "almost completely redesigned", with new AI content. Source: Dhaka Tribune/BSS [2026-05-15] https://www.dhakatribune.com/bangladesh/education/410282/nctb-chairman-textbooks-being-revised-to
- **An entirely new curriculum is now planned for 2028, not 2027.** Education Minister ANM Ehsanul Hoque Milon announced this on 1 July 2026, and a committee has been formed. Sources: TBS [2026-07-01] https://www.tbsnews.net/bangladesh/education/new-curriculum-be-introduced-2028-not-2027-education-minister-1477336 ; The Daily Star [2026-07-02] https://www.thedailystar.net/news/education/news/hsc-exams-start-today-4213801
- **2027 is an interim year with four new compulsory subjects:**
  - From Grade 4: Sports and Culture.
  - From Grade 6: Technical and Vocational Education, and "Learning with Happiness".
  - Sources: Prothom Alo [2026-06-08] https://en.prothomalo.com/youth/education/22w4ttw8e6 ; The Daily Star [2026-07-13] https://www.thedailystar.net/news/bangladesh/education/news/edn-system-go-beyond-textbooks-4222571
- **History content is being revised again for 2027.** Additions include November 7 and Khaleda Zia's role, which makes curriculum content politically sensitive. Source: Dhaka Tribune/BSS [2026-05-20] https://www.dhakatribune.com/bangladesh/education/410721/abdul-khaleque-ensure-cent-percent-error-free

### Conflicting reports
- **Start year of the new curriculum.** In July 2025 the NCTB said it would start in 2027 with Grade 6 (Dhaka Tribune, 2025-07-17). In November 2025, pilot textbooks for Grades 1 and 6 were also mentioned for 2027 (TOB News [2025-11-15] https://tob.news/?p=108195). The later government statement moved the start to **2028** (TBS, 2026-07-01). I treat 2028 as current.
- **Whether 2028 covers all grades or is phased.** Prothom Alo (2026-06-08) reports this "has not yet been decided".

### Unverified
- **Institution-based assessment for Classes 6–9 from 2027.** One outlet reports that the National Curriculum Coordination Committee (NCCC) approved it (Daily New Nation [2026-09-06] https://dailynewnation.com/news/854077). I found no NCTB circular, so this is Partly verified.
- I found no official statement on whether Class 11–12 textbooks change in 2027. HSC candidates in 2026 sat the full 2012-based syllabus (see Q2).

### Implications for product design
- **Build rubric and syllabus packs for the 2012-based revised curriculum (2026–2027).** Expect a major change in 2028, possibly phased and possibly with a different assessment philosophy. Keep syllabus, question-type and marks mappings in versioned, data-driven configuration, not code.
- **Keep content maps per academic year.** Textbook content, especially History, Bangladesh and Global Studies, Bangla and ICT, is revised yearly and is politically sensitive.
- **Support separate Bangla- and English-version textbook editions.** Both are revised in parallel.

---

## Q2. SSC and HSC exam format, numbers, grading and re-scrutiny

### Verified facts: SSC 2026
- **Dates.** Written exams ran 21 Apr–20 May 2026, practicals 7–14 Jun 2026, with 3,885 centres and 30,666 institutions. Registered examinees were 1,857,344: 930,305 boys and 927,039 girls, with 1,418,318 under the general boards, 304,286 (or 303,286 in some reports) under the madrasah board and 134,660 under the technical board. Sources: Financial Post BD [2026-04-20] https://www.thefinancialpostbd.com/news/6073 ; Bangladesh Pratidin [2026-04-21] https://en.bd-pratidin.com/national/2026/04/21/61107 ; Daily Campus [2026-04-19] https://english.thedailycampus.com/school/2457
- **Results (10 Aug 2026).**
  - 1,829,485 sat the exam and 1,138,877 passed, a pass rate of **62.25%**.
  - 116,676 got GPA-5.
  - The general boards' pass rate was 64.05%, a 19-year low.
  - For comparison, SSC 2025 had a 68.45% pass rate and 139,032 GPA-5.
  - Sources: The Daily Star [2026-08-10] https://www.thedailystar.net/news/bangladesh/education/news/ssc-pass-rate-falls-6225-gpa-5-holders-also-decline-4244231 ; The Daily Star [2026-08-11] https://www.thedailystar.net/news/bangladesh/education/news/ssc-pass-rate-hits-19-year-low-4244971 ; Prothom Alo [2026-08-10] https://en.prothomalo.com/youth/education/j06836and4
- **SSC 2025 had 1,928,970 examinees.** Source: BSS [2026-04-20] https://www.bssnews.net/news-flash/379590
- **Reasons officials gave for the lower results.** Weak English and maths, stricter marking, **common question papers across all boards (the first time since 2006)**, full syllabus, and CCTV in every centre. Source: Agami Somoy [2026-08-10] https://www.agamirsomoy.com/en/bangladesh/education/hcjysixy2ns0
- **SSC 2026 format (NCTB, 3 Jan 2025).**
  - Subjects without practicals: **70 marks written (creative/"essay") + 30 marks MCQ**.
  - Subjects with practicals: **75 marks theory + 25 marks practical**.
  - Creative questions (CQ) were kept, and 33 subjects got customised short syllabi.
  - Source: BSS [2025-01-03] https://www.bssnews.net/news/235550
- **NCTB revisions on 22 Sep 2025.**
  - Bangla 2nd Paper: the translation item (10 marks) became news-report writing.
  - ICT: short-answer questions were removed, and MCQ went from 15 to 25 marks.
  - Finance and Banking: 15 short-answer questions, of which 10 must be answered.
  - Sources: BSS [2025-09-25] https://www.bssnews.net/news/315444 ; Prothom Alo [2025-09-24] https://en.prothomalo.com/youth/education/e4ln52af2b
- **Subjects marked out of 50.** Physical Education, Career Education and ICT; all others are out of 100. Source: Daily Campus [2025-06-26] https://english.thedailycampus.com/school%20/4. This is a single source, but it is consistent with the ICT change above.
- **NCTB publishes the official mark-distribution documents.** Its page "২০২৬ সালের এসএসসি ও সমমান পরীক্ষার সংশোধিত প্রশ্নের ধরন ও নম্বর বণ্টন" (revised question types and mark distribution for SSC 2026) lists them (page updated 23 Jan 2025). I could not download the PDF. http://nctb.portal.gov.bd/pages/static-pages/6922dce3933eb65569e12972

### Verified facts: HSC 2026 and 2025
- **HSC 2026.** Exams started 2 July 2026 with **1,270,583 candidates** from 9,439 institutions at 2,697 centres:
  - 1,069,714 under the general boards, 92,905 under the madrasah board and 107,964 under the technical board.
  - Written exams ended 8 Aug and practicals by 15 Aug.
  - It was the first HSC with **identical question papers across the general boards**.
  - All centres had CCTV, and police wore body cameras.
  - The minister promised examiner training, **fewer scripts per examiner**, and random re-marking of sample scripts.
  - Source: The Daily Star [2026-07-02] https://www.thedailystar.net/news/education/news/hsc-exams-start-today-4213801
- **HSC 2026 delays.** Floods pushed the Chattogram board's written exams to 9 Sep. Results are expected **7–15 Nov 2026**, so they are not yet published. Sources: viewsbangladesh [2026-09-23] https://viewsbangladesh.com/hsc-equivalent-results-expected-between-november-7-15/ ; Jagonews24 [2026-09-16] https://www.jagonews24.com/en/education/news/96139
- **HSC 2025.** Pass rate 58.83% (a 21-year low) and 69,097 GPA-5. Source: The Daily Star [2025-10-16] https://online.thedailystar.net/news/bangladesh/education/news/5883-students-pass-hsc-equivalent-exams-4011326
- **Grading scale (SSC and HSC, unchanged in 2026).**

  | Marks | Grade | Grade point |
  |---|---|---|
  | 80–100 | A+ | 5.00 |
  | 70–79 | A | 4.00 |
  | 60–69 | A− | 3.50 |
  | 50–59 | B | 3.00 |
  | 40–49 | C | 2.00 |
  | 33–39 | D | 1.00 |
  | 0–32 | F | 0.00 |

  The pass mark is 33%. For the optional 4th subject, only grade points above 2.00 count, as a bonus. The final GPA is capped at 5.00. Source: Shikkhok Batayon/teachers.gov.bd blog (accessed 2026-09-27) https://www.teachers.gov.bd/index.php/blog/details/849025. The 2026 results were again reported in GPA-5 terms (above).

### Verified facts: re-scrutiny and re-evaluation (major change in 2026)
- **New law on marking.** Parliament passed the **Public Examinations (Offences) (Amendment) Act 2026** on 7 Jul 2026, and it was gazetted on 9 Jul.
  - "Whoever over-assesses or under-assesses any public examination answer script" can get up to **2 years' imprisonment**, a fine, or both. No one can be convicted unless a **third examiner** confirms the over- or under-marking.
  - It also creates offences for "digital manipulation" of exam databases, organised exam crime, and bringing prohibited electronic devices into exam centres.
  - Sources: The Daily Star [2026-07-07] https://www.thedailystar.net/news/bangladesh/education/news/jail-unfair-marking-ssc-hsc-exams-under-new-law-4218206 ; Sarabangla [2026-08-20] https://en.sarabangla.net/education/post-19784/ssc-re-scrutiny-results-likely-on-sept-10/
- **First year of full re-marking.** In 2026 a challenged SSC script could, for the first time, be **fully re-evaluated**. Before this, re-scrutiny ("board challenge") only rechecked totals, blank items, OMR bubbles and data entry.
  - Applications ran online 11–17 Aug 2026.
  - **402,052 candidates** challenged **1,056,458 written scripts**, plus 231,471 practical scripts.
  - Results on 10 Sep: marks changed for 56,259 candidates, grades changed for 27,836, 4,585 moved from fail to pass, and 3,079 newly got GPA-5. Total GPA-5 rose to 119,755.
  - Sources: TBS [2026-09-10] https://www.tbsnews.net/bangladesh/education/ssc-re-scrutiny-4585-more-pass-gpa-5-count-rises-119755-1539001 ; Prothom Alo [2026-09-11] https://en.prothomalo.com/youth/education/my7djgahco ; Prothom Alo [2026-08-18] https://en.prothomalo.com/youth/education/b99zarcq98
- **Limits on future re-evaluation.** The minister said re-marking more than 1.2 million scripts was "not practically possible" and that a **policy with criteria for which scripts can be re-evaluated** will be issued. Scripts with serious errors or unusual discrepancies will get priority. Source: TBS [2026-08-17] https://www.tbsnews.net/bangladesh/education/govt-plans-new-policy-after-ssc-answer-script-review-applications-exceed-12

### Conflicting reports
- **SSC 2026 examinee count:** 1,857,344 registered (Inter-Board Committee, via several outlets); **1,851,423** (BSS, 2026-04-20); **1,829,485** actually sat (results). These measure different stages.
- **Fail-to-pass after re-scrutiny:** 4,585 (TBS; Prothom Alo article body) versus 4,085 (Prothom Alo headline [2026-09-10] https://en.prothomalo.com/youth/education/ff53ql6ll9). I use 4,585.
- **SSC 2026 result date:** the minister first said 20 July (Prothom Alo, 2026-06-08). Results actually came out on 10 Aug.
- **Exact CQ/short-answer/MCQ split per subject.** The NCTB (BSS 2025-01-03) states 70/30, and 75+25 for practical subjects. School syllabi show that the written part itself includes short-answer items. For example:
  - Mathematics: 50 CQ + 20 short answer + 30 MCQ.
  - Physics: 40 CQ + 10 short answer + 25 MCQ + 25 practical.
  - Source: Cantonment Public School and College, Saidpur 2025 syllabus [2025-03-25] https://cpscs.edu.bd/wp-content/uploads/2025/03/Nine-English-Version-Syllabus-2025.pdf
  - These are consistent, since short answers form part of the 70 "written" marks. The subject-level tables still need the NCTB PDF.

### Unverified or partly verified
- **HSC 2026 format.** Non-practical subjects are **70 CQ + 30 MCQ**. Practical subjects are **50 CQ + 25 MCQ + 25 practical**. Timing is **3 hours: MCQ first (30 minutes, or 25 minutes for 25 marks), then CQ (2 hours 30 minutes or 2 hours 35 minutes) with no break**. Candidates must pass theory, MCQ and practical separately. Sources are only secondary routine sites, e.g. https://hsc.routine.bd/ [2026-07-23] and https://checkresultbd.com/hsc-routine-2024-en/ [2024-04-03]. This is Partly verified, as the long-standing format consistent across sources.
- **2026 re-scrutiny fee per paper.** Historically about Tk 150 via Teletalk, but I found no 2026 source. Unverified.

### Implications for product design
- **Core question types.** CQ items are 10 marks each, split into (ka) knowledge, (kha) comprehension, (ga) application and (gha) higher-order. There are also 2-mark short-answer items, MCQs on OMR, and a separate practical. The marking engine must model per-sub-part marks and "answer N of M" choice rules.
- **Pass rules.** Each component has its own pass requirement (theory, MCQ, practical). Grades map to the A+ to F table, and the 4th subject counts only as a bonus.
- **Selling points: consistency and audit trails.** Fear of fines and jail for mis-marking, plus mass re-evaluation, make second-marker consistency checks, drift detection and per-script evidence logs valuable to boards and to examiners themselves. The expected re-evaluation criteria policy is a regulatory hook worth tracking.
- **Human decision rights.** Examiners are now legally liable for over- or under-marking. The product should position itself as **decision support, with a human giving the final mark**, and should keep an evidence trail that a "third examiner" can review.

---

## Q3. School-level internal assessment

### Verified facts
- **The 2024 interim guideline (NCTB, 11 Sep 2024) for the Classes 6–9 annual exam.**
  - Each subject: 30% continuous assessment plus 70% of a 100-mark, 3-hour written exam.
  - **Subject teachers write the question papers** by following NCTB sample papers, which may not be copied exactly. The head of the institution is responsible for confidentiality.
  - Question setters must provide **sample answers and rubrics** for open-ended items.
  - **No separate OMR sheets**: students write objective answers in the answer script.
  - Sources: school-hosted copy of the NCTB guideline (accessed 2026-09-27) http://ggbhs.edu.bd/assets/56/73/09/52d6417c1340dfa163550d0da5f79e77208aa79c.pdf ; The Bangladesh News [2024-09-11] https://bangladeshnews.live/education/news/annual-examination-of-70-marks-in-6th-9th-with-learning-assessment
- **2025–2026: schools went back to half-yearly and annual (yearly) exams plus class tests, set in the board style.** For example, one school's Class 9 plan for 2025:
  - Class Test 1 and Class Test 2 are 20 marks each.
  - Half-yearly and yearly exams mirror the SSC pattern. Maths is 50 CQ (answer 5 of 8) + 20 short answer (10 of 15) + 30 MCQ. Physics and Chemistry are 40 CQ (4 of 7) + 10 short answer (5 of 7) + 25 MCQ + 25 practical. English 1st Paper follows the board's 100-mark item list.
  - Source: Cantonment Public School and College, Saidpur [2025-03-25] https://cpscs.edu.bd/wp-content/uploads/2025/03/Nine-English-Version-Syllabus-2025.pdf
- **NCTB has issued revised guidance for 2026.** It covers the subject structure, allocated marks, weekly periods and a **revised assessment guideline for Classes 6 to 9–10** (page updated 23 Jan 2025). I could not retrieve the PDF contents. http://nctb.portal.gov.bd/pages/static-pages/6922dce3933eb65569e12972
- **Continuous-assessment forms for SSC 2026.** The Rajshahi board published a revised "continuous assessment form" for SSC 2026 [2026-05-18], which suggests schools submit some school-based marks. https://rajshahiboard.gov.bd/ (SSC corner page)

### Conflicting reports
- **2027 assessment model.** A Daily New Nation report [2026-09-06] says Classes 6–9 will move to "institution-based assessment" from 2027. How this differs from today's school-set half-yearly and annual exams is not clear.

### Unverified
- **Test, pre-test and model-test practice.** Pre-test or test exams before SSC/HSC form fill-up, and model tests, are widely described informally. I found **no 2025–2026 official circular** prescribing their format. They appear to be set by each institution in board format. Unverified.
- **Share of schools buying question papers from commercial "guide" publishers or coaching centres rather than writing their own.** Unverified.

### Implications for product design
- **Internal exams are the best entry point.** Teachers set their own CQ papers, so they are high volume, need no board approval, and differ from school to school. The product must accept **arbitrary teacher-written question papers plus teacher-written sample answers and rubrics**, which the NCTB guideline already requires setters to produce. It must also handle **objective answers written inline in the script**, since there is no OMR in school exams.
- **Target cycles.** Build around the calendar: class tests, half-yearly (around June), annual (around November–December) and test exams (around October–December before SSC). Model the 30/70 continuous/summative weighting as a configurable scheme.

---

## Q4. Scale: institutions, students and teachers

### Verified facts
- **Institutions (BANBEIS Bangladesh Education Statistics 2024):**

  | Type | 2024 | 2023 |
  |---|---|---|
  | Junior secondary schools | 2,547 | 2,406 |
  | Secondary schools | 16,570 | 16,562 |
  | School sections of school-and-colleges | 1,514 | 1,480 |
  | Colleges | 4,876 | 4,821 |
  | Madrasahs (Dakhil–Kamil) | 9,269 | 9,259 |

  Source: New Age [2025-11-16] https://www.newagebd.net/post/education/282265/school-college-madrassah-amenities-on-decline
- **BANBEIS 2023 "at a glance".**
  - Secondary schools: 18,968, of which 628 are government.
  - School and college: 1,480 (63 government). Colleges: 3,341 (637 public). Madrasahs: 9,259 (3 government). English-medium schools: 123.
  - Secondary students: 8,166,188. Secondary teachers: 246,784.
  - Source: BANBEIS PDF (accessed 2026-09-27) https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-banbeis/2024/12/18eb15a7026f431394e022af7e36a03a.pdf
- **Students and teachers in 2024 (BANBEIS).**
  - 9,063,422 students in secondary schools and school sections. Madrasah students: 2,796,191.
  - Secondary and higher-secondary students overall: 14,751,222, down 554,341 from 2023.
  - **Secondary teachers: 293,289** (92,492 female). Madrasah teachers: 128,522, of whom only 9.19% are trained.
  - Sources: New Age (accessed 2026-09-27) https://www.newagebd.net/post/education/280974/number-of-trained-teachers-declines ; https://www.newagebd.net/post/education/275383/number-of-secondary-higher-secondary-students-falls
- **Private and MPO share.** The Education Minister told Parliament that **34,129 non-government institutions** employ **598,994 teachers** and 206,699 staff. Of these, **6,179 are outside MPO** (2,712 schools, 223 school-and-colleges, 863 colleges, 1,092 madrasahs, 1,289 technical). Sources: The Daily Star [2026-04-08] https://www.thedailystar.net/news/bangladesh/education/news/60295-teaching-posts-vacant-mpo-institutions-milon-tells-parliament-4146711 ; TBS [2026-04-08] https://www.tbsnews.net/bangladesh/govt-nationalise-private-teachers-jobs-if-policy-decision-made-milon-1405936. Combined with BANBEIS (628 government out of 18,968 secondary schools), **about 97% of secondary schools are non-government**, and most of those are MPO-funded.
- **BBS Private Educational Institution Survey 2024.**
  - 92,391 private institutions, of which 26,104 are MPO.
  - High schools: 15,932, of which 14,215 are MPO. Dakhil madrasahs: 6,511, of which 5,166 are MPO.
  - All 13,902 Qawmi madrasahs are non-MPO.
  - Sources: TBS [2026-07-27] https://www.tbsnews.net/bangladesh/education/non-mpo-teachers-struggle-years-unpaid-teaching-affect-education-quality ; Daily Campus [2025-09-23] https://english.thedailycampus.com/school/687
- **English-medium (O/A level) schools.**
  - June 2026 Cambridge series: **more than 43,500 entries, about 12,000 students, 90 active schools**. That breaks down as more than 25,000 IGCSE/O Level entries and more than 18,000 AS/A Level entries. Source: TBS [2026-08-13] https://www.tbsnews.net/economy/corporates/cambridge-entries-bangladesh-rise-8-1514641
  - Pearson Edexcel runs as well, through the British Council.

### Conflicting reports
- **English-medium students.** BANBEIS 2023 gives 28,013 students in 123 schools. The Daily Campus [2025-05-22], citing BANBEIS, gives **140 registered schools and 68,825 students** (https://english.thedailycampus.com/english-medium/305). Registered counts clearly undercount the many unregistered English-medium schools.
- **Secondary school count.** BANBEIS's "secondary education" figure (18,968 in 2023) includes junior secondary schools. The 2024 split (2,547 + 16,570 = 19,117) uses a different grouping. Always state which definition is used.

### Unverified
- The total number of English-medium schools, including unregistered ones. Estimates commonly cited run into the thousands, but I found no official figure.
- The number of **English-version** (national curriculum in English) students and schools. The NCTB confirms English-version books up to Grade 9, but I found no enrolment figure.
- A 2025 edition of BANBEIS statistics.

### Implications for product design
- **Market size.** The addressable secondary market is roughly 20,000 schools plus 9,300 madrasahs, 4,900 colleges, about 9 million secondary students and about 290,000 secondary teachers. The buyer is overwhelmingly **non-government MPO institutions** with tight budgets: government pays basic salaries, but schools fund extras from fees. Price per student or per script in taka and target school management committees.
- **Madrasahs.** They are a large segment (Dakhil/Alim). They have specialised subjects (Arabic, Quran, Hadith), weaker ICT (see Q5) and fewer trained teachers.
- **English-medium schools.** They are a small (about 12,000 Cambridge candidates) but premium, early-adopter niche. Their CAIE/Edexcel mark schemes differ from NCTB's CQ format.

---

## Q5. Digital infrastructure and payments

### Verified facts
- **BTRC, July 2026.**
  - Mobile subscriptions: **190.44 million**. Mobile internet subscriptions: **121.52 million**. Total internet: 136.75 million. Mobile broadband (4G): 108.81 million.
  - Mobile internet penetration: 68.79%.
  - Source: BSS [2026-09-09] https://www.bssnews.net/special-stories/422612 (June figures: BSS [2026-08-02] https://www.bssnews.net/special-stories/410979)
- **BBS ICT Access and Use Survey 2025–26, Q4 (Apr–Jun 2026).**
  - Households: **99% have a mobile phone; 75.1% have a smartphone; 58.2% have internet; 9.1% have a computer**.
  - Individuals aged 5 and over: 89.6% use a mobile phone, 65.6% own one, 59.2% use the internet, and 11.8% use a computer.
  - Sources: The Daily Star [2026-09-20] https://www.thedailystar.net/news/technology/news/mobile-phone-use-reaches-896-bangladesh-bbs-4278021 ; The Financial Express [2026-09-20] https://thefinancialexpress.com.bd/trade/mobile-phone-ownership-rises-to-656pc ; newsbangladesh [2026-09-21] https://www.newsbangladesh.com/english/information-technology/news/127169
- **Feature phones remain widespread.** A government adviser said about 50% of people still do not use data-capable phones and the cheapest smartphone costs about **Tk 9,000**. A subsidised low-cost smartphone is targeted for October 2026. Source: The Financial Express [2026-09-05] https://thefinancialexpress.com.bd/trade/low-cost-smartphones-likely-to-hit-market-in-october
- **Device tiers.**
  - In July–September 2025, feature phones and smartphones sold roughly **50:50 by units**, though smartphones were about 80% of value.
  - The best-selling band is **Tk 15,000–25,000**. Retailers say 70–75% of rural students buy phones under Tk 20,000.
  - Brand shares (Statista via the article): Xiaomi about 18%, Samsung about 17.5%, Vivo about 12%, Realme about 10%, Oppo about 9%, Apple about 5%.
  - Source: Daily Campus [2025-11-29] https://english.thedailycampus.com/economy/1247
- **School ICT (BANBEIS 2024).**
  - Secondary schools: **computer lab in 40.25%**, digital lab in 33.12%, 14,342 schools with multimedia facilities.
  - Colleges: computer lab in 64.13%.
  - Madrasahs: computer lab in 13.23%; 6,172 have a computer or internet connection.
  - All of these fell from 2023. Source: New Age [2025-11-16] (link in Q4)
- **Planned devices for teachers.** The minister announced a "**One Teacher, One Tab**" plan and multimedia classrooms. Source: Digi Bangla [2026-04-07] https://digibanglatech.news/173197
- **Mobile financial services (MFS).**
  - **250 million accounts and 2.0 million agents** (Dec 2025).
  - Merchant payments are only **4.52%** of MFS value; cash-in, cash-out and person-to-person transfers make up over 85%.
  - Bangla QR has about 1 million merchants.
  - Source: Bangladesh Bank, Payment Systems Report 2025 https://www.bb.org.bd/pub/annual/psdreport/paymentreport_dec2025.pdf
  - MFS moved about Tk 5,883 crore a day in 2025. bKash reports 42 million active users and about 1 million merchants; Nagad claims 28.2 million. Source: The Daily Star (accessed 2026-09-27) https://www.thedailystar.net/ds/business-plus/news/tk-6000cr-moves-daily-not-every-wallet-winning-4220811
- **Nagad's status.** Nagad has run **under a Bangladesh Bank-appointed administrator since Aug 2024** on a temporary licence. It received interoperability approval in Dec 2025. Source: TBS [2025-12-16] https://publisher.tbsnews.net/economy/banking/bb-gives-licence-nagad-interoperable-payment-system-1311696
- **Fee collection already runs through MFS.** bKash has an "Education Fee" payment flow that institutions use. Example: State University of Bangladesh notice (accessed 2026-09-27) https://sub.ac.bd/notice/109

### Conflicting reports
- **Smartphone use.** 75% of households have a smartphone (BBS), but the adviser says about half of individuals lack data phones (FE). These are consistent, because household access is not the same as individual ownership.
- **Brand shares.** Statista and Counterpoint/IDC-derived figures differ, e.g. Samsung at 28% on devicesfinder.com, a low-reliability source.

### Unverified
- The share of secondary schools with **working** broadband, rather than just "internet connection", and its typical bandwidth.
- Typical RAM and storage of phones owned by teachers. My inference is 3–6 GB RAM, entry-level Android 12–14 devices in the Tk 12,000–25,000 band. This is not verified.
- How institutions typically pay SaaS vendors (MFS merchant account, bank transfer, or card). MFS merchant share is low, so bank or EFT invoicing plus bKash/Nagad for small schools is likely. Not verified.

### Implications for product design
- **Phone-first capture.** Script capture should be **Android-phone-first**, work on entry-level devices with 3–4 GB RAM, and support **offline capture with deferred upload**, because only 58% of households and a minority of schools have internet. Do not assume a school computer lab: 60% of secondary schools and 87% of madrasahs lack one.
- **Low data use.** Keep upload payloads small by compressing on the device and cropping each page. Many teachers will use personal phones on mobile data.
- **Payments.** Support **bKash/Nagad merchant payments** alongside bank invoices. Don't depend on Nagad for continuity, given its administrator-run status.

---

## Q6. Law and regulation

### Verified facts
- **Personal Data Protection Act, 2026 (Act No. 63 of 2026).** Enacted by Parliament on **10 April 2026**, repealing the Personal Data Protection Ordinance 2025 (Ordinance 61, gazetted 6 Nov 2025) and the Amendment Ordinance 2026 (Ordinance 23, 5 Feb 2026). **Commencement: in force from 6 Nov 2025, except sections 23 and 31–35, which take effect 18 months later (about May 2027).** Sources: DataGuidance [2026-05-11] https://www.dataguidance.com/news/bangladesh-parliament-bangladesh-enacts-personal-data ; The Financial Express [2026-04-09] https://thefinancialexpress.com.bd/home/parliament-passes-31-bills-related-to-ig-era-ordinances ; bdlaws act page http://bdlaws.minlaw.gov.bd/act-details-1692.html
- **Children under the Act.**
  - A child is **anyone under 18**, or another age the government sets (s.2(19)).
  - Section 9 (as I decoded it from bdlaws) says a child's data may be processed only with the consent of a **parent or legal guardian**, using the procedure regulations will set. Processing must protect the child's rights and interests, and parental consent stays valid until the child turns 18.
  - Sources: bdlaws s.2 http://bdlaws.minlaw.gov.bd/act-1692/section-57268.html ; s.9 http://bdlaws.minlaw.gov.bd/act-1692/section-57275.html ; Securiti [2026-06-29] https://securiti.ai/bangladesh-personal-data-protection-act-overview/
- **Other obligations under the Act.**
  - Consent must be explicit, specific, informed and revocable.
  - Lawful bases other than consent include contract, legal obligation and vital interests.
  - Data subjects can access, correct and port their data, withdraw consent, and object to or restrict **automated decisions**.
  - Records of processing must be kept at least **5 years**.
  - Breaches must be reported to the Authority.
  - "Significant data fiduciaries" must appoint a Chief Data Officer.
  - The Act applies to processors outside Bangladesh that serve Bangladeshi data subjects.
  - Sources: Securiti [2026-06-29] (above) ; Mahbub & Company (accessed 2026-09-27) https://mahbub-law.com/key-highlights-of-the-personal-data-protection-ordinance-2025-for-businesses/
- **Data classification and cross-border transfer (as of the March 2026 revised text).**
  - Section 29(1) sets **four tiers: public, internal, confidential and restricted**.
  - Transfers abroad need **consent, a contract with the data subject, or the data subject's interest** (the examples given include "education") (s.29(3)).
  - Destinations must have "suitable technology" prescribed by regulation (s.29(4)).
  - Source: CCIA submission (April 2026) https://ccianet.org/wp-content/uploads/2026/04/CCIA-Views-on-Bangladeshs-Personal-Data-Protection-Ordinance.pdf
- **Localisation narrowed in early 2026.** The 2026 amendment removed the broad "synchronous local backup" (localisation) rule. Localisation now applies only to **restricted data and about 35 designated critical information infrastructures**. Criminal liability for companies was replaced by fines. Sources: TBS op-ed by Faiz Ahmad Taiyeb [2026-03-14] https://www.tbsnews.net/thoughts/business-child-data-profiling-why-did-meta-exert-undue-pressure-data-protection-ordinance ; CCIA (above)
- **Data regulator.** The **National Data Management Act, 2026 (Act 80 of 2026, 10 April 2026)** replaces the 2025 Ordinance. It creates the National Data Management Authority, attached to the **Prime Minister's Office**, as the data-protection enforcer and interoperability operator. Sources: bdlaws http://bdlaws.minlaw.gov.bd/act-1709/act-chapter-print-2761.html ; Daily Star critique [2025-11-18] https://online91.thedailystar.net/law-our-rights/news/new-data-laws-bangladesh-critique-4038266
- **Cyber law.**
  - The **Cyber Security Ordinance 2025** (Ordinance 25, 21 May 2025) repealed the Cyber Security Act 2023 and for the first time made crimes committed using AI an offence (TBS [2025-05-22] https://www.tbsnews.net/bangladesh/govt-issues-gazette-cyber-security-ordinance-1149021).
  - It has since been replaced by the **Cyber Suraksha (Security) Act 2026 (Act 81 of 2026, 10 April 2026)**, amended by Act 99 of 2026 (bdlaws http://bdlaws.minlaw.gov.bd/act-1538.html ; Digi Bangla [2026-04-11] https://digibanglatech.news/173569).
  - A further amendment adding "rumour and disinformation" offences (up to 10 years) was being prepared in July 2026 (Prothom Alo [2026-07-29] https://en.prothomalo.com/bangladesh/wbq9kji6z7).
- **National AI Policy 2026–2030 is a draft, not adopted.**
  - Draft v1.1 came out in January 2026. Public consultation ran 26 Jan–8 Feb 2026, and **Draft v2.0** followed on 9 Feb 2026. The portal says the committee is reviewing responses. No adopted version had been found as of 3 Aug 2026.
  - Sources: https://aipolicy.gov.bd/ (accessed 2026-09-27) ; The Financial Express [2026-01-29] https://thefinancialexpress.com.bd/national/draft-ai-policy-tightens-state-oversight ; The Leveraged Years [2026-08-03] https://www.theleveragedyears.com/ai-regulation-news/bangladesh-national-ai-policy-2026-2030-draft-v2
  - Draft v2 provisions I read in the PDF:
    - Four risk tiers.
    - **Education is listed among high-risk sectors under a strict-liability regime.**
    - Rights to explanation, contestation and **human review** of AI decisions with significant effects, with education named.
    - Mandatory Algorithmic Impact Assessments for high-risk private systems.
    - Children's data to be stored in Bangladesh or in "trusted" jurisdictions.
    - For education specifically: "Student data, examinations, and academic records shall be protected by strict data-privacy and governance standards", "AI-resistant assessments", and 5-year retention of logs for high-risk AI.
    - Drafting of an AI Act to begin by 2028.
    - Source: https://aipolicy.gov.bd/docs/national-ai-policy-bangladesh-2026-2030-draft-v2.0.pdf
- **ICT Act 2006.** It remains listed on bdlaws, with no repeal note in the text I retrieved, and was amended in 2013. It still governs electronic records and digital signatures. http://bdlaws.minlaw.gov.bd/act-950.html (Partly verified)

### Conflicting reports
- **Children's profiling ban.** Section 9(3) of the 2025 Ordinance **banned tracking, monitoring, profiling and targeted advertising of children** (English copy of the ordinance: https://dpo-india.com/Resources/Privacy_Regulations_in_Asia_Pacific_Countries/Bangladesh-Personal-Data-Protection-Ordinance,2025(Ordinance.No.61-2025).pdf). The **enacted Act's s.9**, as I decoded it from bdlaws, has three subsections: consent, protecting interests, and validity to age 18. The profiling ban does not appear there. It may have been removed or moved elsewhere. This needs a Bangla-literate lawyer to confirm.
- **AI training on children's data.** Former special assistant Faiz Taiyeb said "processing children's data for modeling or AI training has been declared a criminal offense" (Digi Bangla, 2026-04-11). He also said the BNP government dropped criminal provisions for large-scale privacy violations. Draft AI Policy v1.1 proposed banning the use of children's data to train AI; that wording is not in v2's text as I read it. **Treat training on student scripts as high-risk until counsel confirms.**
- **Localisation.** SCL [2026-04-23] https://bd-scl.com/insights/personal-data-protection-ordinance-2025-compliance.html still says confidential and restricted data "must be stored within Bangladesh". CCIA, TBS and the Daily Star say the 2026 amendment removed broad localisation. SCL appears to describe the original ordinance.
- **Penalties.** DataGuidance says fines of up to BDT 5 million. TBS [2026-04-20] https://publisher.tbsnews.net/thoughts/personal-data-protection-ordinance-law-protects-you-everyone-except-state-1416106 says up to 5% of turnover. Earlier ordinance summaries say 1–2% of turnover, or 2–5% for significant fiduciaries.
- **Enactment date.** The Financial Express puts passage on Thursday, 9 April. DataGuidance and bdlaws say 10 April. The Cyber Act is dated 10 April on bdlaws, but Prothom Alo says 30 April.

### Unverified
- Whether the National Data Management Authority has actually been **constituted and staffed**, and whether any regulations exist yet: the consent procedure for children, the list of "suitable" destination countries, the breach-notification timeline, and the criteria for significant fiduciaries.
- **I found no specific rule on the use of AI in examinations or in marking student scripts.** The closest instruments are the Public Examinations (Offences) (Amendment) Act 2026 (digital manipulation and device offences) and the draft AI Policy's education clauses.
- Whether exam scripts or marks are classified as "confidential" or "restricted" under s.29.

### Implications for product design
- **Treat every student as a child (under 18).** Build **verifiable parental or guardian consent**, collected through the school, plus a lawful-basis record for the school as data fiduciary (contract, education interest). The school is the controller and the vendor is the processor, so the data processing agreement (DPA) must pass obligations through. A 5-year processing register is mandatory.
- **Model training is off by default.** Do **not train or fine-tune models on student scripts** without explicit opt-in and legal sign-off, given the conflicting reports on AI training and children's profiling. Minimise identifiers: mask names and roll numbers on the image and pseudonymise.
- **Hosting.** Hosting in Bangladesh or the region is the safer default. Cross-border transfer probably rests on consent or contract (s.29(3)), but keep an **in-country data residency option** for board or government contracts. The draft AI policy wants children's data kept in Bangladesh or "trusted" jurisdictions.
- **Automated decisions.** Offer contestation and human review, and log model versions, inference records and rationales for at least 5 years. This covers both the Act's automated-decision rights and the draft AI policy's high-risk and education requirements.

---

## Q7. Government exam digitisation

### Verified facts
- **MCQ answers go on OMR sheets in SSC and HSC** and are machine-read. OMR bubble errors are one of the things checked in re-scrutiny. Sources: Sarabangla [2026-09-23] https://en.sarabangla.net/bangladesh/post-32775/1684-examiners-face-action-over-ssc-exam-sheets-errors/ ; board routine instructions (secondary copy) https://checkresultbd.com/hsc-routine-2024-en/
- **Board administration is online.** Registration and form fill-up are online (e.g. Madrasah Board e-services https://www.ebmeb.gov.bd/). Results come by web and SMS, and re-scrutiny results appear at rescrutiny.eduboardresults.gov.bd (Prothom Alo, https://en.prothomalo.com/youth/education/pa9zmer3d9).
- **2026 control measures.** CCTV in every exam room, a central monitoring cell, police body cameras (Daily Star, 2026-07-02), common question papers, examiner training, and **random-sample expert re-evaluation of marked scripts** (BSS [2026-04-20] https://www.bssnews.net/news/379743). Examiners got **20 days instead of 15** to mark HSC scripts (Jagonews24, 2026-09-16).
- **Paper scripts still travel physically.** Examiners collect scripts from the board and return them, and the board's computer centre flags "blank mark" and "script wanting" problems. Source: Dhaka Board HSC 2026 notice [2026-07-04] https://dhakaeducationboard.gov.bd/data/20260704182642769322.pdf
- **Teachers' Portal (Shikkhok Batayon, a2i).** It is the national teacher content platform, with about 690,000 members on its live dashboard (accessed 2026-09-27) https://www.teachers.gov.bd/index.php/dashboard
- **Anonymised marking at a university.** RUET is piloting "unique coding" for anonymous marking (2025–26). Source: TBS Graduates [2026-05-05] https://tbsgraduates.net/education/no-more-biased-marking-ruet-introduces-coding-method-in-answer-script-evaluation/
- **A local AI assessment startup has government backing.** "Correct", an AI assessment-management and OMR startup, received a Prime Minister's startup grant. Source: SME TV [2026-07-17] https://smetvonline.net/news-details/bd-prime-minister-has-presented-a-startup-grant-cheque-to-an-ai-driven-edtech-startup-sme-tv

### Conflicting reports
- **Teachers' Portal membership:** 676,342 on one page versus about 689,936 on the dashboard. One vendor's case study claims "6,500,000+" registered teachers (https://riseuplabs.com/teachers-portal-connects-over-650000-educators-nationwide/ [2026-03-31]), which is implausible.

### Unverified
- **I found no board on-screen marking (scan-and-mark) pilot and no AI grading initiative** for SSC/HSC in Bangladesh up to 2026-09-27. India's CBSE introduced on-screen marking for Class 12 in 2026 (Indian Express [2026-02-11]), a regional precedent Bangladesh boards may look at.
- Any a2i or ICT Division project specifically on AI-assisted assessment. The draft AI Policy says public-sector AI apps will be **centrally coordinated by the ICT Division**, with a national Bangla LLM as the first project.

### Implications for product design
- **Boards are an adjacent but slower market.** Their current reform path is human-centred: training, random sampling, full re-evaluation and legal deterrents. A **scan-and-assist marking or "second-reader" QA tool** fits naturally. Integration hooks: **OMR-compatible MCQ** handling, the roll-number and code system on script covers, and output for tabulation.
- **Public-sector sales will need ICT Division alignment.** Once the AI policy is adopted, expect to use shared platforms and APIs, possibly with the Bangla LLM. Plan for an in-country deployment option.

---

## Q8. Examiner workload, pay and marking quality

### Verified facts
- **Pay per script.**
  - SSC examiners are paid **Tk 35 per script** and HSC examiners **Tk 40**. Payment took 7–8 months, and sometimes more than a year (Ittefaq).
  - In June 2025 the inter-board coordination committee approved raising pay to **Tk 45 (SSC)** and **Tk 50 (HSC)**, and scrutineers' pay from Tk 5 to Tk 8. Dhaka board promised to pay within 60 days of results.
  - Sources: Shikkhabarta, citing the Dhaka board exam controller [2025-06-20] https://shikshabarta.com/222653/ ; Ittefaq [2025-06-14] https://www.ittefaq.com.bd/736209/
- **Head examiner rate (primary evidence).** Rajshahi board's HSC 2024 head-examiner statements show a rate of **Tk 35 per script (Tk 32 for ICT)**, applied to 12% of supervised scripts plus the head examiner's own 350–600 scripts. https://rajshahiboard.gov.bd/wp-content/uploads/2025/06/H24H002_002.pdf
- **Scripts per examiner.**
  - **300–500** in about 15 days, while also teaching. Teacher leaders cite **500–600 in 10–15 days** for high-enrolment subjects.
  - Some examiners have family members or students mark scripts for them, and the board warned this is illegal.
  - A Bangladesh Examination Development Unit (BEDU) study found **faulty evaluation**: marks for wrong answers, under-marking of correct answers, and head examiners not re-checking properly.
  - Source: Ittefaq [2025-06-14] (above)
- **HSC 2026 allotments.** Dhaka board's Bangla-I notice shows **300 or 400 scripts** allotted per examiner. Source: https://dhakaeducationboard.gov.bd/data/20260704182642769322.pdf [2026-07-04]
- **Marking quality problems in 2026.**
  - Record re-scrutiny, with 27,836 grade changes (Q2).
  - **Jashore board: 1,684 examiners and head examiners face action**, including a proposed 2-year ban, after 2,436 results changed. The same board blacklisted 72 examiners after HSC 2025 re-scrutiny, and 290 in 2020.
  - Source: Sarabangla [2026-09-23] (link in Q7)
- **HSC 2026 incidents.** Errors in Physics and Chemistry questions, wrong question sets distributed, and an assistant professor suspended for having students fill in MCQ sheets during evaluation. Source: Agami Somoy [2026-08-08] https://www.agamirsomoy.com/en/bangladesh/education/hnqiy5rgquid
- **Mixed messages to examiners.** In April 2026 the minister told examiners to be "liberal": "if nine out of ten lines ... are correct, it should be awarded". He also said a proportional cap on scripts per teacher had been set. Source: BSS [2026-04-20] https://www.bssnews.net/news/379743. By July, examiners could be jailed for over- or under-marking (Q2).

### Conflicting reports
- **Whether the Tk 45/50 rates were actually paid for SSC and HSC 2026.** They were approved in June 2025, but I found no 2026 confirmation. The ministry also has not published the 2026 per-examiner script cap ("proportional rate").
- **Government recruitment exams are a separate scale.** The Finance Division revised rates in 2026 to Tk 130 per full script and Tk 35 per MCQ script. Source: BSS [2026-07-04] https://b.bssnews.net/news/402382. Do not confuse these with board SSC/HSC rates.

### Unverified
- The exact 2026 cap on scripts per examiner, and the total number of SSC/HSC examiners per year.

### Implications for product design
- **Pricing.** At about Tk 35–50 per script and 300–600 scripts per cycle, an examiner earns roughly Tk 10,000–30,000 per board cycle. An AI assist must save real time per script at a price well below the per-script fee. Price per script in the Tk 2–10 range, as a hypothesis to test.
- **Positioning.** The main pains are **time pressure, consistency and legal exposure**. Pitch the product as consistency-checking (flag outliers and missed totals, sum sub-marks automatically, catch blank marks) and as an **auditable evidence trail**, rather than as a replacement for the marker.
- **Automated error checks.** Common re-scrutiny errors (inside-page marks not totalled, OMR bubble mistakes, blank marks) can be caught deterministically. This is a quick win before any AI grading.

---

## Summary table

| Claim | Status | Source |
|---|---|---|
| 1 Sep 2024 circular rolled back NC 2022; groups reinstated; 2012-based books | Verified | Daily Star 2024-09-01; FE 2024-09-01; Dhaka Tribune 2024-09-01 |
| SSC 2026 students used short syllabus; Class 9 in 2025 → SSC 2027 full 2012 syllabus | Verified | Dhaka Tribune 2024-09-01; BSS 2024-10-16; BSS 2025-01-03 |
| Primary still on 2022 curriculum | Partly | Dhaka Tribune 2025-07-17 |
| Secondary on revised 2012 curriculum in 2026 | Verified | Dhaka Tribune/BSS 2026-05-15 |
| New curriculum from 2028 (not 2027) | Verified | TBS 2026-07-01; Daily Star 2026-07-02 |
| New curriculum from 2027 (earlier plan) | Contradicted | Dhaka Tribune 2025-07-17 (superseded) |
| 4 new compulsory subjects in 2027 (Grades 4 and 6) | Verified | Prothom Alo 2026-06-08; Daily Star 2026-07-13 |
| Institution-based assessment for Classes 6–9 from 2027 | Partly | Daily New Nation 2026-09-06 |
| SSC 2026 format: 70 written + 30 MCQ; practical subjects 75 + 25 | Verified | BSS 2025-01-03 (NCTB) |
| SSC 2026 ICT MCQ raised to 25; Bangla 2nd translation → news report | Verified | BSS 2025-09-25; Prothom Alo 2025-09-24 |
| Written part includes short-answer items (e.g. Maths 50 CQ + 20 SA + 30 MCQ) | Partly | CPSCS school syllabus 2025-03-25 |
| HSC: 70 CQ + 30 MCQ; practical subjects 50 + 25 + 25; MCQ first, 3 h total | Partly | hsc.routine.bd 2026-07-23; checkresultbd 2024 |
| SSC 2026 registered examinees 1,857,344 | Contradicted (1,851,423 per BSS) | Financial Post BD 2026-04-20; BSS 2026-04-20 |
| SSC 2026: 1,829,485 sat; 62.25% pass; 116,676 GPA-5 | Verified | Daily Star 2026-08-10; Prothom Alo 2026-08-10 |
| SSC 2025: 1,928,970 examinees; 68.45%; 139,032 GPA-5 | Verified | BSS 2026-04-20; Daily Star 2026-08-10 |
| HSC 2026: 1,270,583 candidates; results expected 7–15 Nov 2026 | Verified | Daily Star 2026-07-02; viewsbangladesh 2026-09-23 |
| HSC 2025: 58.83% pass; 69,097 GPA-5 | Verified | Daily Star 2025-10-16; BSS 2025-10-16 |
| GPA scale A+ ≥ 80 (5.0) … F < 33; 4th-subject bonus above 2.0 | Verified | teachers.gov.bd blog; 2026 results reported in GPA-5 |
| Common question papers across boards in 2026 | Verified | Daily Star 2026-07-02; Agami Somoy 2026-08-10 |
| Public Examinations (Offences) (Amendment) Act 2026: up to 2 years for over/under-marking; third-examiner check | Verified | Daily Star 2026-07-07; Sarabangla 2026-08-20 |
| Full re-evaluation added to re-scrutiny for the first time (SSC 2026) | Verified | Prothom Alo 2026-08-18; TBS 2026-09-10 |
| 402,052 applicants; 1,056,458 scripts; 27,836 grade changes; 3,079 new GPA-5 | Verified | TBS 2026-09-10; Prothom Alo 2026-09-11 |
| 4,585 fail→pass after re-scrutiny | Contradicted (4,085 in one headline) | TBS 2026-09-10 vs Prothom Alo 2026-09-10 |
| Govt to issue re-evaluation criteria policy | Verified (announced) | TBS 2026-08-17 |
| School annual exams: teacher-set papers with rubrics; 30/70 CA/summative (2024) | Verified | NCTB guideline copy; bangladeshnews.live 2024-09-11 |
| 2025–26 schools run class tests, half-yearly and yearly exams in board CQ format | Partly | CPSCS 2025 syllabus |
| Official format for test/pre-test/model exams | Unverified | none found |
| BANBEIS 2024: 16,570 secondary, 2,547 junior secondary, 4,876 colleges, 9,269 madrasahs | Verified (via news) | New Age 2025-11-16 |
| Secondary teachers 293,289 (2024); students 9.06 m | Verified (via news) | New Age (BANBEIS 2024) |
| 34,129 non-govt institutions; 598,994 teachers; 6,179 non-MPO | Verified | Daily Star 2026-04-08; TBS 2026-04-08 |
| About 97% of secondary schools non-government | Verified (derived) | BANBEIS 2023 (628 govt / 18,968) |
| English-medium: 123 schools / 28,013 students (BANBEIS 2023) vs 140 / 68,825 | Contradicted | BANBEIS 2023 PDF; Daily Campus 2025-05-22 |
| Cambridge June 2026: 43,500+ entries, about 12,000 students, 90 schools | Verified | TBS 2026-08-13; Daily Star |
| English-version enrolment count | Unverified | — |
| BTRC Jul 2026: 190.44 m mobile; 121.52 m mobile internet; 136.75 m internet | Verified | BSS 2026-09-09 |
| BBS Q4 FY26: 75.1% households smartphone; 58.2% household internet; 9.1% computer | Verified | Daily Star 2026-09-20; FE 2026-09-20 |
| About 50% of people lack data phones; cheapest smartphone about Tk 9,000 | Partly | FE 2026-09-05 |
| Best-selling phone band Tk 15–25k; 50:50 feature/smart by units | Partly | Daily Campus 2025-11-29 |
| Secondary schools with computer lab 40.25%; madrasahs 13.23% (2024) | Verified (via news) | New Age 2025-11-16 |
| MFS 250 m accounts; merchant payments 4.52% of value | Verified | Bangladesh Bank PSD Report 2025 |
| Nagad under BB administrator, temporary licence | Verified | TBS 2025-11-02 / 2025-12-16 |
| PDPA 2026 (Act 63) enacted 10 Apr 2026, repealing PDPO 2025 and 2026 amendment | Verified | DataGuidance 2026-05-11; FE 2026-04-09; bdlaws |
| PDPA in force from 6 Nov 2025; ss.23, 31–35 after 18 months | Partly | DataGuidance FAQ |
| Child = under 18; parental consent; valid to 18 (s.9) | Verified | bdlaws s.2, s.9; Securiti 2026-06-29 |
| Ban on profiling/targeted ads of children retained in Act | Contradicted / Unverified | Ordinance s.9(3) had it; decoded Act s.9 lacks it |
| Children's data for AI training is a criminal offence | Unverified | Taiyeb via Digi Bangla 2026-04-11 only |
| Four-tier data classification; cross-border on consent/contract/interest | Partly | CCIA Apr 2026 (on Mar 2026 text) |
| Broad localisation removed; only restricted data and CII | Partly / Contradicted by SCL | TBS 2026-03-14; Daily Star; vs SCL 2026-04-23 |
| PDPA penalties: BDT 5 m cap vs up to 5% of turnover | Contradicted | DataGuidance vs TBS 2026-04-20 |
| National Data Management Act 2026 (Act 80); authority under PMO | Verified | bdlaws; Daily Star 2025-11-18 |
| Authority constituted and regulations issued | Unverified | — |
| Cyber Security Ordinance 2025 repealed CSA 2023 (21 May 2025) | Verified | TBS 2025-05-22; bdlaws |
| Cyber Suraksha Act 2026 (Act 81) replaced the ordinance; amended by Act 99 | Verified | bdlaws; Digi Bangla 2026-04-11 |
| National AI Policy 2026–30: Draft v2 (9 Feb 2026), not adopted | Verified | aipolicy.gov.bd; TLY 2026-08-03 |
| Draft AI policy lists education as high-risk; human review; student data protection | Verified (draft text) | Draft v2 PDF |
| Specific rule on AI in exams or student-script marking | Unverified (none found) | — |
| ICT Act 2006 still in force (as amended) | Partly | bdlaws act-950 |
| MCQs on OMR in board exams | Verified | Sarabangla 2026-09-23; board instructions |
| Board on-screen marking or AI grading pilot | Unverified (none found) | — |
| Random-sample expert re-evaluation and examiner training in 2026 | Verified | BSS 2026-04-20; Daily Star 2026-07-02 |
| HSC 2026 examiners given 20 days (was 15) | Partly | Jagonews24 2026-09-16 |
| Teachers' Portal about 690k members | Partly (figures conflict) | teachers.gov.bd dashboard |
| Examiner pay Tk 35 (SSC) / Tk 40 (HSC) per script | Verified | Shikkhabarta 2025-06-20; Ittefaq 2025-06-14; Rajshahi board statement |
| Raise to Tk 45 / Tk 50 approved (June 2025) | Partly | Shikkhabarta 2025-06-20 |
| Raise actually paid in 2026 | Unverified | — |
| 300–600 scripts per examiner in 10–15 days | Verified | Ittefaq 2025-06-14; Dhaka Board notice 2026-07-04 |
| BEDU study found faulty evaluation | Partly | Ittefaq 2025-06-14 |
| Jashore board: 1,684 examiners face action (SSC 2026) | Partly | Sarabangla 2026-09-23 |
