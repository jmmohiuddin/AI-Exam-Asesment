# Comprehensive Product Architecture and Strategy Report: AI-Powered Examination Assessment and Academic Intelligence Platform

- **Drive ID (primary, later version, modified 17:41):** `1XlHNbHPLpgCwDU8FejqyR7uXgt7RmAdin21hk1no6W0`
- **Drive ID (earlier version, modified 16:55):** `1Fv0n2nVySe4ZR7j_hWesHRYpK7sXMPNlkl7tREWJVIY` (material differences are in the "Differences vs earlier version" section below)
- **Topic:** Product vision, personas, JTBD, current and future exam workflow in Bangladesh, MVP options, information architecture, state machine, human-AI boundaries, review-console UX, screen inventory, security/RBAC, analytics, localization, competitor benchmark, KPIs, roadmap, risks and assumptions for an AI-assisted paper-script grading platform.
- **Method:** I read both Google Docs in full through the Drive connector: about 74k characters (later) and 67k characters (earlier), including the reference lists. I cross-checked their internal consistency and recomputed the arithmetic (RICE scores, thresholds). I compared the two versions section by section. I did not verify any external claim on the web. Everything marked **[Analyst note]** is my judgement, not the document's.
- **Nature of source:** The document shows the usual signs of an AI "deep research" output: generic enterprise phrasing, `[cite: 4, 5]` placeholder artifacts, few in-text citations, and a reference list heavy on ResearchGate, Scribd, G2/Capterra and blogs. It has no primary research: no interviews, pilots or measured data.

---

## Main findings

1. **Positioning.** The product is explicitly "**not** an unsupervised automated grading bot" but an "**AI-powered assessment intelligence platform**" that acts as "an expert co-pilot for teachers and an operational intelligence engine for educational institutions". It is framed as an "end-to-end operational and analytical intelligence layer" that turns physical or digital scripts into "verified results and pedagogical insights".
2. **Vision statement (verbatim):** "To transform educational assessment from a slow, administrative burden into an instant, fair, and evidence-grounded intelligence ecosystem that improves teacher efficiency and accelerates student learning outcomes."
3. **Core technical stack claimed:** computer vision, "layout-aware OCR", multimodal LLMs "fine-tuned on curriculum-specific rubrics", and a human-in-the-loop (HITL) review workflow. The headline claim is that it "reduces grading cycles by up to 70% while improving inter-rater reliability".
4. **Bangladesh-specific hooks:** NCTB "Srijonshil" (Creative Question, CQ) evaluation, Bangla-English mixed-script OCR, low-bandwidth resilience, and "board-compliant" tabulation sheets mirroring Dhaka/Rajshahi Board ledgers.
5. **Traditional vs proposed:** turnaround "2 to 4 weeks for school internal exams; 6 to 8 weeks for public board examinations" → "within hours"; "99%+ consistency across evaluated cohorts"; insights → "item-level diagnostic analytics; taxonomy-mapped skill tracking (Bloom's/NCTB); automated pedagogical intervention plans".
6. **Problem → module:** grading fatigue → Confidence-Routed Review Queue ("60–80%" less burden); subjective bias → Double-Blind Verification Engine; Srijonshil misalignment → NCTB 4-Tier Rubric Parser; tabulation errors → Automated Tabulation Engine ("100% mathematical accuracy", ERP sync).
7. **Personas (four detailed; ecosystem map also names External Board Examiners, IT Admins and Parents without personas):**
   - **Senior Subject Teacher/Examiner:** 4–6 classes, >250 students, moderate literacy, smartphone-first. Fears misread handwriting, lost partial credit for maths steps, misread regional phrasing. Demands "complete decision authority over every score"; success = "70% reduction in grading time".
   - **Examination Controller:** high literacy; 100% accurate tabulation, immutable audit logs, fewer re-scrutiny appeals.
   - **Principal:** early view of weak subjects; "verifiable executive dashboards rather than ungrounded predictions".
   - **Student (Grades 6–12):** question-level justifications; scanned script beside the rubric.
8. **JTBD matrix.** Each persona's job maps to one screen: Teacher → REV-01, Controller → TAB-01, Principal → ANALYTICS-01, Student → STU-01. Example trigger: "150 handwritten scripts arrive after a term exam"; outcome "Grade papers in half the time without scoring drift".
9. **Current Bangladesh workflow.** Said to span "14 distinct operational steps", but only **10** are listed: Word authoring to NCTB guidelines → printing/sealed envelopes → 2–3 hour exam → collection and roll sorting → controller allocates bundles → red-pen marking → cover-sheet transcription → scrutinizer re-adds onto ledgers → operators type into Excel/ERP → report cards and notice board.
10. **Future workflow gains claimed:** "60–70% reduction in evaluation time"; tabulation "from days to minutes"; "100% math accuracy"; OCR-based roll-number mapping "eliminates script loss".
11. **Service blueprint (5 layers):** frontstage (setup portal, mobile scanning, review console, tabulation/analytics); backstage (asset validator, **Celery/Redis** async queue, UI renderer, ERP sync/export); human checkpoints (controller approval, scan verification, teacher override, scrutinizer sign-off); AI (layout parser/deskewer, "Bangla-STEM Hybrid OCR", LLM rubric evaluator, confidence calibration); data (encrypted image vault, anonymized embeddings in a vector store, immutable audit log, ERP DB sync).
12. **MoSCoW scope.** Given verbatim in the "Proposed MVP" section below.
13. **Five design principles:** (1) Teacher Sovereignty; (2) Radical Explainability / visual evidence grounding, with "Black-box scoring is strictly prohibited"; (3) Calibrated Uncertainty over Blind Confidence; (4) Zero-Loss Tabulation Auditability; (5) Localized Technical and Contextual Resilience (client-side compression, offline queue, Bangla-English support).
14. **Four MVP options:** A, pure AI grading plugin (desktop PDF) rejected for ignoring ingestion and tabulation; **B, Ingestion + Verification + Tabulation: SELECTED**; C, full exam suite (authoring, printing, seating, parent app) rejected as bloat; D, ERP analytics layer rejected as "garbage-in, garbage-out".
15. **Information architecture.** Tenant hierarchy: Platform Tenant → School → Campus → Academic Year → Class → Section → Subject → Assessment → Student → Script Answer. Seven navigation areas: Dashboard, Assessment Management (question-paper parser, rubric architect), Ingestion & Batch (capture, monitor, Student ID Resolver), Review REV-01 (confidence queues, **Answer Grouping Workspace**, verification console), Tabulation TAB-01, Analytics ANALYTICS-01 (including "difficulty index, distractor stats"), Administration (including an AI performance dashboard).
16. **Core flow:** teacher creates assessment and rubric → staff mobile batch scan → AI OCR/segment/score → teacher reviews flagged answers (REV-01) → controller audits the ledger (TAB-01) → publish.
17. **State machine:** DRAFT → READY_FOR_INGESTION → INGESTION_PROCESSING → CONFIDENCE_ROUTED → {AUTO_VERIFIED (C≥0.85) | GUIDED_REVIEW (0.60–0.85) | MANUAL_REVIEW (<0.60)} → REVIEW_COMPLETED → TABULATION_LOCKED → PUBLISHED. Useful invariants: rubric points = max marks; frames pass blur/lighting checks; roll number mapped or flagged; every override has a reason tag and user ID; 100% verified before lock; published grades immutable except via formal re-scrutiny.
18. **Automation levels (5):** MCQ bubble sheets **Fully Automated**; short formula/numeric maths **AI-Assisted** (batch approve, spot checks); NCTB CQ **AI-Suggested (HITL)** (teacher confirms sub-marks (a)–(d)); open essay/diagram **Human-Approved** (AI only extracts/highlights; auto-publish blocked); tabulation **Fully Automated** with a ∑sub-marks == total parity check.
19. **REV-01 layout:** 60/40 split, with the script viewer and SVG bounding boxes on the left (Green #28A745 satisfied, Amber #FFC107 partial, Red #DC3545 incorrect/unreadable/crossed-out) and the rubric workspace on the right. Keyboard-first controls: Space approves and moves to the next script; 0–9 sets the score; E opens the reason tag; F flags; ←/→ navigates. The header example shows "Script 42/150" and "Confidence 88%". Review is **script-by-script (vertical)** in this version.
20. **Screen inventory:** 11 screens (see the architecture table).
21. **Confidence-tier UX:** High = pre-approved into a batch queue ("Optional spot-check sample; single batch approval"); Medium = guided review with pre-selected rubric items; Low = AI suggestion suspended, "Blank Score Canvas".
22. **Edge cases:** missing page (PAGE_SEQUENCE_ERROR), unmapped roll number, crossed-out block, mixed Bangla-STEM line (joint parser), **prompt injection written by a student** (confidence set to C=0.0 and a TAMPERING_ALERT raised), and network loss during review (IndexedDB cache and sync).
23. **Security:** TLS 1.3, AES-256 at rest. **Automated double-blind masking** of the name, gender and roll number header (e.g., "STU-88392"), unblinded only after publication.
24. **RBAC (6 roles):** Super Admin, School Admin, Exam Controller, Senior Teacher, Scrutinizer, Student/Parent. Only the Super Admin and the Controller can publish; students see only their own scripts.
25. **Analytics tiers:**
    - Teacher level: Bloom radar chart, misconception clustering (worked example: "42% of students incorrectly applied v=u−at instead of v=u+at"), and auto-generated remedial plans.
    - Leadership level: subject and teacher performance curves, "Curriculum Coverage Efficiency".
    - Engineering level: Confidence Calibration Index, inter-rater reliability.
26. **Accessibility:** WCAG 2.1 AA, high-contrast mode, keyboard-only operation, 400% zoom.
27. **Localization:**
    - Srijonshil structure: 10 marks per CQ, split as (a) Knowledge/Gnan 1, (b) Comprehension/Anudhaban 2, (c) Application/Proyog 3, (d) Higher-order/Uchchator 4.
    - A joint Bangla-English OCR "trained on regional handwriting datasets" (no dataset is named).
    - Board-format tabulation exports.
    - WASM client-side compression from "~5MB to <300KB" and an offline-first queue.
28. **Competitor benchmark:** Gradescope (Turnitin), generic LMS quiz engines (Canvas/Moodle), and local school ERPs (not named in this version). See the competitor table below.
29. **Differentiation claims:** "Native Framework Integration (Blue Ocean Opportunity)" (because Western platforms "require rigid page templates"); evidence-grounded confidence routing; "Complete Administrative Closure" ("cryptographically audit-trailed" tabulation plus ERP sync); "Diagnostic Academic Intelligence (Value Multiplier)".
30. **Usability plan:** 20 secondary teachers (Bangla and English medium), 5 controllers, 3 principals. Scenarios: Srijonshil rubric for a 100-mark **Physics** exam, scan 50 scripts, review 50, override and publish. Thresholds: ≥90% completion; **<25 s per multi-part creative paper (target <12 s)**; <3 keypresses per edit; NASA-TLX <40 (target <25); SUS >75 (target >88).
31. **North Star metric:** "The total number of student answer scripts successfully processed and teacher-verified through the platform per academic term."
32. **KPIs:** time to first assessment setup <15 min; ≥60% teacher time saved; ≥92% first-pass AI-teacher agreement; <0.1% severe unflagged errors; ≥90% term-over-term school retention.
33. **Roadmap:** **Phase 1 MVP (months 1–6):** mobile capture with WASM compression; OCR for **"printed English/Bangla text and handwritten digits"** only; Srijonshil rubric engine; confidence-routed review console; PDF/Excel tabulation. **Phase 2 (7–12):** answer grouping; class learning matrix and teacher diagnostics; regional ERP APIs; student feedback portal; **offline-first PWA queue**. **Phase 3 (13–24):** OCR for maths derivations and diagrams; AI draft rubrics; multi-branch benchmarking; appeals.
34. **RICE scores (arithmetic verified correct):** Srijonshil Rubric Builder 13.5; Confidence Review Queue 10.8; Mobile Capture 9.0; Short Answer Grouping 4.3; Student Diagnostic Portal 4.2; AI Draft Rubric 1.5. The inputs are invented; there is no reach data.
35. **Risks:**
    - AI misreads handwriting (High/High) → confidence routing and evidence.
    - Teacher resistance (High/Medium) → co-pilot positioning.
    - Data leak (High/Low) → encryption and masking.
    - Rural outages (Medium/High) → offline PWA.
36. **Assumptions table:** see the Assumptions section. The key cited "evidence" is "79.7% of educators agree AI workflows improve fairness when transparent", with no source.
37. **Decision framework answers:** primary user = Senior Subject Teacher; economic buyer = "School Management Committee, Principal, or Regional Educational Board Officer"; fully automated = deskew, page order, MCQ, summation, ledger; approval required = all Srijonshil answers, essays, overrides, publication; most important screen = REV-01; highest-risk workflow = **ingestion and student identification**; biggest UX risk = fatigue; biggest adoption barrier = teacher scepticism about Bangla handwriting. "Wow" line: "reduced our term exam grading and tabulation cycle from 3 weeks to 2 days … gave every parent a detailed diagnostic breakdown … on day one."
38. **Pricing.** There is **no pricing, revenue model, willingness-to-pay or market-size figure anywhere** in this document, in either version.
39. **Sources listed (later version):** ResearchGate (CQ structure; SSC CQ analysis; Gradescope paper), Gradescope guides, G2, Capterra, blog reviews, Emerald (private tutoring in Bangladesh), Scribd, a guidebook seller and an SDG report. They are thin and secondary, and most concern Gradescope.

---

## Quantitative claims table

| Claim | Value | Source cited | Source type | Credibility H/M/L + why |
|---|---|---|---|---|
| Reduction in grading cycle / effort | "up to 70%"; elsewhere 60–80% and 60–70% | None inline | Assertion | **L**: three different ranges in one document; no pilot data. |
| Consistency of AI scoring | "99%+ consistency across evaluated cohorts" | None | Assertion | **L**: undefined metric; consistency ≠ accuracy; no model exists yet. |
| Turnaround today | 2–4 weeks (school internal); 6–8 weeks (board) | None | Assertion | **M**: plausible order of magnitude for Bangladesh; unsourced. |
| Tabulation accuracy | "100% mathematical accuracy" | None | Design claim | **M/H** for arithmetic summation (deterministic code); **L** as a claim about end-to-end marks, which depend on OCR of roll numbers and marks. |
| Teacher load | 4–6 classes, >250 students; 150-script batches | None | Persona assumption | **M**: plausible; not researched. |
| Current workflow | "14 distinct operational steps" | None | Assertion | **L**: only 10 are listed (internal inconsistency). |
| Confidence thresholds | High ≥0.85; Medium 0.60–0.85; Low <0.60 | None | Design parameter | **M** as a starting design; **L** as validated values (no calibration data; the earlier version used 0.88/0.70). |
| Image compression | ~5MB → <300KB via WASM | None | Technical estimate | **M**: achievable with JPEG/WebP; OCR legibility at 300KB for a dense Bangla page is unverified. |
| Usability thresholds | <25 s per multi-part CQ paper (target <12 s); SUS >75 (>88); NASA-TLX <40 (<25); ≥90% completion | None | Target | **L**: 12–25 s for a full multi-part creative paper is implausible for genuine verification (see critique). |
| Usability cohort | 20 teachers, 5 controllers, 3 principals | Plan | Plan | **H** as a plan; not executed. |
| KPIs | <15 min setup; ≥60% time saved; ≥92% agreement; <0.1% severe unflagged errors; ≥90% retention | None | Target | **L/M**: aspirational; ≥92% agreement on Bangla handwritten CQs is unproven. |
| Educator attitude | "79.7% of educators agree AI workflows improve fairness when transparent" | "Studies show" (none named) | Unattributed statistic | **L**: false precision, no source; likely hallucinated or taken out of context. |
| Srijonshil marks structure | 1+2+3+4 = 10 per CQ | ResearchGate "Structure of creative question" | Academic / secondary | **H**: matches the standard NCTB CQ format. |
| RICE scores | 13.5, 10.8, 9.0, 4.3, 4.2, 1.5 | Internal | Invented inputs | **M** arithmetic (checked correct); **L** inputs (no reach data). |
| Roadmap timing | MVP 1–6 months; V1 7–12; V2 13–24 | None | Plan | **L/M**: MVP scope includes Bangla handwriting OCR, which is research-grade; 6 months is optimistic. |
| Headline outcome | "3 weeks to 2 days" | None | Aspirational quote | **L**: illustrative marketing line. |

---

## Proposed MVP / scope (exactly as proposed) and critique

**As proposed (MoSCoW, later version):**
- **MUST HAVE (MVP Core):**
  1. Mobile and flatbed script ingestion via PWA queue.
  2. Layout-aware Bangla-English STEM OCR engine.
  3. NCTB Srijonshil 4-tier rubric setup engine.
  4. Confidence-routed teacher review workspace (REV-01).
  5. Automated master tabulation sheet export (PDF/Excel).
- **SHOULD HAVE (V1):** answer grouping for short responses; school ERP and LMS roster SSO integration; student feedback portal with annotated script viewer; class-level topic learning gap matrix.
- **COULD HAVE (V2):** AI draft rubrics from question papers; audio feedback annotations; predictive board-exam modelling; student appeal workflow.
- **SHOULD NOT HAVE:** fully autonomous unsupervised publishing; live webcam proctoring; conversational admin chatbots.
- **Minimum viable journey:** Create Assessment Metadata → Define 4-Tier Rubric → Mobile Scan Scripts → Review Flagged Answers → Export Tabulation Sheet.
- **Grades:** the student persona covers Grades 6–12 (secondary and higher secondary). No MVP grade band is specified.
- **Subjects:** not specified for the MVP. Physics is used in the usability scenario and in the maths misconception example. STEM plus Bangla is implied by the "Bangla-English STEM OCR".
- **Question types in scope:** MCQ/OMR bubble sheets (fully automated), short formula/numeric, NCTB CQ (a)–(d), open essay/diagram (human-approved). The document never says which of these are in the MVP.

**Critique [Analyst note]:**
- **Too broad for an MVP, and internally contradictory.** The Must list bundles five hard problems into six months: mobile capture and page assembly; roll-number/identity resolution; Bangla + English + maths handwriting recognition; LLM scoring with *calibrated* confidence; and a tabulation/publishing workflow. Each is a product on its own, and handwritten Bangla OCR on unconstrained scripts is an open research problem.
- **The roadmap quietly contradicts the MVP.** The Must list says "Bangla-English STEM OCR", but Phase 1 of the roadmap delivers only "OCR for printed English/Bangla text and **handwritten digits**". Handwritten Bangla prose, which is what CQ answers are, is therefore *not* in the Phase 1 deliverable. Either the MVP cannot grade CQs or the roadmap is wrong; this is the most important scoping inconsistency.
- **Offline is in the principles and risk mitigation but pushed to Phase 2.** The risk matrix relies on the "Offline-First PWA Queue" to mitigate rural outages, yet the roadmap ships it in months 7–12.
- **Answer grouping and the student portal leak into the MVP.** The navigation puts an "Answer Grouping Workspace" inside REV-01, and the publish step "publishes results to student portals", but both features are V1.
- **No grade, subject or question-type cut.** A credible MVP would pick, for example, one grade band (9–10), one or two subjects, and a narrow question type (maths/physics CQ parts (c)/(d) with numeric working, or short answers), and would defer free-form Bangla prose. The document picks none.
- **Tabulation/publishing is a separate operations product** that could ship *before* AI grading as a wedge capturing item-level marks; the document couples it to AI grading.

---

## Proposed product architecture / modules

| Module / Screen | Function | Phase in doc |
|---|---|---|
| AUTH-01 | SSO, multi-tenant school selector, MFA | MVP (implied) |
| EXAM-01 Assessment Builder + Question Paper Parser | Metadata; PDF/image upload; sub-question extraction | MVP |
| RUBRIC-01 Rubric Architect | NCTB 4-tier criteria, point weights, keyword tags; invariant: rubric sum = max marks | MVP |
| SCAN-01 Mobile Ingestion (PWA) | Edge detection, blur check, perspective correction, WASM compression, batch upload | MVP (offline queue V1) |
| BATCH-01 Processing Monitor + Student ID Resolver | OCR progress, failed scans, unmapped roll numbers | MVP |
| AI pipeline | Layout Parser/Deskewer → Bangla-STEM hybrid OCR → LLM rubric evaluator → confidence calibration (C∈[0,1] per sub-question) | MVP |
| REV-01 Central Review Console | 60/40 split, SVG evidence boxes, keyboard-first, confidence queues | MVP (core screen) |
| TAB-01 Master Tabulation Ledger | Auto-sum, anomaly/override audit, grade lock, PDF/Excel export, ERP sync | MVP (ERP sync V1) |
| ANALYTICS-01 | Bloom radar, misconception clustering, item difficulty, concept gap matrix | V1 |
| STU-01 Student/Parent viewer | Marked script, rubric checklist, comments | V1 |
| DASH-01/02, Admin, AI Performance Dashboard | Executive and teacher dashboards; RBAC, CSV rosters; OCR accuracy/agreement/latency | Unclear |
| Infrastructure | Celery/Redis async queue; encrypted object store; vector store for embeddings; append-only audit ledger; relational DB; ERP sync | MVP |

---

## Competitors (as presented in this document)

| Name | Country | Segment | What they do (per doc) | Pricing | AI grading of handwriting? | Bangla? | Source / credibility |
|---|---|---|---|---|---|---|---|
| Gradescope (Turnitin) | US | Higher-ed STEM | Dynamic point rubrics; AI answer grouping; "basic question item statistics" | Not stated | "English text and single-line math equations"; "Requires strict fixed-template paper layouts for AI grouping" | No | Gradescope guides, G2, Capterra, blog review. **M**: the template requirement is partly true (fixed-template assignments for AI grouping per Gradescope's formatting guide), but "basic auto-grading" undersells it. |
| Canvas / Moodle quiz engines | US / global | Digital LMS | Online MCQ/essay, rule autograding | Not stated | None | No | No specific source. **M**: generic. |
| "Local School ERP Systems" (unnamed here) | Bangladesh | School admin | Records, fees, manual mark entry | Not stated | None | UI only | No source. **M**. The earlier version named Eduman and ClassTune. |

The document names no Indian AI graders (GradeFoundry, VedaAI, Saraswati AI, etc.). Its competitive picture is therefore much thinner than D2's. See D0.

---

## Assumptions

Stated in the document:
1. "Teachers will accept AI scoring suggestions if visual evidence is provided." Rated High confidence / High risk; the evidence is the unsourced 79.7% figure; to be validated by REV-01 usability tests.
2. "Mobile smartphone cameras can capture sufficient script image quality." High / Medium; the evidence is a WASM deskewing claim (not evidence); to be validated by field tests on low-end Android phones.
3. "Schools will pay for assessment platforms that reduce tabulation labor." Medium / High; "Institutions spend significant budget on manual scrutiny and tabulation overtime" is unsourced; to be validated by pilot sales with school management committees.

Implicit (my extraction):
4. Srijonshil CQ remains the dominant assessment format for grades 6–12. [Analyst note] This is currently true again after the 2024 rollback, but policy is volatile; see the critique.
5. Schools have staff to scan scripts, rosters with roll numbers, and a controller/scrutinizer function (a large-school assumption).
6. LLMs can produce *calibrated* confidence per sub-question that is deterministic.
7. Double-blind grading is desirable and feasible in schools where teachers grade their own sections.
8. Schools use ERPs with integrable APIs.
9. The principal or SMC is the buyer, and the teacher is the user.
10. Board-format tabulation sheets are relevant to internal school exams.

---

## Recommendations (as made by the document)

- Build MVP Option B (ingestion + verification + tabulation). Position it as a HITL co-pilot. Never auto-publish.
- Invest first in REV-01, the "Core UI Investment", which it credits with driving "70% evaluation speed increase".
- Automate deterministic tasks (deskew, page order, OMR, summation). Require approval for all CQ, essay and override actions.
- Route by confidence thresholds (0.85 / 0.60) and show visual evidence.
- Use "Verified scripts processed per term" as the North Star.
- Run the 28-person usability study with SUS and NASA-TLX.
- Exclude proctoring, chatbots and autonomous grading.

**[Analyst note]** Reuse the state-machine invariants, override-reason logging, prompt-injection handling and confidence-tier UX; they are the most reusable parts. Re-scope the MVP (one grade band, 1–2 subjects, constrained question types), treat Bangla handwritten prose OCR as a gated research spike, and drop batch auto-approve until calibration is proven.

---

## Open questions

1. Which grades, subjects and question types are in the MVP? (Not specified.)
2. Is handwritten Bangla prose OCR in Phase 1 or not? (The MoSCoW list and the roadmap conflict.)
3. How is confidence C computed and calibrated, and on what labelled dataset? "Deterministic" LLM confidence is asserted, not designed.
4. Where does training and evaluation data for Bangla-English handwriting come from, and who owns consent for student scripts?
5. Who scans: teachers, office staff, or a service? What is the per-script scanning labour, and does it eat the time saved?
6. Does double-blind masking make sense for internal exams where the teacher knows the class and the handwriting?
7. Are "board-compliant" tabulation sheets relevant? Board exams are marked by board-appointed examiners, not purchased by schools.
8. Pricing, willingness to pay, budget owner and sales cycle are entirely absent.
9. Which ERPs, and do they have APIs?
10. What is the policy and regulatory stance (the Bangladesh data protection framework, and the Ministry or boards' view of AI-assisted marking)?
11. What happens to physical scripts: is the digitised copy the record of truth for re-scrutiny?

---

## Critical assessment

- **Scope explosion.** The MVP spans capture, identity, trilingual handwriting OCR, LLM scoring, calibration, review UX, tabulation, ERP sync, and implicitly the student portal and answer grouping. There are 11 screens, 6 RBAC roles, 5 service layers, WCAG compliance, analytics, and prompt-injection defence. This is an 18–36 month platform presented as a 6-month MVP. The "Option C rejected as bloat" framing is ironic, because Option B as specified is close to C minus authoring and printing.
- **Unvalidated features presented as facts:**
  - "99%+ consistency", "100% mathematical accuracy", "60–80% reduction" and "≥92% agreement" are targets written as outcomes.
  - "Custom OCR model … trained on regional handwriting datasets" names no dataset.
  - "Cryptographically verifiable audit trails" is not designed.
  - "Deterministic" confidence from an LLM is a contradiction in terms without a separate calibration model.
- **Fabricated-looking statistics:** the "79.7% of educators", "42% of students…", "14 steps" (10 listed) and the `[cite: 4, 5]` artifact next to the North Star.
- **Implausible review speed.** A target of <12 s (threshold <25 s) per *multi-part creative paper*, which is 3–5 CQs of 4 sub-parts each plus MCQ, means under 1 s per sub-answer. That is rubber-stamping, not verification. The earlier version's "<12 s per answer block" is far more plausible, so the later version probably mis-edited it.
- **Automation-bias risk increased in the later version.** C≥0.85 goes to "Batch Auto-Approve" with an "Optional spot-check". This contradicts "Teacher Sovereignty" and the claim that all Srijonshil answers "require approval". The earlier version explicitly listed automation bias as a High risk with random mandatory checks; the later version dropped it.
- **Curriculum assumptions (outdated or volatile).**
  - [Analyst note] The document assumes that NCTB Srijonshil CQ (1+2+3+4) is the stable national format. It does not mention the 2021 competency-based national curriculum, which reduced traditional written exams in favour of continuous assessment, or its **rollback in late 2024**. After the rollback, the government reverted to the pre-2021 (2012) curriculum and CQ-based annual exams for grades 6–9 (the *earlier* version cites a Bangladesh Post item "Annual exams for grades 6–9 with creative questions: NCTB").
  - So the CQ assumption is *currently* correct, but for reasons the document does not understand. Further reform is possible, and a product hard-coded to 1+2+3+4 carries policy risk.
  - The rubric engine should be framework-agnostic, with CQ as a template.
- **Board confusion.** "Board-compliant tabulating sheets (Dhaka Board, Rajshahi Board)" and "Regional Educational Board Officer" as buyer conflate internal school exams (the realistic market) with public SSC/HSC exams. Those are marked under board control and are a different, government-procurement market.
- **Competitor claims.** The claim that Gradescope requires fixed templates while this platform is "template-free" is a strong differentiation claim with no technical basis. Template-free parsing of unconstrained handwritten booklets is much harder, and a fixed answer-sheet template (question boxes, QR roll ID) is arguably the *right* MVP choice. "Blue Ocean" is hype.
- **Hype language:** "Radical Explainability", "Zero-Loss", "absolute mathematical accuracy", "enterprise-grade", "Value Multiplier", "Blue Ocean".
- **Missing economics.** There is no pricing, cost per script, LLM/OCR cost, WTP, market size or sales motion.
- **Missing field research.** There are no teacher interviews, no observation of actual script formats (loose sheets, "Othirikto Khata", answer booklets), and no sample scripts.
- **Security and privacy.** There is no mention of Bangladesh-specific data protection, parental consent, data residency, or LLM vendor data use for minors' scripts.

---

## Differences vs earlier version (Drive ID `1Fv0n2nVySe4ZR7j_hWesHRYpK7sXMPNlkl7tREWJVIY`, 16:55)

The earlier version is organised as "Part 1–26" with numbered "Artifacts". The substance overlaps about 70%, but several product decisions differ materially:

1. **Review paradigm.** Earlier: **"Horizontal-First Workspaces"** is design principle #4. Review goes question-by-question across all students (e.g., all answers to Q3c), with a Student Vertical Script View as secondary; the mock-up shows "Q3: Kinetic Energy [CQ 3c] Reviewed 42/50". Later: script-by-script review ("Script 42/150"; Space moves to the next script) and horizontal review disappears. Bias control shifts from horizontal ordering to double-blind header masking. [Analyst note] Horizontal review is the better-evidenced pattern (Gradescope) and should not have been lost.
2. **Confidence thresholds.** Earlier: High ≥88%, Medium 70–87%, Low <70%. Later: 0.85 / 0.60. The later version is more permissive in both bands.
3. **Automation bias.** Earlier risk matrix: "Evaluators display automation bias, approving AI suggestions without review" (High), mitigated by "mandatory manual verification checks on randomly selected scripts". Later: the risk is removed and high confidence becomes batch auto-approve with an optional spot-check.
4. **Personas.** Earlier: 7 named archetypes: Nusrat Jahan (Physics teacher, 150+ scripts/cycle), Prof. Rafiqul Islam (Controller), Dr. A. K. Azad (Principal; cautious on ROI), Fahmida Khan (Coordinator), Tanvir Hossain (IT Admin; wants offline-first and REST APIs), Samin Ahmed (Grade 10), Jahangir Alam (Parent; SMS). Later: 4 unnamed personas plus JTBD; Parent and IT Admin dropped.
5. **Exam structure detail.** Earlier states "A standard 100-mark assessment allocates 30 marks to MCQs and 70 marks to Creative Questions". It names the stimulus (Uddipok) and the loose supplementary sheets (Othirikto Khata), and says head teachers recheck a "10% sample". Later drops these field details.
6. **Named BD ERPs.** Earlier names **Eduman and ClassTune** as incumbent ERPs and planned REST API connectors (V1); ERP sync appears in Flow 4 ("pushing final grade payloads directly to … Eduman via REST API"). Later says only "popular regional school ERP systems".
7. **MVP options.** Earlier A = manual digital grading tool (rejected: "insufficient efficiency gains"); D = API-only middleware into ClassTune/Eduman (rejected: "lack of direct UX control"). Later: A = desktop PDF plugin; D = ERP analytics layer.
8. **MVP boundary.** Earlier Must: "Mobile & Desktop batch scan ingestion"; "Bangla and English **handwritten** layout parser & HTR"; rubric builder; horizontal review with hotkeys; summation and CSV/Excel export. V1 adds SMS on publish and teacher consistency benchmarking; **answer grouping is V2** (V1 in later). Won't list adds **payroll/fees/HR**, printing control and **scanner driver development**.
9. **Roadmap.** Earlier: **MVP months 1–4** (desktop scan, Bangla/English HTR, rubric, horizontal review, export); **V1 5–8** (mobile scanner, Eduman/ClassTune connectors, heatmaps, student portal); **V2 9–12** (rubric co-pilot, calibration, answer grouping, question bank analytics); **13+** (cross-school benchmarking, predictive SSC/HSC modelling, remedial generators). Later: mobile-first 6-month MVP, 24-month horizon. The earlier version also contradicts itself: its Must list includes mobile, but its roadmap puts mobile in V1.
10. **HTR specifics.** Earlier names **GraDeT-HTR** (a decoder-only Transformer with a grapheme tokenizer). It cites "approximately 13,000 grapheme variations", conjuncts (Juktoborno) and the matra headline, and "isolated character accuracy is 96%+, page segmentation requires tuning". It targets **Bangla HTR Token Error Rate <4.5%** and benchmarks on "1,000 real student scripts". The later version drops the named model and error-rate targets in favour of a vague "custom OCR model".
11. **Three-layer vision (earlier only):** Assess / Analyze / **Improve**, where the Improve layer covers "automated student practice sets" and "institutional resource allocation guides". Later drops Improve.
12. **Active learning.** Earlier: override reasons ("Valid alternative scientific method", "Partial credit awarded", "OCR text extraction error") feed "the continuous model retraining pipeline". Later: audit only; no retraining loop is stated.
13. **Edge cases.** Earlier has missing loose sheet (Othirikto Khata), **answer written in the wrong area** (auto-remap Q2→Q4 with a toast), crossed-out text, mixed Banglish ("joint Banglish vocabulary decoding heads"), and blur (Laplacian variance <100). Later adds prompt injection, unmapped ID and network loss, and drops wrong-area remapping.
14. **RBAC.** Earlier has **Head of Department** (edit/lock rubrics, section sign-off) and the Principal as "Executive Sign-off"; students can "Request Appeal". Later has Scrutinizer and School Admin, drops HoD, and makes appeals a Phase 3 feature.
15. **Screen inventory.** Earlier: 8 modules and about 33 screens (adds a question bank/rubric library, a GPA calculator, a teacher equity benchmark, an appeal view, and HTR CER/token-cost monitoring). Later: 11.
16. **Competitor table.** Earlier: Gradescope ("Industry Gold Standard" horizontal review), **Eduman/ClassTune**, and **generic LLM chatbot wrappers**. Later swaps the chatbots for LMS quiz engines and adds the "fixed-template" criticism of Gradescope.
17. **Differentiation.** Earlier gives explicit Table Stakes / Differentiators / White-Space lists; white space includes "Institution-Wide Teacher Grading Calibration & Equity Benchmark" and "Automated REST API Gradebook Sync for Bangladesh Local ERPs". Earlier "Core Strategic Moat" = Bangla/English HTR + Srijonshil rubric engine + BD ERP connectors. Later moat = localization + confidence routing + diagnostic intelligence.
18. **RICE.** Earlier scores are **10× the formula** (e.g., 10×3×0.9/6 = 4.5, shown as 45.0), with Effort in person-weeks. They rank the horizontal review queue (57.0) and confidence routing (56.7) above ingestion (45.0), and list an appeal engine at 8.0 as "Should Not Have". The table contains `[cite: …]` artifacts. The later scores are arithmetically correct.
19. **KPIs.** Earlier North Star = verified *answers* processed **monthly**; **>4 exam cycles per school per month**; 65%+ time saved; Bangla HTR TER <4.5%; HAR >88%; severe discrepancy <0.5%; **NRR >115%**; >70% ERP integration. Later: per-term North Star, ≥92% agreement, <0.1% anomaly, ≥90% retention.
20. **Usability plan.** Earlier: 12 teachers (6 urban, 6 semi-urban), 2 controllers, 4 admins; targets >95% completion, <12 s per answer block, SUS >82, NASA-TLX <35.
21. **Risks and assumptions.** Earlier includes a **Commercial risk**: "Institutions resist purchasing software separate from existing ERPs", mitigated by a "plug-in Assessment Intelligence layer via API". Its assumptions: "Teachers prefer Horizontal Question Review" = "Strongly Validated (Global benchmarks like Gradescope confirm 3x speed gains)"; "Schools will pay…" = "In Progress (Strong demand driven by desire for automated ERP sync)" (no evidence given).
22. **Highest-risk workflow.** Earlier: "Optical text extraction and spatial layout parsing of variable Bangla handwriting". Later: ingestion and student identification.
23. **Offline spec.** Earlier: encrypted IndexedDB queue, WebP "up to 80%" size reduction, background resumable sync. Later: WASM 5MB→<300KB.
24. **Sources.** Earlier cites more technical and Bangladesh-specific material: arXiv HTR papers, Kaggle Bengali.AI, the NCTB site, Bangladesh Post (CQ annual exams for grades 6–9), TBS, ClassTune, Pathshalasoft. [Analyst note] It is the more technically grounded draft; the later one is more polished but less evidenced.

**Net:** The later version is not a strict improvement. It gained a state machine, prompt-injection handling, JTBD and correct RICE arithmetic. It lost horizontal review, the automation-bias safeguard, the named HTR approach and error-rate targets, the BD ERP names, the commercial risk, the active-learning loop and the field-level exam details.

---

## Confidence + Relevance to product decisions

- **Confidence in the document's factual claims:** **Low–Medium.** The Srijonshil structure and the generic workflow description are credible. Nearly all numbers are unsourced targets, and one statistic (79.7%) looks fabricated.
- **Confidence in the design content (UX, state machine, HITL boundaries):** **Medium–High** as a design starting point. The patterns are sound and industry-standard (Gradescope-like review, confidence routing, audit logs).
- **Relevance:** **High** for UX/HITL design, the review console, the state model, RBAC, edge cases and KPI definitions. **Medium** for MVP scope; the proposed Option B framing is useful, but the scope must be cut hard. **Low** for market, pricing and competition; see D2.
- **Most decision-relevant takeaways:**
  1. Resolve the Phase 1 OCR contradiction by deciding whether handwritten Bangla prose is in or out.
  2. Restore horizontal (question-wise) review and mandatory random spot-checks.
  3. Make rubrics framework-agnostic, with Srijonshil as a template.
  4. Treat tabulation and item-level mark capture as a possible early wedge.
  5. Commission real field research, sample scripts and pricing work, none of which exists in this document.
