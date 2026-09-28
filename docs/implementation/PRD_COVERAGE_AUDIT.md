# PRD Coverage Audit — what is built, what is left

| Field | Value |
|---|---|
| Date | 2026-09-28 |
| Audited against | `docs/01-PRD.md` §15–§29 (106 functional requirements; 85 Must, 18 Should, 3 Could) |
| Code state | commit `bf58951`; backend 5,173 LOC / 312 tests passing / 78% coverage; web 2,619 LOC / 31 tests |
| Method | Every FR checked against the migrations (25 tables), the 16 live endpoints, `khata/engines/`, and `web/src/`. Verified by running the backend suite, not by reading the previous status notes. |

## 1. Headline

| Measure | Value |
|---|---|
| FRs fully delivered | **8 / 106** (7.5%) |
| FRs partially delivered | **18 / 106** (17%) |
| FRs not started | **80 / 106** (75%) |
| **Must (MVP) FRs, weighted** | **≈ 18% complete** (8 full + 18 partial of 85) |
| Endpoints built vs SD §12.1 catalogue | 16 of ~100 |
| Modules built vs SD §2 | 4 of 23 (`identity`, `org`, `assessment`, `aigateway`) — and `assessment` is a thin merge of what the spec splits into `exams`, `rubrics`, `capture`, `review`, `results` |

**What this means.** The spine is real and load-bearing: multi-tenant RLS, the rubric model, the deterministic scoring engine, the state machine, and a teacher review screen proven end to end in a browser. But the MVP as the PRD defines it is roughly **one-fifth built**. The PRD itself budgets Phase 1 at Nov 2026 – Apr 2027 (≈6 months of team time); the remaining ~82 requirements are consistent with that.

## 2. Status by area

Legend: ✅ delivered · 🟡 partial · ⬜ not started

| Area | ✅ | 🟡 | ⬜ | State |
|---|---|---|---|---|
| ORG — org, users, roster | 0 | 4 | 3 | Tables exist; **no student entity at all**, no roster import, no consent. `exam_candidate` is a stand-in. |
| CUR — curriculum | 0 | 0 | 4 | Nothing. No packs, no paper templates, no choice rules. |
| EXM — exams | 1 | 2 | 5 | Exam + flat items + lock work. No sub-parts, stimulus, MCQ key, QR covers, math editor. |
| RUB — rubrics | 5 | 1 | 3 | **Strongest area.** Criteria, alternatives, deductions, ECF, caps, answer specs, validation all implemented as a pure engine. |
| CAP — capture | 0 | 0 | 10 | Nothing. Answers are submitted as plain text. No Android app, no pages, no images, no PDF import, no attendance. |
| PRC — processing | 0 | 1 | 4 | Synchronous `evaluate` endpoint only. No queue worker, no region mapping, no identity redaction before AI calls, no processing modes. |
| AI | 2 | 1 | 10 | Criterion decisions + evidence + deterministic scoring work against a Fake provider. No capability registry, transcript, risk model, mathcheck, OMR, injection detection, second opinion. |
| REV — review | 1 | 5 | 5 | One-script review screen works. No question-wise queue, reason codes, masked items, region remap, offline. |
| HITL | 0 | 0 | 5 | Nothing. Corrections are stored but not classified or fed back. |
| MOD — moderation | 0 | 2 | 1 | Lock blocks on undecided items. No sample, no blind re-mark, no unlock-with-OTP. |
| RES — results | 0 | 1 | 8 | Script totals only. **No results engine**: no component pass rules, grades, GPA, tabulation, report cards, publish. |
| FBK / APL / ANL / AIQ / ADM / EXP | 0 | 1 | 21 | Nothing beyond audit tables. No slips, re-checks, dashboards, gate workflow, settings, exports. |

## 3. Delivered in full (8)

`FR-EXM-01` create exam · `FR-RUB-01` criteria + model answer · `FR-RUB-03` alternatives · `FR-RUB-04` deductions + ECF · `FR-RUB-05` answer specs (numeric tolerance, sig-figs, units) · `FR-RUB-07` pre-lock validation · `FR-AI-03` criterion decisions with evidence · `FR-AI-04` deterministic mark from criterion decisions.

## 4. Partial (18) — and what is missing from each

| FR | Built | Missing |
|---|---|---|
| FR-ORG-01/02 | `organization`, `school`, `academic_year`, `class_level`, `section` tables | No API, no school profile fields (EIIN, mediums, shifts, logo) |
| FR-ORG-04/05 | `app_user`, `role_assignment`, `teaching_assignment`; role deps enforce access | No staff-management API; assignments do not drive queues |
| FR-EXM-02 | Flat items with marks | Sub-parts (ka/kha/ga/gha), stimulus (uddipok), choice rules |
| FR-EXM-07 | All 9 lifecycle states + guards in `engines/workflow` | `moderation`, `published`, `recheck` never reachable |
| FR-RUB-08 | Lock; rubric rows are versioned | No post-lock re-version flow, no impact view, no re-suggest |
| FR-PRC-01 | Script status enum | No page entity, no reasons, no dashboard |
| FR-AI-10 | Blank → `cannot_determine` + `needs_teacher` | Crossed-out and not-attempted detection |
| FR-REV-02/03/07 | Review card (answer, model answer, rubric, AI reasoning, evidence, confidence); confirm + edit | Image crops and zoom, remap region, mark blank, completeness view |
| FR-REV-08/10 | Responsive layout; AI can be absent | No keyboard shortcuts; no explicit L0 manual mode |
| FR-MOD-02/03 | Lock blocked while items undecided | No capture-completeness check; unlock has no OTP or versioning |
| FR-RES-01 | Script total recomputed from confirmed items | No sub-question → question → component → subject rollup |
| FR-ADM-03 | `audit_event` + hash chain tables | No writer wired to actions, no viewer, no export |

## 5. The five things that block everything else

1. **No student entity.** `roster` does not exist, so consent (`FR-ORG-06`), results per student, slips, re-checks and privacy requests have nothing to hang off. Everything downstream of marking is blocked on this.
2. **No results engine.** `engines/results/` is an empty directory. `TR-RES-01` requires ≥200 fixture cases at 100%; none exist. This is a *pure* engine — it needs no AI, no capture and no vendor keys, and it is the product's stated value even with AI switched off.
3. **No capture.** Ten FRs, the Android app, and the entire image pipeline. This is the largest single block and needs an Android SDK that is not in this environment.
4. **No worker.** `khata/worker/` is empty; evaluation runs synchronously inside the request. Processing modes, re-processing and batch AI all need the Postgres queue that the migration already provisions.
5. **No capability registry.** `FR-AI-01` gates every other AI FR. Without `capability_cell` + levels, "honest capability" (PP-3) is a claim, not a mechanism.

## 6. Non-functional and release gates

| Gate (PRD §29, MVP/G1) | Status |
|---|---|
| All Must FRs pass their criteria | ✗ ~18% |
| Security pen test, no High findings | ✗ not run |
| DPIA approved | ✗ not started |
| Regression + red-team suites green | ✗ do not exist |
| Result-engine fixture suite at 100% | ✗ engine does not exist |
| Gate reports for every cell above L0 | ✗ no registry, no gold set |
| Bangla linguistic review | ✗ not started |
| Training material and runbook | ✗ not started |

Phase 0 validation (EXP-01..06, gate G0) has not run either: no legal opinion, no design partners, no consented scripts, no model bake-off. Per the roadmap those gate the AI levels that Phase 1 ships.

## 7. Recommended order for the remaining work

Sequenced so that each step is provable on its own, cheapest-to-prove first. Steps 1–3 need no AI keys, no images and no Android.

1. **`engines/results`** + the ≥200-case fixture suite — grades, GP, GPA with the 4th-subject rule, component pass rules, choice rules, rounding. Pure, deterministic, fully specified by VF-05.
2. **`engines/mathcheck`** — numeric tolerance, units, sig-figs, expression equivalence. Consumes the `AnswerSpec` the rubric engine already defines.
3. **OTP sign-in** — tables and config already exist; the web client already codes for the `status` discriminator.
4. **`roster` module** — students, enrolment, consent (CT-1..3), Excel/Bijoy import with dry-run and validation report.
5. **`curriculum` module** — packs, paper templates, choice rules; then exam sub-parts and MCQ keys on top.
6. **Worker + pipeline** — Postgres queue lanes, then capture (upload, pages, PDF import), then region mapping and identity redaction.
7. **Results module, moderation, publish** (publish gated on step-up OTP), then re-checks, exports and dashboards.
8. **`infra/`** — Dockerfile, compose, CI running both gate suites; Playwright specs for the slice.
9. **Android capture app** — blocked in this environment (no SDK).
