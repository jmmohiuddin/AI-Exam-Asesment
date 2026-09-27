# Technical Decisions (ADRs)

Format: context → decision → consequences. Each ADR cites the requirement it resolves. Research sources: library research 2026-09-28 (PyPI/GitHub, official docs).

---

## ADR-001 Authentication approach (resolves TR-AUTH-04)
- **Context:** TR-AUTH-04 asks Keycloak vs framework libraries. TO-7 requires "one team can operate it"; DEC-39 fixes mobile + password + SMS OTP.
- **Decision:** Framework libraries, no IdP in MVP. `pwdlib[argon2]` (argon2id) for hashing; `PyJWT` HS256 access tokens (15 min, `sub`, `tid`, `jti`, `exp`); **opaque** refresh tokens (`secrets.token_urlsafe(32)`, SHA-256 stored, `family_id`, device-bound, rotated on use, reuse ⇒ revoke family); refresh idle timeout 12 h web / 30 d capture app (audit T10). OTP: 6 digits, 5-min validity, 5 sends/hour/number, hashed at rest. Lockout 10 failures/15 min. Breached-password check via a local top-N list (no network call). SMS behind a `SmsGateway` interface; dev = console gateway.
- **Consequences:** No crypto hand-rolled (libraries do hashing/signing). Platform-staff SSO + hardware MFA (TR-AUTH-05) is **not** covered; revisit with an IdP for platform staff only before pilot.

## ADR-002 Job queue (TR-ARC-04, TR-BE-02)
- **Decision:** **procrastinate 3.x** (MIT, maintained) on PostgreSQL. Queues = lanes `priority, standard, batch_submit, batch_collect, pdf, import, maintenance`. `RetryStrategy(max_attempts=5, exponential_wait=2)`. Periodic tasks for the 22:00 cut-off, retention, monitors, chain anchoring. Jobs are deferred **inside the business transaction** (outbox semantics).
- **Gaps we cover ourselves:** durable idempotency via `UNIQUE` keys on our own rows (e.g. pipeline stage runs keyed by `(script_id, stage, input_hash)`, TR-PIPE-01); tenant-scoped async operation resource `async_operation` (RLS) that `GET /v1/jobs/{id}` reads; admin dead-letter view reads `procrastinate_jobs` (status `failed`).
- **Consequences:** The worker process runs procrastinate's async loop; our task bodies are sync functions (run in threads). Tests use procrastinate's in-memory connector for unit tests and the real DB for integration.

## ADR-003 Persistence stack
- **Decision:** SQLAlchemy 2.0 ORM (sync, pinned `>=2.0,<2.2`) + psycopg 3 + Alembic. FastAPI sync endpoints (thread pool). Postgres 16.
- **Tenancy:** every request/job opens a transaction and calls `select set_config('app.tenant_id', :tid, true)` (transaction-local, pool-safe). RLS policies on every tenant table: `tenant_id = current_setting('app.tenant_id')::uuid`, `FORCE ROW LEVEL SECURITY`. The app connects as `khata_app` (no BYPASSRLS, not owner); migrations run as `khata_owner`. Platform-global tables have no RLS but the app role gets read-only grants where appropriate.
- **Audit append-only:** `khata_app` has INSERT/SELECT only on `audit_event`; hash chain `hash = sha256(prev_hash || canonical_json(event))` per tenant, sequence per tenant via a lock row.

## ADR-004 Extended item state machine (resolves audit T5/T6)
`ItemState`: `pending, unmapped, processing, failed, manual_ready, evidence_only, suggested, confirmed, edited, flagged, moderated, locked, recheck`.
Adds to 07 §4.1: `processing→unmapped`; `processing→failed`; `failed→manual_ready|evidence_only` (degrade) and `failed→processing` (retry); `suggested|evidence_only→processing` (re-suggest after clarification/rubric version/teacher request — only while not teacher-decided); `flagged→confirmed|edited`; `manual_ready|confirmed|edited→flagged`; `moderated→edited` (moderator adjust / send back); `locked→confirmed|edited` only through exam unlock (MarksLocked→Reviewing); `recheck→locked`. "Not attempted" is `Decision.not_attempted=true` (mark 0), not a state. `ExamState` is a separate enum per SD §14.1. Both machines are pure transition tables with property tests; illegal transitions → HTTP 409.

## ADR-005 Object storage and encryption
- **Decision:** `BlobStore` protocol with `S3BlobStore` (boto3, path-style, works with AWS S3 and S3-compatible stores) and `LocalFsBlobStore` (dev/test). **Application-level envelope encryption** for all tenant blobs: AES-256-GCM with a per-tenant DEK, DEKs wrapped by a `Kms` interface (`LocalKms` master key from env in dev; cloud KMS/Vault adapter later). Works identically on any S3-compatible store and gives key shredding for tenant deletion (TR-TEN-03).
- **Note:** the MinIO server project is archived (research 2026-09); the dev compose file pins a MinIO image as an S3 emulator only. Production uses a managed S3-compatible service.
- **Serving:** because blobs are app-encrypted, images are served through an authorised API endpoint that decrypts and streams (short-lived signed URL tokens issued by the API, ≤5 min), not raw presigned S3 URLs.

## ADR-006 AI provider abstraction and default provider
- **Decision:** `AiProvider` protocol: `generate_structured(request) -> ProviderResult` (image parts with detail control, JSON schema, timeout, token/cost accounting) and optional batch `submit/collect`. Capability flags per adapter. Routing table (cell → provider/model/version/params) is versioned data. Adapters: `FakeProvider` (deterministic, used in dev/test/demo — output derived from the rubric and a fixture transcript, clearly labelled `provider=fake`), `GeminiProvider` (google-genai: `response_json_schema`, media resolution), `AnthropicProvider` (anthropic SDK: structured output via JSON schema, Message Batches). OpenAI adapter deferred (same interface).
- **Model IDs are config** (06 candidates: `gemini-3.8-flash`, `claude-haiku-4-5`, `claude-sonnet-5`). The default is chosen by EXP-02; nothing in code assumes a vendor.
- **Safety in the gateway, not the caller:** rejects cover/booklet-cover pages; requires header-masked images; student content only in delimited data fields; kill switches (global/vendor/cell/school); budget check; provenance written with every call.
- **Consequences:** No live vendor call is exercised in CI (no keys); adapters are covered by contract tests against recorded/mocked responses.

## ADR-007 Frontend stack
Vite + React + TypeScript (strict), React Router, TanStack Query, i18next (BN default for teachers, EN), KaTeX, CSS custom-property design tokens from 05 §4 (no heavy component library; Radix primitives only where accessibility needs them, e.g. dialogs/menus). Tests: Vitest + Testing Library, axe checks, Playwright e2e. Fonts: Noto Sans Bengali + Noto Sans (self-hosted).

## ADR-008 PDF, QR
WeasyPrint (Pango/HarfBuzz shaping) with embedded Noto Sans Bengali for covers, report cards, ledgers; golden conjunct test (ক্ষ, স্ত্র, র্ক, কি). QR generation with `segno` (BSD); QR decoding on the server with OpenCV `QRCodeDetector` (Apache-2.0). OMR uses OpenCV (deterministic).

## ADR-009 Bijoy → Unicode
No maintained permissive package exists (bijoy2unicode licence ambiguous, unicodeconverter GPL). **Port the mapping and reordering rules from `banglakit/bondhon` (MIT, archived)** with attribution, into `khata.engines.bangla`. Golden corpus tests cover reph, pre-base vowel signs (ি ে ৈ), ya-phala, conjuncts; output NFC-normalised. Ambiguous/low-confidence detections are flagged, never silently converted (TR-BN-01).

## ADR-010 Maths verification
SymPy 1.14 + `math-verify` (Apache-2.0) for LaTeX parsing/equivalence; its signal-based timeouts are disabled (`parsing_timeout=None, timeout_seconds=None`) and **we** enforce the 2 s limit by running checks in a separate process pool with CPU/memory limits and no network (TR-MATH-05). Units: `pint` with a Bangla unit lexicon. Status enum per audit T1.

## ADR-011 Risk model `uncalibrated-v0`
Until per-cell calibration data exists (EXP-01/02), `RiskModel` = hard triggers (06 §5: flags, CAS `different` while AI awards marks, low mapping confidence, multiple attempts, instruction-like text) ⇒ **high**; any of {min criterion confidence < 70, legibility poor/illegible, boundary proximity, second-opinion disagreement} ⇒ **medium**; otherwise **medium** as well — **never `low`** without a calibrated artefact, so no item is L3-eligible and ordering stays conservative. Thresholds are versioned config. The interface accepts a calibrated logistic artefact later (TR-AI-06).

## ADR-012 Repository layout and module boundaries
Monorepo: `backend/` (package `khata`: `core/`, `modules/<name>/`, `engines/`, `worker/`), `web/`, `infra/`, `docs/`. Boundary rules enforced with `import-linter`: `engines` imports nothing from `modules`/`core.db`; modules call each other only through `service.py`. Lint/format: ruff; types: mypy (strict on `engines`, `core`); tests: pytest (+ hypothesis for property tests).

## ADR-013 Uploads and file security
Own resumable chunked-upload scheme (tus-style semantics, per-chunk and whole-file SHA-256): `POST /v1/uploads` → `PUT /v1/uploads/{id}/chunks/{n}` (`X-Chunk-SHA256`) → `POST /v1/uploads/{id}/complete`. Pages are acknowledged only after blob write + DB commit (TR-REL-01). MIME sniffing with `python-magic` (libmagic), allow-list JPEG/PNG/WebP/PDF; images re-encoded (Pillow) to strip metadata/polyglots; PDFs rasterised in a limited subprocess; caps 25 MB/file, 500 MB/PDF import. Malware scan behind `MalwareScanner` interface: `ClamdScanner` (own small zINSTREAM client, ClamAV sidecar) in deployed envs; files are quarantined until clean. Dev uses `NoopScanner` which marks results `scan=skipped-dev` (never allowed when `ENV=production`).

## ADR-014 Identity data protection
`identity` schema holds students and consents. Names encrypted (AES-GCM, per-tenant DEK, ADR-005 KMS). Roster search uses a **blind index**: HMAC-SHA256 (per-tenant key) of normalised name tokens (NFC, য়/য় folding, lower-case Latin), so search works without plaintext in the DB (TR-BN-03, TR-DB-03). Content tables reference `student_uid` only.

## ADR-015 Hosting (DEC-12) — deferred
Not needed to build. The portable profile (containers + PostgreSQL + S3-compatible storage + KMS interface) keeps both BD-datacentre and regional-cloud options open. `infra/` ships Dockerfile + docker-compose; Terraform is deferred until DEC-12 is decided.
