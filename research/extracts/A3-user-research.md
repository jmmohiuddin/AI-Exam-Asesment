# The Assessment and Examination Ecosystem in Bangladesh Education: Customer Discovery and User Research Report

Full title in doc: *"The Assessment and Examination Ecosystem in Bangladesh Education: Comprehensive Customer Discovery and User Research Report"*

- **Drive ID:** `1nhTEQGlS08p04MCXVfAHCz9AqEFwZVM8Cqi5GnyuZag` (Google Doc, about 67k characters, read in full including the source list)
- **Research topic:** Customer discovery for assessment and result-processing software. Covers stakeholders, segmentation, personas, JTBD, journeys, trust in AI, procurement, switching costs, behavioral contradictions, and a strategic pivot recommendation.
- **Apparent method:** Desk research framed as "customer discovery". About 20 sources:
  - News: Dhaka Tribune (Noipunno dysfunctional), Daily Star (curriculum implementation), Bangladesh Post (Noipunno launch), Prothom Alo (question leaks), Daily Sun and Business Times (honorarium revisions for **recruitment** exams)
  - Academic: ResearchGate phenomenological study of teachers' NCF 2021 experiences; social-reproduction analysis of the curriculum; IJISRT 2026 systematic review; EdTech Hub 2025 "AI in Education Across Bangladesh"
  - **Vendor marketing pages:** Edufy, Pipilika Soft, Bidyaan, MMIT Soft, Pathshalasoft, and Vidyalaya (an Indian vendor)
- **Primary research conducted?** **No.** The report reads like a user-research study: it has "evidence-based personas" with names, "empirical field observations", "behavioral evidence", "what users say vs do", and "users verbally request 'automated AI grading' during high-level demos". But no interviews, demos, observations or surveys are described, and no sample, dates or locations are given. Output 20 *proposes* the fieldwork: 30 shadowing sessions, 15 ICT audits, and prototype pilots in rural MPO schools. The named personas (Sultana Parveen, Mohammad Rafiqul Islam, Engr. Shamsul Huda) are **fictional composites**. Claimed sample size: **none**.

---

## Main findings

1. **Market is not homogeneous.** It splits by:
   - **medium:** Bangla-medium, English-version, English-medium, National Curriculum, Madrasa
   - **funding:** Government, MPO-aided, Private/Commercial
   - **geography:** Metropolitan, Peri-urban, Rural
   Treating it as one market "leads directly to product failure".
2. **Noipunno is the cautionary case.** Noipunno was the DSHE + a2i app for NCF continuous assessment of Class VI–VII Proficiency Indicators (PI) and Behavioral Indicators (BI). It assumed internet access and server stability. The report says it:
   - crashed at peak evaluation times and was unusable "for weeks"
   - locked out rural teachers, where "**83%** of students and educators lack stable internet access and hardware"
   - enabled **question-paper leaks** through distributed user IDs
   - drove teachers back to paper and **"shadow khatas"**, and triggered public protests demanding a return to written exams
3. **Nobody wants an AI evaluator; the pivot is to orchestration.** The report says the assumption that institutions and teachers want an automated AI answer-script evaluator is **"disproved by behavioral and institutional evidence"**:
   - Teachers see it as a threat to authority, autonomy, **honorarium income and private tutoring income**.
   - Parents and students fear bias, misread handwriting and unappealable errors.
   - Bangla NLP cannot handle variable handwritten Bangla.
   The primary unmet need is an **offline-first assessment orchestration, mark-verification and result-aggregation platform**.
4. **Stakeholder authority matrix:**
   - **Owner/Chairman:** pays and holds veto.
   - **Principal:** recommends; can block.
   - **VP/Academic Coordinator:** can reject the workflow.
   - **Exam Coordinator:** heavy user; can block by "declaring it unusable".
   - **Subject teachers:** heavy users; low to moderate influence; block through passive resistance.
   - **ICT admin:** technical veto.
   - **Parents:** pay indirectly through fees; block through public protest.
5. **Segments and decision velocity:**

   | Segment | Tech maturity | Decision velocity |
   |---|---|---|
   | Government | Level 1–2 | Very low (bureaucratic) |
   | MPO | Level 1–2 | Low (governing body) |
   | Urban private Bangla/English version | Level 3–4 | High (owner/principal) |
   | Elite English-medium | Level 4–5 | Moderate |
   | Qawmi and Aliya madrasas | Level 1–2 | Low to moderate |

6. **Five tech-maturity levels:**
   1. paper only ("Tabulation Khatas")
   2. paper plus one or two teachers keying marks into Excel
   3. local desktop result software or SMS portals
   4. integrated cloud ERP (Edufy, Pipilika Soft, Bidyaan) with bKash/Nagad fees
   5. multi-branch cloud with mobile apps and analytics
7. **Three named personas** (fictional):
   - **Overburdened Subject Teacher** ("Sultana Parveen")
     - MPO school in Bogura, Level 2 maturity; Bangla and Social Science
     - 4 sections of 65–85 students; paid ৳16,500–22,000/month
     - job: grade 300+ scripts in 10 days; eyestrain, summation errors, double entry
     - board honorarium "≈৳130 per written script"
     - burned by Noipunno; fears AI misreads handwriting and erodes honorarium
     - willing to change if the tool simplifies calculation without taking away authority
   - **Stress-Driven Exam Coordinator** ("Mohammad Rafiqul Islam")
     - urban private Bangla & English version school in Dhaka, Level 3
     - consolidates marks from **45 teachers across 12 grades**
     - pains: late mark sheets, unreadable roll numbers, summation errors, favoritism accusations
     - tools: Excel, WhatsApp, desktop result software
     - rejects anything that needs continuous internet or restricts grading-scale customization
     - high buying influence as recommender
   - **Reputation-Focused Owner** ("Engr. Shamsul Huda")
     - 3-branch, 2,200-student private network in Gazipur, Level 4
     - uses Pipilika Soft or Edufy
     - enthusiastic about tech as marketing, but won't buy anything that triggers teacher or parent pushback
     - absolute buying authority
8. **Exam frequency.** Exam cycles happen **2–4 times a year**: term mid-terms, term finals, Test examinations, Annual summative. Five phases: pre-exam, execution, evaluation, aggregation, publication and review.
9. **"Unseen" friction points:**
   - cover-page summation errors, "estimated **5% to 8%** human calculation error rate"
   - double entry: script cover to physical Tabulation Khata to software or Excel
   - **secrecy-code reconciliation** back to roll numbers, described as "chaotic" and error-prone
   - moving physical bundles to teachers' homes (loss, monsoon moisture)
   - PI/BI continuous-assessment data recorded on scraps of paper
10. **Local competitors (vendor-described):**
    - **Edufy:** bilingual; fees, attendance, SMS, results; urban and semi-urban private schools
    - **Pipilika Soft:** "dominant" in higher education and large colleges
    - **Bidyaan:** cloud; multi-branch; schools, colleges, madrasahs
    - **MMIT Soft:** custom, Dhaka
    - **Pathshalasoft:** Bangla-medium schools and madrasas; offline sync; bKash/Nagad; NCTB alignment
11. **Informal workarounds:**
    - teachers photograph mark sheets and send them to the coordinator on WhatsApp
    - parallel shadow khatas
    - password-protected Excel macro tabulators
    - outsourced data entry to university students or computer-shop operators during result crunches
12. **Moments of truth:**
    - For teachers, the moment is tapping "Submit Marks": an instant confirmation with offline backup builds trust, while a crash that wipes data means rejection.
    - For coordinators, it is running the master tabulation and getting a 100% match across subject sheets, gradebooks and transcripts with no recalculation.
13. **Human control matrix** (key product constraint):

    | Task | Automation level | Human control |
    |---|---|---|
    | MCQ optical scanning | Full (100%) | Only for torn or double-bubbled sheets |
    | Cover-page arithmetic | Full (100%) | Teacher approves the computed sum |
    | Transcription and tabulation | Automated sync | Coordinator reviews anomaly flags |
    | **Subjective short-answer** | **AI assisted / suggested** | **Teacher keeps 100% final override** |
    | **Subjective essay / creative writing** | **Zero automation** | AI limited to grammar and syntax checks |
    | Final grades and merit ranking | Automated computation | Coordinator and Principal sign-off |

14. **Trust-failure scenarios:**
    - different scores for similar answers
    - handwriting or dialect misreads leading to wrong zeros
    - loss of teacher autonomy or forced rigid rubrics
    - parent accusations of arbitrary evaluation
    The AI trust map is high for arithmetic, OMR and GPA, and extreme distrust for subjective grading, handwriting interpretation and black-box scoring.
15. **Buying journey (13 stages):**
    1. problem recognition
    2. internal discussion
    3. vendor discovery (peer recommendation, local vendors)
    4. demo
    5. staff evaluation (coordinator and ICT)
    6. financial negotiation (per-student or annual)
    7. board approval
    8. contract
    9. data migration
    10. in-person training
    11. **pilot in one mid-term cycle**
    12. rollout
    13. annual renewal based on uptime and feedback
16. **Procurement by segment:**

    | Segment | Authority | Sales cycle | Price sensitivity | Contract structure |
    |---|---|---|---|---|
    | Government | Ministry/DSHE tenders | 12–24 months | High | Fixed grant |
    | MPO | Governing Body | 3–6 months | "Extremely high" | Low annual per-student license |
    | Commercial private | MD/Owner | 1–3 months | Moderate | Monthly/annual subscription |
    | Elite English-medium | Board of Trustees | 2–4 months | Low | Enterprise license |

17. **Switching barriers:**
    - migration risk
    - retraining (in-person)
    - no migrations near exams (sales windows only in post-year breaks)
    - bundled ERP lock-in, so a standalone assessment tool must show API integration
18. **Goal conflict.** Teachers want minimal entry burden, protection of tutoring income, autonomy and scoring control. Management wants oversight, speed, lower cost and standardized audited grading.
19. **Behavioral contradictions** (asserted):
    - (1) Teachers say they want automation but resist it for fear that honorariums will be cut or their speed monitored.
    - (2) Principals want AI for marketing but drop it at the first parent complaint.
    - (3) Teachers say mobile is convenient but go back to desktop Excel or paper for mark matrices on small screens with poor connectivity.
20. **Priority scoring (1–5)** across 8 criteria: IF, SP, PU, DI, BA, EV, AI, RB.
    - **Owner:** BA 5, EV 5, PU 1. The financial gatekeeper.
    - **Exam Coordinator:** IF 5, SP 5, PU 5, AI 5. The operational champion.
    - **Subject teacher:** BA 1, AI 5, RB 5. The adoption bottleneck.
21. **Evidence classification (self-rated):**
    - **"Verified":** server instability forces paper fallback; 83% rural lack stable internet; Bangla NLP for subjective evaluation is unreliable
    - **"Strongly Supported":** owners pay for ERP mainly for fees and reputation; **৳130 per script board rate**; shadow khatas
    - **"Hypothesis":** private schools will buy standalone AI grading at high prices
    - **"Indicative":** madrasas prefer offline-first
22. **Strategic pivot (explicit).** "The original hypothesis — building an automated AI answer-script grading engine — **must be abandoned**." Build instead an **Offline-First Assessment Orchestration and Score Verification Platform** with four capabilities:
    - (1) computer-vision score verification: scan cover-page mark matrices and verify subtotals
    - (2) offline-first local sync
    - (3) single-entry result tabulation
    - (4) human-assisted anomaly detection: missing scores, impossible entries, statistical anomalies

---

## Quantitative claims table

| Claim | Value | Source cited in doc | Source type | Credibility (High/Med/Low) and why |
|---|---|---|---|---|
| Rural students and educators without stable internet or hardware | 83% | "Empirical field studies" (probably IJISRT / EdTech Hub) | Academic (unclear) | **Low-Med.** Self-rated "Verified", but the population and definition are unclear. Used as both "students and educators" and "rural students and teachers". |
| Cover-page summation error rate | 5–8% | none | None | **Low.** No source. Much higher than A1's 2–4% school estimate. |
| Board honorarium per written script | ৳130 | Daily Sun "honorarium rates for **recruitment** exams"; Business Times "Govt Doubles Exam Honorarium, Raises Recruitment Pay" | News | **Low.** The sources appear to concern public recruitment exams, not SSC/HSC script evaluation. Likely misattributed. Conflicts with A1 (BDT 15) and A2 (BDT 25–45). |
| MPO teacher monthly pay (persona) | ৳16,500–22,000 | none | None | **Low-Med.** |
| MPO teacher base pay (segment text) | ৳5,000–12,000 | none | None | **Low.** Contradicts the persona in the same doc and A1 (12,500–16,000). |
| Class size (persona) | 65–85 per section; 4 sections | none | None | **Med.** Consistent with other docs. |
| Scripts per teacher | 300+ in 10 days | none | None | **Med.** |
| Coordinator scope | 45 teachers, 12 grades | none | None | Illustrative (persona). |
| Owner network | 3 branches, 2,200 students | none | None | Illustrative (persona). |
| Exam cycles per year | 2–4 | none | None | **Med.** |
| Sales cycle: govt / MPO / private / EM | 12–24 / 3–6 / 1–3 / 2–4 months | none | None | **Low.** Plausible but unsourced. |
| Buying journey | 13 stages | none | None | Framework, not data. |
| Stakeholder priority scores | e.g. Owner BA 5 / PU 1; Coordinator IF/SP/PU/AI 5; Teacher BA 1, AI 5, RB 5 | none | None | Analyst judgment presented as scoring. |
| Noipunno unusable "for weeks" | weeks | Dhaka Tribune "Teachers in trouble as assessment app Noipunno dysfunctional" | News | **Med.** The dysfunction is reported; the duration is unclear. |
| Noipunno scope | Class VI–VII PI/BI | Bangladesh Post | News | **Med-High.** |
| Noipunno-linked question leaks | occurred | Prothom Alo "NCTB warns of action for question 'leaks' in half-yearly exams" | News | **Med.** The link to distributed Noipunno IDs is asserted. |
| Bangla NLP unreliable for subjective grading | qualitative | IJISRT review, EdTech Hub | Academic / grey literature | **Med.** Directionally reasonable as of the sources' dates. Frontier vision-LLMs are moving quickly and this needs a direct benchmark. |

---

## Product-relevant specifics

**Exam types.** Term mid-terms, term finals, Test examinations, Annual summative. Formal board exams use secrecy codes. The report does not detail CQ/MCQ mark splits; it mentions MCQ/OMR, short answers and essays/creative writing.

**Who grades.** Subject and class teachers grade. The exam coordinator aggregates and verifies totals. HODs handle subject consistency. Internal and external examiners work under the exam coordination committee.

**Grading time.** More than 300 subjective scripts in 10 days per teacher (persona). Grading happens at home in the evenings.

**Re-evaluation.** Post-exam "script re-checking requests from parents". Process not detailed.

**Result processing.** Teachers submit physical tabulation sheets or enter scores into local ERPs. The coordinator verifies totals, computes GPA, compiles merit lists and submits to the Principal. Then report cards, SMS and archive.

**Stakeholders and roles.** See the authority matrix above (Main findings, item 4). Decision-maker map:
- primary users: teachers and office staff
- operational champion: Exam Coordinator
- technical gatekeeper: ICT admin
- academic approver: Principal
- financial buyer: Owner, MD or Governing Body
- blockers: tech-averse senior teachers and risk-averse ICT admins

**Personas (verbatim names; fictional):** Sultana Parveen (MPO teacher, Bogura), Mohammad Rafiqul Islam (Exam Coordinator, Dhaka), Engr. Shamsul Huda (school-chain owner, Gazipur).

**JTBD matrix:**

| Role | Functional | Emotional | Social |
|---|---|---|---|
| Teacher | Grade, total and submit error-free sheets on time | No miscalculations, no reprimands | Seen as expert and fair |
| Coordinator | Aggregate, moderate, GPA, merit list | No anxiety over published errors | Show mastery to Principal and governing body |
| Principal | Quality, timely publication, policy | Peace of mind, no parent unrest | Top-performing modern school |
| Owner | Cost, enrollment, fee collection | Protect the investment | Outshine competitors with tech |
| Student | Transparent, accurate scores with feedback | Fair treatment, understand deductions | Peer status, parental expectations |
| Parent | Timely, clear progress reports | Reassurance of fair assessment | Family pride |

**Pain points ranked (User Pain Map, Output 05):**
1. cover-page summation mistakes during late-night grading
2. double-entry transcription
3. server outages and data loss at peak submission
4. parent confrontations over bias or merit-list errors

**User need vs request (verbatim examples):**
- **Need:** eliminate arithmetic cover-page summation errors and verify tabulated marks instantly.
- **Request:** "Give us an automated AI button that grades everything automatically."
- **Preference:** Bangla interface plus WhatsApp notifications.
- **Behavior:** shadow khatas and offline Excel.
- **Business requirement:** "rapid result processing to collect tuition fee dues before issuing exam admit cards".
- **Technical requirement:** "offline-first architecture with local SQLite database synchronization capable of operating in low-bandwidth rural environments".

**Willingness to pay**
- Owners pay for ERP mainly for fee management and reputation.
- MPO schools are "extremely high" price sensitivity and want low annual per-student licenses.
- Commercial private schools accept monthly or annual subscriptions and are moderately sensitive.
- Elite English-medium schools take enterprise licenses with low sensitivity.
- WTP for standalone AI grading at high prices is explicitly labelled an unvalidated **hypothesis**.
- The report gives no BDT price points.

**Switching triggers (verbatim list).** Institutions switch if the product:
- guarantees "100% offline functionality"
- eliminates summation errors
- cuts processing "from weeks to hours"
- integrates with existing ERP databases
- offers affordable per-student pricing

**Rejection triggers.** Institutions reject a product that:
- needs continuous cloud access
- crashes at exam time
- forces complex data entry
- replaces human grading judgment

**Device and connectivity**
- 83% of rural users lack stable internet.
- Small smartphone screens are poor for mark-matrix entry.
- Teachers still use personal phones (WhatsApp photos).
- Offline-first local database with sync.

**Language and medium.** Bangla interface preferred. The platform must handle Bangla/English version schools and madrasas (custom grading scales). The report stresses dialect and spelling variation in Bangla answers.

**Curriculum.** The report is framed around the **NCF (2021) continuous assessment with PI/BI and Noipunno** as a live mandate. It mentions compliance with "shifting NCTB assessment directives" for government schools.

**Integration.** bKash/Nagad fee integrations are common in ERPs. APIs for Edufy, Pipilika and Bidyaan are needed (openness unknown).

---

## Assumptions (stated or implicit)

1. Behavioral claims (shadow khatas, resistance, demo requests) generalize nationally, although they come from Noipunno news and papers about the NCF, not from observation of exam-grading software.
2. Teachers' private-tutoring and honorarium income is threatened by grading automation. For internal exams there is usually no honorarium, so this is mainly a board-exam concern.
3. The NCF/PI/BI continuous-assessment regime is current. **Outdated:** see Critical assessment.
4. Cover-page matrix capture by camera is reliable enough to "eliminate" summation errors.
5. Institution owners in private schools are the buyer. For MPO schools it is the governing body; government schools cannot buy.
6. Assistive AI for short answers is acceptable if the teacher keeps full override, but essays must have zero automation. This is asserted, not tested.
7. Bangla NLP's limits as described in 2025/2026 grey literature also apply to current multimodal LLMs. Not tested.

## Recommendations made by the doc

1. Abandon the automated AI answer-script grading engine as the core hypothesis.
2. Build an **Offline-First Assessment Orchestration and Score Verification Platform**:
   - CV cover-page score verification
   - offline-first local sync (SQLite)
   - single-entry tabulation
   - human-assisted anomaly detection
3. Design for the Exam Coordinator as champion, the Owner/MD as buyer, and the teacher as veto-holder. Never increase teacher data entry or threaten authority.
4. Offer a Bangla UI and WhatsApp-style notifications. Guarantee instant, offline-safe "Submit Marks" confirmation.
5. Integrate with incumbent ERPs (Edufy, Pipilika, Bidyaan) rather than compete head-on. Time sales to post-academic-year breaks. Pilot in one mid-term cycle.
6. Research next:
   - 30 observational shadowing sessions of teachers grading during mid-terms
   - 15 ICT technical-integration audits
   - offline optical score-verification prototypes in rural MPO schools
   - price sensitivity in Qawmi madrasa networks
   - ERP API openness
   - DSHE/NCTB policy on third-party software in board evaluations

## Open questions raised or implied

- Exact price sensitivity, especially for madrasas. The doc gives no numbers.
- Whether ERP vendors will open databases or APIs.
- How DSHE/NCTB regulate third-party software in board evaluations.
- *Implied:* Is AI-suggested short-answer scoring with teacher override actually acceptable to teachers, parents and principals? The human control matrix allows it, but the pivot abandons AI grading.
- *Implied:* Do the "behavioral contradictions" hold for internal exams (no honorarium) as opposed to board exams?
- *Implied:* Would the Coordinator persona adopt a mobile capture flow, given that contradiction 3 says small-screen matrices fail?

## Critical assessment

**The primary research is simulated.** The report uses customer-discovery vocabulary ("evidence-based personas", "empirical field observations", "behavioral evidence", "users verbally request … during high-level demos") without having done any discovery. The named personas are fictional composites, and their details (Bogura, ৳16,500–22,000, 45 teachers × 12 grades, 2,200 students in Gazipur) are invented. **[Analyst note]** Do not cite them as research subjects. Rebuild personas from real interviews.

**The self-assigned evidence grades are inflated.**
- The "Verified" and "Strongly Supported" labels rest on news items, vendor pages and low-tier journals.
- The ৳130/script board honorarium is rated "Strongly Supported" by "Ministry of Education official honorarium rate adjustment notices", but the linked sources cover **recruitment exam** honorarium revisions. This looks like a misapplied citation.

**Internal contradictions**
- MPO teacher pay is ৳16,500–22,000 in Persona 1 but "৳5,000–৳12,000 monthly base" in Output 02.
- The pivot says AI grading "must be abandoned", yet the human control matrix allows "AI assisted / suggested" subjective short-answer scoring with teacher override. So the doc does not actually reject assistive AI, only autonomous AI.
- The report says teachers "claim mobile apps are most convenient" but abandon them for matrix entry, and then recommends mobile or desktop camera scanning of cover matrices. This is reconcilable (capture vs typing) but not discussed.

**Outdated curriculum framing.** The report treats NCF 2021 continuous assessment (PI/BI for Classes VI–VII) and Noipunno as the operating regime. It even lists "Continuous Assessment Data Loss" under the NCF as a current pain point and says government schools struggle with "shifting NCTB assessment directives". **[Analyst note]** Bangladesh reversed the competency-based curriculum in late 2024 and returned to the older (2012-based) curriculum with CQ/MCQ exams for 2025/2026. PI/BI tracking and Noipunno are therefore largely historical. The Noipunno lessons (offline-first, server fragility, teacher distrust) are still valid as a cautionary tale. But the PI/BI pain point and any product feature built around it should be dropped or re-validated.

**Vendor claims presented as fact.** The competitor descriptions (e.g. Pipilika "dominant", Pathshalasoft "established" with "NCTB curriculum alignment") come straight from vendor marketing pages. A "best school management software 2026" page on Bidyaan's own site is not market evidence.

**Unsupported statistics.** The 5–8% cover-page error rate and the 83% rural connectivity gap are presented without traceable sources. The 83% figure is also reused as the "83% deficit" adoption barrier.

**AI stance: reasonable caution, weak evidence.** The claim that Bangla NLP is "technically unable" to evaluate handwritten answers relies on literature reviews. It does not test current multimodal models. It may be true for autonomous grading today, but it is not established for assisted workflows (transcription plus suggested sub-part marks with teacher confirmation).

**Plausible and useful content**
- the stakeholder/veto structure
- the "Submit Marks" moment of truth
- shadow khatas and Excel fallbacks
- the ERP-bundling lock-in
- the sales-window timing (avoid exam periods)
- the need-vs-request distinction

These are credible design heuristics, even though they are not empirically grounded here.

## Confidence level

**Overall: Low-Medium.**
- **Medium** for the qualitative stakeholder and adoption model, the Noipunno lessons and the human control matrix as design principles.
- **Low** for every number, the personas, the procurement durations and the "behavioral evidence", none of which comes from primary research.
- **Low** for its curriculum context, which is outdated.

The pivot recommendation is directionally consistent with A1 and A2. It is not independently evidenced.

## Relevance to product decisions

| Decision | How this doc should inform it | Strength |
|---|---|---|
| Autonomy level of AI | Adopt the human control matrix as a starting policy: full automation for arithmetic, OMR and GPA; *suggested* scores with 100% teacher override for short answers; no auto-scoring of essays or creative writing. Validate with users. | **Strong** (as a design principle) |
| Buyer / champion / veto mapping | Coordinator = champion; Owner/MD or governing body = buyer; teacher = veto; ICT = technical veto. Shapes onboarding, pricing conversations and UX. | Medium-Strong |
| Offline-first architecture | Offline-first local DB with sync; instant offline-safe submit confirmation. | **Strong** (corroborated by A2 and A4) |
| Beachhead segment | Urban private Bangla/English-version schools: high decision velocity, 1–3 month sales cycle. Avoid government; MPO is slow and price-sensitive. | Medium |
| Integration | Must integrate or co-exist with Edufy, Pipilika, Bidyaan, etc. API openness is unknown. | Medium |
| GTM timing | Sell in post-academic-year windows; pilot during one mid-term cycle. | Medium |
| Features around NCF PI/BI continuous assessment | **Do not build** without re-validation; the curriculum has been rolled back. | **Strong** (negative) |
| Pricing | No usable price data; the ৳130/script honorarium is unreliable. | Weak |
| Personas for PRD | Use only as *hypothesis* personas and label them fictional. | Weak |
