# E0 — Cross-notes: contradictions across E1/E2/E3 and commercial constraints on product design

**Inputs:**
- E1: Business Model doc, `1z4jFoRJ…`
- E2: GTM doc, `1Xini8KX…`
- E3: adjacent ERP pricing doc, `1n4V51Ol…`, used for context only

All three were read in full. All three look like AI deep-research outputs: confident, precise-looking figures, few primary sources, and **no customer interviews, pilots or measured accuracy data**. Anything marked **[Analyst note]** is my judgement, not a claim from the documents.

---

## 1. Contradictions between the documents

| Topic | E1 Business Model | E2 GTM | E3 ERP (context) | Comment |
|---|---|---|---|---|
| **Per-script price** | BDT 8.00 (per-script and credit packs). Overage BDT 4.50–7.00. Hybrid effective ≈ BDT 5.6–7.1. Value model uses "BDT 6.00 equivalent". Gabor-Granger test at BDT 6/8/10/12. | **BDT 8–15**. Standard **BDT 10**. | n/a | E2's floor is at E1's ceiling. Neither has WTP evidence. |
| **Per-student price** | BDT 180–250/yr (model uses 200) | BDT 180–300/yr | A whole ERP costs **BDT 42–60/student/yr** (core tiers). Competitors charge BDT 5–10/student/month (60–120/yr). Eduman charges BDT 70–100/yr (per E1). | The AI-grading per-student price is 3–7× what mainstream schools pay for an entire ERP. |
| **Base fee** | BDT 45k (incl. 6,000 scripts) **or** 65k (incl. 10,000) **or** tiers of 25k/65k/180k | Enterprise base **BDT 50k** | ERP core base BDT 15k–25k | E1 contradicts itself. |
| **ACV per customer** | ~BDT 195–225k (1,000 students). Enterprise BDT 350k–1M. | **BDT 750k–1.2M** (2,000 students) | Mainstream ERP 40–65k. Elite EM 350k. | E2's ACV exceeds what elite EM schools pay for their whole ERP. |
| **CAC** | Blended **BDT 22k**. Field sales 35–50k. ERP co-sell 3–6k. | Field **BDT 150k**. Founder 65k. ERP 45k. Inbound 210k. | Blended **BDT 14.5k**. Field 18k. | About a 10× spread. E2's CAC and ACV are both about 5× E1's. |
| **LTV basis** | 3 years of gross profit, zero churn | 4-year retention, zero churn | 7.5% churn formula | None of the documents uses measured churn. |
| **Gross margin** | 64.8% base with HITL. Arithmetic error; corrected ≈ 59%. Range 33.6–81.6%. | "Software GM 82%" (no HITL). KPI ≥80%. | ERP 78–82% | E2 ignores the cost of human review. E1 shows human review is 82% of COGS. |
| **Scripts per student per year** | 36 (6 exams × 6 subjects) | 24 (6 × 4) for SAM/SOM, 48 (6 × 8) for ROI | Tabulation: 3 exam cycles/yr | This input drives both revenue and COGS, and nobody measured it. |
| **Manual / AI time per script** | 20–25 min / 2–3 min | 15 min / 3 min | Tabulation: 35 h per teacher per cycle | |
| **Beachhead** | MVP: **coaching centres + O/A-level exam centres** (credit packs). Then urban private schools. | **Dhaka private English-version + elite Bangla-medium schools + admission coaching chains**. Exec summary says "English-medium". First 5 customers: EM/elite schools. | Recommended ERP target: semi-urban/urban non-MPO private schools, 500–1,500 students | E1 leads with coaching; E2 leads with EV/EM schools. Both include coaching. |
| **Pilot** | **Free, 200 scripts**, 1 grade × 1 subject. Cost "BDT 80". Target variance <2.5%. Auto-convert. | **Free, 14 days, 500–1,500 scripts** (or 500–1,000), 2 subjects, loaned scanner, signed commitment. Gates: ≥90% agreement, >60% time saved. Coaching proof of concept: 2,000+ scripts. | **Paid BDT 5,000**, credited; 1 grade, 1 terminal exam | Free vs paid, and a 200 vs 1,500 script cap. E3 argues free trials fail in Bangladesh. |
| **Freemium / PLG** | Free 30 scripts/month (scored low). PLG CAC BDT 8–12k. | "Not recommended", yet specifies a free tier of 25 scripts/month | "Avoid freemium" | |
| **Billing cadence** | Annual prepay (20% discount vs monthly). Billing aligned with **Jan & Jul**. | Annual contracts. Risk table suggests "flat monthly subscription fees". Bank/cheque payment. | **Annual upfront, invoice Dec 1, due Jan 15. Monthly is unviable.** Bi-annual allowed with a 5% surcharge. | |
| **Payment rails** | bKash/Nagad/Rocket for small buyers; bank wire and invoice for SMCs | Bank transfer / cheque; no cards | Joint-signature bank cheque via the head clerk | Institutions pay by cheque or bank; MFS is only for tutors and small buyers. |
| **Partner rev-share** | ERP 15%. Reseller 15–20% (also "15–25%"). 20% first-year commission. | ERP 15–20% recurring. Reseller 15–20% recurring. Association 20% discount. | Reseller 15% of Year-1 | Rough consensus: **15–20%**. |
| **ERP partners named** | Eduman, Campus360 | Edufy, Eduzone, Aamra EduManager | Smart Software, MSMHS, EduGradUP, Shebashikkha, etc. | No overlap between E1 and E2. None of the partners has been validated. |
| **Institution / student counts** | EM Tier 1 "350+"; coaching "1,200+"; MPO "18,000+" | 36,940 institutions (its components sum to 35,595); 18.2M students; EM 123–168; 150+ coaching networks | 36,710 institutions; 20.2M students; EM 137 formal + ~1,000 unlisted | Use the BANBEIS primary source directly and do not rely on any of these. |
| **HITL design** | Vendor-paid reviewers at BDT 15/review for 12% of scripts. **Also** charges the customer BDT 77,760 for HITL. **Also** a 2-minute teacher audit on every script. | Mandatory teacher review of low-confidence items and teacher sign-off | n/a | Three incompatible designs. The product must choose one (see §3). |
| **API pricing** | $0.04–0.06/script **or** BDT 25k/month + BDT 4/call **or** $0.05/call + $250/month | "REST APIs" for ERP sync; no price | n/a | |
| **OCR approach / accuracy** | Self-hosted PaddleOCR/TrOCR, or Textract. No accuracy figure. | "~88% native Bangla handwriting ICR". Baseline OCR ≥88% within 30 days. | n/a | [Analyst note] Textract does not support Bangla. 88% character accuracy is not grading accuracy. |
| **TAM/SAM/SOM** | None | TAM $7.05B (global AI in education) or $1.85B regional. SAM $18.4–28.2M. SOM $1.2–2.1M ARR. | 1,000 institutions ≈ BDT 66M ERP revenue | E2's sizing is built from assumptions, not research. |

**Arithmetic and internal errors found:**
- E1's Hybrid revenue ignores the included allowance. The correct figure is BDT 19.5M, not 22.5M.
- E2's component institution counts don't sum to its stated total.
- E2's payback figures mix revenue and gross-profit bases.
- E2 plans 10 paid customers in 90 days, but its own founder capacity is 2 pilots per month.
- E1's pilot cost excludes review and staff time.

---

## 2. Where the documents agree (more trustworthy signals)

1. **The value metric is the evaluated script.** An **annual prepaid floor** is required because exam volume is extremely seasonal. Peaks are May–Jun and Nov–Dec, with a secondary peak in Sep–Oct. E1 puts peaks at 10–12× the base.
2. **Buying authority** sits with the owner, MD, principal and SMC/Governing Body. Teachers are users and potential blockers. The payer is the institution, paying annually by cheque or bank transfer.
3. **Sales are relationship-led and in person.** A live demo on the school's own scripts is the key proof. Pilots must be time-boxed, capped and tied to a conversion commitment.
4. **ERP/RMS vendor co-selling** is the lowest-CAC scale channel, at about a 15–20% revenue share.
5. **Human-in-the-loop with confidence flags** is both the trust mechanism and the main cost lever.
6. **Position the product as a teacher's assistant, not a replacement.** Never pitch headcount reduction.
7. **Buying calendar:** budgets and cash peak in **Nov–Jan**. The pain and pilot window is the **May–Jun half-yearly** and Sep–Oct test exams.

---

## 3. Top commercial insights that should constrain the product and technical design

### 3.1 Maximum acceptable cost per script, derived from the documents' own anchors

**Mainstream schools (urban MPO / private, ~1,000 students)**
- Total software budget is roughly **BDT 45–65k/yr** for a *whole ERP* (E3). Principals may self-approve around **≤BDT 25–35k/yr**.
- At 24–36 scripts per student per year (24,000–36,000 scripts), even spending the entire ERP-sized budget on grading gives about **BDT 1.25–2.70 per script** in revenue.
- At a ≥70% gross margin, **fully loaded COGS must be ≤ BDT 0.4–0.8 per script** (≈ **$0.003–0.007**).
- [Analyst note] That leaves no room for vendor-paid human review (BDT 15/review). The mass market is only reachable if the **customer's own teachers do the review** and the AI flag rate is low. A likely route is bundling through ERP partners.

**Premium EM/EV schools and coaching centres**
- Price anchors are **BDT 5–10 per script** (E1 BDT 5.6–8; E2 BDT 8–15).
- At ≥70% gross margin, **COGS must be ≤ BDT 1.5–3.0 per script** (≈ **$0.012–0.025**).
- If vendor-paid review is included (BDT 15 each) with compute around BDT 0.4–1.0, the **review/flag rate must stay ≤ ~5–10%**.

**Per page**
- [Analyst note] Real scripts are likely 4–16+ pages. E1 assumes 4.
- At 8 pages, the budget is roughly **≤ BDT 0.05–0.10 per page** for mainstream schools and **≤ BDT 0.19–0.37 per page** for premium.
- **Cost should be modelled and metered per page, not per script.**

**Inference model tier (illustrative only)**
- [Analyst note] The price bands below are hypothetical ranges, **not verified current prices**. Re-benchmark before deciding.
- Assume a vision-LLM reads ~8 page images directly (~10–12k input tokens) and writes ~2k output tokens of per-part scores and rationale.
- A **small-tier model** (~$0.1–0.3/M input, ~$0.4–2.5/M output) costs about **$0.002–0.011 ≈ BDT 0.2–1.3 per script**. This fits premium segments and may just reach the mainstream ceiling.
- A **mid/frontier-tier model** (~$1–3/M input, ~$5–15/M output) costs about **$0.02–0.08 ≈ BDT 2.4–9.7 per script**. This breaks the mainstream ceiling and consumes most of the premium margin.
- **Design implication:** use a routing/cascade. A cheap model handles the default path; escalation to a stronger model or human review happens only on low confidence. Rubric and answer-key prefixes are cached, pages are batched, and cheap classical OMR/MCQ handling is used wherever possible.

### 3.2 Human review design dominates the economics
- In E1's own base case, human review is BDT 1.80 of BDT 2.20 COGS (**82%**). Gross margin runs from 95% at 0% review to 1.3% at 50% review.
- **Requirements:**
  - (a) A calibrated per-question and per-part **confidence score**
  - (b) A configurable **flag threshold** exposed as a cost/accuracy dial
  - (c) A **fast teacher review UI** (target ≤2–3 minutes per flagged script, per E1/E2)
  - (d) Default reviewers are the **customer's teachers**, not vendor staff
  - (e) Logging of **override rate** (<10% target) and **AI–teacher agreement** (≥90%, E2), with explicit definitions such as exact match vs ±1 mark, per part vs total
- **Seasonal elasticity:** vendor-side reviewers would need to scale 10–12× in May–Jun and Nov–Dec. This is another reason to avoid vendor-paid review for the core offering.

### 3.3 Seasonality means batch throughput, not steady-state
- Architect for **burst batch processing** at 10–12× baseline. Use queueing, serverless or spot GPUs, and priority lanes for result deadlines.
- Keep costs near zero in idle months. Commercially this pairs with annual prepay and allowances plus metered overage, **never unlimited plans**. E3's "unlimited SMS" lesson maps directly onto AI inference.

### 3.4 Demo and pilot drive the sale, so build for them first
- **Live demo:** scan about 5 physical scripts and show segmentation, rubric scoring with partial credit, and a report card within about 7 minutes. That implies **roughly ≤60 seconds per script end-to-end in demo mode** and robust capture from both a feed scanner and a phone.
- **Pilot kit:**
  - Parallel-marking import (teacher marks vs AI marks)
  - An automatic **agreement / time-saved / turnaround report** for the owner or SMC
  - Rubric set-up in under a day
  - Handles 200–1,500 scripts across 1–2 subjects within 14 days
- **Commercial default:** follow E3 and make the pilot **paid and credited** (≈BDT 5,000), timed to the **May–Jun half-yearly** exam. The documents disagree here, so treat it as an experiment.

### 3.5 Distribution through ERPs means API-first
- The cheapest channel (ERP co-sell, CAC BDT 3–45k) and the mass-market budget constraint both point to an **embeddable grading API plus mark export** into RMS/ERP systems (Edufy, Eduzone, Aamra, Eduman and others).
- Build **multi-tenant, partner-scoped** accounts and **per-script and per-page metering** from day 1 so that partner billing and revenue share can be supported.

### 3.6 Payment and packaging constraints
- Institutions pay **annually by cheque or bank transfer** (invoice Dec 1, due Jan 15). **MFS** (bKash/Nagad) is for tutors and small coaching centres. Card payments are irrelevant.
- The billing system needs:
  - Offline invoices, manual payment reconciliation, and grace or auto-lock states
  - Allowance tracking with overage alerts, which matter because peak-month overage is where both revenue and cost land
  - Enrollment or script bands reconciled once a year
- Avoid per-teacher-seat pricing. E3 reports that per-seat pricing leads to shared logins, which undermines audit trails. This matters for grading, where the audit trail of who approved which mark is itself part of the product's value.

### 3.7 Segment and language sequencing
- **Beachhead overlap:** Dhaka private English-version/EM schools plus *written-test* coaching programmes.
- [Analyst note] Before committing to coaching, verify how much of its volume is written rather than MCQ/OMR. Much admission-prep testing is MCQ.
- **English handwriting first; Bangla handwriting (Srijonshil) next.** Bangla is required to reach Tier 2 and MPO schools, but it is the unproven, high-risk capability. No document provides production evidence for it. E2's "~88%" is character-level recognition, not grading accuracy.
- **MPO/rural** schools come later and via partners. Their budgets are BDT 15–25k per year, their decisions are slow (120–180 days), and fee caps limit any pass-through to parents.

### 3.8 Trust, privacy and data residency
- E2's objection handling promises **no training on student data**, encryption, and local or on-prem options. Treat these as product requirements or remove them from the pitch.
- Using a foreign LLM API with minors' exam scripts needs a clear data-processing position.

---

## 4. What to validate before building to these numbers

1. **Page count per script** by exam type, sampled from real schools.
2. Current **per-script checking honoraria**: does anyone pay cash for internal exam marking? This determines whether the pitch is hard savings or soft savings.
3. **Share of written vs MCQ** tests in coaching centres.
4. **Achievable auto-grade agreement and flag rate** on English and Bangla handwriting, using current 2026 models and prices.
5. **Willingness to pay**, through real price tests: E1's Gabor-Granger at BDT 6/8/10/12, and the hybrid vs per-student test.
6. **Principal self-approval threshold** and SMC timing.
7. **ERP partner appetite** and acceptable revenue share.
8. **Scanner availability**, and whether phone capture is sufficient.
