# 09 — QA and Testing Strategy

| Field | Value |
|---|---|
| Document Name | QA & Testing Strategy |
| Version | 1.0 |
| Status | Baseline |
| Date | 2026-09-27 |
| Owner | QA Lead (AI evaluation with AI Lead) |
| Purpose | Defines how every important behaviour is tested (functional, AI, security, performance, human workflow) and the entry/exit criteria for each release gate. |
| Source Research | S07 (POCs, red team, fault tolerance), S08 (evaluation framework, statistical testing), S05 (experiments); VF-15..VF-25 |
| Dependencies | `01-PRD.md` (acceptance criteria), `02-TRD.md` (TR IDs), `06` (metrics, gates, red team), `07` (HITL), `08` (security/privacy) |

---

## 1. Test levels and ownership

| Level | Scope | Owner | Automation |
|---|---|---|---|
| Unit | Pure functions: scoring, results, maths checks, Bijoy conversion, risk model, validators | Developers | 100% automated, CI |
| Property-based | Scoring and result invariants (bounds, monotonicity, idempotence) | Developers | CI |
| Integration | Module interactions with DB, object store, queue; provider adapters against vendor sandboxes/mocks | Developers + QA | CI (mocks), nightly (live sandbox) |
| API / contract | OpenAPI conformance, error model, authz matrix | QA | CI |
| UI / E2E | Web flows (Playwright), Android flows (Espresso/UI Automator) | QA | CI (smoke), nightly (full) |
| AI evaluation | Gold/Challenge/Red-team evaluation, gates | AI QA | On change + scheduled |
| Non-functional | Performance, load, chaos, DR, accessibility, security | QA / SRE / Security | Scheduled + pre-release |
| Human workflow | Usability, time-motion, pilot observation | UX + Product | Per phase |

## 2. Test environments and data
- **Dev/CI:** synthetic data only (generated rosters with Bangla names; synthetic scripts from volunteer-written pages with no real student data).
- **Staging:** synthetic + red-team data; never real student data.
- **Eval project:** consented, de-identified datasets (GS/DS/CS/RT/OMR) under access control (`08` §1).
- **Production:** smoke tests with a dedicated test tenant; live audit (06 §4.2 LA).
- **Test data rules:** no production data copied to lower environments; secrets are scoped per environment.

---

## 3. Functional testing
Test cases derive from PRD acceptance criteria (one or more cases per FR). Priority suites:

| Suite | Coverage | Key cases |
|---|---|---|
| Org & roster | FR-ORG-01..07 | Bijoy import of 500 rows; duplicate rolls; consent types; role scoping |
| Exam & paper | FR-EXM, FR-CUR | Template instantiation; choice-rule validation; MCQ key changes post-exam (recalculation + audit); state transitions (legal and illegal) |
| Rubric | FR-RUB | Sum validation; ECF fixtures; answer spec tolerance/units; post-lock versioning impact list |
| Capture | FR-CAP | QR boundaries; unreadable QR; no CT-1; spread split; late supplementary; offline 70-script session; kill-mid-upload |
| Processing | FR-PRC | Status accuracy; identity isolation; mode SLAs (simulated); re-processing rules |
| Review | FR-REV | Queue scoping; leases; masking rate; reasons required; undo; manual mode; batch confirm blocked below L3 |
| Knowledge | FR-HITL | Clarification re-suggests only pending items of the same question/exam; confirmed items untouched; scope isolation across exams and tenants |
| Moderation & lock | FR-MOD | Sampling; blind mode; blockers; unlock OTP |
| Results | FR-RES | **Result fixture suite (≥200 cases)**; imports; validation; publication versions |
| Re-check | FR-APL | Different marker enforced; AI hidden; result versioning |
| Admin & privacy | FR-ADM | Retention jobs (dry-run notice, deletion, certificate); data requests; support grants |

### 3.1 Result engine fixture suite (TR-RES-01)
Hand-computed by two assessment specialists independently and reconciled. Covers:
- choice rules: first-N vs best-N; over-answered;
- component pass rules (e.g., written below 33% of its marks, total ≥33 → fail);
- MCQ below pass mark;
- practical absent vs zero;
- 4th subject: GP below/at/above 2.0; GPA cap 5.0;
- rounding boundaries (x.5); half-marks;
- grade table edges (32/33, 79/80);
- weighted combination (30/70);
- absent students excluded from averages;
- re-check version increments.

**Zero tolerance:** any failure blocks release (NFR-INT-01).

---

## 4. Integration testing
- Provider adapters: contract tests with recorded responses (structured output, errors, timeouts, batch lifecycle), plus nightly live-sandbox checks on the pinned versions.
- SMS gateway: OTP delivery and retry; fallback gateway.
- Object store: signed URL expiry; per-tenant keys; deletion.
- PDF: Bangla shaping snapshots (conjunct-heavy strings, mixed scripts, KaTeX).
- Excel/CSV exports: round-trip import into partner ERP formats (EXP-11).

## 5. API testing
- OpenAPI conformance (schemathesis-style fuzzing).
- **AuthZ matrix tests** generated from `08` §5.3: every role × endpoint × scope (own/other section, other school, other tenant). Expected allow/deny.
- **Tenant isolation suite:** cross-tenant reads/writes via API and direct DB with the app role → all denied (TR-DB-02).
- Idempotency: duplicate POSTs with the same key → single effect.
- Rate limits and OTP send limits.

## 6. UI testing
- Web E2E (Playwright) for UF-01…UF-09 happy paths plus key edge cases (`04` §4).
- Visual regression for Bangla/English screens at 360, 768, 1366 and 1920 widths; conjunct rendering snapshots.
- Android: Espresso flows for CAP-01…05; **device matrix**: 5 popular models in the Tk 15–25k band (Android 10–14, 3–6 GB RAM), plus one low-light and one high-glare test condition.
- i18n completeness: no missing keys; pseudo-locale check for truncation.

## 7. Accessibility testing
- Automated axe checks in CI (0 serious/critical).
- Manual audit per release: keyboard-only review of 20 items; NVDA/TalkBack spot checks for review cards and forms; contrast verification of semantic colours; 200% zoom reflow.

## 8. Security testing
| Test | When | Pass criteria |
|---|---|---|
| SAST, dependency, container, secret scanning | Every PR | No critical/high unresolved |
| DAST (staging) | Weekly | No high |
| External penetration test (web, API, Android) | Before G1, then yearly | No open High; Medium with a dated plan |
| AuthZ/tenant isolation suites | Every PR | 100% pass |
| Upload attack tests (polyglot files, huge images, malformed PDFs) | Release | Rejected safely |
| Audit chain tamper test | Release | Detects modification |
| Planted-name identity-isolation test (200 payloads) | Every AI-affecting release | 0 leaks |
| Device security (rooted device, local storage extraction) | Pre-pilot | Queue data encrypted; PIN enforced |
| Prompt-injection red team | See §12 | 06 §7.3 criteria |

## 9. Performance and load testing
| Test | Target | Method |
|---|---|---|
| Review latency | NFR-PERF-01 | Synthetic clients with network throttling (4G/3G profiles) from a Dhaka-like latency profile |
| Processing SLA | NFR-PERF-02 | Simulated night: 150k pages submitted by 22:00 with mocked vendors at realistic latencies and rate limits; completion by 07:00 |
| API | TR-PERF-01 | 500 concurrent reviewers; p95 ≤300 ms |
| Capture app | NFR-PERF-03 | Device lab timing |
| Result computation | TR-PERF-03 | 200-student class ≤5 s; 2,000-student school ≤60 s |
| Soak | 72 h at pilot peak | No memory growth; queue stable |
| Chaos | Kill workers/API instances; DB failover; vendor 5xx storms | No lost pages; exactly-once effects; degraded mode per TR-REL-03 |
| DR | Annual | RPO/RTO met (TR-DR-01) |

---

## 10. AI evaluation testing (see `06` §4)
- **Gate runs** for every new cell, model, prompt, pipeline or risk-model version: full GS + CS + RT; metrics with CIs; subgroup cuts; signed report.
- **Regression suite** (TR-MLOPS-03) on every AI-affecting change: GS subset (~500 items per subject) + RT. Block on QWK −0.02 or severe +0.5 pp beyond tolerance, or any RT failure.
- **Statistical practice:**
  - bootstrap CIs by student (B = 2,000);
  - paired comparisons between configurations on the same items (paired bootstrap for ΔQWK, McNemar for exact-agreement changes);
  - rare-event bounds via exact binomial (rule of three) for severe errors.
- **Shadow evaluation** (S): candidate configurations run on live items without display; compared with teacher decisions and live audit.

## 11. OCR, mathematics and Bangla evaluation

| Evaluation | Dataset | Metrics | Thresholds / use |
|---|---|---|---|
| Reading (general) | GS double-keyed transcripts (100 scripts per subject) | CER, WER, **CTER** (negation/number/sign/unit/variable flips) | L1 transcript display: CER ≤10%, CTER ≤2% (06 §4.3) |
| Bangla reading | BM strata of GS; public BN-HTRd/Bongabdo (diagnostic only) | CER/WER per legibility tier; conjunct-error rate (sampled manual review) | Diagnostic for the DEC-37 decision; BM prose gate |
| Mixed script | Code-switched items in CS | CER on Latin tokens inside Bangla lines; unit/variable preservation | Risk features |
| Bangla numerals | OMR set + numeric items | Digit accuracy (০–৯ vs 0–9 normalisation) | ≥99.5% on clear writing (Validation Required) |
| Maths reading | Maths strata | Expression exact match; CAS-verified equivalence rate; step segmentation accuracy | Diagnostic; feeds L2 gate |
| Maths engine | Fixture suite (≥500 numeric, ≥300 expression, ≥100 equation, ≥100 multi-step) + EXP-03 | False "equivalent" rate; false "different" rate; cannot-parse rate; timeout rate | False equivalent ≤0.5% (TR-MATH-02) |
| Units | 200 unit cases incl. Bangla unit words | Dimension-check accuracy | 100% on fixtures |
| OMR | OMR set (≥5,000 bubbles) | Unflagged misread rate; flag rate | ≤0.1% / ≤5% (TR-OMR-01) |
| Mapping | GS region annotations | Mapping accuracy; blank FN/FP | L1 gate |

## 12. Red-team testing (EXP-08)
- The set and categories are defined in 06 §7 (≥200 items).
- Run on every AI-affecting release. Results go into the gate report.
- Quarterly refresh with new attack patterns (including Bangla paraphrased instructions).
- Pass criteria: 06 §7.3. **Failure blocks the release.**

## 13. Regression testing (non-AI)
- The full automated suite on every merge.
- A curated set of **golden exams** (synthetic): complete exam lifecycles replayed end-to-end with deterministic mocked AI outputs, verifying that results, reports and audit trails are byte-identical (or diff-explained) across releases.

## 14. Model regression testing
- Pinned model versions per cell. The vendor version watch alerts on alias changes (TR-MLOPS-06).
- Any version change → gate run (not just the regression subset) before activation.
- Rollback path: the previous route stays deployable. Switching back requires no gate if within 90 days and the same dataset version.

## 15. Human workflow testing

| Test | Phase | Method | Measures |
|---|---|---|---|
| Usability (EXP-09) | 1 | Moderated sessions, 12–20 teachers | Task success, time, SUS, trust items |
| Time-motion (EXP-05) | 0 (prototype) / 2 (pilot) | Crossover manual vs assisted | Minutes per script; accuracy vs gold |
| Capture study (EXP-04) | 0 | Timed capture of real booklets | s/script, retake rate, QR success |
| Automation-bias probe | 2 | Masked-item gap; seeded known-wrong suggestions in the **pilot's training exam only** (never in live exams) | Catch rate of seeded errors (target ≥90%) |
| Moderation workflow | 2 | Observe HoDs | Time, friction |
| Pilot observation | 2 | Site visits during half-yearly | Qualitative issues, workarounds |

**Ethics note:** seeded wrong suggestions are used only in training exercises with teacher awareness. They are never used on live student scripts.

## 16. Defect severity and release criteria

| Severity | Definition | Examples | Release rule |
|---|---|---|---|
| Sev-1 | Wrong results, data loss, data exposure, cross-tenant access, AI finalising without a teacher | Result fixture failure; leak in planted-name test | Block; hotfix |
| Sev-2 | Core workflow blocked without workaround; AI gate breach in production | Review card fails on Android Chrome | Block release |
| Sev-3 | Workflow impaired with workaround | Export column order wrong | Fix within 2 releases |
| Sev-4 | Cosmetic | Minor alignment | Backlog |

## 17. Gate test checklists
- **G1 (pilot readiness):**
  - all M-requirement tests pass;
  - result fixtures 100%;
  - isolation/authz 100%;
  - pen test with no High;
  - DPIA approved;
  - gate reports for all cells above L0;
  - red team passes;
  - load test at 2× pilot peak;
  - DR restore test;
  - accessibility audit;
  - Bangla linguistic review;
  - runbooks and support rota.
- **G2 (pilot exit):** pilot metrics (PRD §30); no Sev-1 in pilot; live-audit results within gates.
- **G3 (production):** SLOs for 2 months; cost within ceiling; incident drills done.
