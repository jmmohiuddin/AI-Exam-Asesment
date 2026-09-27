# Implementation Audit — Khata (AI-Assisted Exam Script Marking Platform)

| Field | Value |
|---|---|
| Date | 2026-09-28 |
| Scope | Phase 0 audit before any implementation |
| Inputs | `docs/00`–`11` (spec package v1.0), `research/`, repository state at commit `5d70948` |
| Author | Lead engineering agent |

---

## 1. Existing Architecture
**None implemented.** The repository contains only the product-definition package (`docs/00`–`11`) and research extracts. There is no application code, no build tooling, no infrastructure code, no tests.

The *specified* architecture (source of truth, TRD §3, SD §1–3) is:
- **Modular monolith** (DEC-11): one Python 3.12 / FastAPI codebase, two process types (API, worker) from one image; math sandbox as an isolated process pool.
- **PostgreSQL 16** as system of record **and** job queue (`SKIP LOCKED`), RLS for tenant isolation, separate `identity` schema with column encryption.
- **S3-compatible object storage** (MinIO for portable profile), per-tenant keys, signed URLs ≤5 min.
- **Clients:** React + TypeScript PWA (all staff, review usable at 360 px); native Kotlin Android capture app.
- **AI:** provider abstraction, ≥2 vendors, per-cell capability levels L0–L3, deterministic engines for all arithmetic/rules.

## 2. Existing Features
None. All ~90 FRs (PRD §15) are unimplemented.

## 3. Existing Database
None. Target entity model: SD §7 (≈50 entities across org/roster/curriculum, exams/scripts/marking, results/metering/AI governance/audit).

## 4. Existing APIs
None. Target catalogue: SD §12.1 (`/v1/...`, OpenAPI 3.1, RFC 9457 errors).

## 5. Existing UI
None. Target: 30 web screens (SCR-01..30) + 5 capture screens (CAP-01..05) per `04`/`05`.

## 6. Existing AI Systems
None. No vendor accounts, keys, prompts or evaluation datasets exist in the repo. **The default model is not chosen** — it depends on the EXP-02 bake-off on real consented scripts (06 L7), which has not run. Candidates: Gemini 3.8 Flash, Claude Haiku 4.5, gpt-5.6-luna (default reader-grader); Claude Sonnet 5 / gpt-5.6-terra (second opinion).

## 7. Existing Tests
None.

## 8. Existing Infrastructure
None in repo. Local environment (verified 2026-09-28):

| Tool | Status |
|---|---|
| Python 3.12.13, uv 0.12 | ✔ |
| PostgreSQL 16.14 (Homebrew, running) | ✔ — used for dev + integration tests incl. RLS |
| Redis (running) | ✔ — not used (TR-ARC-03 forbids extra stateful stores) |
| Node 26, pnpm 9 | ✔ |
| Playwright Chromium (cached) | ✔ |
| Docker | Installed, **daemon down** — docker-compose provided but not verifiable locally |
| Android SDK / JDK | **Missing** — Kotlin capture app cannot be built or tested in this environment |
| MinIO | Missing — dev uses a filesystem storage adapter behind the same interface |

## 9. Technical Debt
Not applicable (greenfield). Risk of *creating* debt: the spec is large; the main mitigation is vertical slices with tests and module boundaries from day one.

## 10. Missing Requirements (gaps that block or shape implementation)

| # | Gap | Resolution for implementation |
|---|---|---|
| G1 | **No General Mathematics paper template** (08 has only Physics) although Maths is an MVP subject | Build from PRD FR-CUR-02: CQ 50 (answer 5 of 8, each ka1+kha2+ga3+gha4) + SA 20 (10 of 15 × 2) + MCQ 30 = 100. Marked `verification: pending` like the Physics pack |
| G2 | Default AI model undecided (EXP-02) | Provider abstraction + config route table; a deterministic **Fake provider** for dev/tests/demo; real adapters behind config. All cells ship at **L1 or lower** until a gate report exists (PRD §13.2), so production behaviour does not depend on the choice |
| G3 | Risk model needs calibrated per-cell artefacts trained on gold data that does not exist | Risk service with the 06 §5 signal vector, the **hard triggers**, and a versioned `uncalibrated-v0` rule model (conservative: never "low" without calibration). A calibrated artefact plugs into the same interface |
| G4 | Gate thresholds are provisional (06 §4, 11 §2) | Stored as versioned config, not code |
| G5 | TR-AUTH-04 decision (Keycloak vs libraries) | ADR-001 |
| G6 | DEC-12 hosting region | Not needed to build; portable profile (containers + Postgres + S3 API) keeps it open |
| G7 | UI needs endpoints absent from SD §12.1 (list exams, `/me`, preferences, notifications, lock checklist, unlock, lease release, script-complete, page-view tracking, report-AI-error, moderation outcome) | Added under `/v1` as documented extensions (OpenAPI is the source; listed in `IMPLEMENTATION_CONTEXT.md`) |
| G8 | Review-card data missing from `Suggestion` (per-criterion evidence/quote/reason, verification badges, uncertain spans, attempt/crossed-out/instruction flags, reason-code enum) | `AiCriterionDecision` carries evidence + reason; `Suggestion.flags` and `verification` JSON; `ReasonCode` enum = the 8 chips in 05 |
| G9 | Spare blank covers vs `CoverSlot.student_uid` required | `student_uid` nullable; linked later with an audit event |
| G10 | No Comment/Feedback entity for teacher-approved comments | `FeedbackComment` (draft/approved) when FR-FBK is built |
| G11 | No `Device` table in SD §7 though named in §2 | Added with the identity module (refresh-token binding) |

## 11. Conflicts With PRD (and between documents) — with resolutions

| # | Conflict | Source | Resolution |
|---|---|---|---|
| C1 | Severe-error definition: 06 = abs ≥ **max**(2, 50% of max); PRD §30 reads as "or" | 06 L213 vs 01 L630 | Use **06** (the evaluation spec owns metric definitions) |
| C2 | Unflagged-severe thresholds: PRD ≤0.5% / demote >1% everywhere; 06 ≤1% at L2, ≤0.5% at L3 | 01 L630 vs 06 L262/L339 | Per-level thresholds from **06** (config); PRD value = pilot target |
| C3 | Production cost bar: PRD G3 ≤ BDT 2.5; TRD/06 target 3.0, ceiling 6.0 | 01 L707 | Not a build conflict: metering reports cost; budget caps use 06/TRD values (config) |
| C4 | Coordinator content visibility: "progress only" vs "progress and marks, no images" | 08 L234 vs L283 | Coordinator sees **marks + progress, never script images/AI content** unless also the assigned teacher or a re-check assignee (the more specific §6.3 rule) |
| C5 | Endpoint role column in SD §12.1 omits HoD/Teacher where 08 RBAC grants them | SD L439-462 vs 08 §5.3 | **08 §5.3 is authoritative**; the policy module is generated from it |
| C6 | Platform AIQ Reviewer / Assessment Specialist roles missing from the RBAC matrix | 07 L56-57 | Platform roles `platform_admin`, `platform_aiq`, `platform_assessment`, `platform_support` (internal endpoints only) |
| C7 | Principal "sign off re-check by original marker" has no RBAC row | 07 L53 | Permission `recheck.approve_original_marker` → Principal |

## 12. Conflicts With TRD / System Design — with resolutions

| # | Conflict | Source | Resolution |
|---|---|---|---|
| T1 | CAS status names differ | 06 L312/L404 vs TRD TR-MATH-04 | One enum: `equivalent`, `equivalent_domain_caveat`, `different`, `cannot_parse`, `cannot_decide` |
| T2 | Grounding rule checks evidence **bbox** but P6 schema has no bbox | 06 L121 vs L106 | Evidence = `{region_id, span?, quote?, bbox?}`; full-transcript mode requires quote (fuzzy ≥0.9); evidence-only mode requires bbox ⊂ mapped region |
| T3 | Second-opinion trigger has no operator grouping; s7 would fire on every non-maths item | 06 L325 | `(max≥3 ∧ s1<cell_median) ∨ (item has answer_spec ∧ s7∈{different,cannot_parse}) ∨ s9`; 35% cap enforced per exam |
| T4 | τ_high/τ_low and "mapping confidence low" undefined | 06 L321 | Versioned per-cell config; `uncalibrated-v0` defaults marked *Validation Required* |
| T5 | Item state machine gaps (no Flagged→Confirmed, no re-suggest path, no unlock path, no moderator-adjust, no failure state; Unmapped only from Pending although mapping happens during Processing) | 07 L82-102 | Extended item machine (ADR-004). "Not attempted" is a decision attribute, not a state |
| T6 | Exam and item state names collide (`Processing`, `Recheck`) | 03 §14.1 vs 07 §4.1 | Separate enums `ExamState`, `ItemState` |
| T7 | `THEORY_WRITTEN` pass-rule component undefined | 08 L128 | Component groups in template: `THEORY_WRITTEN = [CQ, SA]`; configurable; `verification: pending` |
| T8 | Alternatives are item-level (RubricVersion) but endpoint is `/questions/{id}/alternatives` | SD L304 vs L455 | Knowledge artefacts scoped to the **item** (sub-part); endpoint `/v1/items/{id}/alternatives` |
| T9 | Offline prefetch 30 items vs 5-min lease and ≤5-min signed URLs | 05 L291 vs SD L370/L378 | Online: prefetch 5, lease 5 min (renewed). Offline mode (Should, FR-REV-09) deferred |
| T10 | Web session 12 h idle vs 15-min access tokens | 08 L219 vs TR-AUTH-03 | Compatible: access 15 min; refresh idle 12 h (web), 30 d (capture app) |
| T11 | Second opinion "priority to finish by 07:00" vs P8 in batch | 03 L598 vs 06 L81 | Standard mode: P8 in a second batch wave; sync fallback if not collected by 05:00 |
| T12 | Object versioning keeps "deleted" images 30 more days | TR-BAK-02 vs 08 §3 | Deletion certificate states the 30-day version/backup tail |
| T13 | Exemplars' consent basis unstated | 06 L129 vs 07 L199 | Exemplars require CT-2 on the source item, same exam only, exclude C11/C12; off by default (Should) |
| T14 | UI copy/keyboard mismatches between 04 and 05 (digit keys, ←/→, risk/level labels, masked copy) | 04 L309/L361 vs 05 L101-186 | **05 wins** (more detailed): `1–9` focus criterion; `←/→` change decision when a criterion is focused, else prev item; `0–9`+Enter total override; labels from the 05 glossary |

## 13. Missing Components (relative to the spec)
Everything is missing. Components that **cannot be delivered in this environment**: Android capture app (no SDK/JDK), cloud infra apply (Terraform), real SMS gateway, real KMS/Vault, ClamAV daemon, vendor AI calls (no API keys), gold-set evaluation (no consented data). Each gets a local substitute behind the production interface.

## 14. Security Concerns (enforced in code)
1. RLS through a **non-owner, non-superuser app role** (`khata_app`) with `FORCE ROW LEVEL SECURITY`. The local dev superuser bypasses RLS, so isolation tests connect as the app role.
2. Tenant context via `SET LOCAL` / `set_config(..., true)` per transaction (pool-safe), never session-level.
3. Identity schema: names encrypted with a per-tenant DEK (envelope). Dev KMS = local master key; interface allows Vault/KMS.
4. The provider layer itself rejects `cover`/`booklet_cover` pages and requires masked images (TR-AI-08).
5. Prompt injection: student content only in delimited data fields; structured output only; instruction-text detector.
6. Upload: MIME sniffing (not extension), re-encoding, PDF rasterisation in a limited subprocess, size caps (25 MB / 500 MB).
7. No PII in logs (structured logging + scrubber).
8. Audit hash chain per tenant; append-only enforced by revoked UPDATE/DELETE grants + trigger.

## 15. Performance Concerns
- Review-queue queries (TR-DB-07): composite indexes on `(exam_id, item_id, state, risk)`; partitioning deferred until volume justifies it.
- Image payloads ≤300 KB/item: WebP crops at display resolution.
- AI latency/cost: batch lane, cached rubric prefix, second-opinion cap.
- Results for 200 students ≤5 s: pure in-memory engine over one bulk load.

## 16. Recommended Changes
1. Adopt the conflict resolutions in §11–12 (recorded as ADRs).
2. Treat 08 §5.3 as the single RBAC source; the permission table is code, tested as a matrix.
3. Add API extensions for UI needs (G7) under `/v1`.
4. Seed every AI cell at L0/L1; L2+ only via a gate record. Synthetic gate records in dev are labelled synthetic.

## 17. Migration Requirements
Greenfield: Alembic forward-only migrations from revision 0001. Expand/contract practice from the first production deploy.

## 18. Implementation Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Scope (≈90 FRs, 2 clients, eval harness) far exceeds one delivery increment | Partial product mistaken for complete | Vertical slices; `REQUIREMENT_TRACEABILITY.md` reports status per FR honestly |
| No real AI keys / gold data | AI quality unmeasurable | Fake provider + adapter contract tests; eval harness tested on synthetic data, labelled as such |
| Android app not buildable here | Capture path incomplete | Web/PDF upload implements the same server contract (`/scripts`, `/pages`, `/submit`) the Android app will use |
| RLS mistakes → cross-tenant leaks | Critical | Isolation suite running as the app role from the first migration |
| Bangla rendering in PDFs | Unusable report cards | HarfBuzz-based renderer with embedded Noto Sans Bengali; conjunct check |

## 19. Technical Decisions Required
Recorded in `docs/implementation/TECHNICAL_DECISIONS.md` (ADR-001…).
