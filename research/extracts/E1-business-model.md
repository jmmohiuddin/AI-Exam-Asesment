# E1 — Business Model Architecture, Pricing Strategy, and Unit Economics Blueprint for an AI-Powered Assessment Platform

- **Drive ID:** `1z4jFoRJPMGpRXIxbaBf0ObStltBrrgRpFOBH32vmvHc`
- **Topic:** Monetization model selection, pricing tiers, per-script COGS, gross margin, CAC/LTV, pilot economics, and expansion (API / white-label) for an AI exam-script grading platform in Bangladesh. The text calls the engine the "Nimikh Assessment Engine".
- **Method (as stated or implied):** Desk research. It uses vendor pricing pages (CoGrader, Eduman, MockExam.bd), third-party blog roundups of LLM/OCR prices ("GPT-4o-mini API Pricing 2026", "Gemini API Pricing 2026", G2, GetDeploying), Bangladeshi news items about exam dates, a Reddit thread, and a coaching-centre directory blog. It scores 13 business models on a 7-criterion 1–10 rubric (/70) and builds a deterministic spreadsheet-style model: 100 institutions, 3.6M scripts, 1 USD = 120 BDT. There are no customer interviews, no pilot data and no measured OCR/LLM accuracy. Inline "[cite: N]" markers appear in only a few places and do not map cleanly to the source list. **[Analyst note]** The doc has the hallmarks of an AI deep-research output: ASCII tables, uniform confidence, exact-looking derived numbers.
- **Extent read:** 100% of the document (≈74.6k characters: body plus the ~22-item source list).

---

## Main findings

1. **What is sold.** The product is framed as "assessment automation, grading consistency, teacher time recovery, and institutional assessment intelligence", not raw LLM/OCR access. The claimed value outcomes are "85% Teacher Time Recovery" and a "48-Hour Result Turnaround". The core value metric is the **evaluated answer script**.
2. **Recommended primary model.** The doc recommends a **Hybrid (Model F)**: an annual base subscription with a tiered script allowance and overages. Example: **BDT 45,000/yr including 6,000 scripts, then BDT 5.00/script overage**. It scored **60/70**, the highest of 13 models.
3. **Phased monetization.**
   - (a) Initial GTM: Hybrid, sold to commercial coaching centres and private English-medium and Bangla-medium schools.
   - (b) As relationships mature: per-student annual licensing embedded in the Result Management System (RMS).
   - (c) International scaling: a Developer Assessment API and white-label engine for EdTech/LMS/ERP vendors.
   - The summary lists a different progression: "Coaching Credit Packs → Institutional Hybrid SaaS → Enterprise API Infrastructure".
4. **Headline claimed economics.** The doc claims:
   - CAC payback **under 2 months**
   - 3-year LTV:CAC **above 19:1**
   - Gross margin **64%–85%**, depending on the HITL audit percentage and infrastructure optimisation
   - The executive summary target is ">70%"; the blueprint summary gives "64.8%–81.6%".
5. **Segmentation (Bangladesh), with estimated counts, student ranges and annual EdTech budgets:**
   - Tier 1, international/premium English-medium: **350+** institutions; 300–2,500 students; **BDT 250,000–1,500,000**. Examples: Scholastica, Mastermind, Sunbeams, ISD. Curricula CAIE/Edexcel/IB. Low price sensitivity.
   - Tier 2, urban private schools/colleges: **2,500+**; 1,000–8,000 students; **BDT 100,000–500,000**. Examples: Viqarunnisa, Ideal, Notre Dame, Holy Cross, Rajuk Uttara. National Curriculum (Bangla and English version). WTP is described as "high" if results drop from **3 weeks to 48 hours**.
   - Tier 3, commercial coaching: **1,200+**; 500–15,000 students; **BDT 150,000–1,200,000**. Examples: Udvash, Unmesh, Mentors', UCC, OMECA, Retina, Medico. Paper checking is described as a variable cash cost paid to external evaluators.
   - Tier 4, suburban/MPO: **18,000+**; 200–1,200 students; **BDT 20,000–80,000**. High price sensitivity; procurement goes through the SMC.
   - Tier 5, tutors/freelancers: **100,000+**; 10–100 students; out-of-pocket or freemium.
6. **Customer value model.** Representative Tier 2 school or coaching branch with **1,200 students**, grades 6–12:
   - 6 exam events/yr (2 terms + 4 model/class tests) × 6 subjects = **43,200 scripts/yr**
   - At **20 min/script**, that is **14,400 teacher-hours**
   - Contract checkers are paid **BDT 15–35/script** (baseline BDT 25), giving **BDT 1,080,000/yr**
   - Tabulation takes 3 min/script, or **2,160 admin hours = BDT 150,000**
   - Total manual cost: **BDT 1,230,000/yr**
   - AI workflow: **30 s** automated processing and **2 min** teacher audit per script
   - Software cost at **BDT 6.00/script-equivalent = BDT 259,200**; HITL at **12% × BDT 15 = BDT 77,760**
   - Total: **BDT 336,960**, giving net savings of **BDT 893,040 (72.6%)** and **12,000+ teacher-hours** recovered
7. **Value-driver table:**
   - Manual checking **20–25 min/script** versus **2–3 min** auditing
   - Result turnaround **14–21 days** versus **24–48 h**
   - Contract checker cost **BDT 15–35/paper** versus software COGS of **BDT 0.40–1.20/script**
8. **Seasonality.**
   - Peak volume in May–June (half-yearly and HSC) at **10× base** and in Nov–Dec (finals) at **12× base**; secondary peak Sept–Oct (test exams)
   - Low in Jan and Jul–Aug; the doc cites "7 non-exam months"
   - January is the "Annual Base Collection" cash month
   - Conclusion: an upfront annual subscription floor is mandatory.
9. **Competitor benchmarks.**
   - CoGrader **$15–19/teacher/month**, 350 submissions/month
   - Gradescope **$3–7/student/yr**
   - Crowdmark **$3–6/student/course**
   - ZipGrade **$6.99/teacher/yr** (OMR/MCQ only)
   - Edcafe AI **$7.99–14.99/month** (the text is garbled: "14.99permonth(96/year)")
   - Eduman ERP: **BDT 5,000–10,000 setup + BDT 70–100/student/yr**
   - MockExam.bd: **BDT 299/paper checked** (O/A-level mocks), presented as the premium WTP ceiling
10. **Infrastructure price benchmarks:**
    - AWS Textract **$0.0015/page** (basic) and **$0.015/page** (forms/tables)
    - Google Document AI **$1.50/1,000 pages**
    - Self-hosted PaddleOCR/TrOCR about **$0.0005/page**
    - GPT-4o-mini **$0.15/M input, $0.60/M output**
    - Gemini 1.5 Flash **$0.075/M input, $0.30/M output**
    - "DeepSeek V4 Flash" **$0.14/M input, $0.28/M output**
11. **13-model scorecard (/70):**
    - A Pure Institution 46; B Per-Script 54; C Per-Student 53; D Per-Exam 43; E Credit Packs 57
    - **F Hybrid 60 (winner)**; G Freemium 45; H Pilot→Contract 56 ("conversion >60%")
    - I Custom Enterprise 50 (ACV >BDT 500k, 6–12-month cycles); J Developer API 59; K White-Label ERP 56
    - L Reseller 50 (partner haircut 15–25%); M Government Board 43
12. **Model mechanics as specified:**
    - A: BDT 10,000/month or BDT 100,000/yr unlimited
    - B: BDT 8.00/script
    - C: **BDT 180–250/student/yr**, framed as a "Digital Assessment Fee" of BDT 15–20/month passed to parents
    - D: BDT 25,000 per exam event
    - E: 5,000 credits = 5,000 scripts
    - G: free 30 scripts/month
    - H: free pilot of up to 200 scripts
    - K: revenue share or wholesale to Eduman, Campus360
    - L: 15–20% commission
    - M: SSC/HSC tenders
13. **Per-script COGS stack** (assuming a **4-page** handwritten Srijonshil script):
    - OCR: self-hosted on L40S spot, **BDT 0.24** (0.06/page)
    - LLM: GPT-4o-mini with 1,800 input / 400 output tokens (cached), **BDT 0.061**
    - Hosting/storage: **BDT 0.10**
    - Base software COGS: **BDT 0.401**
    - HITL at 12%: **BDT 1.80**
    - **Total: BDT 2.20/script**
14. **HITL sensitivity at a BDT 8.00 price:**

    | HITL review rate | Total COGS (BDT) | Gross margin |
    |---|---|---|
    | 0% | 0.40 | 95.0% |
    | 5% | 1.15 | 85.6% |
    | 12% | 2.20 | 72.5% |
    | 20% | 3.40 | 57.5% |
    | 30% | 4.90 | 38.8% |
    | 50% | 7.90 | 1.3% |

    The HITL rate must stay at or below **12–15%** to keep GM above 70%.
15. **Six-model financial comparison** (100 institutions, 100,000 students, **3,600,000 scripts/yr**, 36 scripts/student/yr):

    | Model | Pricing | Revenue (BDT) | GP (BDT) | GM | CAC (BDT) | 3-yr LTV (BDT) | LTV:CAC | Payback | Break-even |
    |---|---|---|---|---|---|---|---|---|---|
    | Per-script | 8.00/script | 28.8M | 20.88M | 72.5% | 25k | 626,292 | 25.1 | 1.4 mo | 14 |
    | Per-student | 200/student/yr | 20.0M | 12.08M | 60.4% | 20k | 362,292 | 18.1 | 2.0 mo | 22 |
    | SaaS tiers | 120,000/school | 12.0M | 4.08M | 34.0% | 18k | 122,292 | 6.8 | 5.3 mo | 58 |
    | **Hybrid** | 45k + 5/script | **22.5M** | **14.58M** | **64.8%** | **22k** | **437,292** | **19.9** | **1.8 mo** | **18** |
    | Enterprise | 350,000/network | 35.0M | 27.08M | 77.4% | 80k | 812,292 | 10.2 | 3.5 mo | 11 |
    | API | $0.05 (BDT 6)/request | 21.6M | 20.16M | 93.3% | 5k | 604,692 | 120.9 | 0.3 mo | 10 |

    Common COGS: AI/compute **BDT 1,443,600**; HITL **BDT 6,480,000** (zero for the API, where the client handles review); total **BDT 7,923,600**.
16. **Scenarios for the Hybrid model:**

    | Scenario | Institutions | Students | Scripts | HITL rate | Cost/script (BDT) | Revenue (BDT) | COGS (BDT) | GM |
    |---|---|---|---|---|---|---|---|---|
    | Conservative | 30 | 30,000 | 1.08M | 25% | 4.15 | 6.75M | 4.482M (compute 432k + HITL 4.05M) | **33.6%** |
    | Base | 100 | 100,000 | 3.6M | 12% | 2.20 | 22.5M | — | **64.8%** |
    | Aggressive | 250 | 300,000 | 10.8M | 5% | 1.15 | 67.5M | 12.42M (compute 4.32M + HITL 8.1M) | **81.6%** |
17. **CAC by channel:**
    - Direct field sales (Tier 1/2): **BDT 35,000–50,000**
    - PLG (Tier 5): **BDT 8,000–12,000**
    - Channel partners/resellers (Tier 3 and divisional cities): **BDT 15,000–22,000** (20% first-year commission)
    - ERP co-selling (Tier 2/4): **BDT 3,000–6,000** (15% revenue share)
18. **Pricing psychology.**
    - 20% discount for annual prepay versus monthly
    - Per-student framing: BDT 180/student/yr = **BDT 15/student/month**, passed to parents as a "Digital Assessment & Analytics Fee"
    - Good/Better/Best anchoring
19. **Recommended tier card:**

    | Plan | Target | Annual base (BDT) | Included scripts | Overage (BDT/script) |
    |---|---|---|---|---|
    | Starter | Small coaching/tutors | 25,000 | 3,500 | 7.00 |
    | Professional | Medium schools (core) | 65,000 | 10,000 | 5.50 |
    | Enterprise | Large networks | 180,000 | 32,000 | 4.50 |
    | Developer API | EdTech/LMS vendors | 25,000/month | — | 4.00/call |
20. **Payments.** bKash, Nagad and Rocket for credit packs and small bills; bank wire with formal invoice for SMCs; billing aligned with tuition collection in **January and July**.
21. **Pilot protocol.**
    - 1 grade, 1 subject (e.g., Grade 9 General Science)
    - **200 free scripts max**
    - Dual calibration with a senior teacher
    - Sign-off on a time-saved report and "Diagnostic Accuracy Variance (<2.5%)"
    - Auto-convert to an annual Hybrid contract, or deactivate
    - Claimed pilot cost: **200 × BDT 0.40 = BDT 80**
22. **Procurement.** Teacher endorsement (accuracy), then principal approval (turnaround and parent reporting), then SMC sign-off on budget. Per-student-per-month framing is said to ease approval.
23. **API monetization.**
    - **$0.04–0.06 (BDT 4.80–7.20) per evaluated script**
    - Minimum **$250/month (BDT 30,000) including 5,000 calls**
    - GM **>90%**
    - Expansion targets India, SEA and MENA
24. **Integration paths.** A standalone suite for coaching centres, and an embedded RMS/LMS module (e.g., inside Eduman) feeding report cards and parent SMS.
25. **Risk register:**

    | Risk | Probability / Impact | Mitigation |
    |---|---|---|
    | Teacher resistance | H/H | Frame as "AI Teaching Assistant" |
    | API cost inflation | M/H | Self-host open-source LLMs |
    | Seasonal revenue drop | H/M | Mandatory annual subscription |
    | Bangla OCR inaccuracy | M/H | Pre-processing plus HITL |
    | Commodity AI (ChatGPT) | H/M | Workflow/LMS/rubrics |
    | Payment delays | M/M | MFS plus auto-lock access |
26. **Alternative launch scenarios:**
    - A (MVP): prepaid credit packs, **1,000-credit blocks at BDT 8.00/credit**, for coaching and O/A-level exam centres
    - B: Hybrid, **BDT 65,000 base + BDT 5.50/script**, for urban private schools and colleges
    - C: custom enterprise, **BDT 350,000–1,000,000/yr**
    - D: API at **$0.05/call + $250/month commitment**
27. **Pricing experiments:**
    - Gabor-Granger at **BDT 6/8/10/12** per script: start at BDT 10 and step down 15% with **30 coaching centres**
    - Hybrid versus per-student with **20 schools**: BDT 200/student/yr versus BDT 45k + BDT 5/script
    - Pilot cap of **100 versus 250 scripts** across **40 trial accounts**

---

## Quantitative claims table

| Claim | Value | Source cited | Source type | Credibility H/M/L + why |
|---|---|---|---|---|
| Contract checker fee per script | BDT 15–35 (baseline 25) | None specific | Unsourced assertion | **L** — no BD source. Most schools grade internal exams with salaried teachers; per-script honoraria mainly apply to board exams and some coaching centres. |
| Manual checking time | 20–25 min/script | None | Assumption | **M** — plausible for a full Srijonshil paper; the GTM doc uses 15 min. |
| AI audit time | 2–3 min/script | None | Assumption | **L** — unvalidated. It depends on UI and on how many items are flagged. |
| Result turnaround | 14–21 days → 24–48 h | None | Assumption | **L–M** — the baseline is plausible; 48 h ignores scanning logistics. |
| Base software COGS | BDT 0.40/script | Derived | Model | **L** — assumes 4 pages, text-only LLM after OCR, and 2024-era prices. |
| Total COGS at 12% HITL | BDT 2.20/script | Derived | Model | **M** as arithmetic; **L** as a forecast. |
| OCR cost (self-hosted) | BDT 0.24/script (L40S $0.67/h, 1,320 pages/h) | Blog roundups | Secondary web | **L** — no evidence that PaddleOCR/TrOCR read Bangla handwriting adequately. |
| Textract cost | $0.0015/page = BDT 0.72/4 pages | AWS via blogs | Vendor price (secondary) | **M** on price; **[Analyst note]** Textract has no Bangla support to my knowledge, so this figure is irrelevant for Bangla scripts. |
| Google Document AI | $1.50/1,000 pages | Blogs | Vendor price (secondary) | **M** |
| GPT-4o-mini price | $0.15/$0.60 per M tokens | GetDeploying/G2 blogs | Secondary | **M** (was the list price) — stale model choice as of 2026. |
| Gemini 1.5 Flash price | $0.075/$0.30 per M | Blog | Secondary | **L** for current use — 1.5-series models are superseded. |
| "DeepSeek V4 Flash" price | $0.14/$0.28 per M | None | Unverified | **L** — model name and price not verified here. |
| LLM tokens per script | 1,800 in / 400 out | None | Assumption | **L** — 400 output tokens is too few for per-part scores and feedback on a multi-question paper. |
| HITL reviewer fee | BDT 15/script reviewed | None | Assumption | **L–M** |
| HITL rate target | 12% (5–25% in scenarios) | None | Assumption | **L** — no accuracy data behind it. |
| GM at BDT 8 & 12% HITL | 72.5% | Derived | Model | M (arithmetic correct) |
| Hybrid revenue, 100 institutions | BDT 22.5M | Derived | Model | **L** — **arithmetic error** (see Critical assessment). |
| Hybrid GM | 64.8% | Derived | Model | L–M |
| Blended CAC (hybrid) | BDT 22,000 | None | Assumption | **L** — conflicts with the same doc's field-sales CAC of 35–50k. |
| 3-yr LTV (hybrid) | BDT 437,292 | Derived | Model | **L** — assumes zero churn and no discounting. |
| LTV:CAC | 19.9:1 (range 6.8–120.9) | Derived | Model | **L** |
| CAC payback | 1.8 months | Derived | Model | **L** |
| Segment counts | 350+ / 2,500+ / 1,200+ / 18,000+ / 100,000+ | None | Unsourced | **L** — EM count conflicts with the GTM doc (123–168); MPO ~18,000 is roughly consistent with BANBEIS. |
| Segment EdTech budgets | BDT 20k–1.5M | None | Unsourced | **L** |
| CoGrader price | $15–19/teacher/mo, 350 submissions | cograder.com | Vendor page | **M–H** (check current) |
| Gradescope | $3–7/student/yr | classpoint/GPTZero blogs | Secondary | **M** |
| Crowdmark | $3–6/student/course | Blog | Secondary | M |
| ZipGrade | $6.99/teacher/yr | Blog | Secondary | M |
| Eduman | BDT 5–10k setup + BDT 70–100/student/yr | edumanbd.com | Vendor page | **M–H** |
| MockExam.bd | BDT 299/paper | Vendor site | Vendor page | M — consumer O/A-level niche, not institutional. |
| Seasonal peaks | 10× (May–Jun), 12× (Nov–Dec) | None | Assumption | **L–M** — the direction is right; multipliers are unsourced. |
| Scripts per student per year | 36 (6 exams × 6 subjects) | None | Assumption | L–M — GTM uses 24 and 48. |
| Pilot cost | BDT 80 for 200 scripts | Derived | Model | **L** — excludes HITL, calibration labour, travel and scanning. |
| Pilot → contract conversion | >60% | None | Assertion | L |
| API price | $0.04–0.06/script; $250/mo incl. 5,000 calls; also BDT 25,000/mo + BDT 4/call | None | Assumption | **L** — three inconsistent API price cards. |
| Reseller commission | 15–20% (also "15–25%" haircut; 20% first-year) | None | Assumption | M (typical) |
| ERP rev-share | 15% | None | Assumption | M |
| FX | 1 USD = 120 BDT | None | Assumption | M — roughly current. |

---

## Buyer / decision maker / user / payer analysis

| Segment | User | Buyer | Approver | Beneficiary | Influencer / Blocker |
|---|---|---|---|---|---|
| Tier 1 international | Subject teachers, dept heads | Head of School / Principal | Board of Trustees | Students, parents | IT admin (blocks if integration fails) |
| Tier 2 urban private | Class teachers, exam committee | Principal / VP | Governing Body / SMC | Management, students | Senior teachers (tech hesitancy) |
| Tier 3 coaching | Branch tutors, evaluators | MD / Founder | CFO | Branch ops, students | **Part-time checkers (block because of fee loss)** |
| Tier 4 suburban/MPO | Assistant teachers | Headmaster | SMC Chairman | Teachers, headmaster | Local IT vendors |
| Tier 5 tutors | Tutor | Self | Self | Tutor, tutees | Parents |

- **Payer.** Not separated from buyer. The doc implies the institution pays, and suggests the cost can be **passed to parents** as a BDT 15–20/month "Digital Assessment Fee". **[Analyst note]** In MPO schools, government gazettes regulate fees (see E3). A new parent-facing fee line may not be permissible or politically easy there. This needs validation.
- **Procurement path:** teacher endorsement, then principal, then SMC budget sign-off.
- **[Analyst note]** One blocker is under-weighted. In coaching centres, the part-time checkers whose income disappears are also the likely HITL workforce. In schools, teachers may lose exam-checking honoraria where they exist. The product therefore has to position reviewers as retained participants.

## Pricing model(s) proposed

- **Primary:** Hybrid annual base with script allowance and overage.
  - Card 1: BDT 45,000 incl. 6,000 scripts + BDT 5.00 overage.
  - Card 2 (tiers): Starter BDT 25,000 / 3,500 scripts / BDT 7.00; Professional BDT 65,000 / 10,000 / BDT 5.50; Enterprise BDT 180,000 / 32,000 / BDT 4.50.
  - Card 3 (Scenario B): BDT 65,000 base + BDT 5.50.
- **MVP alternative:** prepaid credit packs at **BDT 8.00/script** in 1,000-credit blocks.
- **Per-student:** **BDT 180–250/student/yr** (model uses BDT 200).
- **Enterprise:** **BDT 350,000–1,000,000/yr** (Model I says ACV >BDT 500k).
- **API:** $0.04–0.06/script (BDT 4.80–7.20), $250/mo minimum incl. 5,000 calls; or BDT 25,000/mo + BDT 4.00/call; or $0.05/call.
- **Freemium:** 30 scripts/month (scored low; mentioned for PLG).
- **Free pilot:** 200 scripts (experiment: 100 vs 250).
- **Effective per-script price implied by tiers:** Starter ≈ BDT 7.14, Professional ≈ BDT 6.50, Enterprise ≈ BDT 5.63. The value model uses "BDT 6.00/script equivalent".

## Unit economics & cost assumptions (every assumption stated)

| Assumption | Value |
|---|---|
| Script length | **4 handwritten pages** (Srijonshil creative format) |
| Handwritten text tokens | ~**1,600** per 4 pages |
| System prompt + answer key + rubric | ~**800** tokens; prompt caching cuts repeated rubric tokens by **50–80%** |
| Effective LLM input | **1,800** tokens (after caching) |
| LLM output | **400** tokens |
| LLM | **GPT-4o-mini** at **$0.15/M input, $0.60/M output**, giving $0.00027 + $0.00024 = **$0.00051 ≈ BDT 0.061/script** |
| OCR, cloud option | AWS Textract **$0.0015/page = BDT 0.72/script**; Textract forms/tables **$0.015/page**; Google Document AI **$1.50/1,000 pages** |
| OCR, chosen option | Self-hosted **PaddleOCR/TrOCR** on **L40S spot at $0.67/h**, **~1,320 pages/h**, giving **~$0.0005/page ≈ BDT 0.06/page = BDT 0.24/script** |
| Infra/storage | S3 image compression + DynamoDB = **BDT 0.10/script** |
| Base software COGS | **BDT 0.401/script** |
| HITL trigger | Confidence **<85%** or flagged |
| HITL reviewer | Paid **BDT 15/script reviewed** |
| HITL rate | **12%** base (25% conservative, 5% aggressive) |
| Effective COGS | **BDT 2.20** (base); **4.15** (25%); **1.15** (5%) |
| Scripts per student per year | **36** (6 exam cycles × 6 subjects) |
| FX | **1 USD = 120 BDT** |
| Automated processing time | **30 s/script** |
| LTV | **3 years of gross profit, no churn, no discount rate** |
| Break-even client volume | Stated (14/22/58/18/11/10) with **no fixed-cost base disclosed** |
| API model | Client handles HITL, so HITL cost = 0 |
| Not modelled at all | Scanning labour and hardware; customer success/onboarding labour; payment processing fees; VAT/tax (**[Analyst note]** BD software VAT/AIT not addressed); failed/re-scanned pages; multi-model verification passes; engineering/R&D; Bangla-specific model training |

**Key structural insight (from the doc's own numbers).** Human review is **82%** of the base-case COGS (BDT 1.80 of 2.20). AI compute is a rounding error by comparison. Gross margin is therefore driven almost entirely by the flag/review rate, not by LLM price.

## GTM: beachhead, sales process, pilot design, onboarding, customer success, channels

- **Beachhead.** Commercial coaching centres and O/A-level exam centres for the MVP (credit packs). Coaching plus private English- and Bangla-medium schools for the initial Hybrid. Urban private schools/colleges for the growth phase.
- **Sales process:** teacher validation in pilot, then principal, then SMC. Framing is per-student-per-month.
- **Pilot:** 1 grade × 1 subject; ≤200 free scripts; senior-teacher dual calibration; time-saved report plus a variance <2.5% target; auto-convert or deactivate.
- **Channels:**
  - Direct field sales (Tier 1/2; CAC BDT 35–50k)
  - PLG for tutors (BDT 8–12k)
  - Resellers in Chittagong/Rajshahi/Sylhet (BDT 15–22k; 20% first-year commission)
  - ERP co-sell with Eduman and Campus360 (BDT 3–6k; 15% rev share)
- **Onboarding / customer success.** Not specified beyond the pilot. There is no CS cost line in the model.
- **Expansion:** RMS embedding, parent video diagnostics (+30% premium under consideration), API for India/SEA/MENA.

## Assumptions

1. Institutions pay cash for script checking today, or will value teacher time as cash.
2. A 4-page script is representative.
3. OCR plus a text LLM pipeline is adequate for Bangla handwriting, diagrams and math.
4. A 12% HITL rate is achievable at launch.
5. Customers accept annual prepaid contracts plus overage billing in peak months.
6. Schools can pass fees to parents.
7. There is no churn over 3 years.
8. The customer mix is uniform: 1,000 students per institution.
9. ERP vendors will co-sell for a 15% share.
10. LLM prices stay flat or fall; self-hosting is the hedge.
11. Teachers accept "AI Teaching Assistant" framing.
12. Pilot conversion is above 60%.

## Recommendations (as made by the doc)

1. Launch with Hybrid (base + allowance + overage), or credit packs for coaching MVPs.
2. Require an upfront annual floor to beat seasonality.
3. Keep HITL at or below 12–15%.
4. Run bounded 200-script free pilots with auto-conversion gates.
5. Frame price per student per month for SMCs.
6. Offer MFS plus bank invoice and bill in Jan/Jul.
7. Build the ERP co-sell channel for low CAC.
8. Later, release the Assessment API for international scaling.
9. Run the three pricing experiments (Gabor-Granger, Hybrid vs per-student, pilot cap).

## Open questions

- **Raised by the doc:** At what volume do self-hosted fine-tuned models beat hosted APIs? How does WTP shift in India, Nepal and Vietnam? Do video parent reports justify a 30% premium?
- **[Analyst note] Additional:**
  1. What is the real page count per script by exam type (class test vs term final vs model test)?
  2. What auto-grade accuracy on Bangla handwriting is achievable, and hence what flag rate?
  3. Who performs HITL: vendor-paid reviewers or the customer's own teachers? The doc does both, inconsistently.
  4. Do Bangladeshi schools actually pay per-script checking fees for internal exams?
  5. Is overage billing collectible from SMC-governed institutions?
  6. What is the scanning workflow, and who bears its cost?
  7. What fraction of coaching-centre tests are MCQ/OMR (already cheap) versus written?
  8. What are data-protection obligations for minors' exam data?

---

## Critical assessment

1. **Arithmetic error in the recommended model's revenue.** At 100 institutions × 36,000 scripts under "BDT 45k base incl. 6,000 scripts + BDT 5 overage", correct revenue is 45,000 + 30,000 × 5 = **BDT 195,000/institution = BDT 19.5M**, not 22.5M. The doc charged overage on all 36,000 scripts and ignored the included allowance. The scenarios use a flat **BDT 6.25/script** (22.5M/3.6M = 6.75M/1.08M = 67.5M/10.8M), which is also inconsistent with the stated tier cards. Corrected hybrid GM at base ≈ (19.5M − 7.92M)/19.5M ≈ **59%**, not 64.8%.
2. **LTV is not an LTV.** It is 3 years of gross profit with **zero churn** and no discounting. The per-script model's "25.1:1" and the API's "120.9:1" are artefacts. The CAC used (BDT 22k blended) is below the doc's own direct field-sales CAC (BDT 35–50k), yet the beachhead is sold via field sales.
3. **Pilot cost of BDT 80 is unrealistic.** It counts only BDT 0.40 software COGS × 200. It omits HITL (12% × BDT 15 × 200 = BDT 360 at minimum), senior-teacher calibration, rubric set-up, travel, scanner provisioning and CS time. **[Analyst note]** The realistic pilot cost is plausibly in the tens of thousands of BDT in staff time. The GTM doc's scanner alone is BDT 45,000.
4. **Stale and likely non-viable LLM/OCR assumptions.**
   - GPT-4o-mini and Gemini 1.5 Flash are 2024-generation models; "DeepSeek V4 Flash" is unverified. All prices come from secondary blogs.
   - More important than price: the pipeline assumes OCR then text-only LLM. **[Analyst note]** Off-the-shelf PaddleOCR/TrOCR and Textract are not known for usable *Bangla handwriting* recognition, and Textract does not support Bangla. A realistic pipeline probably needs multimodal vision-LLM page reading or a custom Bangla HTR model. Either changes COGS materially: image tokens per page, more output tokens for per-part rationales, possibly two-pass verification. The BDT 0.061 LLM cost could be understated by **one to two orders of magnitude**, and still stay under BDT 1–6 depending on model tier.
   - Must be re-benchmarked with current 2026 prices and actual Bangla-handwriting accuracy.
5. **4-page script assumption.** **[Analyst note]** A full Srijonshil term-final paper (e.g., 7 creative questions × 4 sub-parts) commonly runs well beyond 4 pages. Class tests may be 1–4 pages. Cost per script should be modelled per page with a distribution, not fixed at 4.
6. **HITL is the real cost driver and is double-counted or mis-assigned.**
   - The unit-economics section makes HITL a vendor COGS (BDT 15/review, 12%).
   - The customer value model *also* charges the customer BDT 77,760 for HITL.
   - The value table assumes **every** script gets a 2-minute teacher audit.
   - Three incompatible HITL designs. The product must decide who reviews (see E0).
7. **Customer savings rest on a questionable cash baseline.** The "BDT 1,080,000 direct checking outlay" assumes schools pay contract checkers BDT 15–35/script for internal exams. **[Analyst note]** In most Bangladeshi schools, internal scripts are checked by salaried teachers, so savings are time, not cash. The ERP doc itself (E3) warns that "staff reduction" pitches create resistance. The cash-savings case is more plausible for coaching centres that pay external evaluators, and that is not evidenced here either.
8. **Segment counts and budgets are unsourced.** "350+" international/EM schools conflicts with the GTM doc's 123–168 formal EM schools (the ERP doc says 137 formal plus ~1,000 unlisted). "1,200+ coaching" versus GTM's "150+ networks" and "Top 10 (~500 branches)". The EdTech budgets (e.g., Tier 4 BDT 20–80k) have no citation.
9. **Internal contradictions.**
   - Hybrid base: BDT 45k/6,000 scripts versus Professional BDT 65k/10,000 versus Scenario B BDT 65k + 5.50.
   - API: three different price cards.
   - Per-student: BDT 180–250 versus model BDT 200 versus "BDT 180 = BDT 15/month".
   - Billing months: Jan/Jul versus "January Annual Base Collection".
   - GM target >70% (exec) versus base case 64.8%.
   - Reseller cut 15–20% versus 15–25%.
   - "85% teacher time recovery" versus the value model's 12,000 of 14,400 hours ≈ 83–90%.
10. **Seasonality contradicts the margin story.** Overage revenue concentrates in 2–3 peak months, but so do HITL reviewer demand and GPU load. A 10–12× peak in HITL means hiring or contracting reviewers seasonally. That is not modelled and is a real operational risk.
11. **Missing Bangladesh-specific evidence.** There are no interviews, no LOIs, no observed WTP, no data on how many institutions scan papers, no internet or scanner penetration data, no data on current per-script honoraria, and no regulatory review (fee caps, data protection). The only BD pricing anchors are Eduman (ERP) and MockExam.bd (a consumer niche).
12. **Framing risk.** "Pass cost to parents" may collide with government fee-regulation gazettes for MPO institutions (E3).

## Confidence + Relevance to product decisions

- **Confidence in the doc's numbers: Low–Medium.** Structural logic is sound: script as value metric; annual floor for seasonality; HITL rate as the margin lever; ERP co-sell as a cheap channel. Most quantities are unsourced assumptions, one headline figure is arithmetically wrong, and the AI cost basis is stale and technically doubtful for Bangla handwriting.
- **Relevance: High** for these product decisions:
  - (a) Instrument **cost per page and per script** and the **flag/review rate** as first-class metrics.
  - (b) Design the review UI so the **customer's own teachers** do HITL, not vendor-paid reviewers, or explicitly price HITL.
  - (c) Build for **batch, seasonal peaks** of 10–12× baseline.
  - (d) Price-anchor range is roughly **BDT 5–8/script** for premium or coaching segments; E0 argues mainstream schools need far lower.
  - (e) Plan an **API/white-label** surface for ERP partners early.
