# B-Series Cross-Notes: Contradictions and Consolidation Across B1, B2, B3

- **B1:** *Comprehensive Technology Feasibility Research Report*, Drive `1ZMBR8-uNJoinESx5XOIafBbOydAL21JGmshZCc6PYfA`. Extract: `B1-tech-feasibility.md`.
- **B2:** *System Architecture and AI Model Selection*, Drive `1f0nDi9XXEqvcUYYkFqnK4OdLQT6_zhSQv1KUEXRcEsY`. Extract: `B2-architecture-model-selection.md`.
- **B3:** *Technical Feasibility and System Risk Analysis*, Drive `1D9ujrUcFGzaUQnW5UJI1zATdvE4OYP_ALV6agPlqMSE`. Extract: `B3-technical-risk.md`.

All three read as AI-generated deep-research outputs. They share structural tells: dangling `[cite: N]` markers with no numbered bibliography, blog and price-aggregator sources, uniform tables of unsourced numbers, and the same dated model set (Claude 3.5 Sonnet / GPT-4o / Gemini 2.0). Judgements below marked **[Analyst note]** are mine.

---

## 1. Where the three documents agree (high-confidence consensus)

1. **No monolithic VLM grader.** All reject "image → one multimodal LLM → score" for high-stakes grading: error propagation, no audit trail, hallucination, cost.
2. **A specialised, staged pipeline:** IQA/preprocessing → layout/segmentation → HTR/OCR → evaluation → confidence → human review → deterministic aggregation and audit.
3. **Math via OCR→LaTeX→SymPy.** Mathpix is the primary math OCR in all three. SymPy is used for symbolic equivalence, and LLMs are kept away from arithmetic.
4. **Deterministic objective scoring** (exact match / regex / Levenshtein), deterministic totals, and a PostgreSQL ledger.
5. **Structured JSON rubrics** with concepts, weights and penalties are a prerequisite for consistent partial credit.
6. **HITL is mandatory** for low-confidence items, diagrams, open-ended (especially Bangla literature) essays and appeals.
7. **Diagram grading is not ready** for the MVP.
8. **The MVP should be constrained** to STEM (plus English in B1), templated or anchored answer sheets, and excluded essays and diagrams.
9. **Bangla handwriting is the hardest perception problem.** Isolated-character accuracy of about 98% (CMATERdb, BanglaLekha-Isolated, Ekush) does not transfer to continuous script.
10. **Handwritten prompt injection** is a real threat (B2, B3). Treat HTR output strictly as data.
11. **Measure against a human inter-rater baseline** (QWK, MAE), not generic LLM benchmarks.

---

## 2. Contradictions between the documents

### 2.1 Bangla handwriting accuracy (the most consequential disagreement)

| | B1 | B2 | B3 |
|---|---|---|---|
| Full-page / continuous Bangla HTR | CER 12.83–18.68%, WER 36.01–48.63% (Flor Gated-CNN, CRNN, Transformer on BN-HTRd / BanglaWriting) | Fine-tuned TrOCR CER 10.89%; GraDeT-HTR CER ~8.4%; Qwen2.5-VL-7B CER 6.5–12%; Google Vision 20–35%; Tesseract >45% | Fine-tuned "Swin + BanglaBERT" TrOCR **CER <3% (1.9%)**; zero-shot VLM >12% (12.4%); Tesseract >35% (38.5%) |
| GraDeT-HTR | WER ~22–28% | Line-level 71.2%, CER ~8.4% | Not mentioned |
| Verdict | **"Unviable for high-stakes autonomous grading"**; 100% human review for Bengali scripts | Feasible with specialised fine-tuned HTR + image audit + confidence routing | **"FEASIBLE"** |
| Gate | Bengali WER ≤25% for automated short text | Switch to direct VLM if CER <3% at <$0.20/M | CER ≤3% to launch; abandon if >5% |

**Better supported: B1.**
- Its figures trace to real public benchmarks (BN-HTRd, BanglaWriting, the ResearchGate offline-Bangla-HTR study, the GraDeT-HTR arXiv paper).
- It explains the isolated-vs-continuous gap correctly.
- B2's numbers sit in the same general range, but its source column is empty.
- B3's CER 1.9% has only a dangling `[cite: 1]`. It is 5–10× better than anything the other docs cite, and it attributes the result to an architecture (BanglaBERT as a *decoder*) that does not match how BanglaBERT works.

**[Analyst note]** Plan for CER around 8–18% on real BD student handwriting until a local benchmark says otherwise. Treat B3's <3% as a *target gate*, not an expectation. Notably, B2's own decision rule ("switch to direct VLM ingestion only if CER <3%") implicitly concedes that nobody currently achieves 3%.

### 2.2 Does any AI mark become final without a human?

| B1 | B2 | B3 |
|---|---|---|
| **No.** Even C_total ≥0.85 is "staged for batch one-click teacher approval"; <0.85 goes to a focus queue; <0.50 is fully manual | **Yes.** ACS ≥0.88 is auto-accepted "without human intervention"; 0.70–0.88 is auto-accepted if two models agree within 0.5 marks; target 85–90% auto-acceptance | **Yes.** s(x) ≤ λ̂ auto-commits; 5% random audit sampling |

**Better supported: B1's position for the MVP.**
- It matches the Gradescope precedent B1 documents (AI groups answers, humans grade) and BD trust sensitivities. B2's own reference on the CBSE OSM controversy in India shows public-trust risk from digital marking.
- B2 and B3 auto-accept rates are unvalidated.
- **[Analyst note]** A phased approach is defensible: 100% teacher confirmation in the pilot, then auto-accept once measured false-high-confidence is below about 2% (B1's gate) on a local gold set.

### 2.3 Confidence scoring and routing thresholds

| | B1 | B2 | B3 |
|---|---|---|---|
| Method | Weighted composite: OCR log-prob, layout IoU, 1 − semantic variance (N=3, T=0.3), rubric cosine | Weighted composite ACS: HTR, layout, semantic softmax, 1 − multi-pass disagreement | **Conformal prediction (SCOPE)** on a non-conformity score (entropy, HTR softmax, ensemble variance, CAS errors) |
| Thresholds | ≥0.85 batch approve; <0.85 focus review; <0.50 manual | ≥0.88 auto; 0.70–0.88 second model; <0.70 human; MVP <0.82; "highest reliability" <0.80 (inverted logic) | λ̂ certified for FDR α=0.02; ensemble spread >0.5 → human; diagram conf <0.85 → human |

**Better supported: B3's *approach*, B1's *thresholds*.**
- Calibrating a threshold on held-out labelled data to a target error rate is methodologically superior to hand-picked weights and cut-offs, and B3 is the only document that proposes it.
- But B3 over-claims "certified" guarantees. SCOPE is a pairwise-judging method, and exchangeability breaks across schools.
- B2's thresholds are internally inconsistent: it calls a lower escalation threshold "more conservative".
- **[Analyst note]** Start with simple split-conformal or empirical threshold calibration on the gold set. Report the false-high-confidence rate (B1's <2% gate), and re-calibrate per subject and per school cohort.

### 2.4 Primary LLM for subjective grading and whether to self-host it

| B1 | B2 | B3 |
|---|---|---|
| **Self-hosted Qwen2.5-VL-72B** primary ("cost efficiency"); GPT-4o / Claude 3.5 Sonnet fallback | **Gemini 2.0 Flash API** primary; Gemini 2.5 Pro / Claude 3.5 Sonnet escalation; GPT-4o verifier; GPT-4o mini failover | **Claude 3.5 Sonnet + GPT-4o dual-LLM ensemble** (Gemini Pro third) via API, LiteLLM failover |

**Better supported: B2's cost logic (cheap first-pass model, escalate hard cases), but not its specific model.**
- B1's self-hosted 72B VLM is expensive at pilot scale and contradicts its own cost argument.
- B3's always-on dual frontier ensemble contradicts its own $0.0088/script cost. B2 shows ensembles on every item cost +200–250%.
- **[Analyst note]** Every named model is dated or deprecated as of Sept 2026 (Claude 3.5 Sonnet, GPT-4o, Gemini 2.0 Flash). The model choice should be decided empirically by B2's 10-pipeline bake-off on current models, with Bangla comprehension explicitly tested. None of the three docs measured LLM Bangla grading quality.

### 2.5 Direct image to LLM vs OCR-first

- **B1:** OCR-first. Subjective items go to a VLM, but the MVP routes transcripts. The confidence formula relies on OCR log-probs.
- **B2:** OCR-first **plus** an image crop attached for audit (cascade options C/D). Direct multimodal is used "only as an audit pass". It gives an explicit trigger to switch to direct VLM (Bangla CER <3% at <$0.20/M).
- **B3:** OCR-first. The zero-shot VLM is "technically infeasible". Grounding requires bbox citations.

**Better supported: B2 (dual-path).** It addresses the key failure B2 and B1 both name, a dropped negation "না", by letting the grader see the pixels. **[Analyst note]** This should also be tested head-to-head against direct-VLM transcription, since modern VLMs may now beat specialised Bangla HTR. None of the docs has current data.

### 2.6 RAG vs full-context rubrics

- **B1:** uses RAG with semantic concept decomposition and BanglaBERT embeddings (cosine ≥0.82) for concept matching.
- **B2:** **No RAG.** Inject the complete marking scheme in context. Use text-embedding-3-large plus an LLM pass for alternative answers.
- **B3:** no RAG. Uses pre-compiled JSON micro-rubrics with required and negative concepts.

**Better supported: B2/B3.** Rubrics per question are small, and retrieval adds a failure mode. **[Analyst note]** B1's fixed cosine threshold on BanglaBERT (not a sentence-embedding model) is weak.

### 2.7 Who assigns partial credit in math

- **B1:** fully deterministic step rules. The LLM only labels the error type.
- **B2:** SymPy locates the erroneous step, then **an LLM applies the rubric** to the symbolic diff. DeepSeek R1 is the math fallback.
- **B3:** a deterministic rule engine with carry-forward, penalty caps, and randomised numeric equivalence.

**Better supported: B3 (with B1).** It keeps determinism and handles carry-forward errors, which is how BD examiners actually mark. B2's LLM allocation and LLM fallback reintroduce non-determinism. **[Analyst note]** None of the three handles equation-level (solution-set) equivalence correctly; all rely on `simplify(a − b) = 0`.

### 2.8 Cost per unit (order-of-magnitude disagreement)

| | B1 | B2 | B3 |
|---|---|---|---|
| Headline | **$0.06–0.09 per page** (incl. human review) | **$0.0289 per 8-page script** (≈$0.0036/page, incl. human review) | **$0.0088 per script** (compute only) |
| Human review assumption | $0.15 **per page**, 25% review rate | $0.15 **per script**, 8% escalation | $0.05 per escalated item; not in the average |
| Gate | ≤$0.08/page compute | — | ≤$0.03/script; abandon >$0.10 |

For an 8-page script, B1's cost is about $0.50–0.70 and B2's about $0.03: roughly a 20× difference, almost entirely from human-review pricing and escalation-rate assumptions.

**Better supported: B1 (more conservative and more transparent).** B2's $0.15 per full-script review implies seconds of teacher time for 8 handwritten pages. B3 omits human cost and assumes 65% of scripts need only TrOCR. **[Analyst note]** All three agree human review is the dominant cost. The real unknowns are escalation rate and minutes per review, and the pilot must measure both.

### 2.9 Latency

- **B1:** 3.5–8.0 s per page, async; P95 gate <10 s/page.
- **B2:** 3.2–3.8 s per page for C/D.
- **B3:** P95 2.8 s per *script* for its most complex architecture; POC target <5 s per script.

**Better supported: B1.** B3's number is implausible with Mathpix plus dual-LLM calls per question. Latency is not a critical constraint for async exam marking anyway.

### 2.10 Infrastructure and deployment

| B1 | B2 | B3 |
|---|---|---|
| Cloud-native microservices: NGINX, RabbitMQ, Kubernetes + KEDA, vLLM/TensorRT, PostgreSQL + S3 (local); GPU sizing up to 32×H100 | Lean: single GPU for HTR in the MVP, Gemini API, PostgreSQL; self-hosted YOLOv8 in production; `AIProvider` abstraction | Heaviest: Kafka + Redis, Kubernetes HPA, Triton/vLLM on L4, LiteLLM, AWS S3 Object Lock + KMS, Prometheus/Grafana, DLQ, 99.99% availability |

**Better supported: B2 for the MVP.** B1 and B3 over-engineer for a pilot of 5–10 schools. **[Analyst note]** A monolith plus a Postgres-backed job queue, one GPU (or pure APIs) and object storage in-country is sufficient through the pilot. The useful bits from B3 (idempotency keys, DLQ, override-rate alerts) are cheap to add without Kafka or Kubernetes.

### 2.11 Cloud vs on-prem, and data residency

- **B1:** local BD data residency required (cites the Personal Data Protection Ordinance 2025 at bdlaws). Also uses US APIs under ZDR contracts and names AWS Textract / Google Document AI. This is self-contradictory.
- **B2:** "BDPA" requires in-country storage and 7-year retention. It self-hosts HTR for sovereignty but sends grading to the Gemini API. The citation is a paper on **India's** DPDP Act 2023, which is a wrong-jurisdiction source.
- **B3:** does not address BD law. It uses AWS S3/KMS (no BD region) and US LLM APIs.

**Better supported: B1**, as the only doc citing the actual BD instrument, but none resolves whether cross-border *processing* is permitted. **[Analyst note]** This needs legal review of the Ordinance text. B2's infeasibility trigger ("a regulatory ban on cloud LLM APIs for educational records") is the right risk to test early. Design for PII redaction before any external call regardless.

### 2.12 Timelines, data volumes and benchmark size

| | B1 | B2 | B3 |
|---|---|---|---|
| Benchmark / gold set | 5,000 double-blind graded papers; 500-output calibration | **300 scripts**, 3 teachers | **10,000 scripts**; 5,000 for conformal calibration |
| Training data | 50k BN + 20k EN + 15k STEM pages | Not specified (fine-tune HTR) | 10k BN-HTRd + local |
| Timeline | 18 months (Phase 0 is 3 months, 5,000 images) | MVP → production, undated | **28 weeks**, incl. 14 POCs in 8 weeks and a 20,000-script pilot in 6 weeks |
| Pilot | 5 institutions (Dhaka, Chittagong), 10,000 exams | 300 scripts from Dhaka and Chittagong centres | 10 institutions, 20,000 scripts |

**Better supported: B2's 300-script start and B1's phased timeline.** B3's timeline is unrealistic. **[Analyst note]** 300 double-graded scripts is enough to rank pipelines and estimate human QWK. Larger sets can follow the pilot.

### 2.13 Accuracy / agreement targets

| | B1 | B2 | B3 |
|---|---|---|---|
| Human–human QWK | 0.75–0.85 observed | Targets ≥0.78 prose, ≥0.92 STEM | Not stated |
| AI target | QWK ≥0.80 on the high-confidence subset; within-1-mark ≥92% | Match the human baseline; scorecard claims D ≥0.89 | κ ≥0.88 vs master teachers |
| Degradation | Uncorrected-HTR QWK <0.55 | — | 87% of math grading discrepancies stem from transcription |

**Better supported: B2's principle** (the AI target is the local human–human baseline, per subject) **combined with B1's subset framing** (QWK on auto-graded items plus a false-high-confidence rate). B2's "D ≥0.89" and B3's κ ≥0.88 for essays are unsupported. B1 and B3 agree that transcription quality, not reasoning, is the dominant error source.

### 2.14 MVP scope

- **B1:** STEM **and English**, Grades 9–12, fixed templates, answer clustering. Excludes Bangla literature, diagrams and un-templated homework.
- **B2:** full-subject 300-script benchmark (including Bangla and English prose). The MVP is TrOCR → Gemini Flash → SymPy across question types.
- **B3:** **STEM only** (Math, Physics, Chemistry), anchored forms, MCQ, short answers and bounded derivations.

**Better supported: B1/B3 (narrow).** **[Analyst note]** Open issue: BD secondary STEM answers are often written in Bangla (Bangla-medium), so "STEM-only" does not avoid Bangla HTR. Only B1 implicitly handles this by including English-medium. B1's **answer clustering** (the Gradescope pattern) is unique to B1 and is a strong, low-risk MVP feature the others miss.

### 2.15 Internal-consistency quality

| Doc | Key internal contradictions |
|---|---|
| B1 | Mathpix cost ($0.015/page vs $20–40 per 1k pages); "100% human review for Bengali" vs automated Bengali short-text gate; local residency vs US APIs; microservices / 32×H100 vs a 5-school pilot |
| B2 | Inverted threshold logic (0.82 "conservative" MVP vs 0.88 production "reducing review"); "no ensemble" but the medium band averages two models; "deterministic math" but an LLM assigns partial credit and R1 is the fallback; India DPDP cited for BD law |
| B3 | $0.0088 cost assumes 65% TrOCR-only scoring vs an always-on dual-LLM architecture; human cost excluded; "serverless" vs Kafka + K8s; BN-HTRd claimed to fix code-switching; Bangla "FEASIBLE" while the MVP excludes text-heavy subjects |

---

## 3. Which document to trust for what

| Decision area | Most reliable source | Why |
|---|---|---|
| Bangla HTR expectations | **B1** | Traceable benchmark numbers; conservative; correct isolated-vs-continuous distinction |
| Architecture pattern and cascade | **B2** | Clear topology comparison; dual-path OCR + image audit; routing/cascade logic; AIProvider abstraction |
| Model bake-off / experiment design | **B2** (+ B1 experiments 1, 3–7) | 10-pipeline comparison, 300-script three-teacher gold set; B1 adds bias and calibration experiments |
| Risk register and HITL triggers | **B3** | Most complete; RPN prioritisation; grounding requirement; injection red-team |
| Product de-risking lever | **B3** | Anchored answer sheets, QR/ID checksums, bounded boxes |
| Rubric schema and partial credit | **B3** (+ B1) | Carry-forward, negative concepts, typed criteria (deterministic_math / numeric / semantic) |
| Competitive precedent | **B1** | Gradescope answer clustering, documented from official guides |
| Cost modelling | **B1** (with caution) | Most conservative human-review assumption; all three are unvalidated |
| Infrastructure | **B2** | Least over-engineered |
| Legal / residency | **None adequate** | B1 cites the right instrument but contradicts itself; B2 cites the wrong country; B3 is silent |

---

## 4. Consolidated list of every model / vendor / tool, and which doc names it

Legend: **R** = recommended as primary/selected; **F** = fallback or secondary role; **M** = mentioned or compared only; **X** = explicitly rejected or baseline-to-beat.

### 4.1 Handwriting / text OCR (HTR)

| Model / tool | B1 | B2 | B3 | Notes / [Analyst note] |
|---|---|---|---|---|
| TrOCR-Large (Handwritten), Microsoft | R (English) | R (English and general) | R (fine-tuned core HTR) | English-only out of the box; Bangla needs a new decoder |
| Fine-tuned TrOCR for Bangla / "TrOCR-Bangla" | M | R (Bangla, with GraDeT) | **R** ("Swin + BanglaBERT decoder") | B3's architecture description is technically dubious |
| Fine-tuned multilingual TrOCR (code-switch) | — | R (mixed-language) | — | Does not exist off the shelf |
| GraDeT-HTR | **R** (Bangla; fine-tune) | R (Bangla) | — | arXiv 2509.18081; most Bangla-specific named model |
| Flor Gated-CNN | M (baseline) | — | — | |
| CRNN (custom) | M | M | — | |
| CompoundDenseNet | — | M (isolated chars) | — | |
| BanglaNet (Inception-ResNet-DenseNet) | M (ResNet-DenseNet ensembles) | M | — | |
| ViT (Patch6) character classifier | — | M | — | |
| Bornonet | — | — | M (reference only) | |
| Tesseract v5 (Bangla) | — | X (baseline, pipeline 4) | X (Approach A) | |
| Google Cloud Vision API | — | F (English HTR fallback) | — | No BD region |
| Google Cloud Document AI | M (English HTR) | — | — | No BD region |
| AWS Textract | M (English HTR) | — | — | No BD region; no Bangla handwriting |
| LightOnOCR | — | M (evidence tier 3) | R-alt (English HTR) | Printed-document oriented |
| Qwen2.5-VL-7B(-Instruct) | M (self-hosted OCR/VLM) | F (Bangla HTR fallback; "self-hosted OCR guard") | — | Bangla quality unverified |
| BanglaBERT | R (embeddings for synonym matching) | — | R (LM "decoder" priors for HTR) | ELECTRA encoder; check license |

### 4.2 Math OCR and symbolic tools

| Model / tool | B1 | B2 | B3 | Notes |
|---|---|---|---|---|
| **Mathpix API** | **R** (buy initially) | **R** (math-HTR) | **R** (buy) | Consensus; external API, so residency and cost need verifying |
| SimpleTex | F | — | — | Chinese commercial service |
| Pix2Text | F (open-source build fallback) | — | — | |
| Pix2Tex (LaTeX-OCR), fine-tuned | — | — | F | Printed-formula oriented |
| "Swin-Transformer" math OCR | — | — | M | Unspecified |
| Nougat (fine-tuned) | — | F | — | Printed PDFs; poor fit for handwriting |
| **SymPy** | **R** | **R** | **R** | Consensus |
| SageMath | M | — | — | |
| Z3 (theorem prover / SMT) | M | — | R (with SymPy) | |
| ANTLR grammar compiler | — | — | R | |
| CDM metric | — | — | R (metric) | arXiv 2409.03643 |
| DeepSeek R1 | — | F (math fallback; math/logic audit) | — | Non-deterministic; China-hosted API |

### 4.3 Layout, segmentation, vision utilities

| Model / tool | B1 | B2 | B3 | Notes |
|---|---|---|---|---|
| OpenCV (Laplacian, CLAHE, Sauvola, homography, Radon, contours) | R | R | R | Consensus |
| BRISQUE (IQA) | — | — | R | |
| YOLOv8-Doc | **R** | R | R | Not an official model name; AGPL-3.0 |
| YOLOv8-Segment | — | — | R (diagrams) | |
| LayoutLMv3 | R/M | R | R (5-class fine-tune) | CC BY-NC-SA weights: commercial risk |
| Layout-Parser | M | — | — | |
| Table Transformer (TATR) | — | R (tables) | — | |
| DocSAM | — | — | R/M | Research code |
| Spatial GNN (Q–A mapping) | — | — | R | Unspecified; needs training data |
| Positional graph associator (rules) | — | R | — | |
| Template negative subtraction (Gradescope-style) | **R** (MVP) | — | — | |
| QR / barcode registration anchors | — | — | **R** | Product-design lever |
| SAM-2 (Segment Anything 2) | M (diagrams, experimental) | — | — | |
| CLIP | M (diagrams) | — | — | |
| Fine-tuned BERT question-intent classifier | — | — | R | Unspecified |
| Sentence-transformers | — | — | R | Unspecified |

### 4.4 LLMs / VLMs for grading, rubric compilation and verification

| Model | B1 | B2 | B3 | Status note (Sept 2026) [Analyst note] |
|---|---|---|---|---|
| Qwen2.5-VL-72B | **R** (primary subjective, self-hosted) | — | — | Heavy multi-GPU; Qwen license |
| Qwen3-VL-30B / "72B" | M | — | — | "72B" size doubtful |
| Claude 3.5 Sonnet | F (fallback) / M | R (escalation, high-tier evaluator, diagrams, rubric) | **R** (primary judge, rubric compiler, primary provider) | Deprecated/retired |
| GPT-4o | F / M | R (verifier), F | **R** (second judge, fallback) | Superseded |
| GPT-4o mini | — | F (low-cost router, failover) | — | Superseded |
| Gemini 2.0 Flash | — | **R** (primary workhorse: subjective, feedback, routing) | — | Likely retired |
| Gemini 2.0 Flash-Lite | — | M (Architecture E easy items) | — | Likely retired |
| Gemini 2.5 Flash | — | F (secondary router, diagrams) | — | Price and date in B2 doubtful |
| Gemini 2.5 Pro | — | R (reasoning specialist, escalation, verification) | — | |
| "Gemini Pro" (unversioned) | — | — | R (third judge) | Unspecified |
| o3-mini | — | M (Architecture E hard items) | — | Text-only |
| DeepSeek V3 | — | M/R (text-only grader post-HTR) | — | Promo price quoted; China-hosted API |
| DeepSeek R1 | — | F | — | |
| Llama 3 | — | — | M (open-source option) | |
| OpenAI text-embedding-3-large | — | R (alternative-answer matching) | — | Bangla quality unverified |

### 4.5 Serving, orchestration, infrastructure, ops

| Tool | B1 | B2 | B3 |
|---|---|---|---|
| vLLM | R | M (JSON mode for Qwen) | R |
| TensorRT-LLM | R | — | — |
| NVIDIA Triton | — | — | R |
| LiteLLM router | — | — | R |
| Internal `AIProvider` abstraction | — | **R** | — |
| RabbitMQ | R | — | — |
| Apache Kafka + Redis | — | — | R |
| Kubernetes (+ KEDA) | R | — | R (+ HPA) |
| NGINX API gateway | R | — | M (generic gateway) |
| PostgreSQL | R | R | R (+ RLS) |
| S3-compatible object storage (local BD) | R | R (local BD cloud) | R (**AWS** S3 Object Lock / WORM) |
| AWS KMS | — | — | R |
| Prometheus / Grafana / Alertmanager | — | — | R |
| Flutter mobile app (offline-first, SQLite queue) | R | — | — |
| WebRTC / HTML5 camera capture SDK | — | — | R |
| Python regex + Levenshtein | M (exact match) | R | M |
| GPUs: NVIDIA L4 / A10G / L40S / H100 | R (sizing table) | M (A10G) | R (L4) |
| AES-256, TLS 1.3, HMAC-SHA256 / SHA-256 audit | R | — | R (SHA-256) |

### 4.6 Datasets and benchmarks named

| Dataset | B1 | B2 | B3 | Notes |
|---|---|---|---|---|
| BN-HTRd | R (benchmark) | M | **R** (fine-tuning; 108,147 words / 788 pages) | Real, document-level Bangla HTR |
| BanglaWriting | M | — | — | Real |
| CMATERdb (3.1.2) | M | M | — | Isolated chars |
| Ekush | M | — | — | Isolated chars |
| BanglaLekha-Isolated | M | M | — | Isolated chars |
| IAM (English HTR) | M | — | — | |
| In-the-wild Bengali scene-text benchmark (arXiv 2608.03884) | — | — | M (ref) | Scene text, not handwriting |
| MMLU / GSM8K | — | X (irrelevant) | — | |
| Proposed local gold sets | 5k double-graded + 50k/20k/15k training pages | 300 scripts | 10k benchmark + 5k calibration | |

### 4.7 Competitors and precedents

| Name | B1 | B2 | B3 |
|---|---|---|---|
| Gradescope (Turnitin) | **R** (architectural precedent: answer clustering) | — | — |
| CBSE On-Screen Marking (India) controversy | — | M (ref, public-trust lesson) | — |
| Eklavvya (answer-sheet OCR blog) | — | M (ref) | — |

---

## 5. Consolidated takeaways for product decisions [Analyst note]

1. **Architecture:** a staged pipeline with deterministic math and objective scoring and HITL. Unanimous, adopt it.
2. **Perception is the bottleneck.** Budget for Bangla CER around 8–18% until measured. Run B2's pipeline bake-off (updated to current models, including direct-VLM transcription) on a roughly 300-script, three-teacher gold set before choosing any HTR or LLM.
3. **Humans confirm every mark in the pilot** (B1). Move to auto-accept only after measuring a false-high-confidence rate below 2% via calibrated thresholds (B3's idea, done simply).
4. **Product levers beat model levers:** anchored or templated sheets with QR IDs (B3), plus answer clustering for teacher grading (B1).
5. **Replace every named LLM** with current-generation equivalents, re-price from official vendor pages, and verify Bangla comprehension directly.
6. **Resolve data residency legally** before sending any script image to a foreign API. None of the docs does this correctly.
7. **Keep the MVP infrastructure small.** Defer Kafka, Kubernetes, GNNs, diagram models and conformal research.
8. **Measure human review minutes per page early.** It dominates cost and explains the 20× cost disagreement between B1 and B2.
