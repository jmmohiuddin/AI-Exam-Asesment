# Comprehensive Data Strategy and Governance Framework for AI-Powered Educational Assessment Platforms in Bangladesh and International Jurisdictions

- **Drive ID:** 1zo9Blx60j-pQ4B1hIOu_VW7RVy8_dcPROJ2ixdLsN54
- **Topic:** Data strategy for a Bangladeshi AI exam-script grading platform. Covers data inventory, lifecycle, classification tiers, retention, minors' data and consent, Bangladeshi and international legal landscape, ownership and licensing, governance org, zero-trust access, acquisition and pilot plan, dataset sizes, representativeness, annotation and gold standard, feedback-loop poisoning defence, training-data reuse options, data moat, data quality metrics, storage architecture and schema, lineage, deletion, unit costs, build vs buy, ethics, roadmap, and a governance Q&A.
- **Method (as stated / inferred):** AI-generated deep-research synthesis (Gemini-style link list, stray `[cite: 10]` markers). No original data. Legal sources are mostly secondary or informal:
  - Scribd uploads of the "Bangladesh Personal Data Protection Ordinance, 2025" and a "Cyber Security Act 2023 overview".
  - A ResearchGate / Semantic Scholar paper titled "The Personal Data Protection Act, 2026 of Bangladesh, Privacy and Global Data Governance".
  - A ResearchGate paper on "Cyber Security Act 2026 in Bangladesh".
  - News: Prothom Alo "Govt issues gazette of Cyber Security Ordinance"; TBS News; Dhaka Tribune.
  - A lawyer's blog and **several Facebook posts**.
  - Also: FTC 2020 COPPA ed-tech blog, Public Interest Privacy Center (FERPA), FPF, EFF, TrustArc, Sanitized.ai, a NAEM blogspot page on the creative question, teachingbd24 (question-paper site).

  No official gazette or bdlaws.minlaw.gov.bd citation appears. The extraction covers 100% of the doc text (about 79k characters).

---

## Main findings

1. **Five pillars:** data minimization and zero-trust privacy; NCTB Srijonshil and multilingual alignment; gold-standard annotation; proactive compliance (Bangladesh plus GDPR/FERPA/COPPA); closed-loop data economics via active learning. Target market: primary, secondary and higher-secondary institutions in Bangladesh first, then international.

2. **Functional data tiers:**
   - Operational processing: scans, rubrics, tokenized IDs.
   - AI evaluation: gold benchmarks, predictions, confidence, token log-probs.
   - Model improvement: *fully de-identified* segments, bboxes, transcriptions, validated overrides.
   - Analytics/BI: aggregated.
   - System monitoring.
   - **Prohibited:** direct contact details, addresses, financial data, raw biometric templates, political or religious attributes.

3. **Data inventory with retention (Table 1):**

   | Data source | Elements | Sensitivity | Owner | **Retention** | AI usage |
   |---|---|---|---|---|---|
   | Student Identity Vault | Name, roll, registration no., class, section | Highly sensitive | Student/Institution | Duration of active contract | **Strictly prohibited** |
   | Institutional metadata | School name, EIIN, board, medium, address, admin | Confidential | Institution | **Contract + 7 years** | Aggregated analytics only |
   | Exam metadata | Subject, grade, year, term, marks, time | Internal | Institution/Platform | Indefinite | Prompt context |
   | Questions & marking schemes | Stems, model answers, step rubrics | Internal | Institution/Board | Indefinite | Prompt conditioning & embedding |
   | Raw answer image | Full scans | Sensitive | Institution/Student | **Raw: 30 days; redacted: contract term** | Vision processing |
   | Extracted text | Bboxes, Unicode, LaTeX | Internal | Platform (derived) | **Contract + 2 years** | Fine-tuning & prompt input |
   | AI assessment outputs | Score, criteria, confidence | Internal | Platform | Contract term | Calibration analysis |
   | Human evaluation layer | Teacher marks, overrides, reasons | Confidential | Institution | **Contract + 1 year** | Fine-tuning & alignment (**opt-in**) |
   | Platform telemetry | Timestamps, latency, clickstreams | Internal | Platform | **365 days** | Operational only |

4. **Sixteen-stage lifecycle with controls:**
   1. Generation: exam cover sheets with an isolated PII header zone.
   2. Collection: **TLS 1.3 + mTLS**; MD5 checksum.
   3. Ingestion: WAF, sandboxing, rate limits, MIME sandboxing.
   4. Validation: DPI, lighting, blur, page count; failures go to re-scan.
   5. Identification/redaction: DL header detection, crop or mask, replace with `student_hash`.
   6. OCR/extraction: multilingual OCR plus VLM into JSON.
   7. Normalization: Unicode for Bengali graphemes, LaTeX.
   8. Storage: object, SQL and vector stores.
   9. Annotation: de-identified segments, expert labels.
   10. Human verification: teacher accept or override, with required rationale tags.
   11. AI evaluation: LLM scoring with token-level confidence.
   12. Model evaluation: QWK and MAE on benchmarks.
   13. Analytics: anonymized; **DP noise plus cohort threshold N ≥ 10**.
   14. Model improvement: validated triplets into SFT/DPO.
   15. Archiving: at term end, WORM cold storage with customer-managed keys.
   16. Retention/deletion: crypto key shredding plus overwrite on contract expiry or data subject request.

5. **Five classification tiers (Table 5):**

   | Tier | Contents | Access | Encryption | **Retention** |
   |---|---|---|---|---|
   | 1 Public | Syllabi, NCTB sample exams, board schemes | Public CDN/API | Optional | Indefinite |
   | 2 Internal | System logs, metrics, traces | RBAC | AES-256 | **90 days** |
   | 3 Confidential | School contracts, teacher accounts, **rubrics** | RBAC + MFA | AES-256 (KMS) | **Contract + 7 years** |
   | 4 Sensitive | Redacted scripts, extracted text, AI scores | ABAC | Column-level AES-256 | **Contract + 2 years** |
   | 5 Highly Sensitive | Student names, **NIDs**, unredacted PII, hashes | Strict isolation, break-glass only | HSM | **Duration of student enrollment** |

6. **Minors and consent:**
   - Under the **Contract Act 1872** minors lack capacity, so ToS signed by students are void.
   - Authorization chain: institution (in loco parentis / contractual mandate) → institutional Data Processing Agreement → parental/guardian privacy notice → student rights portal (access, correction, deletion).
   - The platform positions itself as an "authorized outsourced institutional service provider", explicitly borrowing from **FERPA 34 CFR § 99.31** and **COPPA 16 CFR § 312.8** "ed-tech exceptions". The institution authorizes "in lieu of individual parental consent" when processing is limited to institutional assessment.
   - Parents are informed via school-distributed templates. Rights requests come from parents or emancipated students via the school.

7. **Bangladeshi legal claims (stated status as given by the doc):**
   - **"Personal Data Protection Act 2026 (Law 63 of 2026) / Personal Data Protection Ordinance 2025"**, treated as **in force**. Claimed content:
     - Personal data is the citizen's "personal property".
     - Principles: lawfulness, purpose limitation, minimization, accuracy, storage limitation, integrity/confidentiality, accountability.
     - **Section 5**: consent as a primary lawful basis, plus exceptions for legal obligation and "institutional service contracts".
     - **Data localization**: at least one real-time synchronized local copy of "restricted" or CII-origin data in Bangladesh.
     - Rights: access, correction, erasure, portability, withdrawal of consent.
     - "Sec 2" is cited for re-identification.
   - **"Cyber Security Act 2023 / Cyber Security Ordinance 2025 / CSA 2026"**, all three named together as one regime:
     - **Sec 26**: unauthorized collection or use of identity information is criminal.
     - **Secs 19 & 23**: system interference and fraud; security controls against alteration of records.
     - **Sec 22** (in Table 7): cited against unverified score overrides.
   - **ICT Act 2006 (amended)**: e-signatures, admissibility of digital records, service provider liability.
   - **Contract Act 1872**: minors' capacity.

8. **International claims:**
   - **GDPR / UK GDPR:**
     - Art. 6(1)(b) contract and 6(1)(f) legitimate interests for operations.
     - Art. 9 special-category isolation.
     - **Art. 22** complied with by being a HITL decision-support tool with final authority at the educator.
     - SCCs plus Data Transfer Impact Assessments for transfers.
     - Art. 28 (subprocessors) and Art. 4(1) (re-identification) in the risk table.
   - **FERPA:** "school official exception" 34 CFR § 99.31(a)(1)(i). Conditions: institutional service otherwise performed by employees, "direct control", no re-disclosure.
   - **COPPA:** FTC ed-tech guidance. Collection only for educational purposes under school authorization; no advertising or profiling.

9. **Privacy risk matrix (Table 7):**

   | Risk | Driver | Control | Residual risk |
   |---|---|---|---|
   | Unmasked script PII | BD PDPA s5, CSA s26 | ML bbox redaction + header crop | Low |
   | Model PII leakage | GDPR Art 6, FERPA | Regex + NER scrubbing, tokenization | Very low |
   | Subprocessor retention | BD PDPA local copy, GDPR Art 28 | **Enterprise Zero-Data-Retention contracts** | Low |
   | Illegal cross-border flow | BD PDPA restricted-data directives | **Primary DB in local cloud region** | Low |
   | Unverified overrides | CSA s22 | Immutable cryptographic ledger | Low |
   | Unauthorized secondary AI use | BD PDPA s5, COPPA | **Opt-in separating operations from training** | Very low |
   | Re-identification via analytics | GDPR Art 4(1), BD PDPA s2 | DP noise, N ≥ 10 | Low |

10. **Ownership split:**
    - Raw scripts and identity: student/institution (**controller**).
    - Custody: platform (**processor/fiduciary**).
    - Processing rights: via the service agreement.
    - Derived text and vectors: "joint ownership / platform derivative technical asset".
    - **Fine-tuned weights: exclusive platform property.**
    - Training license: separable clause, **non-exclusive, royalty-free, revocable**, covering "fully de-identified, non-re-identifiable" text and scoring metadata.

11. **Governance organization:** CDO over DPO, CISO, AI Ethics & Annotation Director, and Lead Data Engineer.

    Policy table:
    - Access control: zero-trust least privilege (CISO); JIT break-glass.
    - Secondary use: "Dual-Opt-In Data Licensing" (DPO); DPA opt-in flag checked before ML export.
    - Subprocessor audit: annual SOC 2 Type II review plus API traffic inspection.
    - Erasure: crypto purge (Lead Data Engineer).
    - Data quality: **automatic pipeline halt if evaluation QWK < 0.70** (AI Eval Specialist).

12. **Zero-trust access path:** production (PII) → redaction/anonymization → de-identified vault (tokenized IDs, masked images) → developer sandbox (synthetic or de-identified only). Production access needs MFA, hardware tokens and JIT short-lived credentials. **Break-glass needs dual custody (CISO + DPO)** and is logged to a write-once SIEM.

13. **Acquisition channels (Table 3):**
    - Partner schools: low cost, 100k+ scripts/yr, medium legal risk (needs DPA opt-in), primary flywheel.
    - Teacher calibration network: stipends, **5k–20k scripts**, gold standard.
    - Academic open datasets: **1k–10k**, baseline OCR.
    - Synthetic generation: 1M+, zero PII, edge cases.

14. **Pilot rollout:**
    - **Phase 1:** 10 schools / 10,000 scripts (5 Bengali-medium plus 5 English-version, urban Dhaka). OCR, layout, prompts, PII redaction.
    - **Phase 2:** 50 schools / 75,000 scripts. Peri-urban and rural in Dhaka, Chattogram and Rajshahi; varied paper, scanners and ink.
    - **Phase 3:** 100 schools / 200,000 scripts. "All eight general education boards", technical and madrasah boards; specialized subjects.
    - **Phase 4:** 500 schools / 1M+ scripts. Full production, active learning.

15. **Dataset requirements (Table 4):**

    | Use case | Volume | Labels | Target |
    |---|---|---|---|
    | Bangla/English OCR | **150,000 line items** | Bboxes + Unicode | **CER < 2.5%** |
    | Srijonshil layout parser | **25,000 pages** | Region boxes (CQ parts A–D, stems, margins) | **IoU > 0.90** |
    | Math expression OCR | **50,000 equations** | LaTeX + SymPy trees | **Expression accuracy > 96%** |
    | CQ Part-A recall scoring | **30,000 answer pairs** | Binary match | **Exact match > 98%** |
    | CQ Parts B/C/D | **100,000 evaluated scripts** | Multi-criteria rubric, partial credit | **QWK ≥ 0.75** |
    | Confidence calibration | **20,000 multi-rater scripts** | Disagreement variance | **ECE < 0.03** |

16. **Representativeness targets:**
    - Geography: urban 40%, peri-urban 30%, rural 30%.
    - Medium: Bengali medium 70%, English version 25%, English medium/Cambridge/Edexcel 5%.
    - Stream: Science 40%, Humanities 35%, Business 25%.
    - Capture: 300+ DPI flatbed 50%, mobile/variable light 50%.
    - Mixed script: "Banglish", and Bangla with English terms and equations.
    - Labels by CQ sub-part: **A = 1 mark (knowledge), B = 2 (comprehension), C = 3 (application), D = 4 (higher-order), total 10**.

17. **Annotation pipeline:** Tier-1 primary marker, Tier-2 independent blind marker, QWK agreement check; on disagreement, a Tier-3 master adjudicator sets the gold label. Annotators are **certified secondary and higher-secondary teachers** in the specific NCTB track, blind to AI and to peers.

    IRR thresholds:
    - **QWK ≥ 0.85:** gold.
    - **0.70 ≤ QWK < 0.85:** keep for the training pool.
    - **QWK < 0.70:** adjudicate and refine the rubric.

    A batch is certified gold at **QWK ≥ 0.75** (stated twice).

18. **Override feedback loop:** teacher override → discrepancy payload → heuristic integrity filter → verification queue → fine-tuning corpus. Overrides are held in staging. **Overrides more than 20% away from the AI baseline require structured justification** (for example "Misidentified Handwriting", "Alternative Valid Logic", "Partial Credit Adjustment"). Staged overrides are **sampled and audited** by senior specialists before entering training.

19. **Training-data options (Table 10):** A synthetic/public only; B anonymized aggregate; **C institutional opt-in (recommended)**; D student opt-in; E commercial licensing; F federated. Option C is a dual-tier legal structure: operations under an SLA, and training under a separate **Institutional Data Contribution Addendum**, with pricing discounts or analytics as the incentive. The summary later recommends "**Strategy B** (Balanced Data Strategy with Institutional Opt-In)", a labelling inconsistency.

20. **Data moat:** NCTB 4-part CQ corpus; Bangla/English handwritten image database; teacher override and disagreement matrix; misconception knowledge graphs. The doc claims generic multimodal LLMs have "elevated CER" on Bangla handwriting.

21. **Data quality metrics (Table 8):**

    | Dimension | Metric | Target |
    |---|---|---|
    | Accuracy | OCR CER (daily sampling) | **< 2.5%** |
    | Completeness | Missing page ratio | **0.00%** (reject upload) |
    | Consistency | Intra-teacher grading variance | **QWK ≥ 0.80** (weekly) |
    | Validity | Schema compliance | 100% (dead-letter queue) |
    | Uniqueness | Duplicate scripts | Zero |
    | Timeliness | Scan-to-ingest latency | **< 300 s** |
    | Traceability | Lineage coverage | 100% (block model export) |
    | Representativeness | Regional cohort delta | **< 5%** deviation (monthly) |

    Image quality gates: **minimum 200 DPI (300 recommended for Bengali)**; **Laplacian variance > 100**; **skew ≤ 5°**, otherwise affine deskew.

22. **Curriculum drift:** every score carries a `curriculum_version` tag (for example `NCTB-2026-SSC-v1.2`). A new benchmark is built before prompts or weights are updated when NCTB or the Ministry changes formats.

23. **Storage:**
    - S3/GCS object storage (KMS AES-256; **lifecycle to cold after 30 days**).
    - PostgreSQL ("multi-region ACID") for identity tokens, exams, rubrics and scores.
    - MongoDB/DocumentDB for OCR JSON.
    - Qdrant/Milvus vectors, **built only from de-identified text**.
    - Snowflake/BigQuery for anonymized analytics and audit logs.

    Schema: `student_identity_vault` (encrypted national ID, encrypted name, roll), `answer_scripts` (student_hash, raw and redacted URIs, `is_opted_in_for_training` default FALSE), `extracted_answers` (`cq_sub_part` in A/B/C/D/MCQ, OCR confidence), `assessment_records` (AI score, confidence, rationale, model version, teacher final score, override flag, reason code, teacher_id).

    Lineage chain: final score → teacher review event → AI inference payload → prompt version, config and model weights ID → extracted text and bbox → redacted image → raw upload plus scanner metadata.

24. **Security and deletion:** header cropping plus **HMAC-SHA-256** tokenization; synthetic sandbox; **ZDR contracts** with third-party providers; in-country mirroring. Deletion runs: request → controller verification → identity token revocation → primary DB delete → object key shredding in the HSM → vector and index flush → **deletion certificate** to the controller.

25. **Unit costs (Table 9):**
    - Per page: $0.0005 acquisition + $0.008 OCR + $0.0005 storage + **$0.02 human review (sampled)** = **$0.029**.
    - Per 8-page script: **$0.232**.
    - 100k scripts/year: **$23,200**.

    Build vs buy: **build** Bangla OCR (fine-tune TrOCR/Donut); **lease** LLM APIs first, then move to open-weight models (Llama/Mistral).

26. **Ethics:**
    - Automation bias: marks hidden until the teacher clicks "Evaluate Script".
    - Handwriting penalty: balanced training plus normalization layers.
    - Surveillance: no non-educational third-party access to analytics.

27. **Roadmap:**
    - Phase 0 (months 1–3): DPAs, threat model, synthetic seed.
    - Phase 1 (months 4–6): PII redaction, layout parser, review UI.
    - Phase 2 (months 7–9): 10-school pilot, 10k scripts.
    - **Phase 3 (months 10–12): deploy in-country database replication in Bangladesh**, vector DB, active learning.
    - Phase 4 (months 13–18): fine-tune open-weight VLMs.
    - Phase 5 (months 19–24): 500 institutions, SOC 2 Type II.
    - Phase 6 (month 25+): international (GDPR/FERPA/COPPA).

28. **Q&A answers (key):**
    - Minimum data: scans, question papers and rubrics, `student_hash`, teacher scores.
    - **Avoid collecting** names, NIDs, phone numbers, biometrics, addresses, financial data, non-academic margin notes.
    - Customer-owned: raw scripts, identity, **official grades**, custom school guidelines.
    - Usable for AI: de-identified text, bboxes, rubric-score pairs, override justifications, **only with the addendum**.
    - Anonymization: (a) header cropping, (b) **salted HMAC-SHA-256** of roll and registration numbers, (c) **NER redaction of names in answer text**.
    - **Retention: raw 30 days; redacted images and text contract + 2 years; audit logs 365 days.**
    - **Never send to external AI:** raw unredacted images, identity records, teacher contact info, credentials.
    - Train on customer data only if all hold: (a) opt-in addendum, (b) PII redaction passed, (c) hygiene filters against single-teacher bias, (d) residency compliance.
    - Leakage: **group split by student, school and exam paper**.
    - First 10 schools give 10k seed scripts; first 100 give 200k.

---

## Quantitative claims table

| Claim | Value | Source cited | Source type | Credibility H/M/L + why |
|---|---|---|---|---|
| Raw image retention | 30 days | None | Design choice | M as a design choice. **Risky** against Bangladeshi result and re-scrutiny timelines and appeals. |
| Redacted scripts / extracted text retention | Contract + 2 years (Table 1 says contract term for redacted) | None | Design choice | L–M: internally inconsistent. |
| Human evaluation retention | Contract + 1 year | None | Design choice | L–M: shorter than the AI outputs derived from it (Tier 4: +2 years). |
| Institutional metadata / Tier 3 | Contract + 7 years | None | Design choice (tax/audit-style) | M. |
| System logs vs audit logs vs telemetry | 90 days / 365 days / 365 days | None | Design choice | L: conflicts with C2's immutable audit trail and with appeal needs. |
| Identity vault retention | Active contract (T1) vs student enrollment (T5) | None | Design choice | L: contradictory. |
| Analytics cohort floor | N ≥ 10 | None | Common k-anonymity heuristic | M. |
| OCR dataset | 150k lines, CER < 2.5% | None | Author judgement | L: C1 cites about 10.89% CER for fine-tuned TrOCR on real Bangla handwriting. < 2.5% is unproven for Bangla handwriting. |
| Layout dataset | 25k pages, IoU > 0.90 | None | Judgement | M. |
| Math OCR | 50k equations, > 96% expression accuracy | None | Judgement | L–M: handwritten maths expression recognition state of the art (CROHME-type) is typically well below 96% expression-level accuracy. [Analyst note] |
| CQ Part-A exact match | 30k pairs, > 98% | None | Judgement | L–M: needs OCR to be near perfect on short answers. |
| CQ B/C/D | 100k scripts, QWK ≥ 0.75 | `[cite: 10]` (unresolvable) | Unresolvable | M as a target: modest and realistic relative to C1/C2. |
| Calibration set | 20k multi-rater scripts, ECE < 0.03 | None | Judgement | M: 20k multi-rater scripts is very costly (≥ 40k human markings). |
| Teacher calibration network | 5k–20k scripts | None | Judgement | M. |
| Pilot sizes | 10/50/100/500 schools; 10k/75k/200k/1M+ | None | Plan | L–M: no basis given for volume per school. |
| Representativeness | 40/30/30; 70/25/5; 40/35/25; 50/50 | None | Judgement | L: no BANBEIS or board statistics cited. |
| IRR tiers | ≥ 0.85 gold; 0.70–0.85 train; < 0.70 adjudicate; gold batch ≥ 0.75 | None | Judgement | L–M: internally inconsistent (0.85 vs 0.75). |
| Intra-teacher consistency | QWK ≥ 0.80 | `[cite: 10]` | Unresolvable | L–M. |
| Pipeline halt | QWK < 0.70 | None | Judgement | M: matches C1's guardrail (< 0.70). |
| Override justification trigger | > 20% variance | None | Judgement | M. |
| Image gates | ≥ 200 DPI (300 recommended), Laplacian > 100, skew ≤ 5° | None | Folk heuristics | L–M: must be calibrated locally. |
| Scan-to-ingest | < 300 s | None | Judgement | M. |
| Unit cost | $0.029/page; $0.232/script; $23,200 per 100k | None | Worked example | M for arithmetic (checks). L for inputs: $0.008/page OCR and $0.02/page sampled review are unsourced. |
| Customer school volume | 100k+ scripts/yr | None | Judgement | L. |
| Bangladeshi PDP law | "Act 2026, Law 63 of 2026" / "Ordinance 2025" | ResearchGate/SemanticScholar paper title; Scribd | Secondary / unofficial | **L: no official gazette cited. See Critical assessment.** |
| Data localization | Real-time local copy of restricted/CII data | Same | Secondary | L. |
| Cyber law section numbers | s19, s22, s23, s26 | Scribd CSA 2023 overview; blogs | Secondary | L–M: they match CSA 2023 numbering; applicability after the 2025 ordinance is unverified. |

---

## Frameworks/processes proposed (step by step)

**A. Sixteen-stage lifecycle:** see finding 4. Each stage has a named risk and a control (Table 2).

**B. Minor-data authorization hierarchy:**
1. Institutional mandate.
2. DPA signed by an authorized administrator.
3. Parental notice via the school.
4. Rights portal (access, correction, deletion via the school).
5. Separate opt-in addendum for training.

**C. Anonymization (3 steps):** header crop, salted HMAC-SHA-256 tokenization, NER redaction in text.

**D. Zero-trust access:** production → redaction → de-identified vault → developer sandbox. Break-glass needs CISO + DPO and SIEM logging.

**E. Annotation to gold:**
1. Two blind certified-teacher markers.
2. QWK check.
3. Adjudicator on disagreement.
4. Batch certified at QWK ≥ 0.75 (or item-level ≥ 0.85).

**F. Override hygiene:**
1. Stage the override.
2. Heuristic filter.
3. Justification if > 20% variance.
4. Senior specialist sample audit.
5. Only opted-in and redacted data enters SFT/DPO.

**G. Training eligibility gate:** four conditions (addendum, redaction pass, hygiene, residency).

**H. Drift:** curriculum version change → benchmark → score delta → prompt/rubric update → corpus refresh. Every score is version-tagged.

**I. Deletion:** request → controller verify → token revocation → DB delete → key shred → index flush → certificate.

**J. Pilot and roadmap:** four school phases; seven time phases (months 0–25+).

---

## Specifics a PRD/TRD needs

- **Retention durations (as proposed, with conflicts flagged):**
  - Raw scans 30 days.
  - Redacted scans contract term (T1) or contract + 2 years (T5 and Q&A).
  - Extracted text contract + 2 years.
  - AI outputs contract term (T1) or contract + 2 years (T5).
  - Teacher marks and overrides contract + 1 year.
  - Institutional metadata, contracts, teacher accounts contract + 7 years.
  - Rubrics indefinite (T1) or contract + 7 years (T5).
  - Exam metadata and questions indefinite.
  - Telemetry 365 days; system logs 90 days; audit logs 365 days.
  - Identity vault contract term or enrollment duration.

  [Analyst note] The PRD must reconcile these and anchor them to board result, re-scrutiny and appeal windows and to institutional record-keeping duties.
- **Access control roles:**
  - Platform governance: CDO, DPO, CISO, AI Ethics & Annotation Director, Lead Data Engineer, AI Eval Specialist, Security Architect.
  - Models: RBAC for Tier 2; RBAC + MFA for Tier 3; ABAC for Tier 4; break-glass with dual custody (CISO + DPO) for Tier 5.
  - JIT credentials; developers see synthetic or de-identified data only.
  - Combine with C2's six educational roles.
- **Anonymization approach:** header zone on cover sheets; DL header detection and crop; salted HMAC-SHA-256 `student_hash`; NER on text; vectors only from de-identified text; analytics DP noise and N ≥ 10.
- **Third-party LLM exposure rules:**
  - Never send raw unredacted images, identity records, teacher contact details or credentials.
  - Only redacted crops and text, under enterprise ZDR contracts.
  - Annual SOC 2 Type II review plus API traffic inspection.
  - Residency compliance before any training transfer.
- **Consent and legal basis:** institutional DPA for operations; separate opt-in addendum for training (`is_opted_in_for_training` default FALSE); parental notice via the school (notice, not consent).
- **Which corrections feed which store:**
  - Teacher overrides → staging repository → (filter, justification, sample audit) → SFT/DPO fine-tuning corpus (opt-in only).
  - Gold labels come from the annotation network (Tier-1/2/3), not from operational overrides.
  - Model evaluation uses an isolated, versioned benchmark repository.
- **Gold dataset sizes:**
  - Teacher calibration network 5k–20k scripts.
  - Calibration set 20k multi-rater scripts.
  - OCR 150k lines; layout 25k pages; maths 50k equations; Part-A 30k pairs; B/C/D 100k scripts.
- **Audit sampling:** "sampled and audited" staged overrides; daily CER sampling; weekly intra-teacher check; monthly representativeness review. No percentages are given.
- **Metrics and targets:** CER < 2.5%; layout IoU > 0.90; maths > 96%; Part-A > 98%; B/C/D QWK ≥ 0.75; ECE < 0.03; intra-teacher QWK ≥ 0.80; pipeline halt at QWK < 0.70; 0% missing pages; latency < 300 s; representativeness delta < 5%.
- **Image ingest gates:** ≥ 200 DPI (300 recommended), Laplacian > 100, skew ≤ 5°.
- **Security:** TLS 1.3, mTLS, WAF, KMS/HSM, column-level encryption, WORM archive, SIEM.
- **Localization:** primary DB in a "local cloud region"; in-country mirror (Phase 3).
- **Unit economics:** $0.232 per 8-page script.

---

## Assumptions

1. A Bangladeshi personal data protection statute (Act 2026 or Ordinance 2025) is in force with the cited sections and a localization clause.
2. Schools can lawfully authorize processing of minors' data in place of parents under Bangladeshi law. This is a borrowed US FERPA/COPPA concept; no Bangladeshi source is given.
3. A "local cloud region" exists in Bangladesh for the primary DB.
4. Header-zone cover sheets can be standardized across partner schools. Board exams already use OMR/registration cover sheets; internal exams vary.
5. Salted hashing plus header crop plus NER makes data "fully de-identified, non-re-identifiable".
6. Enterprise ZDR contracts are available and auditable.
7. Certified NCTB teachers can be recruited as annotators at stipend rates, at 5k–20k script scale.
8. Institutions will opt in for pricing discounts.
9. OCR costs $0.008/page and sampled review $0.02/page.

---

## Recommendations (from the doc)

1. Adopt institutional opt-in (Option C, called "Strategy B" in the summary) for training. Keep operations and training legally separate.
2. Isolate PII at the ingestion edge. Engineers never see live PII.
3. Build a proprietary NCTB CQ 4-part, Bangla handwriting corpus as the moat. Build OCR in-house and lease LLMs initially.
4. Establish multi-rater gold data with QWK thresholds and adjudication.
5. Stage and audit teacher overrides before training.
6. Version every score by curriculum. Re-benchmark on curriculum change.
7. Keep a local data copy for Bangladeshi compliance. Adopt SCC/DTIA, FERPA and COPPA patterns for international expansion.
8. Use crypto-shredding for deletion, with deletion certificates.
9. Pilot 10 → 50 → 100 → 500 schools.

---

## Open questions

1. **What is the actual legal status and text of Bangladesh's personal data protection law as of September 2026?** Is it an Ordinance 2025 still in force, ratified as an Act in 2026, or lapsed? Which sections govern consent, children, localization, cross-border transfer and penalties?
2. Does Bangladeshi law require **parent/guardian consent** for processing a minor's data, and can an institutional DPA substitute for it? [Analyst note] Earlier Bangladeshi PDP drafts reportedly contained guardian-consent provisions for children. The doc does not analyze this.
3. Are exam scripts or scores "restricted" data or CII-origin data subject to localization? If schools are private, are they CII at all?
4. Is there a hyperscaler region inside Bangladesh? If not, how is "primary DB in local cloud region" met: a local data centre, a local provider, or colocation?
5. How long must schools and boards legally retain answer scripts and marks? How long do result publication, re-scrutiny and appeals take? The 30-day raw deletion must follow these, not precede them.
6. What happens to fine-tuned weights when an institution **revokes** its training license (machine unlearning, retraining cadence)?
7. Is "Dual-Opt-In" (Table 6) institution plus parent, or institution plus teacher? This is undefined.
8. What is the lawful basis for keeping teacher override data and teacher IDs? Teachers are data subjects too.
9. Does handwriting itself count as identifying or biometric data under the Bangladeshi statute? Redacted crops still carry handwriting.
10. The EU AI Act is not mentioned. What obligations apply at international expansion? (See Critical assessment.)

---

## Critical assessment

**Legal claims about Bangladesh (each flagged with its stated status):**

| Claim in doc | Stated status | Date given | [Analyst note] assessment |
|---|---|---|---|
| "Personal Data Protection Act 2026 (Law 63 of 2026)" | Treated as **enacted and in force** | 2026 | **Unverified.** The only sources are a ResearchGate/Semantic Scholar paper *title* and a Scribd upload of the *Ordinance 2025*. No gazette or bdlaws citation. The doc writes "Act 2026 / PDPO 2025" with a slash, **conflating an interim-government ordinance with a parliamentary act**. Section numbers (s5 grounds, s2 definitions) and "Law 63 of 2026" cannot be confirmed. Must be verified against the official gazette before any PRD reliance. |
| "Personal Data Protection Ordinance 2025" | Treated as equivalent to the Act | 2025 | Plausible that an ordinance was promulgated by the interim government in 2025. [Analyst note] Ordinances not laid before and approved by the new Parliament can lapse, so current force depends on post-2026-election ratification. Verify. |
| Personal data is the citizen's "personal property" | Stated as law | — | Unverified characterization; appears in commentary. Do not rely on it. |
| Data localization: real-time local copy of "restricted"/CII data | Stated as a mandate | — | The concept appeared in earlier Bangladeshi PDP drafts (2022–2024), which drew criticism. The final text and applicability to ed-tech are unverified. The doc then **schedules in-country replication for months 10–12, after the months 7–9 pilot**, so it is non-compliant by its own reading during the pilot. |
| "Cyber Security Act 2023 / Cyber Security Ordinance 2025 / CSA 2026" | All listed as one regime, no status distinction | 2023/2025/2026 | [Analyst note] CSA 2023 replaced the Digital Security Act 2018. The doc's own source (Prothom Alo) reports a **Cyber Security Ordinance 2025 gazette**, which to my knowledge repealed CSA 2023. A "CSA 2026" (ratification?) is cited only via a ResearchGate title. The doc cites **section numbers (19, 22, 23, 26) that match CSA 2023 numbering** without checking whether the ordinance or act kept them. **Possibly outdated.** |
| ICT Act 2006 (amended) | In force | 2006 | Broadly correct as a framework for e-records and e-signatures. Its notorious s57 was repealed earlier; not relevant here. |
| Contract Act 1872: minors cannot contract | In force | 1872 | Correct in substance (s11; majority at 18 under the Majority Act 1875). But it does **not** by itself establish an "in loco parentis" or "school official" basis in Bangladesh. Those are **US FERPA/COPPA concepts transplanted without Bangladeshi authority**. |

**International claims:**
- **COPPA citation is wrong.** 16 CFR § 312.8 is the *confidentiality, security and integrity* provision, not an "ed-tech exception". School authorization in place of parental consent comes from **FTC guidance/FAQs**; the doc's source is a 2020 FTC blog. [Analyst note] My understanding is that the FTC's 2025 COPPA Rule amendments **declined to codify** a school-authorization exception, and amended § 312.8 to require a written security program and § 312.10 to require a written retention policy. Verify. COPPA applies only to children **under 13**.
- **FERPA:** the school-official exception is correctly described in substance. It applies only to US schools receiving federal education funding.
- **GDPR:**
  - Art. 6(1)(f) legitimate interests is **not available to public authorities** for their tasks. For public schools the basis would more likely be 6(1)(e), with the platform as processor under Art. 28.
  - Art. 22 compliance "by HITL" fails where items are **auto-finalized without meaningful human review** (C2's auto-finalize cell; C1's 85–95% formative coverage). Rubber-stamp review does not count.
  - A DPIA (Art. 35) is omitted; likely mandatory for large-scale processing of children's data with new technology.
  - Salted HMAC tokens are **pseudonymization, not anonymization** (Recital 26), so the "fully de-identified, non-re-identifiable" claim is overstated.
- **EU AI Act omitted.** [Analyst note] AI systems intended to evaluate learning outcomes are listed as **high-risk (Annex III, education)**. Obligations include risk management, data governance, logging, human oversight, accuracy and robustness documentation, and conformity assessment. The application date for Annex III obligations (August 2026 originally, with proposed postponement) should be verified for Phase 6.
- **UK GDPR:** mentioned but not analyzed. Recent UK reform to automated decision-making rules is not reflected.

**Internal contradictions:**
- Identity vault retention: contract (T1) vs enrollment (T5).
- Redacted images: contract (T1) vs contract + 2 years (T5 and Q&A).
- AI outputs: contract (T1) vs contract + 2 years (T5).
- Rubrics: indefinite (T1) vs contract + 7 years (T5).
- System logs 90 days vs audit logs 365 days vs "immutable" archival.
- "Avoid collecting names and NIDs" vs a schema with `encrypted_national_id` and `encrypted_student_name`, and Tier 5 listing NIDs.
- Gold threshold QWK ≥ 0.85 (IRR tiers) vs ≥ 0.75 (batch certification).
- Object storage "lifecycle to cold after 30 days" vs raw "purged at 30 days".
- **WORM** archive vs erasure rights (works only via crypto-shredding; must be explicit).
- "Option C" recommended vs "Strategy B" in the summary.
- "Multi-region" PostgreSQL vs localization.
- The retention answer "audit logs 365 days" contradicts the need for audit trails in appeals (C1, C2).

**Factual errors about Bangladesh:**
- "**All eight general education boards**": [Analyst note] Bangladesh has **nine** general boards (Dhaka, Rajshahi, Cumilla, Jashore, Chattogram, Barishal, Sylhet, Dinajpur, Mymensingh) plus the Madrasah and Technical boards.
- The CQ 1/2/3/4 = 10 structure is correct for the SSC/HSC creative question. The doc ignores curriculum churn (the 2023 curriculum reform and its 2024–25 rollback).
- The doc says the platform targets "primary" institutions but designs everything around SSC/HSC CQ and streams (Science/Humanities/Business apply only from grade 9).

**Unrealistic or over-engineered:**
- CER < 2.5% for Bangla handwriting (vs about 10.89% cited in C1).
- > 96% handwritten maths expression accuracy.
- A C-suite governance org (CDO, DPO, CISO, Ethics Director) and SOC 2 for an early-stage startup.
- mTLS for mobile capture clients (heavy client certificate management).
- MD5 for integrity (use SHA-256).
- DP noise on institution dashboards (utility cost, little benefit at N ≥ 10).
- 20k *multi-rater* calibration scripts (about 40k+ markings).
- $0.232/script cost is plausible, but review at $0.02/page "sampled" does not match C2's review-rate model.

**Citation quality:** legal claims rest on Scribd, Facebook posts, a personal law blog, ResearchGate titles and news. There are no primary sources. `[cite: 10]` markers are unresolvable.

---

## Confidence level + Relevance to product decisions

- **Confidence in the doc's content:**
  - **Architecture and governance patterns** (PII isolation at the edge, tokenization, de-identified dev sandbox, training opt-in separated from service DPA, staged override hygiene, curriculum version tags, crypto-shredding with certificates, group-based splits, lineage chain): **Medium–High**. These are standard good practice.
  - **Bangladeshi legal content: Low.** Status is conflated, sources are unofficial, and section numbers are unverified.
  - **International legal content: Medium–Low**, with specific errors (COPPA § 312.8, GDPR 6(1)(f) for public bodies, anonymization vs pseudonymization, EU AI Act omission).
  - **Numeric targets and dataset sizes: Low–Medium.** They are unsourced, and several are optimistic.
- **Relevance: Very high** for the Data Governance, Privacy and Security sections of the TRD, the DPA and addendum contract design, the data model, the pilot plan and annotation operations. Before any of it becomes requirements:
  1. Commission a **Bangladeshi legal verification** (official gazette text of the PDP instrument and cyber ordinance/act, their current force, children's consent, localization, cross-border rules).
  2. **Reconcile retention** with board and school result, re-scrutiny and appeal timelines.
  3. Recalibrate OCR targets from a real Bangla handwriting baseline.
  4. Decide the localization hosting approach early (it gates the pilot, not Phase 3).
