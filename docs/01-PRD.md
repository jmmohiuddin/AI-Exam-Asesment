# 01 — Product Requirements Document (PRD)

| Field | Value |
|---|---|
| Document Name | PRD — AI-Assisted Exam Script Marking Platform for Bangladesh (working name: **"Khata"**) |
| Version | 1.0 |
| Status | Baseline for Phase 0 (validation) and Phase 1 (MVP build). Items marked *provisional* depend on named experiments. |
| Date | 2026-09-27 |
| Owner | Chief Product Officer |
| Purpose | Defines **what** the product does and **why**: users, scope, MVP, requirements with acceptance criteria, success metrics, commercial model and roadmap. |
| Source Research | `00-research-synthesis.md` (S01–S15, V1, V2; VF-, EV-, CON- IDs) |
| Dependencies | `10-registers.md` (DEC-, ASM-, RSK-, EXP-, OQ-); implemented by `02-TRD.md`, `03-system-design.md`; detailed by `06`, `07`, `08`; UX in `04`, `05` |

> Working name: "Khata" (খাতা = answer script). Branding is a separate decision.

---

## 1. Executive Summary

**Problem.** Bangladeshi secondary teachers mark thousands of handwritten, board-format (CQ + MCQ) answer scripts every term, then copy marks by hand through cover sheets, mark slips, Excel and ERPs before results can be published (EV-03). Marking quality has become a national issue. The SSC 2026 full re-evaluation changed 27,836 grades, and mis-marking public exams is now a criminal offence (VF-08). No product grades handwritten Bangla-script answers (VF-23). The research also shows that fully autonomous AI grading is neither accurate enough nor acceptable (VF-18, VF-12, VF-13).

**Product.** A marking workspace for **school internal exams**:

1. Teachers set up the paper and a rubric from NCTB-format templates.
2. Scripts are captured with an Android phone, using a QR cover sheet printed per student.
3. The platform reads each answer and, where proven reliable, **suggests criterion-level marks with visible evidence**.
4. **Teachers confirm or correct every mark**, question by question.
5. Totals, pass rules, GPA, tabulation sheets and report cards are computed deterministically.

Each AI capability is switched on per subject, question type and script language **only after it passes an evaluation gate** (support levels L0–L3, DEC-04). The product therefore delivers value even when AI is off: no re-copying of marks, no arithmetic errors, faster results.

**MVP.** Private urban secondary schools in Dhaka; Grades 9–10; **General Mathematics and Physics**; Bangla-medium and English-version; class tests, half-yearly, annual and test exams. Bangla handwritten prose is shown as evidence only (L1) until proven (DEC-21).

**Plan.** Phase 0 validation experiments come first, because no primary research exists yet (Oct 2026–Jan 2027): legal opinion, human-agreement baseline, model bake-off on real scripts, capture time-motion, buyer interviews. The MVP is built in parallel. The pilot runs on the half-yearly exams (May–Jul 2027). Production launches for the annual exams (Nov–Dec 2027).

**Success.** Pilot schools cut teacher minutes per script by ≥30% (marking + totalling + entry) and tabulation time by ≥80%. They publish results ≥5 working days sooner. AI-suggested marks meet their per-cell agreement gates, and severe unflagged errors stay ≤0.5% of audited items.

---

## 2. Problem Statement

| # | Problem | Who feels it | Evidence | Confidence |
|---|---|---|---|---|
| P1 | Marking handwritten CQ scripts is slow. A teacher marks hundreds of scripts per term alongside teaching. | Subject teachers | S01, S02 (modelled); VF-09 (board examiners: 300–600 scripts in 10–20 days) | M (internal-exam time not measured: OQ-01) |
| P2 | Marks are copied by hand 3–5 times, causing summation, transcription, row-shift and component-rule errors, rework and disputes. | Teachers, exam coordinators, ICT/office staff | S02, S03 (qualitative convergence) | M |
| P3 | Marking is inconsistent across teachers and over a long marking session. No evidence trail exists for disputes. | Students, parents, principals | VF-08 (board scale); S02 (English essay variance, unverified) | H (board) / M (internal) |
| P4 | Results take 2–4 weeks. Students get totals, not item-level feedback. | Students, parents, principals | S01, S02, S11 (unmeasured) | M |
| P5 | Existing tools don't help. ERPs handle only mark entry and tabulation (after manual marking). Global AI graders don't handle Bangla handwriting, the CQ format, or Bangladeshi school workflows. | Schools | VF-16, VF-23; S12 | M–H |

**Problem we are NOT solving:** board (SSC/HSC) marking, question-paper leaks, fee collection, attendance, learning content, homework platforms.

---

## 3. Opportunity

- **Market:** ~16,600 secondary schools, ~97% non-government, plus 4,900 colleges and 9,300 madrasahs; 293k secondary teachers (VF-10). Target segment initially: private schools in Dhaka with premium tuition (count to be built in Phase 0; no verified figure).
- **Why now:**
  - (1) The 2026 marking crisis and the new law make consistency and evidence valuable (EV-01).
  - (2) The 2012-format CQ/MCQ assessment has been restored (VF-01), and schools now set board-format papers internally (VF-06).
  - (3) Multimodal models have become capable and cheap enough to make assisted marking feasible for numeric/English work (VF-17, VF-21).
  - (4) Nobody serves Bangla-script handwritten marking (VF-23).
- **Why us / right to win (to be earned, not assumed):**
  - depth in the Bangladeshi CQ workflow;
  - trust architecture (teacher authority, evidence, audit);
  - a consented local dataset built with design partners;
  - school relationships.

  The AI model itself is **not** a moat (EV-28).

---

## 4. Product Vision

| Element | Definition |
|---|---|
| **Vision** | Every Bangladeshi student's script is marked consistently, explainably and quickly, and every teacher spends their time on judgement rather than arithmetic and copying. |
| **Mission (3 years)** | Become the trusted marking workspace for internal exams in Bangladesh's private secondary schools. Cut marking-to-results time in half, with AI assistance that is proven per subject and question type and never replaces the teacher's decision. |
| **Core problem** | Slow, error-prone, unevidenced marking and result processing of handwritten board-format scripts (P1–P4). |
| **Primary user** | Subject teacher who marks scripts (Grades 9–10, Maths/Physics in MVP). |
| **Secondary users** | Exam coordinator (results and progress), Head of Department (moderation), capture operator, principal (oversight), school admin/ICT. |
| **Buyer** | Owner/MD (private) or Governing Body/SMC (MPO), advised by the principal (EV-07). |
| **Decision maker** | Principal (operational approval) + owner/SMC (budget). |
| **Recipients** | Students and parents (results, feedback); they are data subjects whose consent is needed (EV-30). |
| **Value proposition** | "Mark faster, total never, publish sooner, and defend every mark." Teachers keep full authority. The platform removes copying and arithmetic, organises marking question-by-question, and suggests marks with evidence **only where it has proven reliable**. |
| **Differentiation** | (1) Native NCTB CQ/MCQ paper and rubric model, including component pass rules and GPA. (2) Handles Bangla, English and maths handwriting, with honest per-cell capability levels. (3) Evidence-grounded, auditable marks. (4) Works on phones, offline capture, Bangla UI. (5) Deterministic results engine. Not differentiating: "we use AI". |
| **Product boundaries** | Internal school exams only. No board marking, no autonomous grading, no student-facing app in MVP, no ERP replacement. |

### 4.1 Product Principles
These are binding and used to resolve design disputes.

| ID | Principle | Operational meaning |
|---|---|---|
| PP-1 | **Teacher sovereignty** | The teacher decides every mark (DEC-05). AI proposes; it never finalises. The teacher can always turn AI off for an exam or question. |
| PP-2 | **Evidence before score** | Every AI suggestion shows *where* in the script and *which* rubric criterion. Ungrounded suggestions are never shown (DEC-33). |
| PP-3 | **Honest capability** | AI is enabled only in cells that passed gates. The UI states the level ("AI suggests" vs "AI shows text only"). |
| PP-4 | **Deterministic where possible** | Arithmetic, rules, GPA, MCQ bubbles and choice rules are computed by tested code, never by a model (DEC-09). |
| PP-5 | **Never add data entry** | Any feature that adds typing for teachers must remove more than it adds (EV-08). |
| PP-6 | **Works in Bangladeshi conditions** | Phone-first capture, offline queue, low bandwidth, Bangla UI, Bijoy conversion (EV-09, EV-10). |
| PP-7 | **Minimum data, maximum protection** | No names on answer pages; identity is separated from content; no training on student data by default (DEC-13, DEC-14). |
| PP-8 | **Measured claims only** | Marketing and in-product statements use measured numbers (DEC-31). |

---

## 5. Goals

| ID | Goal | Measure | Target (pilot) | Target (production yr 1) |
|---|---|---|---|---|
| G-1 | Reduce teacher effort | Teacher minutes per script (marking + totalling + mark entry) vs school baseline (EXP-05 method) | −30% | −40% |
| G-2 | Eliminate copying and arithmetic errors | Result-affecting arithmetic or transcription errors per 1,000 scripts (audit) | 0 attributable to platform computation | 0 |
| G-3 | Faster results | Working days from last exam to published results | ≥5 days faster than baseline | ≥7 days faster |
| G-4 | Trustworthy AI assistance | Per-cell gates (06 §4); severe unflagged errors on audit | Gates met for enabled cells; ≤0.5% | ≤0.2% |
| G-5 | Adoption | % of enrolled teachers (MVP subjects) marking in-app per exam | ≥70% | ≥80% |
| G-6 | Commercial validation | Paid pilot conversion; retention | ≥3 schools convert | ≥85% term-over-term school retention |
| G-7 | Unit economics | AI variable cost per 10-page script | ≤BDT 3.0 (DEC-18) | ≤BDT 2.5 |

## 6. Non-goals

- Replace teachers or auto-publish marks (DEC-05).
- Mark SSC/HSC board scripts or sell to education boards (v1).
- Grade Bangla literature essays or creative writing automatically (L0/L1 only).
- Proctoring, online exams (CBT), question banks for sale, content/LMS, fees, attendance, HR/payroll.
- Student or parent mobile apps (v1).
- Train AI models on student data (DEC-13).
- Rank teachers by performance on dashboards (OQ-18; the default is aggregated only).

---

## 7. Target Users

| Segment attribute | MVP definition (DEC-02) |
|---|---|
| Institution type | Private (non-government) secondary schools and school-and-colleges; includes MPO institutions only if owner-governed and fast-deciding |
| Location | Dhaka metropolitan area (Phase 3: Chattogram, other divisional cities) |
| Stream/medium | Bangla-medium and English-version (national curriculum in English). English-medium (Cambridge/Edexcel) schools are **out of MVP**, because their mark schemes differ and competitors exist. |
| Size | ~600–4,000 students; ≥2 sections per class in Grades 9–10 |
| Ability to pay (proxy) | Monthly tuition ≥ BDT 2,500 (hypothesis; validated in EXP-06) |
| Grades | 9–10 (Science group for Physics; all groups for General Mathematics) |
| Exam types | Class tests, half-yearly, annual, pre-test/test and model tests (all internal) |
| Secondary experiment | 1–2 coaching centres running written tests (Maths/Physics, Grades 9–10 / SSC prep) |

## 8. Personas

> **These are hypothesis personas.** The research contains no interviews (§1.3 of 00). The personas are built from verified context (VF-06, VF-09, VF-11) and qualitative research patterns (S02, S03). They must be replaced with interview-based personas after EXP-06. Names are illustrative.

| ID | Persona | Context | Jobs & pains | What they need from us | What makes them reject us |
|---|---|---|---|---|---|
| PER-1 | **Subject Teacher**: "Farhana", Physics, 9 yrs experience | 4 sections of Grades 9–10, 45–70 students each; sets the paper and rubric; marks at home in the evenings; Android phone (Tk 15–25k); shared staff-room computer | 250+ scripts per exam cycle; fatigue after long sessions; totalling and transferring marks; disputes with parents | Faster marking, no totalling, confidence she can defend marks, control over every mark, works on her phone | AI that feels like surveillance or overrides her; extra typing; misread handwriting presented as fact |
| PER-2 | **Exam Coordinator**: "Rafiq", academic coordinator | Consolidates marks from ~40 teachers; runs tabulation in Excel/ERP; answers to the principal | Late mark submissions; illegible mark slips; wrong component pass rules; re-printing report cards | Live progress view, validated marks, one-click tabulation/report cards, export to ERP | Anything needing constant internet at peak times; losing grading-scale flexibility |
| PER-3 | **Head of Department / Senior Teacher** (moderator) | Responsible for subject standards; checks samples | Can't see inconsistency until too late | Blind moderation samples, disagreement reports | Excess review load |
| PER-4 | **Principal / Owner** (buyer) | Reputation, GPA-5 yield, parent satisfaction, cost | Disputes, delays, errors that become public | Fewer disputes, faster results, evidence in disputes, clear cost | Parent or teacher backlash; opaque AI; unpredictable bills |
| PER-5 | **Capture Operator** (office or lab assistant) | Handles bundles after exams | — | Fast, forgiving capture; clear "what's missing" | Slow capture, many retakes |
| PER-6 | **Student / Parent** | Receive results; consent as data subjects | Opaque totals; re-check is slow | Item-level breakdown, fair re-check | Feeling judged by a machine |
| PER-7 | **AI Quality Reviewer** (internal, platform staff) | Monitors per-cell quality, runs gates | — | Evaluation dashboards, gold sets, gate workflow | — |

## 9. Jobs-to-be-Done

| Persona | Functional job | Emotional job | Social job |
|---|---|---|---|
| Teacher | "When a bundle of scripts arrives, help me award fair marks per sub-part and hand in correct totals without re-adding or copying, so I finish before the deadline." | Not dread the evenings; not fear an arithmetic mistake being exposed | Be seen as fair and competent |
| Coordinator | "When marking closes, give me validated, complete marks so I can produce tabulation sheets and report cards without re-keying." | No anxiety about published errors | Show control to the principal |
| HoD | "Before results go out, let me check that each teacher marked to the same standard." | Confidence | Maintain department reputation |
| Principal/Owner | "Publish accurate results quickly and defend them if challenged." | Peace of mind | A modern, fair school in parents' eyes |
| Student/Parent | "Understand where marks were lost and get a fair re-check." | Fairness | — |

---

## 10. User Stories

Priority: M = Must (MVP), S = Should (by Production), C = Could (later).

| ID | As a… | I want… | So that… | Pri | Requirements |
|---|---|---|---|---|---|
| US-01 | School admin | to import my student roster from Excel (including Bijoy text) | I don't retype names and rolls | M | FR-ORG-03 |
| US-02 | School admin | to record parent consent per student | the school complies with the PDPA | M | FR-ORG-06, PRV-02 |
| US-03 | Teacher | to create an exam from an SSC-style template and adjust marks and choice rules | setup takes minutes | M | FR-EXM-01, -02, FR-CUR-02 |
| US-04 | Teacher | to write each question's rubric and model answer, starting from a CQ template | the platform (and colleagues) mark to my standard | M | FR-RUB-01..05 |
| US-05 | Teacher | to test my rubric on a few sample answers before marking | I can fix ambiguities early | S | FR-RUB-09 |
| US-06 | Coordinator | to print QR cover sheets with MCQ bubbles per student | scripts are identified automatically | M | FR-EXM-05 |
| US-07 | Capture operator | to capture scripts quickly with my phone, even offline | capture doesn't eat the time we save | M | FR-CAP-01..07 |
| US-08 | Capture operator | to be told immediately when a page is blurred or missing | I don't have to re-find scripts later | M | FR-CAP-04, -05 |
| US-09 | Coordinator | to see which students' scripts are missing or absent | nothing gets lost | M | FR-CAP-09, -10 |
| US-10 | Teacher | to mark one question across all students at a time | I stay consistent and fast | M | FR-REV-01 |
| US-11 | Teacher | to see the student's answer, the rubric and the AI's suggestion with the evidence highlighted | I can decide quickly and confidently | M | FR-REV-02, FR-AI-03 |
| US-12 | Teacher | to change a criterion mark with one tap and give a one-tap reason | corrections are fast and the system learns within my exam | M | FR-REV-03, -04 |
| US-13 | Teacher | to add "also accept this answer" once and have it applied to the remaining answers | I don't repeat myself 60 times | M | FR-HITL-02 |
| US-14 | Teacher | to mark manually without any AI suggestion when I prefer | I stay in control | M | FR-REV-10, PP-1 |
| US-15 | Teacher | to know *why* an answer was flagged | I spend time where it matters | M | FR-AI-06 |
| US-16 | Teacher | the totals, component pass/fail and grade to be computed for me | I never add numbers | M | FR-RES-01..03 |
| US-17 | HoD | to blind-re-mark a sample of each teacher's scripts and see disagreements | standards are consistent before publication | M | FR-MOD-01 |
| US-18 | Coordinator | to import practical and other-subject marks and produce a board-style tabulation sheet and report cards | results come out of one system | M | FR-RES-05, -07, -09 |
| US-19 | Coordinator | to export marks in my ERP's import format | we keep using our ERP | M | FR-EXP-01 |
| US-20 | Parent (via school) | to receive an item-level result slip | I understand where marks were lost | M | FR-FBK-01 |
| US-21 | Coordinator | to log a re-check request and have a different teacher re-mark | disputes are handled fairly and on record | M | FR-APL-01..03 |
| US-22 | Principal | to see exam progress and results summaries | I know we'll publish on time | M | FR-ANL-01 |
| US-23 | Principal | to see how often teachers agree with AI suggestions in our school | I can judge whether it helps | S | FR-AIQ-01 |
| US-24 | AI quality reviewer | to promote or demote a capability cell with evidence | only proven AI is used | M | FR-AIQ-03 |
| US-25 | School admin | to see usage against our allowance | there are no billing surprises | M | FR-ADM-04 |
| US-26 | Teacher | to review on my phone during a commute | I use dead time | M | FR-REV-08, DEC-20 |
| US-27 | Teacher | a draft comment per student that I can edit | feedback is feasible at scale | S | FR-AI-11 |
| US-28 | Teacher | similar answers grouped so I can mark them together | repetitive answers take seconds | C | FR-AI-12 |
| US-29 | School admin | to delete a student's data on request | we honour rights requests | M | FR-ADM-05 |
| US-30 | Coordinator | a demo on our own scripts in minutes (sales) | the school can decide | S | FR-PRC-04 |

---

## 11. User Journeys (summary; detailed flows in `04-wireframes.md` §3)

| ID | Journey | Steps (happy path) | Moments of truth |
|---|---|---|---|
| J1 | Term setup | Admin imports roster → records consent → assigns teachers to subject-sections → school settings (moderation %, retention, processing mode) | Roster import handles Bijoy and messy Excel |
| J2 | Exam to results | Teacher creates exam from template → enters questions, MCQ key, rubric and model answers → (optional) rubric dry run → locks rubric → coordinator prints QR covers → exam held → operator captures scripts (offline) → upload → overnight processing → teachers review question-wise → HoD moderates sample → coordinator locks marks, imports practical marks → tabulation and report cards → publish | 1) Capture speed. 2) The first 20 reviewed items: are suggestions useful? 3) Totals match exactly. |
| J3 | Re-check | Parent requests via school → coordinator logs the request → assigned to a different teacher (AI hidden) → decision recorded → result version updated → slip re-issued | Fair and documented |
| J4 | AI quality governance | Platform reviewer monitors per-cell metrics → a gate evaluation runs on the gold set for a new model/prompt → promote/demote decision recorded | No silent quality change |

---

## 12. Product Principles
See §4.1 (PP-1 … PP-8).

---

## 13. MVP Scope

### 13.1 In scope (MVP = Phase 1, used in the Phase 2 pilot)

| Dimension | MVP |
|---|---|
| Education segment | Private urban secondary schools, Dhaka (DEC-02) |
| Grades | 9–10 |
| Subjects | General Mathematics; Physics (DEC-03) |
| Mediums | Bangla-medium, English-version |
| Assessment types | Class test, half-yearly, annual, pre-test/test/model test: all school-internal, board-format |
| Paper components | CQ (ka/kha/ga/gha, choice rules), short answer (SA), MCQ (cover-sheet bubbles; inline fallback), practical marks (imported, not captured) |
| Capture | Android app (offline, QR, spread capture) + PDF import (DEC-28) |
| AI capabilities | Page/region detection, question-label reading, transcription, criterion evidence and suggested marks **at gated levels per cell**, maths/numeric verification, risk-based routing, injection/blank/crossed-out detection, MCQ bubble reading (deterministic) |
| Human workflow | Question-wise review with confirm/edit per item; masked items; scoped clarifications and alternatives; HoD blind moderation sample; lock; appeals by a different teacher |
| Results | Deterministic totals, component pass rules, grades, GPA with 4th-subject rule, tabulation sheet, report card PDF, Excel/CSV export |
| Administration | Roster, roles, consent, settings, usage metering, audit log viewer, deletion requests |
| Languages | Bangla and English UI; Unicode throughout; Bijoy import conversion |

### 13.2 MVP capability matrix (initial target levels, all subject to gates)

L0 = manual; L1 = evidence only (transcript and highlights, no score); L2 = suggested criterion marks, confirm per item; L3 = batch-confirm eligible. **Every cell ships at L1 or lower and is promoted only through the gate process (FR-AIQ-03).** "Target" is the level we aim to reach during the pilot if the gates pass.

| Subject × item type | English-version (Latin script) target | Bangla-medium target | Notes |
|---|---|---|---|
| MCQ via cover-sheet bubbles | Deterministic (teacher resolves ambiguities, confirms per script) | Deterministic | DEC-22 |
| MCQ letters written inline (fallback) | L2 | L2 (ক/খ/গ/ঘ) | Single-character reading |
| Maths CQ ka (1 mark; formula/definition/short value) | L2 | L2 (if numerals/notation pass) / else L1 | |
| Maths CQ kha/ga/gha (2/3/4 marks; worked solutions) | L2 | L2 / else L1 | CAS verification (DEC-32) |
| Maths SA (2-mark short answers) | L2 | L2 / else L1 | |
| Physics CQ ka (definition, prose) | L2 | **L1** | DEC-21 |
| Physics CQ kha (explanation, prose) | L2 | **L1** | DEC-21 |
| Physics CQ ga (numerical application) | L2 | L2 / else L1 | Units check |
| Physics CQ gha (higher-order; mixed numeric + reasoning) | L2 (never L3 in v1) | L1 | S09: 4-mark part needs human emphasis |
| Diagrams (ray diagrams, graphs, geometry constructions) | L1 (region shown, "diagram present" flag) | L1 | No diagram scoring in MVP |
| Any item, low legibility / unmapped | Routed to manual review | Routed to manual review | |

**L3 is not expected before Phase 3.** It requires two exam cycles of L2 evidence (06 §4.3).

### 13.3 Out of scope (deliberately)

- SSC/HSC board marking; English-medium (Cambridge/Edexcel) mark schemes; madrasah-specific subjects (Arabic).
- Grades 6–8 and 11–12 (Phase 3/4).
- Subjects other than General Mathematics and Physics (Phase 3/4).
- Automatic scoring of Bangla prose, essays and creative writing; diagram scoring.
- Student/parent accounts, apps or portals; online exams; proctoring.
- Question paper generation or question bank (a candidate Phase 4 module; S04 shows demand).
- ERP features (fees, attendance); iOS capture app.
- Model training on customer data.

### 13.4 Why this MVP (rationale)

1. **Feasibility-first cells.** Maths/physics numeric work and English-version short prose are the most mature AI capabilities (EV-15). Bangla prose is not ready (EV-14), so it is shown as evidence only, not excluded.
2. **Value that doesn't depend on AI.** Question-wise review, deterministic totals and results, and tabulation address P2 and P4 even at L0 (EV-03). This protects against kill criteria K1/K2 (10-registers §5).
3. **Segment where schools set the papers** (VF-06), owners decide fast (EV-12), and premium tuition can absorb per-script pricing (EV-25).
4. **Grades 9–10** are SSC-format, high-stakes-for-reputation years, and the 2028 curriculum is likely to reach them last (VF-02; phasing undecided).

## 14. Future Scope

| Capability | Earliest phase | Precondition |
|---|---|---|
| Higher Maths, Chemistry, English (EV) | Phase 3 | Gates on each cell |
| Grades 6–8, 11–12 | Phase 3–4 | Templates; 2028 curriculum clarity for 6–8 |
| Bangla prose suggestions (Physics ka/kha BM; Bangla, BGS) | Phase 4 | Gate pass (EXP-02 follow-ups; specialist HTR) |
| Answer grouping for bulk review | Phase 4 | Embedding-based clustering validated |
| Cover-sheet mark capture for paper-marked scripts (digit recognition + sum verification) | Phase 3 | Low-risk AI; S01/S02/S03 wedge |
| Student/parent portal, SMS/WhatsApp delivery | Phase 4 | Consent model |
| ERP partner API and webhooks | Phase 4 | ≥2 ERP partners |
| Question-paper builder from question bank | Phase 4 | Content rights (S04 OQ) |
| Coaching-centre package (weekly written tests, rank lists) | Phase 3–4 | EXP-06 add-on |
| L3 batch confirmation | Phase 3 | Two cycles of L2 evidence |
| Model fine-tuning with opted-in data | Phase 5 | DEC-13 conditions |
| Diagram scoring | Phase 5 | Research |
| Low-stakes autonomous practice-test marking | Phase 5 | DEC-05 revisit conditions |

---

## 15. Functional Requirements

Format: **ID | Requirement | Priority (M/S/C/W) | Rationale / trace | User | Acceptance criteria | Dependencies.** "M" = MVP. Full technical realisation is in `02-TRD.md`.

### 15.1 Organisation, users and roster (FR-ORG)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-ORG-01 | Create an organisation with one or more schools. School profile: name (Bangla/English), EIIN (optional), board, mediums/versions, shifts, logo. | M | DEC-38 | Admin | An owner with 2 schools sees both. School data is isolated between organisations (tenant test passes). | TR-TEN-01 |
| FR-ORG-02 | Define academic year, classes, groups (Science/Humanities/Business), versions (BM/EV), shifts and sections. | M | VF-01 (groups reinstated) | Admin | Class 9 → group Science → version EV → section A can be created. Students belong to exactly one section per year. | FR-ORG-01 |
| FR-ORG-03 | Import roster from Excel/CSV: roll, name (BN/EN), class, group, version, section, optional subject choices (4th subject). Auto-detect and convert Bijoy/ANSI to Unicode. Show a validation report before commit. | M | S02, S04 (Bijoy) | Admin | A 500-row file with 20 Bijoy-encoded names imports with correct Unicode. Duplicates and missing rolls are reported. Nothing is committed until confirmed. | TR-BN-01 |
| FR-ORG-04 | Staff accounts (mobile number) and role assignments: Org Owner, School Admin, Exam Coordinator, HoD/Moderator, Teacher, Capture Operator. Permissions are scoped per school and, for teachers, per subject-section. | M | S09 roles, DEC-39 | Admin | Role matrix (`08` §5) enforced by API tests. A teacher cannot open scripts of unassigned sections. | SEC-01 |
| FR-ORG-05 | Assign teachers to subject × section(s) per academic year; allow multiple markers per exam question. | M | S02 | Admin, Coordinator | Assignments drive the review queues. Reassignment mid-exam moves unreviewed items only. | FR-ORG-04 |
| FR-ORG-06 | Record consent per student: (a) processing for marking (required for AI use); (b) data contribution for evaluation/improvement (separate, optional). Evidence of consent: uploaded form or recorded method. Students without consent (a) are marked at L0 (AI off) automatically. | M | VF-12, EV-30, DEC-13 | Admin | Toggling consent off stops AI processing for that student's future scripts. Existing AI outputs are deleted within 24 h. The export lists consent status. | PRV-02 |
| FR-ORG-07 | Organisation-level view across schools for owners (results summaries, usage). | S | S03 persona | Owner | An owner of 3 schools sees aggregated summaries without per-student data from schools where the owner has no school role. | FR-ANL-04 |

### 15.2 Curriculum and paper templates (FR-CUR)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-CUR-01 | Platform-maintained, versioned curriculum packs (e.g., `NCTB-SEC-2012R-2026`): class → group → subject → paper → chapter → topic, in Bangla and English. The MVP ships General Mathematics and Physics for Classes 9–10. | M | DEC-16, VF-01 | Platform, Teacher | The pack loads as data. The version is pinned on each exam. Updating the pack does not alter existing exams. | TR-CUR-01 |
| FR-CUR-02 | Paper templates with component structure and choice rules, e.g. Maths: CQ 50 (answer 5 of 8, each 10 = ka1+kha2+ga3+gha4) + SA 20 (10 of 15 × 2) + MCQ 30. Physics: CQ 40 (4 of 7) + SA 10 + MCQ 25 + Practical 25. Class-test templates (e.g., 20 marks). | M | VF-03, VF-04 | Teacher | Creating an exam from a template produces the structure. Totals equal the template total. Choice rules are stored and used by the result engine. | FR-EXM-02 |
| FR-CUR-03 | Schools can clone and customise templates (marks, counts, choice rules) for internal variants. | M | VF-06 (teacher-set papers) | Teacher, Coordinator | A custom template "Class Test — 25 marks, 2 CQ" can be saved and reused. | FR-CUR-02 |
| FR-CUR-04 | Items carry chapter/topic (optional) and cognitive level (default from CQ part: ka = knowledge, kha = comprehension, ga = application, gha = higher-order; editable). | M (level) / S (chapter) | VF-04; analytics | Teacher | The item analysis report groups by cognitive level. Chapter tags are optional. | FR-ANL-03 |

### 15.3 Exam setup (FR-EXM)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-EXM-01 | Create an exam: type (class test / half-yearly / annual / pre-test / test / model), class, group, version(s), sections, subject paper, date, template, marking deadline, processing mode. | M | VF-06 | Teacher, Coordinator | The exam appears in the coordinator's calendar and each assigned teacher's list. | FR-CUR-02 |
| FR-EXM-02 | Define question structure: questions, sub-parts, marks, stimulus (uddipok) text/image, choice rules. Bangla, English and maths input. | M | VF-04 | Teacher | Structure validation: sub-part marks sum to the question total; choice-rule totals match the paper total. | FR-EXM-04 |
| FR-EXM-03 | Upload a question paper (PDF, image, DOCX) and get an AI-drafted structure (questions, sub-parts, marks, text) to confirm and edit. | S | Setup time (S04 JTBD) | Teacher | For a typed paper, ≥90% of sub-parts are detected with correct marks. Nothing is saved until the teacher confirms. | AI-REQ-09 |
| FR-EXM-04 | Rich text input supporting Bangla Unicode, English, a math editor (LaTeX-backed, with a visual palette), and images. Pasting Bijoy text auto-converts. | M | S02, S04 | Teacher | Pasting "Avwg" (Bijoy) yields "আমি". Maths renders in Bangla and English UIs. | TR-BN-01 |
| FR-EXM-05 | Generate print-ready A4 PDF QR cover sheets per student per paper: school, exam, class, section, roll, student name (**identity zone**), QR (pseudonymous script ID), MCQ bubble grid (with set code), and an instruction line ("write question numbers clearly, e.g. ২(গ)"). Also blank "unassigned" covers for late additions. | M | DEC-07, DEC-14, DEC-22 | Coordinator | 60 covers print on a standard laser printer. QR decodes at 300 dpi and in phone capture. A blank cover can be linked to a student in the app. | FR-CAP-02 |
| FR-EXM-06 | MCQ answer key per set (e.g., ক/খ/গ/ঘ sets), with an option to void or accept multiple answers for a question after the exam (with audit). | M | S14 | Teacher | Changing the key after marking recalculates MCQ marks with an audit event. | FR-RES-01 |
| FR-EXM-07 | Exam lifecycle states: Draft → Rubric Locked → Capturing → Processing → Reviewing → Moderation → Marks Locked → Published (+ Re-check). Actions allowed per state. | M | S11 state machine | All | Illegal transitions are rejected (API tests). Unlock requires coordinator reason + OTP. | TR-WF-01 |
| FR-EXM-08 | Clone an exam or rubric from a previous term. | S | Setup effort | Teacher | The clone keeps the structure and rubrics and resets capture and marks. | — |

### 15.4 Rubrics and model answers (FR-RUB)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-RUB-01 | Per item: rubric criteria (description, marks, evidence expectation), model answer, marking notes. | M | EV-16 (reference + rubric improves AI) | Teacher | An item is **AI-eligible** only if it has a model answer and criteria that sum to the item marks. Otherwise it is marked at L0 with a visible reason. | ASR-01 |
| FR-RUB-02 | CQ criterion templates by part and subject (e.g., Physics ga: "identifies correct formula (1) / substitutes values with units (1) / correct result with unit (1)"), editable. | M | Speed of authoring (ASM-11) | Teacher | Selecting a template pre-fills criteria. The teacher edits text and marks. | FR-CUR-02 |
| FR-RUB-03 | Alternative accepted answers and methods; equivalent forms (e.g., 0.5 = 1/2 = 50%); synonyms (e.g., বেগ/velocity). | M | S05, S09 | Teacher | Alternatives appear in the prompt and in the review card. | FR-HITL-02 |
| FR-RUB-04 | Common mistakes with deductions; error-carried-forward (ECF) policy per multi-step item (penalise the first error once; credit later correct method). | M | S07, DEC-32 | Teacher | With ECF on, a wrong value in step 1 carried correctly through steps 2–3 loses only step-1 marks (unit test on a fixture). | ASR-04 |
| FR-RUB-05 | Answer specifications: numeric (value, tolerance, unit, significant figures policy), expression (LaTeX), MCQ key. | M | DEC-32 | Teacher | 9.8 m/s² with ±0.1 tolerance accepts 9.81 and rejects 98. Unit missing applies the configured deduction. | TR-MATH-01 |
| FR-RUB-06 | AI-drafted rubric from question + model answer, for teacher acceptance. | S | Authoring time | Teacher | The draft is labelled "AI draft". It cannot be locked without teacher edits or an explicit accept per item. | AI-REQ-09 |
| FR-RUB-07 | Rubric validation before lock: marks sums, missing model answers, conflicting alternatives, criteria without observable evidence ("good explanation" → warning). | M | Quality of AI input | Teacher | Lock is blocked on errors; warnings are shown. | — |
| FR-RUB-08 | Rubric lock before marking. Post-lock edit creates a new rubric version, shows the impact (items already confirmed that could change) and re-suggests unconfirmed items. Confirmed items change only if the teacher re-confirms. | M | DEC-15, audit | Teacher, HoD | Version history viewable. Every mark records its rubric version. | TR-AUD-01 |
| FR-RUB-09 | Rubric dry run: the teacher uploads 3–5 sample answers (or picks from captured scripts) and sees AI suggestions before locking. | S | Early error discovery | Teacher | Dry run results in ≤2 min (priority mode). Not counted against the allowance. | FR-PRC-04 |

### 15.5 Capture (FR-CAP)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-CAP-01 | Android capture app: sign in, download exam capture sessions, capture offline. Android 10+, 3 GB RAM class devices. | M | DEC-28, VF-11 | Capture operator, Teacher | Works in flight mode for a full session of 70 scripts. | NFR-DEV-01 |
| FR-CAP-02 | Script boundaries from QR cover detection. Page order by capture order. Unreadable QR → manual student pick from roster. | M | DEC-07 | Operator | Capturing covers A, pages, cover B, pages yields 2 scripts with correct pages. The pick-list fallback works offline. | FR-EXM-05 |
| FR-CAP-03 | Two-page spread capture with automatic split into left/right pages. Auto-capture on page turn (stability detection). | M (split) / S (auto-trigger) | Capture time (ASM-02) | Operator | A 10-page booklet is captured in ≤6 shots. Auto-trigger false captures <5%. | NFR-PERF-04 |
| FR-CAP-04 | On-device quality checks (blur, glare, cut-off edges, excessive skew, too dark) with immediate retake prompt. The operator can override with reason. | M | S07 IQA | Operator | Deliberately blurred pages are flagged ≥95% of the time on the test set. | TR-CAP-02 |
| FR-CAP-05 | Page checks: blank-page detection, duplicate page detection, page count vs expected range, supplementary sheet prompt ("any loose sheets?"). | M | EV-05 | Operator | A duplicate spread is flagged. A blank page is marked "blank" (kept, not processed). | — |
| FR-CAP-06 | Edit script before upload: insert, reorder, delete, rotate pages; attach supplementary sheets captured later (scan the cover again, then add pages). | M | EV-05 | Operator | A late supplementary sheet can be appended to the right script after upload, with an audit event. | — |
| FR-CAP-07 | Encrypted local storage, resumable background upload, Wi-Fi-only option, per-page compression (target ≤400 KB at legibility), upload progress. | M | EV-09, VF-11 | Operator | Killing the app mid-upload loses no pages. Local files are encrypted at rest and deleted after server acknowledgement. | SEC-07 |
| FR-CAP-08 | PDF import (from sheet-fed scanners, 200–300 dpi): split into scripts by QR covers. | M | DEC-28 | Coordinator | A 700-page PDF of 70 scripts splits correctly. Mis-splits are reported for manual fix. | TR-CAP-05 |
| FR-CAP-09 | Capture dashboard per exam: expected vs captured scripts per section, missing students, scripts with issues. | M | S02 (lost scripts) | Coordinator | The list of not-yet-captured students is exportable. | FR-ANL-01 |
| FR-CAP-10 | Mark student absent (distinct from zero) and "script not submitted". | M | S02 (absent ≠ 0) | Coordinator | Absent students show "ABS" in results and are excluded from averages per school policy. | FR-RES-06 |

### 15.6 Processing (FR-PRC)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-PRC-01 | Status per script and page (queued, processing, ready, needs attention), with reasons. | M | Transparency | Coordinator, Teacher | The status matches pipeline events. A failed page shows its reason and retry. | TR-PIPE-01 |
| FR-PRC-02 | Map answer regions to questions and sub-parts (question-label detection + layout). Continuations across pages are linked. Unmapped regions become an "unmapped" queue item for the teacher. | M | RSK-19 | Teacher | On the gold set, mapping accuracy is measured (06 §3). Unmapped or ambiguous items never receive an AI score. | AI-REQ-02 |
| FR-PRC-03 | Before any external AI call, remove the identity zone (cover sheet) and redact detected names or rolls on answer pages. Only answer-region images and transcripts are sent. | M | DEC-14, PRV-05 | — | Audit of 200 AI request payloads shows no cover-sheet imagery and no roster names (automated test with planted names). | TR-PRV-02 |
| FR-PRC-04 | Processing modes: **Standard** (batch; ready by 07:00 for uploads before 22:00), **Priority** (≤60 min; extra cost), **Demo/Dry-run** (≤60 s per script, limited). | M (Std, Pri) / S (Demo) | DEC-34 | Coordinator | SLA measured per job. The mode is selectable per exam and billed accordingly. | NFR-PERF-02 |
| FR-PRC-05 | Re-processing on rubric version change (unconfirmed items), model/prompt change (only before review starts, or on explicit request), or teacher request for one item. | M | FR-RUB-08 | Teacher | Re-processed items show a "new suggestion" badge. Confirmed marks are never silently changed. | — |

### 15.7 AI assistance (FR-AI)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-AI-01 | Support level per capability cell (subject × item type × script/language), set by the platform through gates. Schools may **lower** the level (to L0/L1) per exam or item, never raise it. | M | DEC-04 | Platform, Teacher | Level changes are logged with evidence reference. The UI shows the level on each item. | FR-AIQ-03 |
| FR-AI-02 | (L1+) Transcript of the answer region with uncertain spans marked; maths shown as rendered LaTeX. It is generated automatically only in cells whose transcript gate passes (06 §4.3 L1-2); elsewhere it is generated **on demand** when the teacher taps "Show text" (cost control, 06 §10). | M | PP-2 | Teacher | The transcript is always shown **with** the image crop, never alone. Uncertain spans are visually distinct. On-demand text returns in ≤20 s p95. | AI-REQ-03 |
| FR-AI-03 | (L2+) For each rubric criterion: decision (met / partly / not met / cannot determine), marks proposed, evidence (image region + quoted span), short reason (≤25 words, in the teacher's UI language). | M | PP-2, S07 grounding | Teacher | Every "met/partly" decision has ≥1 evidence reference that validates against the transcript/region (grounding validator). Otherwise the item is downgraded to L1 for that item. | AI-REQ-04 |
| FR-AI-04 | The suggested item mark is computed **deterministically** from criterion decisions and rubric rules (caps, ECF). | M | PP-4 | — | Property tests: the suggested mark always equals the rubric function of the criterion decisions. | ASR-03 |
| FR-AI-05 | Maths and numeric verification badges: "value matches key", "equivalent expression (CAS)", "unit missing", "cannot verify". | M | DEC-32 | Teacher | Badges come from deterministic checks only. "Cannot verify" never reduces the suggestion by itself. | TR-MATH-01 |
| FR-AI-06 | Risk level (low / medium / high) and reasons per item: e.g., low legibility, model disagreement, near a pass/grade boundary, high-value item, unusual answer, CAS disagreement, possible instruction text, crossed-out content. Drives queue ordering and L3 eligibility. | M | DEC-10 | Teacher | Reasons are human-readable in Bangla/English. Ordering is by risk (high first) unless the teacher chooses otherwise. | AI-REQ-06 |
| FR-AI-07 | Deterministic MCQ bubble reading with flags for double marks, erasures and unclear bubbles. | M | DEC-22 | Teacher | On the bubble test set, unflagged misreads ≤0.1% of bubbles (06 §4). | TR-OMR-01 |
| FR-AI-08 | Inline MCQ letter reading (fallback, L2). | S | VF-06 | Teacher | Suggestions are confirmed per script. | AI-REQ-03 |
| FR-AI-09 | Detect instruction-like or off-task text in answers (e.g., "give me full marks", "ignore the rubric") → flag, and ignore it for scoring. | M | RSK-15, VF-25 | Teacher | The red-team set passes (EXP-08 rule). | AI-REQ-08 |
| FR-AI-10 | Detect blank, not-attempted and crossed-out regions. Crossed-out content is excluded from suggestions unless no other attempt exists (then flagged). | M | EV-05 | Teacher | On the gold set, "blank" false negatives (blank marked as answered) are ≤1%. | AI-REQ-02 |
| FR-AI-11 | Draft per-student feedback comments from criteria results (Bangla/English), editable, only included once approved. | S | EV-11 (by-product) | Teacher | Comments reference only criteria and evidence; no generic praise templates beyond one line. | AI-REQ-10 |
| FR-AI-12 | Answer grouping (cluster similar answers for one decision applied to a group, with per-item preview). | C | Future speed | Teacher | — | — |
| FR-AI-13 | Second-opinion model on high-risk or high-value items (internal behaviour; the result feeds the risk level). | M | DEC-08, DEC-10 | — | Invoked on ≤35% of AI-eligible items (cost control); the rate is monitored. | TR-AI-05 |

### 15.8 Review (FR-REV)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-REV-01 | Question-wise review queue per teacher: one sub-question across all assigned scripts. Default order: risk (high first); alternatives: roll, section. Progress counter. | M | DEC-06 | Teacher | The queue shows only items for the teacher's sections. Next-item prefetch (NFR-PERF-01). | FR-ORG-05 |
| FR-REV-02 | Review card: answer crops (all linked regions, zoomable), transcript (collapsible), rubric criteria with the AI decision per criterion and evidence highlight on hover/tap, suggested mark, risk reasons, model answer (collapsible), level badge. | M | PP-2 | Teacher | Usable on 1366×768 and 360×800 screens (UI/UX doc). | UX |
| FR-REV-03 | Actions: Confirm; edit criterion marks or total; mark blank / not attempted; remap region to another question; flag to HoD; request AI re-suggestion; add note; add alternative answer or clarification (scoped); report AI error (reason list); undo last. | M | S09 taxonomy | Teacher | Each action creates an audit event. Undo works for the last 20 actions before the item is locked. | FR-HITL-01 |
| FR-REV-04 | Reason capture when the teacher's mark differs from the suggestion by ≥1 mark or on any criterion: one-tap reason (misread handwriting; alternative correct; rubric unclear; AI too lenient; AI too strict; partial credit; calculation checked; other + note). | M | S09, DEC-17 | Teacher | Median added time ≤2 s (EXP-09). Can be skipped only by selecting "other". | FR-HITL-01 |
| FR-REV-05 | Masked items: 5% of AI-suggested items per teacher (randomised, min 1 per 20) hide the suggestion until the teacher enters a mark. | M | DEC-33 | Teacher | Masked-item agreement is tracked per teacher (for monitoring, not shown as a score). | FR-AIQ-01 |
| FR-REV-06 | Batch confirm for L3 cells only: batches ≤20 items, each thumbnail visible, 1 in 10 forced open. | S | DEC-04, DEC-33 | Teacher | Not available unless the cell level is L3. | FR-AIQ-03 |
| FR-REV-07 | Script view: all pages; items with final or pending marks; completeness checks (every item decided; every page viewed or auto-classified blank; choice rule satisfied); totals; component status. | M | EV-05, S02 ERR-02 | Teacher, Coordinator | A script cannot be marked "complete" with undecided items or unviewed non-blank pages. | FR-RES-01 |
| FR-REV-08 | Desktop keyboard shortcuts (confirm, next, digits for marks, reason keys). Phone: large tap targets, swipe next. | M | Speed | Teacher | Shortcut map in the UI/UX doc; a full review works without a mouse. | UX |
| FR-REV-09 | Offline-tolerant review: prefetch the next 30 items with images. Decisions queue locally and sync. Conflicts are resolved in favour of the first confirmation, with a notice. | S | EV-09 | Teacher | 20 minutes offline review syncs without loss. | TR-SYNC-02 |
| FR-REV-10 | Manual mode (L0): same review UI without AI suggestions, including for students without consent. | M | PP-1 | Teacher | Switchable per exam, question or student (consent-driven automatically). | FR-ORG-06 |
| FR-REV-11 | Split a question's queue among multiple teachers. | S | Large schools | Coordinator | Items are distributed without duplication. Progress per marker. | FR-ORG-05 |

### 15.9 Human knowledge and corrections (FR-HITL)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-HITL-01 | Every correction is classified (07 §4 taxonomy) and routed to its store: item mark only; rubric clarification; alternative answer; exception rule; transcription error; mapping error; AI reasoning error; product bug. | M | DEC-17 | System | 100% of edits with reasons produce a correction event with routing target (analytics check). | 07 |
| FR-HITL-02 | Scoped clarifications and alternatives added during review apply to **not-yet-confirmed** items of the same question in the same exam. Those items are re-suggested and badged "updated after your clarification". | M | US-13 | Teacher | Adding an alternative re-suggests the remaining items in ≤5 min (priority lane). Confirmed items are untouched. | FR-PRC-05 |
| FR-HITL-03 | Exception rules (e.g., "accept g = 9.8 or 10 m/s²") with scope (question / exam / school subject) and expiry (end of exam by default). School-scope rules need HoD approval. | S | S09 | Teacher, HoD | Rules are listed in exam settings. An expired rule is not applied to new exams. | — |
| FR-HITL-04 | Flag to HoD for adjudication with a comment. HoD decision is recorded and the teacher is notified. | M | S09 escalation | Teacher, HoD | Flagged items block script completion until resolved. | FR-MOD-01 |
| FR-HITL-05 | School instruction library: reusable marking guidance per subject (e.g., "don't penalise spelling in Physics"), approved by HoD, attached to rubrics. | S | S09 instruction hierarchy | HoD | An instruction appears in the review card and in AI context for the scoped subject. | AI-REQ-05 |

### 15.10 Moderation and locking (FR-MOD)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-MOD-01 | A moderation sample per marker (default 5% of scripts, min 3, configurable). The moderator re-marks blind (no teacher mark, no AI). The report shows differences by item. Items beyond tolerance (default >1 mark on items ≥3 marks, any difference on 1–2 mark items) are sent back to the teacher, or to targeted re-review of that question. | M | DEC-27 | HoD | The sample is drawn randomly and stratified by risk. Moderation completes before marks lock. | FR-REV-10 |
| FR-MOD-02 | Pre-lock completeness checks: all scripts captured or accounted for (absent / not submitted); all items decided; flags resolved; moderation complete. | M | S02 | Coordinator | Lock is blocked with a checklist of blockers. | FR-REV-07 |
| FR-MOD-03 | Lock marks. Unlock requires a reason and OTP. All changes after lock are versioned. | M | Audit | Coordinator | The published result references a marks version. | TR-AUD-01 |

### 15.11 Results (FR-RES)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-RES-01 | Deterministic aggregation item → sub-question → question → component (CQ/SA/MCQ/Practical) → paper → subject, applying choice rules. Policy for over-answered choices: **"count the first N attempted in script order"** (default) or "best N" (school setting). | M | VF-04, PP-4 | Coordinator | 100% agreement with the hand-computed test fixture set (≥200 cases incl. edge cases). | TR-RES-01 |
| FR-RES-02 | Component pass rules (pass mark per component, default 33% each, configurable), subject pass/fail. | M | VF-05 | Coordinator | A student with CQ below the pass mark but total ≥33 is marked Fail for the subject (fixture). | TR-RES-01 |
| FR-RES-03 | Letter grade and GP per subject (NCTB table default, configurable); GPA with 4th-subject rule (only GP above 2.00 counts) and cap 5.00. | M | VF-05 | Coordinator | Fixture set with 4th-subject cases passes. | TR-RES-01 |
| FR-RES-04 | Combine assessments (e.g., class tests 30% + half-yearly 70%) per school policy. | S | VF-06 (30/70) | Coordinator | Configurable weights. Rounding rule configurable (default: round half up at the subject total). | — |
| FR-RES-05 | Enter or import marks for components and subjects not marked in-platform (practicals, other subjects) via grid or Excel, with validation. | M | Full results needed | Coordinator, Teacher | Bounds and absent handling are the same as for platform marks. | FR-RES-06 |
| FR-RES-06 | Validation: marks within bounds; absent ≠ 0; missing marks block lock; impossible combinations flagged. | M | S02 errors | Coordinator | An import of 85 for a 70-mark component is rejected with a row reference. | — |
| FR-RES-07 | Tabulation sheet (board-style ledger) by section/class, merit list (ties per school policy), grade distribution. | M | S02, S11 | Coordinator | PDF and Excel. Bangla/English. Matches computed results exactly. | FR-EXP-02 |
| FR-RES-08 | Grace-mark policy (e.g., +k marks if within k of pass), configurable, applied transparently with audit and shown on the ledger. | C | S02 | Coordinator | — | — |
| FR-RES-09 | Publish: report cards PDF (per student, Bangla/English, school branding); optional SMS summary. Published results are versioned. | M (PDF) / S (SMS) | P4 | Coordinator | Publishing requires the coordinator role + OTP. Re-publishing after re-check creates version n+1. | FR-FBK-01 |

### 15.12 Feedback (FR-FBK)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-FBK-01 | Student result slip: marks per question and sub-part, cognitive-level breakdown, component pass status, teacher comments (approved only). | M | P4, DEC-35 | Coordinator, Parent | Generated in the same run as report cards. No AI text appears unless teacher-approved. | FR-AI-11 |
| FR-FBK-02 | Annotated script PDF: marks per region and criteria met (from confirmed decisions), for parent meetings and re-checks. | S | Transparency | Teacher | Only confirmed information appears. | — |
| FR-FBK-03 | Class item analysis: mean % per item and per cognitive level, most common deduction reasons, most frequent alternative answers. | S | Teaching value | Teacher, HoD | Shown after marks lock. | FR-ANL-03 |

### 15.13 Re-check / appeals (FR-APL)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-APL-01 | Log a re-check request (script or item), requester (parent/student via school staff), reason, date, school window policy. | M | DEC-23 | Coordinator | Requests outside the school's window need an override reason. | — |
| FR-APL-02 | Assign to a teacher other than the original marker (or the HoD). AI suggestions and the original mark are hidden until the re-marker decides; afterwards the full evidence and history are visible. | M | DEC-23 | HoD, Teacher | Assignment to the original marker is blocked unless the school has one teacher for the subject (then HoD/principal sign-off). | FR-ORG-04 |
| FR-APL-03 | Record the outcome (unchanged / changed + reason). Results are recomputed and versioned, the slip is re-issued, and the change is visible in the audit log. | M | Audit | Coordinator | The new version is published only via the publish action. The previous version is retained. | FR-RES-09 |

### 15.14 Analytics (FR-ANL) and AI quality (FR-AIQ)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-ANL-01 | Exam progress dashboard: captured, processed, reviewed, moderated, locked, published, per section and marker; deadline risk. | M | S03 champion | Coordinator, Principal | Data freshness ≤5 min. | — |
| FR-ANL-02 | Teacher workload and turnaround (aggregated by default; per-teacher detail only to that teacher and their HoD per school policy). | S | OQ-18 | HoD, Principal | Default configuration shows no per-teacher ranking to the principal. | — |
| FR-ANL-03 | Student performance by subject, chapter, cognitive level; section comparisons. | S | Teaching value | Teacher, Principal | — | FR-CUR-04 |
| FR-ANL-04 | Principal/owner summary: pass rates, grade distributions, GPA-5 counts, trends by exam. | S | Buyer value | Principal, Owner | — | — |
| FR-AIQ-01 | School AI view: per subject and item type, % of AI-suggested items confirmed unchanged, average absolute change, top correction reasons, masked-item agreement (aggregated). | M | Trust, US-23 | Principal, HoD | Numbers match the correction events. Explanations are in plain Bangla/English. | 06 §6 |
| FR-AIQ-02 | Platform AI quality dashboard (internal): per cell, agreement vs gold and vs teachers, severe-error audits, calibration, drift (PSI), cost per page, latency. | M | 06 | AI Quality Reviewer | 06 §6 metrics available daily. | TR-OBS-03 |
| FR-AIQ-03 | Gate workflow: run the evaluation of a candidate (model/prompt/pipeline version) on the frozen gold set; compare to gates; promote/demote cell levels with a signed decision record. | M | DEC-04, DEC-29 | AI Quality Reviewer | No level change without an evaluation report ID. Demotion can be immediate (safety); promotion needs two reviewers. | TR-MLOPS-02 |

### 15.15 Administration (FR-ADM) and Export (FR-EXP)

| ID | Requirement | Pri | Rationale | User | Acceptance criteria | Deps |
|---|---|---|---|---|---|---|
| FR-ADM-01 | School settings: default processing mode, AI level caps, moderation %, re-check window, retention window (90–365 days after publication), grading policies, SMS on/off, UI language default. | M | Configurability | School admin | Changes are audited. Retention changes apply prospectively. | — |
| FR-ADM-02 | Consent management (FR-ORG-06) including bulk import of consent status and printable consent forms (Bangla/English). | M | PRV-02 | School admin | The printable form is produced from the approved legal text. | EXP-10 |
| FR-ADM-03 | Audit log viewer: filter by exam, user, action; export. | M | Accountability | School admin, Principal | Shows who changed which mark, when, from/to, and why. | TR-AUD-01 |
| FR-ADM-04 | Usage and billing: allowance, consumed AI-assisted scripts and pages, projected overage, invoices and payment records (manual reconciliation of bank/cheque/bKash). | M (usage) / S (invoices) | DEC-36, S15 | School admin, Owner | Usage matches metering events. An alert at 80% of the allowance. | TR-BILL-01 |
| FR-ADM-05 | Data subject requests: export a student's data, delete a student's data (with retention-rule exceptions stated), with a deletion certificate. | M | VF-12 | School admin | Deletion completes ≤30 days. Certificate lists stores purged. | TR-PRV-05 |
| FR-ADM-06 | Platform administration: tenants, curriculum packs, templates, model/prompt registry, capability levels, feature flags, support access (time-boxed, consented). | M | Operations | Platform admin | Support access requires school admin approval and expires ≤24 h. | SEC-05 |
| FR-EXP-01 | Excel/CSV exports: marks per item/sub-part/component/subject, per section; mapping presets for common Bangladeshi ERPs (validated in EXP-11). | M | DEC-25 | Coordinator | Round-trip import into at least one partner ERP without manual edits (EXP-11). | — |
| FR-EXP-02 | PDF exports: tabulation sheets, report cards, result slips, moderation report, audit extract. | M | — | Coordinator | Bangla fonts embedded. Prints correctly on A4. | — |
| FR-EXP-03 | Partner API (read results, exam status) and webhooks. | C | Phase 4 | ERP partners | — | — |

### 15.16 Won't Have (v1)
Autonomous finalisation; board marking; English-medium mark schemes; essay/creative writing auto-scoring; diagram scoring; student/parent accounts; proctoring; online exams; LMS/content; fees/attendance; iOS capture; model training on customer data; teacher leaderboards.

---

## 16. Non-functional Requirements

| ID | Category | Requirement | Pri | Acceptance criteria |
|---|---|---|---|---|
| NFR-PERF-01 | Review latency | Next item displays in ≤1.0 s p95 on 4G (≥5 Mbps) and ≤2.5 s p95 on 3G-class (1 Mbps) links, with prefetch | M | Synthetic tests from Dhaka network profiles |
| NFR-PERF-02 | Processing SLA | Standard mode: 99% of pages uploaded by 22:00 have suggestions by 07:00 (local time). Priority: 95% within 60 min. Demo: ≤60 s per 10-page script | M | Job telemetry over pilot |
| NFR-PERF-03 | Capture app | Shutter-to-next-capture ≤1.5 s on a reference device (3 GB RAM, Android 11). App cold start ≤3 s | M | Device lab test |
| NFR-PERF-04 | Capture throughput | A trained operator captures a 10-page script in ≤30 s (target), ≤45 s (limit) | M | EXP-04 |
| NFR-SCL-01 | Volume | Ingest and process ≥100,000 pages/day at peak with standard-mode SLA. Design for 10× growth without re-architecture | M (pilot needs ~20k/day) | Load test at 150k pages/day |
| NFR-AVL-01 | Availability | Web app and API 99.5% monthly (99.9% in declared exam windows). Capture is offline-capable, so server outages must not block capture | M | Uptime monitoring |
| NFR-REL-01 | Durability | No accepted page is lost: server acknowledgement only after durable storage; object storage 11-nines class; daily DB backups + PITR ≥7 days | M | Restore drill per quarter |
| NFR-INT-01 | Correctness | Result computations 100% correct on the fixture suite; any discrepancy is a Sev-1 | M | CI gate |
| NFR-DEV-01 | Devices | Android 10+, ≥3 GB RAM, 12 MP camera. Web: last 2 versions of Chrome/Edge/Firefox; Android Chrome | M | Device matrix test |
| NFR-NET-01 | Bandwidth | Upload ≤400 KB per page average; review item payload ≤300 KB | M | Telemetry |
| NFR-L10N-01 | Localisation | All UI strings in Bangla and English; Bangla fonts (e.g., Noto Sans Bengali / Hind Siliguri) embedded in PDFs; date and number formats per locale; Bangla digits optional | M | Linguistic review by 2 native speakers |
| NFR-A11Y-01 | Accessibility | WCAG 2.2 AA for web (contrast, keyboard, focus, labels). Minimum tap target 44×44 px | M | Audit with axe + manual |
| NFR-SEC-01 | Security | See SEC requirements; OWASP ASVS L2 for web/API | M | Pen test before pilot |
| NFR-PRV-01 | Privacy | See PRV requirements | M | DPIA completed before pilot |
| NFR-COST-01 | Unit cost | AI variable cost ≤ BDT 3.0 per 10-page script (standard mode) at pilot; ceiling BDT 6.0 | M | Monthly cost report |
| NFR-OBS-01 | Observability | Every script traceable across capture → processing → review → result via correlation ID | M | Trace demo |
| NFR-MNT-01 | Maintainability | Curriculum, templates, rubrics, prompts and model routes are data/config, not code | M | Code review checklist |
| NFR-AUD-01 | Auditability | Every mark change and every AI suggestion is reconstructable (inputs hash, model/prompt version, output, user action) for ≥5 years | M | Audit reconstruction test on sample |

---

## 17. AI Requirements (summary; details in `06-ai-model-decision-and-evaluation.md`)

| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| AI-REQ-01 | Every AI capability is attached to a capability cell and a support level; nothing runs outside a registered cell | M | Registry audit |
| AI-REQ-02 | Region and question mapping outputs include confidence. Unmapped or ambiguous regions are never scored | M | Gold-set mapping metrics (06 §3) |
| AI-REQ-03 | Transcription preserves the student's text (no correction of spelling or maths); uncertain spans are marked | M | Critical-error rate (negation/number flips) reported per cell |
| AI-REQ-04 | Criterion decisions must be grounded (evidence spans/regions that validate); ungrounded decisions are discarded | M | Grounding validator pass rate; ungrounded rate <2% |
| AI-REQ-05 | Prompts include the complete rubric, model answer, alternatives, scoped instructions and item metadata; no retrieval from other schools | M | Prompt snapshot tests |
| AI-REQ-06 | Risk scoring combines ≥4 signals and is calibrated per cell (risk–coverage) | M | 06 §5 |
| AI-REQ-07 | Gates per cell for L1/L2/L3 (06 §4) are enforced by the platform | M | Gate report required for level change |
| AI-REQ-08 | Student content is treated as data. Instruction-like content is detected and flagged. The red-team suite passes before any release | M | EXP-08 criteria |
| AI-REQ-09 | Setup assists (paper structure, rubric drafts) always require teacher confirmation | S | UI blocks lock without confirmation |
| AI-REQ-10 | Generated feedback comments cite only confirmed criteria; teacher approval is required | S | Review |
| AI-REQ-11 | All model calls go through the provider abstraction with pinned versions. Any change requires a regression pass | M | TR-MLOPS |
| AI-REQ-12 | No student data used for training (DEC-13) | M | Contract + configuration audit |

## 18. Assessment Requirements

| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| ASR-01 | Item model: stem, sub-parts, max marks, cognitive level, answer spec, rubric criteria, alternatives, deductions, ECF policy | M | Schema validation |
| ASR-02 | Scoring granularity: whole marks by default; half marks allowed per school setting (per item) | M | Rounding fixture tests |
| ASR-03 | Item mark = f(criterion decisions, rubric) deterministic; bounds [0, max] | M | Property tests |
| ASR-04 | Multi-step items support ECF and caps | M | Fixtures |
| ASR-05 | Choice rules: answer N of M per section; over-answer policy (first N / best N) | M | Fixtures |
| ASR-06 | Component pass rules and GPA per VF-05, configurable | M | Fixtures |
| ASR-07 | Every final mark records: marker, time, rubric version, AI suggestion (if any), change and reason | M | Audit test |
| ASR-08 | Double-marking support for moderation, with agreement statistics (exact, ±1, QWK) | M | Moderation report |

## 19. Human-in-the-Loop Requirements (summary; details in `07-hitl-and-continuous-improvement.md`)

| ID | Requirement | Pri |
|---|---|---|
| HITL-01 | Teacher confirms every AI-suggested mark (DEC-05) | M |
| HITL-02 | Teachers can: approve, edit (criterion), reject suggestion (manual mark), request re-evaluation, add instruction/clarification, add alternative answer, add exception rule (S), flag AI error, escalate to HoD | M |
| HITL-03 | HoD adjudicates escalations and moderates samples blind | M |
| HITL-04 | Rubric edits after lock follow the versioning flow (FR-RUB-08) | M |
| HITL-05 | Appeals are re-marked by another teacher, AI hidden (DEC-23) | M |
| HITL-06 | Corrections routed by taxonomy; no automatic model learning (DEC-17) | M |
| HITL-07 | Automation-bias safeguards (masked items, criteria-first, dwell-time monitoring) (DEC-33) | M |

## 20. Curriculum Requirements
FR-CUR-01..04. Versioned curriculum packs as data. Templates for SSC-format papers and class tests. Support for yearly textbook revisions (chapter lists per academic year). No PI/BI (NCF 2021) features (CON-09). Monitor the 2028 curriculum (RSK-10). Details: `08-data-curriculum-security-privacy.md` §2.

## 21. Data Requirements
- DATA-01 (M): Data inventory, classification and retention per `08` §3–4 (DEC-30).
- DATA-02 (M): Identity data separated from script content (pseudonymous script IDs) (DEC-14).
- DATA-03 (M): Gold and evaluation datasets built only from consented data (FR-ORG-06 b), versioned and frozen per release (06 §3).
- DATA-04 (M): Metering data per page/script for billing and cost analysis.
- DATA-05 (M): Correction events stored with taxonomy for analytics and scoped knowledge (07).
- DATA-06 (S): Analytics aggregates exclude cohorts <10 students when shown outside the teacher's own class.

## 22. Analytics Requirements
FR-ANL-01..04, FR-AIQ-01..02. Product analytics (internal): funnel per exam (setup → capture → review → publish), time per item, feature usage, errors. **No product analytics events contain student names or answer content.**

## 23. Security Requirements (summary; details in `08` §5 and TRD §21)

| ID | Requirement | Pri |
|---|---|---|
| SEC-01 | RBAC with school, subject and section scoping, enforced at API and database (row-level security) | M |
| SEC-02 | Tenant isolation tests in CI; no cross-tenant queries possible from the app role | M |
| SEC-03 | TLS 1.2+ everywhere; encryption at rest for DB and object storage; per-tenant data keys for script images | M |
| SEC-04 | OTP for new device, publish, unlock, role changes | M |
| SEC-05 | Support access time-boxed, approved, logged | M |
| SEC-06 | Secrets in a managed vault; no secrets in code or on devices | M |
| SEC-07 | Device storage encrypted; remote wipe of the capture queue on account disable | M |
| SEC-08 | Rate limiting, file-type validation, malware scanning on uploads | M |
| SEC-09 | Prompt-injection defences (AI-REQ-08) | M |
| SEC-10 | Append-only, hash-chained audit log | M |

## 24. Privacy Requirements

| ID | Requirement | Pri |
|---|---|---|
| PRV-01 | School is controller/fiduciary; vendor is processor; a DPA is signed before onboarding | M |
| PRV-02 | Parental/guardian consent recorded per student (VF-12); no AI processing without consent (L0) | M |
| PRV-03 | Data minimisation: no names on answer pages; no NID; only fields needed | M |
| PRV-04 | Purpose limitation: marking and results; improvement uses only opted-in data (DEC-13) | M |
| PRV-05 | External AI receives only de-identified answer regions; vendors on no-training terms; ZDR where available | M |
| PRV-06 | Retention per DEC-30; deletion certificates | M |
| PRV-07 | Data subject rights via school (access, correction, deletion, objection to automated decisions: satisfied by human confirmation of every mark, and human re-mark on request) | M |
| PRV-08 | DPIA before pilot; breach response plan with school notification ≤72 h of confirmation | M |
| PRV-09 | Hosting per DEC-12 after legal opinion | M |

## 25. Admin Requirements
FR-ADM-01..06, FR-ORG-01..07. Platform admin needs: tenant provisioning ≤15 min; curriculum pack publishing; capability level management; incident banner; usage export for finance.

## 26. Teacher Requirements
Key: question-wise review (FR-REV-01), evidence-first card (FR-REV-02), fast actions (FR-REV-03/04/08), manual mode (FR-REV-10), rubric templates (FR-RUB-02), clarifications applied forward (FR-HITL-02), phone usability (DEC-20), Bangla UI (DEC-24). **Teachers never type totals or copy marks.**

## 27. Student (and Parent) Requirements
No accounts in MVP. Students need: no name on pages (DEC-14); an item-level slip (FR-FBK-01); a fair re-check (FR-APL); consent via guardian (PRV-02); results unaffected by handwriting legibility bias (06 §4.4 subgroup gates).

## 28. Institution Requirements
Predictable cost (allowance + alerts: FR-ADM-04); control over AI levels (FR-AI-01, lower only); moderation (FR-MOD-01); audit for disputes (FR-ADM-03); export to ERP (FR-EXP-01); DPA and consent kit (PRV-01/02); a Bangla training pack and onboarding ≤1 week.

---

## 29. Acceptance Criteria (release-level)

| Release | Acceptance |
|---|---|
| MVP (G1) | All **M** FRs and NFRs pass their criteria. Security pen test with no High findings open. DPIA approved. Regression and red-team suites green. Result-engine fixture suite at 100%. Gate reports exist for every cell above L0. Bangla linguistic review done. Training material and runbook ready. |
| Pilot exit (G2) | Success metrics §30 at pilot targets in ≥3 schools; zero data incidents; appeals rate ≤ school baseline. |
| Production (G3) | NFR SLOs held for 2 consecutive months; support staffed for the exam season; billing live. |

## 30. Success Metrics

| Type | Metric | Definition | Pilot target | Guardrail |
|---|---|---|---|---|
| **North Star** | Published scripts | Scripts marked in-app, moderated and included in published results, per term | 10,000 (pilot term) | — |
| Outcome | Teacher time per script | Minutes (marking + totalling + mark entry), time-motion vs baseline | −30% | Never worse than baseline for any cohort |
| Outcome | Results turnaround | Working days from last exam to publication | −5 days | — |
| Quality | Per-cell AI agreement | vs gold (06 §4) | Gate met | Demote on breach |
| Quality | Severe unflagged error rate | Audited AI-suggested items where the suggestion differs from the adjudicated mark by ≥50% of item max (or ≥2 marks) **and** the item was not flagged | ≤0.5% | >1% → demote cell |
| Quality | Masked-item agreement gap | Agreement (teacher, AI) on unmasked minus masked items | Monitor | >10 points → automation-bias review |
| Trust | Appeal rate | Re-check requests per 1,000 scripts | ≤ baseline | — |
| Adoption | Active markers | % assigned teachers who complete ≥80% of their items in-app | ≥70% | — |
| Usability | SUS | Teacher survey | ≥70 | — |
| Economics | AI cost per 10-page script | Metered | ≤ BDT 3.0 | ≤ BDT 6.0 |
| Commercial | Paid conversion | Pilot schools converting to annual plan | ≥3 | — |

## 31. Risks
See `10-registers.md` §3 (RSK-01..20). Top 5 for the PRD: RSK-01 (Bangla HTR), RSK-14 (capture overhead), RSK-11 (teacher non-use), RSK-17 (price ceiling), RSK-16 (legal uncertainty).

## 32. Dependencies

| Dependency | Needed for | Risk |
|---|---|---|
| Legal opinion (Bangladeshi counsel) | Hosting, consent text, DPA | Gate G0 |
| 3–5 design-partner schools with consent | Gold data, pilots | ASM-18 |
| Paid annotators (senior teachers) | EXP-01 gold labels | Budget |
| LLM vendor accounts with no-training terms (≥2 vendors) | AI | Vendor terms |
| SMS gateway (Bangladesh) | OTP, notifications | Low |
| NCTB mark distribution documents; sample papers | Templates | Low |
| ERP partner cooperation | EXP-11 | Medium |

## 33. Assumptions
See `10-registers.md` §2 (ASM-01..22). Critical: ASM-02 (capture time), ASM-04 (time saving), ASM-05 (WTP), ASM-08 (legal), ASM-09 (VLM capability).

## 34. Open Questions
See `10-registers.md` §6. PRD-owned: OQ-18 (teacher analytics policy), OQ-19 (AI-off tier), OQ-21, OQ-22.

---

## 35. Commercial Requirements and Go-to-Market Implications

*(Pricing belongs here, not in technical documents. Technical documents only require metering and billing support.)*

### 35.1 Buyer and purchase
- Buyer: owner/MD or SMC. Champion: coordinator/academic head. Veto: teachers (through non-use), ICT (technical) (EV-07).
- Purchase: annual prepaid invoice, paid by bank transfer or cheque; budget window Nov–Jan (EV-13). bKash/Nagad only for small coaching centres.

### 35.2 Pricing model (hypothesis, DEC-36; tested in EXP-06)
- **Unit:** AI-assisted script (any script with ≥1 item at L1+ processed by AI). Manual-only (L0) scripts and results processing are included in the platform fee, so the non-AI core is never penalised.
- **Plan shape:** annual platform fee including an allowance of AI-assisted scripts, plus overage per script, plus a priority-mode surcharge. Allowances never "unlimited" (EV-26).
- **Price points to test:** BDT 6 / 8 / 10 / 12 per AI-assisted script; per-student alternative BDT 200 / 300 / 400 per year (Grades 9–10). Pilot fee BDT 5,000–10,000, credited (DEC-19).
- **Floor constraints:** AI cost ≤ BDT 3 per script (DEC-18) → ≥65% gross margin at BDT 8+. Teachers review (DEC-26), so there is no vendor labour cost.
- **Anchors to use in sales:** time saved, results turnaround, dispute reduction. Board examiners are paid Tk 35–40 per script (VF-09) as a reference for the market value of marking; no staff-cut pitch.

### 35.3 Beachhead and sales process
1. Target list: 60–100 Dhaka private schools meeting the §7 profile.
2. Founder-led discovery (EXP-06 doubles as the pipeline).
3. Live demo on the school's own scripts in demo mode (≤60 s per script) (FR-PRC-04).
4. Paid pilot on one exam (1–2 sections × 2 subjects), with parallel manual marking of a sample to measure agreement and time.
5. ROI report to the owner/SMC.
6. Annual contract signed Nov–Jan.

Channels after product-market fit: ERP co-sell (15–20% share, Phase 4), regional resellers.

### 35.4 Pilot requirements (product must support)
- Pilot report generated from product data: time per script (from review telemetry plus the baseline measurement), turnaround, agreement between AI suggestions and final marks, moderation agreement, appeals, usage.
- A parallel-marking import (teacher paper marks) to compute agreement on a sample.
- Onboarding ≤1 week: roster import, templates, 90-minute teacher training (Bangla video + in-person), capture station set-up guide.

### 35.5 Customer success requirements
- Exam-season support hours (Bangla), WhatsApp-based support channel, in-app help in Bangla.
- Health signals: active markers, % items reviewed in-app, capture backlog, override spikes.
- Term review with the principal using FR-ANL-04 and FR-AIQ-01.

---

## 36. Product Roadmap (Phases 0–5)

Calendar anchored to the Bangladeshi school year: annual exams Nov–Dec; class tests Feb–Apr; half-yearly around Jun; test/pre-test exams Oct–Dec for Class 10.

| Phase | Window | Features | Technical capabilities | Dependencies | Risks | Success criteria (gate) |
|---|---|---|---|---|---|---|
| **0 — Validation** | Oct 2026 – Jan 2027 | None customer-facing. Research prototype: capture app alpha, annotation tool, bake-off harness. | Gold-set tooling; model harness across ≥2 vendors; CAS verifier prototype | Legal opinion; 3–5 design partners; annotators | Consent delays; data volume | **G0** (10-registers §5): EXP-01, -02, -03, -04, -06, -10 complete; kill criteria not triggered |
| **1 — MVP build** | Nov 2026 – Apr 2027 (overlaps Phase 0) | All **Must** FRs. Class-test alpha at design partners (Mar–Apr 2027). | Modular monolith; pipeline; review app; results engine; audit; metering; security baseline | G0 outcomes for AI levels | Scope creep; Bangla UI quality | **G1**: MVP acceptance §29 |
| **2 — Pilot** | May – Aug 2027 (half-yearly exams) | Paid pilots at 5–10 schools; pilot report; first gate promotions to L2 | Gate workflow in operation; drift monitoring; support runbooks | Pilot contracts | Low adoption; capture overhead | **G2**: §30 pilot targets in ≥3 schools; ≥3 conversions |
| **3 — Production** | Sep – Dec 2027 (test + annual exams) | Should FRs: rubric dry run, AI rubric drafts, feedback drafts, SMS, invoices, answer-level analytics, cover-sheet mark capture for paper-marked scripts; Higher Maths and Chemistry (gated); L3 for eligible cells | Scale to 100k pages/day; billing; SOC-style controls | Pilot learnings | Seasonal peaks | **G3**: SLOs; cost ≤ BDT 2.5; 20–40 paying schools |
| **4 — Expansion** | 2028 | More subjects (English EV, Biology, ICT); Grades 6–8 / 11–12; coaching package; ERP API; parent portal; question-paper builder; Bangla prose L2 where gated; 2028 curriculum packs | Partner API; multi-region option; in-country deployment option if required | 2028 curriculum; ERP partners | Curriculum change; competition | Revenue and retention targets set at G3 |
| **5 — Advanced AI** | 2029+ | Answer grouping; specialist Bangla HTR fine-tuned with opted-in data; diagram assistance; low-stakes autonomous practice marking (if DEC-05 conditions met) | Training pipeline with consent enforcement; model evaluation at scale | DEC-13 conditions | Legal | Measured gains on the frozen benchmark |
