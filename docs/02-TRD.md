# 02 — Technical Requirements Document (TRD)

| Field | Value |
|---|---|
| Document Name | TRD — AI-Assisted Exam Script Marking Platform |
| Version | 1.0 |
| Status | Baseline for Phase 1 build. Items tagged **Validation Required** need Phase 0 data; items tagged **DECISION REQUIRED** have a named owner. |
| Date | 2026-09-27 |
| Owner | Engineering Lead (with AI Lead for §7–11, §16, §34–36) |
| Purpose | Defines the technical requirements the system must satisfy to deliver the PRD: constraints, architecture rules, component requirements, quality attributes, operations, cost and vendor dependencies. |
| Source Research | S05, S06, S07 (architecture and risks, critically filtered), S08–S10, V1, V2; decisions DEC-08..DEC-14, DEC-18, DEC-28, DEC-34, DEC-39 |
| Dependencies | `01-PRD.md` (FR/NFR/AI-REQ/SEC/PRV IDs); `06` (AI), `07` (HITL), `08` (data/security); realised by `03-system-design.md` |

Requirement format: **ID | Requirement | Reason (trace) | Priority (M/S/C) | Acceptance criteria.** M = required for the MVP/pilot (G1).

---

## 1. Technical Objectives

| ID | Objective | Measure |
|---|---|---|
| TO-1 | Correct results, always | 100% of the result-engine fixture suite passes. Zero platform-caused result errors in production. |
| TO-2 | No lost scripts or pages | 0 pages lost after capture acknowledgement |
| TO-3 | Trustworthy AI assistance, evidence-grounded and gated per cell | 06 §4 gates enforced; provenance for 100% of suggestions |
| TO-4 | Works in Bangladeshi conditions | Offline capture; ≤400 KB per page; Bangla everywhere |
| TO-5 | Affordable | AI ≤ BDT 3.0 per 10-page script (target), ≤6.0 (ceiling) |
| TO-6 | Private and secure by default | DPIA passed; pen test with no High findings; tenant isolation tests green |
| TO-7 | Simple to operate | One deployable backend + workers; one team can operate it; no Kubernetes/Kafka in MVP (DEC-11) |
| TO-8 | Vendor-portable | Any LLM vendor swap = configuration + gate run; core deployable to a BD data centre (DEC-12) |

## 2. System Constraints

| ID | Constraint | Source |
|---|---|---|
| CN-1 | No Bangladeshi region at LLM vendors; cross-border legality pending | VF-22, DEC-12 |
| CN-2 | Students <18 → guardian consent; no processing without CT-1/CT-2 | VF-12 |
| CN-3 | Many users have only Android phones; ~40% of schools have labs | VF-11 |
| CN-4 | Intermittent connectivity and load-shedding | EV-09 |
| CN-5 | Highly seasonal load (exam months) | EV-26 |
| CN-6 | Bangla complex-script rendering (conjuncts) in UI and PDFs; Bijoy legacy text in inputs | S02, S04 |
| CN-7 | AI must never finalise marks | DEC-05 |
| CN-8 | Hosted LLMs are not bit-reproducible; audit must store outputs | 06 AI-OQ-4 |
| CN-9 | Small team; MVP by ~Apr 2027 | Roadmap |
| CN-10 | Licensing: avoid AGPL/non-commercial model weights in the product (e.g., YOLOv8 AGPL, LayoutLMv3 CC-BY-NC) | B1/B2 extracts |

---

## 3. Architecture Requirements (TR-ARC)

| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-ARC-01 | **Modular monolith**: one backend codebase with internal modules (identity, org, curriculum, exams, rubrics, capture-ingest, pipeline, review, knowledge, results, reporting, metering, audit, admin, evaluation). Deployed as an API service + worker service from the same image. | DEC-11 | M | Module boundaries enforced by import-lint rules; no cross-module DB writes except via module services |
| TR-ARC-02 | Clients: (a) web app (React + TypeScript PWA) for all staff; (b) native Android capture app (Kotlin) | DEC-20, DEC-28 | M | Both clients use only the public API |
| TR-ARC-03 | State of record in PostgreSQL. Binary content in S3-compatible object storage. No other stateful stores in MVP (queue in Postgres) | Simplicity | M | Infrastructure inventory lists only these stateful services |
| TR-ARC-04 | Asynchronous processing through a durable job queue with idempotent jobs, retries (exponential back-off, max 5), dead-letter state and visibility in the admin UI | Reliability | M | Kill-worker chaos test: all jobs complete exactly-once in effect |
| TR-ARC-05 | **AI Provider Abstraction**: a single internal interface for VLM/LLM calls (sync, batch, structured output, caching hints), with per-cell routing config, version pinning, timeouts and budgets | DEC-08 | M | Swapping the default provider for a cell requires only config + gate report |
| TR-ARC-06 | All curriculum, templates, prompts, model routes, thresholds and capability levels are **versioned data**, referenced from every suggestion's provenance | NFR-MNT-01 | M | A suggestion record resolves to exact versions of every input |
| TR-ARC-07 | Container-based, cloud-portable core. Only portable services: PostgreSQL, S3 API, containers, SMTP/SMS, KMS abstraction | DEC-12 | M | Deployment dry-run on a second environment (e.g., on-prem VM with MinIO) succeeds |
| TR-ARC-08 | Event log of domain events (script captured, item suggested, item decided, marks locked, published) in the DB, for audit, metrics and integrations | Traceability | M | Every state change emits an event with a correlation ID |

---

## 4. Frontend Requirements

### 4.1 Web app (TR-FE)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-FE-01 | React + TypeScript SPA/PWA, responsive from 360 px to 1920 px; i18n with Bangla and English resource bundles; no hard-coded strings | DEC-20, DEC-24 | M | Pseudo-localisation test shows no untranslated strings |
| TR-FE-02 | Bangla font stack with correct shaping (e.g., Noto Sans Bengali / Hind Siliguri); math rendering (KaTeX) inside Bangla text | CN-6 | M | Visual regression of 50 conjunct-heavy strings |
| TR-FE-03 | Review workspace: image viewer with zoom/pan, region overlays, evidence highlight linking, keyboard shortcuts, prefetch of the next N items (N = 5 online, 30 in offline mode) | FR-REV-02/08/09 | M | NFR-PERF-01 met on network throttling profiles |
| TR-FE-04 | Offline-tolerant review: IndexedDB queue of decisions with sync and conflict notices | FR-REV-09 | S | 20-minute offline test passes |
| TR-FE-05 | Accessibility WCAG 2.2 AA (colour contrast, focus, ARIA labels, keyboard access) | NFR-A11Y-01 | M | axe CI with 0 serious issues; manual audit |
| TR-FE-06 | Math input editor (visual palette + LaTeX) for questions, model answers and answer specs; Bijoy paste conversion | FR-EXM-04 | M | Paste of Bijoy text converts; LaTeX renders |
| TR-FE-07 | Bundle ≤300 KB gzipped initial JS for the review route; images lazy-loaded; HTTP caching of static assets | Bandwidth | M | Lighthouse performance ≥80 on a mid-range Android |

### 4.2 Capture app (TR-CAP)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-CAP-01 | Kotlin Android app, minSdk 29 (Android 10); CameraX; ML Kit barcode (on-device) for QR; OpenCV (Android) for edge/quality checks and spread split | DEC-28 | M | Runs on a device matrix of 5 popular models in the Tk 15–25k band |
| TR-CAP-02 | On-device quality checks: blur (Laplacian variance normalised by resolution; threshold calibrated per device class), exposure (histogram clipping), glare (specular blob detection), page cut-off (document edge detection), skew >10°. Feedback in <500 ms | FR-CAP-04 | M | ≥95% of deliberately degraded pages flagged; ≤5% false flags on good pages (test set of 500 captures) |
| TR-CAP-03 | Spread auto-split (detect the gutter; split into 2 pages); auto-capture on stability (optional) | FR-CAP-03 | M/S | 10-page booklet captured in ≤6 shots |
| TR-CAP-04 | Local storage in app-private encrypted storage (Android Keystore-backed); Room DB for the queue; WorkManager for background resumable chunked upload; Wi-Fi-only toggle; per-page JPEG/WebP compression targeting ≤400 KB at ≥1500 px long edge | FR-CAP-07, NFR-NET-01 | M | Force-stop mid-upload → resume with no loss; files encrypted at rest |
| TR-CAP-05 | Script assembly: the QR cover starts a script; subsequent pages are appended; operations for insert/reorder/rotate/delete; late supplementary append via cover re-scan; manual student link when the QR is unreadable (offline roster cache) | FR-CAP-02/06 | M | Scenario tests incl. two consecutive covers (empty script → warning) |
| TR-CAP-06 | Remote wipe of the local queue when the account is disabled; app PIN after 5 min idle | SEC-07 | M | Disable account → queue wiped on next start/online check |
| TR-CAP-07 | Exam session download for offline use: roster subset (names for manual linking only), expected page ranges, booklet profile (cover pages, header mask) | FR-CAP-01 | M | Works in airplane mode after download |

---

## 5. Backend Requirements (TR-BE)

| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-BE-01 | Python 3.12, FastAPI for the HTTP API, Pydantic models as the source of API schemas (OpenAPI 3.1 generated) | Ecosystem fit (CV, SymPy, AI SDKs) | M | OpenAPI published per build |
| TR-BE-02 | Worker processes consume a PostgreSQL-backed job queue (`SELECT … FOR UPDATE SKIP LOCKED` via a maintained library) with priority lanes: `priority`, `standard`, `batch-submit`, `batch-collect`, `maintenance` | TR-ARC-04, DEC-34 | M | Load test at NFR-SCL-01 volumes |
| TR-BE-03 | Workflow/state machine module enforcing exam, script and item transitions (**TR-WF-01**) | FR-EXM-07 | M | Illegal transitions return 409; property tests |
| TR-BE-04 | PDF generation service (HTML→PDF with HarfBuzz shaping; embedded Bangla fonts) for covers, report cards and ledgers | FR-EXP-02 | M | Conjunct rendering verified; 1,000 report cards in ≤5 min |
| TR-BE-05 | Import service for Excel/CSV (rosters, marks) with validation reports, Bijoy→Unicode conversion (**TR-BN-01**), dry-run before commit | FR-ORG-03, FR-RES-05 | M | Fixture files with Bijoy text convert correctly (≥99.5% character accuracy on the test corpus) |
| TR-BE-06 | Notification service: SMS (Bangladeshi gateway) for OTP and optional result summaries; in-app notifications | DEC-39 | M | OTP delivered p95 ≤30 s (gateway SLA); retries |
| TR-BE-07 | Metering service recording billable and cost events (pages processed per mode, AI calls, tokens, cost estimates, scripts per level) (**TR-BILL-01**) | FR-ADM-04, NFR-COST-01 | M | Metering reconciles with vendor invoices within ±3% monthly |

### 5.1 Bangla text handling (TR-BN)
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-BN-01 | Deterministic Bijoy/ANSI→Unicode converter (maintained mapping tables; detection heuristic) used in imports and paste | M | Corpus test ≥99.5% character accuracy; ambiguous cases flagged |
| TR-BN-02 | Unicode NFC normalisation; Bangla digit normalisation (০–৯ ↔ 0–9) for numeric processing; preserve original for display | M | Unit tests |
| TR-BN-03 | Collation and search for Bangla names (roster search) | S | Search finds names regardless of common spelling variants (e.g., য়/য়) |

---

## 6. Database Requirements (TR-DB)

| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-DB-01 | PostgreSQL 16+, managed, with PITR (≥7 days) | NFR-REL-01 | M | Restore drill |
| TR-DB-02 | Row-level security on all tenant tables using `tenant_id` and session settings; the app role cannot bypass RLS (**TR-TEN-01**) | SEC-02 | M | CI test suite attempts cross-tenant reads/writes: all fail |
| TR-DB-03 | Separate `identity` schema (student names, rolls, consent) with column-level encryption under per-tenant keys; content tables reference `student_uid` only | DEC-14 | M | DB dump without keys shows no plaintext names |
| TR-DB-04 | Versioned entities (rubrics, templates, prompts, routes, capability levels, curriculum packs) are immutable rows with version numbers; "current" pointers are separate | TR-ARC-06 | M | Updates create new versions (trigger test) |
| TR-DB-05 | Append-only audit table with a per-tenant hash chain (**TR-AUD-01**) | SEC-10 | M | Tamper test: modifying a row breaks chain verification |
| TR-DB-06 | Migrations are forward-only and versioned; zero-downtime migration practice (expand/contract) | Ops | M | CI migration test on a production-sized snapshot |
| TR-DB-07 | Indexes and partitioning for hot tables (items, suggestions, decisions) by exam / academic year | Performance | S | Queries for a review queue ≤50 ms p95 at 5M items |

(The entity model is in `03-system-design.md` §7.)

---

## 7. AI Requirements (TR-AI)

| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-AI-01 | The capability registry (cells, levels, gate report IDs) is enforced at pipeline dispatch; no AI call for L0 cells or items without CT-2 | DEC-04, PRV-02 | M | Test: an L0 item produces zero provider calls |
| TR-AI-02 | Provider adapters for ≥2 vendors behind TR-ARC-05, supporting: structured output (JSON schema), image input with explicit resolution/detail control, batch API submit/collect, prompt caching, per-call timeout, token/cost accounting | DEC-08 | M | Contract tests per adapter |
| TR-AI-03 | Prompt templates are versioned artefacts with typed variables; student content is inserted only into delimited data fields; system prompts are fixed per version | 06 §2.4 | M | Snapshot tests of rendered prompts |
| TR-AI-04 | Output validation: JSON schema, bounds, region references, grounding check (06 §2.3); one retry; downgrade to L1 on failure | AI-REQ-04 | M | Fault-injection tests |
| TR-AI-05 | Second-opinion and extra-sample orchestration under a per-exam budget (≤35% of AI-eligible items by default) with triggers from 06 §5.2 | DEC-10, FR-AI-13 | M | Budget never exceeded; triggers logged |
| TR-AI-06 | Risk model service: per-cell calibrated model artefact (versioned) computing P(error) and level; hard triggers | 06 §5 | M | Reproduces offline evaluation outputs bit-for-bit on stored features |
| TR-AI-07 | Provenance record per suggestion: input hashes (image, rubric version, prompt version, instructions applied), provider, model ID/version, parameters, raw output (encrypted), validation results, cost, latency | NFR-AUD-01 | M | 100% of suggestions have complete provenance |
| TR-AI-08 | Identity isolation: pages of type `cover`/`booklet_cover` are rejected by the provider layer; header masks are applied before encoding; the transcript name-redaction pass runs before storage (**TR-PRV-02**) | DEC-14 | M | Planted-name test: 0 leaks in 200 payloads |
| TR-AI-09 | Kill switches: per cell, per vendor, per school, and global AI off, effective within 1 min | Safety | M | Toggle test |

## 8. OCR / Handwriting Reading Requirements (TR-OCR)

| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-OCR-01 | Handwriting reading is performed by the selected VLM (no Azure/Textract/Mathpix for Bangla: VF-16) | DEC-08 | M | Bake-off report |
| TR-OCR-02 | Transcripts keep the original script and spelling; maths as LaTeX; uncertain spans marked; legibility class per region | AI-REQ-03 | M | GS evaluation of CTER (06 §4.1) |
| TR-OCR-03 | Optional specialist Bangla HTR second reader as a separate service (CPU inference acceptable for pilot volume), used only if EXP-02 shows benefit | DEC-37 | C | Adopted only with a gate report |
| TR-OCR-04 | On-demand transcript generation for cells where auto-transcripts are off (06 §10) | FR-AI-02 | M | ≤20 s p95 in the priority lane |

## 9. Vision Requirements (TR-VIS)

| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-VIS-01 | Server-side normalisation: EXIF orientation, perspective correction (if needed), deskew, contrast normalisation, resize to the model input size; keep the original | S07 | M | Visual QA set |
| TR-VIS-02 | Page classification: QR cover (decoded), booklet cover (by position per booklet profile + template similarity), blank (ink ratio), answer page | 06 §2.2 | M | ≥99% cover detection; blank precision ≥98% |
| TR-VIS-03 | Region detection via VLM bbox output (06), normalised coordinates; fallback to structured-booklet boxes when the school uses the structured booklet | AI-OQ-1 | M | GS mapping accuracy per L1 gate |
| TR-VIS-04 | Crop generation per item region with padding; images served as tiles or WebP at display resolution | FR-REV-02 | M | Review payload ≤300 KB/item |

### 9.1 OMR (TR-OMR)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-OMR-01 | Cover-sheet MCQ grid with 4 fiducial markers; alignment by homography; fill ratio per bubble with an adaptive threshold; flags for double, faint, erased and none; set code bubble | DEC-22 | M | OMR set: unflagged misread ≤0.1% of bubbles; flag rate ≤5% |
| TR-OMR-02 | Teacher resolution UI for flagged bubbles; per-script MCQ confirmation | DEC-05 | M | — |

## 10. Math Engine Requirements (TR-MATH)

| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-MATH-01 | Numeric checker: parse the student value + unit (Bangla/Latin digits, decimals, fractions, scientific notation); compare to the answer spec with tolerance; significant-figure policy; unit dimension check and conversion (Pint-class library with a Bangla unit lexicon) | FR-RUB-05, FR-AI-05 | M | Fixture suite of 500 numeric cases |
| TR-MATH-02 | Expression checker: LaTeX→SymPy parsing (Math-Verify-style), declared symbol assumptions, `simplify(a−b)==0` with a 2 s timeout, 5-point numeric spot checks in the valid domain, domain-restriction caveat detection | DEC-32, VF-24 | M | EXP-03: false "equivalent" ≤0.5% on parsed pairs |
| TR-MATH-03 | Equation checker: compare solution sets for equations and inequalities (not expression subtraction) | 06 §9 | M | Fixture: 2x=10 ⇔ x=5 equivalent |
| TR-MATH-04 | Step checker: consecutive-step equivalence where applicable; detection of the first arithmetic error for ECF; statuses `equivalent / different / cannot_parse / cannot_decide` | DEC-32 | M | Fixture set of multi-step solutions |
| TR-MATH-05 | Sandboxed execution (separate process, no network, CPU/memory limits) | Security | M | Fuzz test with malicious LaTeX |

## 11. Scoring (Evaluation) Engine Requirements (TR-SCO)

| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-SCO-01 | Item scoring function: f(criterion decisions, rubric rules: caps, deductions, ECF, half-mark policy) → mark ∈ [0, max]; pure function, versioned | FR-AI-04, ASR-03 | M | Property-based tests (bounds, monotonicity) |
| TR-SCO-02 | Same function used for AI suggestions and teacher criterion edits (teachers may override the total, which is stored as a total override with reason) | Consistency | M | — |

### 11.1 Result engine (TR-RES)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-RES-01 | Deterministic aggregation, choice rules, component pass rules, grades, GPA, 4th-subject rule, weighting across assessments, rounding policies; pure, versioned, configurable per template/school | FR-RES-01..04 | M | **≥200 fixture cases** incl. edge cases (absent, over-answered choices, borderline rounding, 4th subject) at 100% |
| TR-RES-02 | Recalculation is idempotent and triggered on any mark or key change; results are versioned; published versions are immutable | FR-RES-09 | M | Recompute equals the stored result |

## 12. Rubric Engine Requirements (TR-RUB)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-RUB-01 | Rubric schema: item → criteria (id, text BN/EN, marks, evidence expectation, type: concept/step/final-answer/unit/format), model answer, alternatives, deductions, ECF policy, answer spec | FR-RUB-01..05 | M | JSON Schema; validation tests |
| TR-RUB-02 | Validation rules (sums, missing model answers, unobservable criteria heuristics) | FR-RUB-07 | M | — |
| TR-RUB-03 | Versioning and lock; post-lock diff and impact analysis (items whose suggestions/marks may change) | FR-RUB-08 | M | Impact list matches affected items |
| TR-RUB-04 | Template library (platform + school) and instantiation into rubrics | FR-RUB-02 | M | — |

## 13. Human Review System Requirements (TR-REV)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-REV-01 | Queue service: per teacher × question queues with ordering (risk, roll, section), claim/lease (5 min) to avoid double work, progress counters | FR-REV-01, -11 | M | Concurrent reviewers never get the same item |
| TR-REV-02 | Decision API: confirm/edit/manual/remap/flag/request-rerun/add-alternative/add-clarification/report-error/undo, each writing an audit event and a correction event | FR-REV-03, 07 §4.2 | M | Contract tests |
| TR-REV-03 | Masking service: deterministic random selection (seeded per exam × teacher) of 5% of AI-suggested items | FR-REV-05 | M | Rate within ±1% over 1,000 items |
| TR-REV-04 | Batch-confirm API for L3 cells only, with batch size ≤20 and forced-open sampling | FR-REV-06 | S | Rejected for non-L3 cells |
| TR-REV-05 | Moderation sampling and blind re-mark workflow | FR-MOD-01 | M | — |
| TR-REV-06 | Telemetry: active time per item (focus-visible time), actions, dwell alerts | 07 §4.3 | M | — |

## 14. Knowledge Base Requirements (TR-KB)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-KB-01 | Scoped knowledge artefacts (clarifications, alternatives, exception rules, instructions, templates) with scope, version, author, approval and expiry | 07 §5.1 | M (clarification, alternative) / S (rules, instructions) | Scope enforcement tests: no cross-tenant or cross-exam leakage |
| TR-KB-02 | Precedence resolver producing the instruction set per item (07 §6) and recording the applied artefact IDs in provenance | 07 §6 | M | — |
| TR-KB-03 | Re-suggestion trigger for pending items when artefacts change | FR-HITL-02 | M | ≤5 min in the priority lane |
| TR-KB-04 | Same-question exemplars (≤3 teacher-confirmed, same exam and school) available to prompts | DEC-40 | S | — |

## 15. Data Pipeline Requirements (TR-PIPE)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-PIPE-01 | Script processing DAG per 06 §2.2 as idempotent jobs keyed by (script_id, stage, input_hash); status per page/script exposed via API | FR-PRC-01 | M | Re-running a completed stage is a no-op |
| TR-PIPE-02 | Standard mode: accumulate jobs until the batch cut-off (22:00 by default), submit vendor batches, collect, and complete all downstream stages by 07:00 | DEC-34 | M | NFR-PERF-02 |
| TR-PIPE-03 | Priority and demo lanes with synchronous vendor calls and separate concurrency limits | DEC-34 | M | — |
| TR-PIPE-04 | Ingestion: checksum verification, dedupe (perceptual hash), AV scan, re-encode, store the original and normalised versions | FR-CAP-07 | M | — |
| TR-PIPE-05 | Evaluation data export (consented CT-3 only) to the eval project via manifests | 08 §1.5 | S | Consent filter test |

## 16. Model Pipeline Requirements (TR-MLOPS)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-MLOPS-01 | Registry of prompts, pipeline configs, model routes and risk models with semantic versions and immutable artefacts | TR-ARC-06 | M | — |
| TR-MLOPS-02 | Evaluation harness: run any candidate configuration on frozen GS/CS/RT, compute 06 §4 metrics with CIs, produce a signed gate report; the gate workflow updates the capability registry | FR-AIQ-03 | M | Report reproducible from stored outputs |
| TR-MLOPS-03 | Regression suite (subset of GS, ~500 items per subject, plus RT) run on every prompt/config/model change in CI; block merges on regression beyond tolerance (QWK −0.02, severe +0.5 pp) | RSK-05 | M | CI gate |
| TR-MLOPS-04 | Shadow mode: a candidate configuration runs on live items in parallel (not shown to teachers) for comparison before promotion | Safe rollout | S | — |
| TR-MLOPS-05 | Release freeze during declared exam windows except safety fixes | 07 §8.1 | M | Deployment tooling enforces the freeze |

## 17. API Requirements (TR-API)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-API-01 | REST/JSON over HTTPS, versioned (`/v1`), OpenAPI 3.1; resource-oriented; cursor pagination; idempotency keys on POSTs that create content | Clients, partners | M | Spectral lint passes |
| TR-API-02 | Chunked, resumable media upload (tus-compatible or equivalent) with per-page checksums | FR-CAP-07 | M | Resume after network drop |
| TR-API-03 | Error model: RFC 9457 problem details with stable error codes and Bangla/English messages | Usability | M | — |
| TR-API-04 | Partner API (read-only results, exam status) + webhooks signed with HMAC | FR-EXP-03 | C | — |

(Endpoint catalogue: `03-system-design.md` §12.)

## 18. Authentication (TR-AUTH)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-AUTH-01 | Mobile number + password; argon2id hashing; breached-password check; lockout after 10 failures/15 min | DEC-39 | M | Security tests |
| TR-AUTH-02 | SMS OTP for new device, reset and sensitive actions; OTP 6 digits, 5-min validity, 5 sends/hour | SEC-04 | M | — |
| TR-AUTH-03 | Token-based sessions: short-lived access tokens (15 min) + rotating refresh tokens bound to the device; revocation list | Security | M | — |
| TR-AUTH-04 | Use a proven identity library/component; do not hand-roll crypto. **DECISION REQUIRED (Eng Lead, Phase 1 sprint 0):** open-source IdP (e.g., Keycloak) vs framework libraries | Build vs buy | M | ADR recorded |
| TR-AUTH-05 | Platform staff SSO + hardware MFA | Security | M | — |

## 19. Authorisation (TR-AUTHZ)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-AUTHZ-01 | Policy-based RBAC per `08` §5.3, with scopes (tenant, school, subject, section, exam) evaluated in a central policy module; DB RLS as the second layer | SEC-01 | M | Permission matrix tests (generated from the matrix) |
| TR-AUTHZ-02 | Pre-exam content confidentiality rule (SEC-11) | SEC-11 | M | Tests |
| TR-AUTHZ-03 | Support access grants: requested by platform staff, approved by the school admin, scoped, time-boxed (≤24 h), logged | FR-ADM-06 | M | — |

## 20. Multi-tenancy (TR-TEN)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-TEN-01 | Shared database, shared schema with `tenant_id` + RLS (see TR-DB-02); per-tenant KMS keys for identity and images | DEC-38 | M | Isolation suite |
| TR-TEN-02 | Tenant-aware rate limits and quotas (allowances) | FR-ADM-04 | M | — |
| TR-TEN-03 | Tenant export and full deletion (with key shredding) | FR-ADM-05 | M | Deletion certificate |
| TR-TEN-04 | Option to run a dedicated deployment for a large customer or in-country hosting from the same artefacts | DEC-12 | C | — |

## 21. Security (TR-SEC)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-SEC-01 | OWASP ASVS L2 for web and API | NFR-SEC-01 | M | Pen test with no High findings |
| TR-SEC-02 | Secrets in a managed vault; rotation 90 days; no secrets in the app binary | SEC-06 | M | Secret scanning in CI |
| TR-SEC-03 | Encryption: TLS 1.2+; at rest AES-256; envelope encryption per tenant for images and identity | SEC-03 | M | — |
| TR-SEC-04 | Upload security: MIME allow-list, re-encoding, sandboxed PDF rasterisation, AV scan | 08 §5.4 | M | — |
| TR-SEC-05 | WAF/CDN, rate limits per user/tenant/IP | 08 §5.1 | M | — |
| TR-SEC-06 | Dependency and container scanning; SBOM per release | Supply chain | M | CI |
| TR-SEC-07 | Prompt-injection defences (TR-AI-03/04; 06 §7) and red-team release gate | AI-REQ-08 | M | EXP-08 pass |

## 22. Privacy (TR-PRV)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-PRV-01 | Consent enforcement at dispatch (CT-1 for capture, CT-2 for AI, CT-3 for datasets) | PRV-02 | M | Tests |
| TR-PRV-02 | Identity isolation for external AI (TR-AI-08) | PRV-05 | M | Planted-name test |
| TR-PRV-03 | Retention jobs per `08` §3 with a dry-run report to the school admin 14 days before deletion of images | DEC-30 | M | Deletion job audit |
| TR-PRV-04 | Personal data never in logs or analytics events (lint + runtime scrubber) | DATA | M | Log scan test |
| TR-PRV-05 | Data subject export/delete with certificates (stores purged, time) | FR-ADM-05 | M | — |

## 23. Audit Logging (TR-AUD)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-AUD-01 | Append-only audit events (actor, role, tenant, action, entity, before/after, reason, correlation ID, client, timestamp) with a per-tenant hash chain and daily anchoring | SEC-10 | M | Chain verification job daily; alert on break |
| TR-AUD-02 | Audit viewer and export (FR-ADM-03) | FR-ADM-03 | M | — |
| TR-AUD-03 | Retention ≥5 years; identity links removed at contract end | DEC-30 | M | — |

## 24. Observability (TR-OBS)
| ID | Requirement | Reason | Pri | Acceptance criteria |
|---|---|---|---|---|
| TR-OBS-01 | OpenTelemetry tracing across API, workers and provider calls; correlation ID from capture to publication | NFR-OBS-01 | M | Trace of one script end-to-end |
| TR-OBS-02 | Metrics: queue depth/age per lane, job latency per stage, provider error rates, cost per page, SLA compliance | Ops | M | Dashboards |
| TR-OBS-03 | AI quality metrics pipeline feeding FR-AIQ-01/02 (06 §6 monitors) daily | 06 §6 | M | — |
| TR-OBS-04 | Error tracking for clients (web, Android) with PII scrubbing | Ops | M | — |

## 25. Error Handling (TR-ERR)
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-ERR-01 | Provider failures: retry with back-off; fail over to the second qualified vendor only for cells where it passed the gate; else degrade the item to L1 with reason | M | Chaos test |
| TR-ERR-02 | Pipeline stage failures surface as "needs attention" with actionable reasons (retake page, link student, remap) | M | — |
| TR-ERR-03 | Client error messages in Bangla/English, non-technical, with a support code | M | — |
| TR-ERR-04 | Never block manual marking because of AI failures (L0 path always available) | M | Kill AI globally → review continues |

## 26. Performance (TR-PERF)
Targets are NFR-PERF-01..04. Additional:

| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-PERF-01 | API p95 ≤300 ms for non-media endpoints at pilot load | M | Load test |
| TR-PERF-02 | Queue fetch for the next 5 items ≤150 ms p95 | M | — |
| TR-PERF-03 | Result computation for a class of 200 students ≤5 s | M | — |

## 27. Scalability (TR-SCL)
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-SCL-01 | Horizontal scaling of stateless API and workers; worker count autoscaled by queue age | M | Scale test to 150k pages/day |
| TR-SCL-02 | Provider rate-limit management: token-bucket per vendor/model; spread across vendors only within gate-qualified cells | M | — |
| TR-SCL-03 | Capacity plan: 100k pages/day peak (pilot+production yr 1) with a path to 1M pages/day by partitioning and adding read replicas; no re-architecture | M | Architecture review |

## 28. Reliability (TR-REL)
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-REL-01 | Page durability: acknowledge to the client only after the object store write + DB record commit | M | Fault test |
| TR-REL-02 | Exactly-once effect for decisions (idempotency keys) | M | — |
| TR-REL-03 | Graceful degradation order: (1) AI second opinions off, (2) priority lane throttled, (3) standard mode delayed, (4) AI off; manual review and results never degraded | M | Runbook drill |

## 29. Availability (TR-AVL)
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-AVL-01 | 99.5% monthly (web/API); 99.9% in declared exam windows | M | SLO dashboards |
| TR-AVL-02 | Multi-AZ database and stateless services in ≥2 zones | M | — |
| TR-AVL-03 | Maintenance windows outside exam seasons; zero-downtime deploys | M | — |

## 30. Backup (TR-BAK)
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-BAK-01 | DB: continuous backup + PITR 7 days; daily snapshots 35 days; encrypted; in a separate account | M | Quarterly restore test |
| TR-BAK-02 | Object storage: versioning with 30-day non-current retention; cross-zone durability | M | — |
| TR-BAK-03 | Deletions honoured after restore (deletion replay log) | M | Restore test includes a deleted student |

## 31. Disaster Recovery (TR-DR)
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-DR-01 | RPO ≤15 min (DB), ≤1 h (objects); RTO ≤8 h (region failure) via IaC rebuild in a secondary region with restored backups | M | Annual DR exercise |
| TR-DR-02 | Capture devices hold unacknowledged pages until the server confirms (natural buffer during outages) | M | — |

## 32. Deployment (TR-DEP)
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-DEP-01 | Infrastructure as code (Terraform); environments: dev, staging (anonymised/synthetic data only), production; eval project separate | M | — |
| TR-DEP-02 | Managed container runtime (not Kubernetes) for API/workers; managed PostgreSQL; S3-compatible storage; KMS | M | — |
| TR-DEP-03 | Hosting region per DEC-12 (**DECISION REQUIRED**); portable deployment profile for a BD data centre (containers + PostgreSQL + MinIO + HashiCorp Vault/KMS) | M | Dry-run |
| TR-DEP-04 | Android app distributed via Google Play (private track for pilots) plus MDM-free sideload option | M | — |

## 33. CI/CD (TR-CI)
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-CI-01 | Pipeline: lint, type-check, unit, integration, contract, isolation, result-fixture, i18n completeness, a11y, security scans, AI regression (for AI-affecting changes) → staging → manual promotion to production | M | All gates enforced |
| TR-CI-02 | Feature flags for incremental rollout per school | M | — |
| TR-CI-03 | Database migration checks and rollback plans | M | — |

## 34. MLOps (TR-MLOPS, continued)
See §16. Additional:
- TR-MLOPS-06 (M): vendor model version watch (weekly), deprecation calendar, and forced re-gate before an alias change.
- TR-MLOPS-07 (S): cost/quality A/B reports for route changes.

## 35. Testing (TR-TEST)
See `09-qa-test-strategy.md`. Mandatory suites: result fixtures, isolation, permissions, pipeline idempotency, OMR set, maths fixtures, AI regression, red-team, capture device matrix, a11y, Bangla rendering, load, chaos, DR.

## 36. AI Evaluation (TR-AIE)
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-AIE-01 | Implement all 06 §4.1 metrics with bootstrap CIs (stratified by student) and subgroup breakdowns | M | Unit tests on synthetic confusion data |
| TR-AIE-02 | Gold/Dev/Challenge/Red-team datasets as immutable manifests with leakage checks (image hash overlap = 0) | M | — |
| TR-AIE-03 | Gate report generator with sign-off workflow | M | — |
| TR-AIE-04 | Live audit sampling (1%, ≥50 per cell per cycle) and blind re-mark tasks for annotators | S | — |

## 37. Monitoring (TR-MON)
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-MON-01 | SLO monitors (availability, processing SLA, review latency) with paging in exam windows | M | — |
| TR-MON-02 | AI monitors per 06 §6, with automatic demotion hooks | M | — |
| TR-MON-03 | Cost monitors: daily cost per page vs budget; alert at 120% | M | — |
| TR-MON-04 | Security monitors: auth anomalies, bulk export, support access, audit chain verification | M | — |

---

## 38. Cost Management and Cost Model (TR-COST)

### 38.1 Requirements
| ID | Requirement | Pri | Acceptance criteria |
|---|---|---|---|
| TR-COST-01 | Per-call cost estimation from token counts and the price table (config) at call time; monthly reconciliation with invoices | M | ±3% |
| TR-COST-02 | Per-exam AI budget = expected scripts × target cost × 1.2; soft cap (alerts) and hard cap (second opinions off) | M | — |
| TR-COST-03 | Price table versioned; the known change (Gemini 3.8 Flash 2027-01-01 price increase, VF-21) pre-loaded | M | — |

### 38.2 Cost drivers and model (assumptions labelled; **Validation Required**)

| Driver | Assumption | Estimate |
|---|---|---|
| AI inference (standard mode) | 06 §10, configuration C1 + C3 | **≈BDT 3.1 per 10-page script** (range BDT 2.5–5.9 by configuration) |
| AI inference (priority mode) | ×2 | ≈BDT 6.2 |
| On-demand transcripts | 10% of items in L1 cells, 900 tokens output | < BDT 0.2 per script (small) |
| OCR (separate) | None (VLM does the reading); specialist HTR optional | 0 in the default |
| Storage | 10 pages × ~350 KB ≈ 3.5 MB per script (originals) + ~1 MB derived; kept ~9 months (DEC-30) at ~$0.023/GB-month | ≈$0.0005 per script (negligible) |
| Bandwidth (egress to reviewers) | ~12 items × 100 KB + page views ≈ 2 MB per script at ~$0.09/GB | ≈$0.0002 per script |
| Compute (API, workers, PDF) | Fixed-ish: pilot environment ≈ $600–1,200/month (Validation Required); scales sub-linearly | Pilot: $0.06–0.12 per script at 10k scripts/month; production (50k/month): ≈$0.02–0.04 |
| Database | Managed PostgreSQL HA ≈ $200–500/month | Included in the fixed cost |
| Monitoring/logging | ≈ $100–300/month | Fixed |
| SMS | OTP ~2 per teacher per month; optional result SMS at ~BDT 0.35 per SMS (S04 range) | Result SMS ≈BDT 0.35 per student per exam if enabled (pass-through) |
| Human review | School teachers (not a platform cost) | 0 (DEC-26) |
| Data annotation (Phase 0) | 06 §4.5: ~225 marker-hours per subject + adjudication; rate BDT 500–800/h (Validation Required) | ≈BDT 250–400k per subject (one-off, plus yearly GS refresh) |
| Live audit (Phase 2+) | 1% of items, ~30 s per item | ≈BDT 0.05 per script |
| Support | Exam-season support staff | Business cost (not modelled here) |

### 38.3 Unit cost views (variable cost only, standard mode, configuration C1 + C3)

| Unit | Formula | Estimate |
|---|---|---|
| Per question (AI-eligible item) | per-script AI ÷ 12 items | ≈BDT 0.26 |
| Per answer script (10 pages) | 06 §10 | ≈BDT 3.1 |
| Per student per exam (2 MVP subjects) | 2 scripts | ≈BDT 6.2 |
| Per exam (section of 50 students, 1 subject) | 50 scripts | ≈BDT 155 |
| Per 1,000 scripts | ×1,000 | ≈BDT 3,100 (+ fixed-cost share: pilot ≈BDT 7,000–14,000; production ≈BDT 2,500–5,000) |
| Per student per year (≈24–36 AI scripts, ASM-22) | ×24–36 | ≈BDT 75–110 (variable) |

The fixed-cost share dominates in the pilot. This is a business-planning concern; the PRD pricing hypotheses (≥BDT 8/script) cover variable cost at ≥60% margin only at production volumes. It must be revisited at G2.

## 39. Vendor Dependencies and Build vs Buy (TR-VEN)

| Subsystem | Build | Buy / API | Open source | Decision | Rationale |
|---|---|---|---|---|---|
| Capture app | ✔ | — | CameraX, ML Kit (on-device), OpenCV | **Build** | Core UX; offline; QR flow |
| OCR / handwriting reading | — | ✔ VLM APIs | GraDeT-HTR (optional) | **API (VLM) + optional OSS** | VF-15/16: no hyperscaler OCR supports Bangla handwriting reliably |
| LLM reasoning/grading | — | ✔ | — | **API, multi-vendor** | DEC-08 |
| Vision pre-processing, OMR | ✔ | — | OpenCV | **Build on OSS** | Deterministic, cheap |
| Math engine | ✔ (glue) | — | SymPy, Math-Verify-style parser, Pint | **OSS** | VF-24; Mathpix not needed |
| Storage | — | ✔ managed S3-compatible | MinIO (portable) | **Buy** | — |
| Database | — | ✔ managed PostgreSQL | PostgreSQL | **Buy (managed OSS)** | — |
| Authentication | — | possibly | Keycloak or libraries | **DECISION REQUIRED** (TR-AUTH-04) | Don't hand-roll |
| SMS | — | ✔ local gateway | — | **Buy** | Local regulations |
| Analytics (product) | ✔ (event table) | — | Metabase (internal BI) | **Build minimal + OSS BI** | Privacy, cost |
| Search | — | — | PostgreSQL full-text | **OSS (built-in)** | No search engine needed |
| Monitoring | — | ✔ managed | OpenTelemetry | **Buy + OSS standard** | — |
| PDF | — | — | HTML→PDF with HarfBuzz | **OSS** | Bangla shaping |
| Payments | Manual invoicing | bKash merchant API (later) | — | **Manual first** | S15 (cheque/bank) |
| Layout models (YOLOv8, LayoutLMv3) | — | — | — | **Not used** | Licences (CN-10); VLM bbox + structured booklet instead |

**Vendor risk register:** LLM vendors (price, deprecation, terms). Mitigation: ≥2 qualified vendors, pinned versions, monthly price review. SMS gateway (availability): secondary gateway. Cloud provider (region, legal): portable core.

## 40. Technical Risks

| Risk | Probability | Impact | Detection | Mitigation | Fallback |
|---|---|---|---|---|---|
| OCR failure on Bangla handwriting | H | M | CTER/CER on GS; C2 correction rate | L1 for Bangla prose; image-first evidence; specialist second reader | Manual marking with workflow benefits |
| Bangla understanding (semantic) errors | M | M | L2 gate on EV vs BM cells | BM prose stays L1; bilingual rubric alternatives | L1 |
| Math evaluation errors (misreads, CAS false positives) | M | H | EXP-03; C6 corrections | CAS as verifier only; ECF deterministic; caveats | Maths items L1 |
| Hallucination (ungrounded evidence) | M | H | Grounding validator stats | Reject ungrounded; downgrade | L1 |
| Incorrect scoring passing review | M | H | Masked gap; moderation; live audit | DEC-33; L3 gates; moderation | Demote cell |
| Model drift / deprecation | M | H | Version watch; PSI; change rate | Pinning; re-gate; shadow | Roll back route |
| Curriculum changes | H | M | NCTB monitoring | Data-driven packs | Manual rubrics |
| Cost explosion (prices, token growth, retries) | M | M | Cost monitors | Budgets, caps, batch, routing | Reduce AI scope |
| Latency at peaks / vendor rate limits | M | M | Queue age | Batch windows, multi-vendor, priority lanes | Delay standard mode |
| Privacy (leak, unlawful transfer) | L | H | Audits, planted-name tests | Isolation, encryption, consent enforcement | Incident response |
| Vendor dependency | M | M | — | Abstraction, 2 vendors | Switch after gate |
| Teacher resistance | M | H | Adoption metrics | UX, sovereignty, training | AI-off mode |
| Data scarcity | H | H | Phase 0 progress | Design partners, annotation budget | Delay promotions |
| Capture overhead | M | H | EXP-04 | Spread capture, PDF import | Mark-capture product |
| Mapping failures (unlabelled answers) | M | M | Remap rate | Label instructions, structured booklet | Manual mapping |
