# Comprehensive Technology Feasibility Research Report: AI-Powered Examination Assessment and Answer-Script Evaluation Platform for Educational Institutions in Bangladesh

- **Drive ID:** `1ZMBR8-uNJoinESx5XOIafBbOydAL21JGmshZCc6PYfA`
- **Topic:** End-to-end technology feasibility of an AI-assisted handwritten answer-script evaluation platform for Bangladesh schools and colleges. It is organised as 24 "Deliverables" (technology landscape, model landscape, pipeline, OCR/HTR, Bangla, math, subjective, rubric engine, confidence/HITL, data, evaluation, security, infra, scalability, cost, build-vs-buy, competitors, risk register, MVP, roadmap, experiments, go/no-go gates, recommended architecture), followed by 25 direct answers to feasibility questions and a final verdict.
- **Method (as presented):** A desk-research synthesis. It cites arXiv papers (GraDeT-HTR, BN-HTRd, Qwen2.5-VL tech report, Bangla character-recognition papers, an arXiv 2604.16504 handwritten-forms benchmark, and real-time answer scoring), ResearchGate (an offline Bangla HTR comparative study), vendor sites (Mathpix, SimpleTex, Qwen blog), Gradescope/Turnitin help guides, blogs (F22 Labs, nullmirror, MLExpert, Medium, beanbag.ai, debuggercafe), Reddit r/LocalLLaMA, and the Bangladesh laws portal (Personal Data Protection Ordinance 2025, bdlaws act-1574). There is no primary experimentation. Inline `[cite: 4]` and `[cite: 17]` markers point to no numbered reference list. **[Analyst note]** The structure, dangling citation tags and uniform table formatting mark this as an AI deep-research output. Most numbers in the tables have no per-cell source.
- **Coverage:** The full document was read (about 73.9k characters, ending in the reference list). It is not truncated.

---

## Main findings

1. **Five technical domains** are identified: image capture and preprocessing, CV layout analysis, OCR/HTR, NLP/VLM/LLM, and symbolic computing.
2. **Per-stage feasibility table (Deliverable 01):**
   - Image quality gate (OpenCV, Laplacian variance, blur-detection CNNs): accuracy 94.0–98.5%, <200 ms/page, <$0.001/page. **Production-Ready.**
   - Preprocessing (CLAHE, Sauvola, perspective homography): 95.0–99.0%, 150–400 ms/page, <$0.001/page. **Production-Ready.**
   - Layout analysis (LayoutLMv3, YOLOv8-Doc, Layout-Parser): 91.2–96.0%, 300–800 ms/page, $0.002/page. **Production-Ready.**
   - English HTR (TrOCR-Large, AWS Textract, Google Cloud Document AI): 92.0–97.5% (WER 3–8%), 0.5–1.5 s/page, $0.005/page. **Production-Ready.**
   - Bengali HTR (GraDeT-HTR, Flor Gated-CNN, custom CRNN): 64.0–87.2% (WER 36–48%), 1.0–3.0 s/page, $0.012/page. **Feasible with Supervision.**
   - Math structure recognition (Mathpix API, SimpleTex, Pix2Text): 95.5–98.5%, 0.4–1.2 s/region, $0.015/page. **Production-Ready.**
   - Symbolic verification (SymPy, SageMath, Z3): "100% (Deterministic)", <50 ms/expression. **Production-Ready.**
   - Subjective evaluation (GPT-4o, Claude 3.5 Sonnet, Qwen2.5-VL-72B): QWK 0.72–0.86, 2.5–7.0 s/response, $0.020–0.040/response. **Feasible with Supervision.**
   - Diagram understanding (SAM-2, CLIP, VLMs): 65–82%, 2–5 s/diagram, $0.035/query. **Experimental.**
   - Confidence and routing (calibrated deep ensembles, temperature scaling): "88–94% calibration", <100 ms. **Pilot-Ready.**
3. **Model landscape (Deliverable 02):**
   - Qwen2.5-VL-7B: 1.2–2.5 s/page, $0.80–1.20 per 1k pages self-hosted, "moderate Bengali HTR".
   - Qwen3-VL-30B/72B: 3.5–8 s/page, $4–8 per 1k pages via API.
   - Claude 3.5 Sonnet: "Latin HTR SOTA; Bengali HTR moderate", $15–30 per 1k requests, "Zero Data Retention".
   - GPT-4o: 1.5–4 s, $12–25 per 1k requests.
   - TrOCR-Large-Handwritten: "IAM WER <4.5%", 300–700 ms/line, $0.15–0.30 per 1k lines, MIT license.
   - GraDeT-HTR: decoder-only transformer with a grapheme tokenizer, "BN-HTRd / BanglaWriting WER 22–28%", 400–900 ms/line.
   - Mathpix API: "Handwritten Math Accuracy 97.8%", 200–500 ms/expression, $20–40 per 1k pages.
4. **The pipeline has 12 stages.** Capture (mobile, flatbed, school MFP; PNG/WebP plus metadata), IQA gate, preprocessing (homography, Radon deskew, CLAHE, colour-channel thresholding to separate ink from template), layout (LayoutLMv3/YOLOv8-Doc), question/sub-question ID (reading labels like "1(a)", "Q2.b", "উত্তর-৩"), HTR routing (Latin→TrOCR-Large, Bengali→GraDeT-HTR, math→Mathpix), answer-to-rubric mapping, hybrid evaluation (objective = exact match; math = LaTeX→SymPy; subjective = VLM + RAG + JSON-schema-constrained concept extraction), confidence engine, HITL routing, deterministic aggregation and audit logging, and SIS/LMS publishing.
5. **HTR feasibility spectrum:**
   - Typeset math/numerics: 98%+.
   - Handwritten math: 95–98%.
   - English HTR: WER 4–8%.
   - Code-switched: WER 15–25%.
   - Full-page Bengali HTR: WER 36–48%.
   - Digit recognition >99%. Scientific notation, chemical equations and units: 94–97%.
   - Mixed Bangla-English raises WER by 10–15% over monolingual Latin.
   - Crossed-out text needs dedicated deletion-stroke segmentation networks.
6. **Bengali is the stated primary bottleneck.** The script has 11 vowels, 39 consonants, 10 numerals, about 16 vowel diacritics (kar), phala modifiers, 280+ conjuncts, and a matra headline.
   - Isolated-character CNN ensembles (ResNet-DenseNet) reach 97.32–98.40% on CMATERdb, Ekush and BanglaLekha-Isolated. The report says this does **not** transfer to full pages.
   - Full-page/word-level results on BN-HTRd and BanglaWriting (Flor Gated-CNN, CRNN, Transformer): **CER 12.83–18.68%, WER 36.01–48.63%**.
   - GraDeT-HTR reportedly reduces WER to about 22–28%.
   - The report concludes that "unassisted Bengali HTR remains **unviable for high-stakes autonomous grading**".
7. **Math pipeline:** handwriting → Mathpix/SimpleTex LaTeX (95.5–98.5% expression-level) → SymPy AST, with `simplify(AST_student − AST_rubric) = 0` → a step-wise partial-credit rule engine. LLMs may only **classify the error type** (e.g. "sign inversion"); deductions stay deterministic.
8. **Subjective grading:**
   - Human–human QWK on secondary descriptive essays: 0.75–0.85.
   - "Fine-tuned" Claude 3.5 Sonnet / GPT-4o with concept rubrics: QWK 0.72–0.86.
   - Uncorrected HTR input: QWK <0.55 (0.45–0.55 in the chart).
   - Named failure modes: verbosity bias, handwriting/neatness bias, and hallucinated intent.
   - Mitigation: RAG plus decomposition into atomic claims, embedding comparison to rubric concepts, and an LLM restricted to claim↔concept classification.
9. **Rubric engine.** A JSON schema carries `question_id`, `max_marks`, `required_concepts[]` (concept_id, description, weight, aliases, `step_validation: deterministic_chemistry_parser`) and `penalty_rules[]`. Alternative answers are matched with BanglaBERT embeddings at **cosine ≥ 0.82**.
10. **Composite confidence:**
    - Formula: `C_total = w1·C_ocr + w2·C_layout + w3·(1 − σ²_semantic) + w4·C_rubric`.
    - C_ocr is the mean token log-prob. σ² is score variance over N=3 samples at T=0.3. C_rubric is the embedding cosine. Weights are calibrated on historical grading data.
    - Routing: **≥0.85** goes to batch one-click teacher approval; **<0.85** goes to a focus queue with red (low-confidence OCR) and yellow (missing concept) highlights; **<0.50** bypasses AI entirely for fully manual grading.
11. **Data needs:**
    - 50,000 Bengali pages from more than 500 writers across all 8 divisions.
    - 20,000 English pages from more than 200 writers.
    - 15,000 STEM pages (SSC/HSC).
    - 5,000 double-blind, 2-grader gold papers.
    - Annotation costs: layout about 3 min at $0.30/page, transcription about 12 min at $1.20/page, rubric attribution about 15 min at $2.50/page.
    - QC: inter-annotator CER ≤2.0%. Consent from administrations and guardians, with redaction of names, rolls and seals.
12. **Evaluation metrics:** CER, WER, P/R/F1, layout IoU ≥0.85, QWK, MAE, RMSE, and within-1-mark agreement ≥92%.
13. **Security and compliance:** "Personal Data Protection Act / Ordinance of Bangladesh" requires local data residency. Other controls: bounding-box PII redaction before inference, ZDR clauses with OpenAI/Anthropic/Google, AES-256 at rest, TLS 1.3, and HMAC-SHA256 append-only audit logs.
14. **Infrastructure:** "cloud-native, microservices". Flutter app → NGINX gateway → RabbitMQ → Kubernetes GPU cluster (CPU preprocessing, YOLOv8 layout, HTR on vLLM/TensorRT, SymPy workers) → PostgreSQL + S3. INT8/FP8 quantisation and KEDA autoscaling on queue depth.
15. **Scalability table (5 pages/student):**

    | Students | Pages | Storage | Peak upload rate | GPUs | Window |
    |---|---|---|---|---|---|
    | 100 | 500 | 1.2 GB | 5 rps | 1× L4 | <10 min |
    | 1k | 5k | 12 GB | 50 rps | 2× A10G | <25 min |
    | 10k | 50k | 120 GB | 500 rps | 8× L40S | <2 h |
    | 100k | 500k | 1.2 TB | 5,000 rps | 32× H100 | <6 h |

16. **Cost model per month:**
    - 10k pages: $900 ($0.090/page).
    - 100k pages: $7,200 ($0.072/page).
    - 1M pages: $61,500 ($0.061/page).
    - Human review is the largest line item: a 25% review rate at $0.15/page gives $375, $3,750 and $37,500.
    - VLM/LLM inference: $250, $1,800 and $12,000. OCR/HTR compute: $120, $1,000 and $8,000.
    - **[Analyst note]** I checked the row arithmetic and it is internally consistent.
17. **Build vs buy:**
    - Build: preprocessing gate, and the review UI plus confidence logic.
    - Fine-tune: GraDeT-HTR on local exam data.
    - Buy: Mathpix initially, with an in-house fallback in Phase 3.
    - Open source: SymPy.
    - Hybrid subjective evaluation: **self-hosted Qwen2.5-VL-72B primary**, commercial APIs as fallback.
18. **Competitor analysis (Gradescope/Turnitin).** Gradescope uses template alignment, background subtraction, AI **answer clustering** and group grading. It does not auto-grade free text on its own. The takeaway: trust comes from "AI for alignment, stroke isolation, and clustering", with humans making the final decisions.
19. **MVP.** Flutter capture → OpenCV IQA/homography → template subtraction and box extraction → router (TrOCR English / Mathpix STEM / exact matcher for structured choice) → SymPy + schema-constrained VLM → calibrated confidence gate and split-screen review.
    - Excluded: autonomous Bengali literature essays, complex diagrams, un-templated homework, and real-time synchronous grading.
20. **Roadmap:**
    - Phase 0 (months 1–3): 5,000 images; benchmark GraDeT, TrOCR, Mathpix and Qwen2.5-VL. Gate: English WER <8%, math LaTeX >95%.
    - Phase 1 (months 4–8): MVP build.
    - Phase 2 (months 9–12): 5 pilot institutions in Dhaka and Chittagong, 10,000 exams. Targets: 60% automation for math/objective, 30% for short text, QWK ≥0.80.
    - Phase 3 (months 13–18): Bengali HTR, Kubernetes scale-out, Canvas/Moodle connectors.
21. **Seven prototype experiments:**
    - Bengali HTR: 100 answers, GraDeT vs a fine-tuned CRNN.
    - English HTR: 100 scripts, TrOCR-Large.
    - Math: 100 derivations through Mathpix+SymPy.
    - Subjective: 100 science answers, Qwen2.5-VL-72B vs Claude 3.5 Sonnet.
    - Verbosity and neatness bias: paired synthetic answers.
    - Human IRR baseline: 3 teachers × 200 essays.
    - Confidence calibration: 500 outputs; flagged scripts must contain >90% of AI errors.
22. **Go/No-Go gates:**
    - English WER ≤6.0%, math LaTeX ≥96.0%, Bengali WER ≤25.0% for automated short text.
    - QWK ≥0.80 on the high-confidence subset.
    - False-high-confidence rate <2.0%.
    - Compute ≤$0.08/page.
    - P95 <10 s/page, asynchronous.
23. **Automation estimates:** STEM 65–80% of grading effort, English/short answer 50–65%, Bengali literature/descriptive 20–35%. Cost $0.06–0.09/page, latency 3.5–8.0 s/page.
24. **What would make the product infeasible:** human–human QWK <0.60 on a subject's rubric, or HTR WER >50% across all engines.
25. **Verdict:** feasible **only as an AI-assisted HITL system**. Fully autonomous grading is unviable.

---

## Quantitative claims table

| Claim | Value | Source cited | Source type | Credibility H/M/L + why |
|---|---|---|---|---|
| Bengali full-page HTR CER | 12.83–18.68% | `[cite: 4]` (dangling); likely ResearchGate "Offline Bangla HTR: comprehensive study" / BN-HTRd | Peer-reviewed / preprint | **M.** Plausible order of magnitude for BN-HTRd baselines; the exact source cell is unresolved. |
| Bengali full-page HTR WER | 36.01–48.63% | Same | Peer-reviewed / preprint | **M.** Consistent with CER ~13–19% at word level; benchmark data, not exam scripts. |
| GraDeT-HTR WER | ~22–28% | arXiv 2509.18081 | Preprint | **M/L.** The paper exists, but the range reads as a paraphrase; the dataset split is unspecified. |
| Isolated Bangla char accuracy | 97.32–98.40% (CMATERdb, Ekush, BanglaLekha-Isolated) | arXiv 1712.09872, 2401.08035 | Preprint | **H** for isolated characters. Irrelevant to full-page grading, and the report says so. |
| English HTR WER | 3–8% (4–8% in text) | None specific | None | **M.** Plausible for clean handwriting; untested on BD student scripts. |
| TrOCR-Large IAM | "WER <4.5%" | None | None | **L/M.** The TrOCR paper reports **CER** (~2.9% on IAM), not WER. Metric confusion. |
| Mathpix handwritten math accuracy | 97.8% | mathpix.com | Vendor marketing | **L.** Vendor claim, no test set named. |
| Math LaTeX extraction accuracy | 95.5–98.5% | SimpleTex blog, Mathpix | Vendor blog | **L.** Vendor/blog; exam-condition handwriting unknown. |
| Numeric digit accuracy | >99% | None | None | **M.** True for MNIST-like isolated digits; Bengali digits in context differ. |
| Scientific notation / chemistry | 94–97% | None | None | **L.** Unsourced. |
| Code-switched WER | 15–25%; +10–15% vs Latin | None | None | **L.** No Bangla-English handwritten code-switch benchmark cited. |
| Human–human QWK (essays) | 0.75–0.85 | `[cite: 17]`, QWK blogs | Blog / unknown | **M.** Typical in AES literature (ASAP), not BD data. |
| AI–human QWK, clean transcript | 0.72–0.86 (also "≈0.80–0.84") | None specific | None | **M/L.** Broadly consistent with AES literature, but it says "fine-tuned Claude 3.5 Sonnet", which is not a public product. |
| AI–human QWK, uncorrected HTR | <0.55 (0.45–0.55) | None | None | **L.** Directionally sensible, but unsourced. |
| Layout analysis accuracy | 91.2–96.0% | MLExpert blog | Blog | **L.** Metric undefined (mAP? accuracy?). |
| Image quality gate accuracy | 94.0–98.5% | None | None | **L.** Unsourced. |
| Diagram understanding | 65–82% | None | None | **L.** Unsourced; metric undefined. |
| Calibration | 88–94% | None | None | **L.** "Calibration %" is not a standard metric. |
| Subjective eval latency/cost | 2.5–7 s; $0.020–0.040/response | None | None | **M.** Order of magnitude plausible for frontier APIs. |
| Claude 3.5 Sonnet cost | $15–30 / 1k requests | None | None | **M.** Plausible for ~2–5k tokens/request at $3/$15 per M. |
| GPT-4o cost | $12–25 / 1k requests | None | None | **M.** Same logic. |
| Qwen2.5-VL-7B self-host | $0.80–1.20 / 1k pages; 1.2–2.5 s/page | Qwen blog, Reddit | Vendor / forum | **L/M.** Depends heavily on GPU and utilisation. |
| Mathpix price | $20–40 / 1k pages (also "$0.015/page") | mathpix.com | Vendor | **L.** Internally inconsistent: $0.015 vs $0.02–0.04 per page. |
| BanglaBERT cosine threshold | ≥0.82 | None | None | **L.** Arbitrary; BanglaBERT is not a sentence-embedding model. |
| Confidence routing thresholds | 0.85 / 0.50; N=3, T=0.3 | None | None | **L.** Design choices, not validated. |
| Annotation cost | $0.30 / $1.20 / $2.50 per page; 3/12/15 min | None | None | **L/M.** Plausible BD rates but unsourced. |
| Inter-annotator CER QC | ≤2.0% | None | None | **M.** Reasonable standard. |
| Data volume | 50k BN + 20k EN + 15k STEM + 5k gold pages | None | None | **L.** Asserted, with no learning-curve justification. |
| Cost per page (blended) | $0.090 / $0.072 / $0.061 | Own model | None | **M** as arithmetic; inputs assumed. |
| Human review cost | $0.15/page, 25% review rate | None | None | **L/M.** Review rate assumed. |
| GPU sizing | 1×L4 … 32×H100 | None | None | **L.** Not derived from throughput. |
| Peak upload | 5–5,000 rps | None | None | **L.** Likely overstated for batch scanning. |
| Automation % | STEM 65–80, EN 50–65, BN 20–35 | None | None | **L.** Estimates only. |
| Latency | 3.5–8.0 s/page | None | None | **M.** Plausible for an async pipeline. |
| Go/No-Go gates | EN WER ≤6%, math ≥96%, BN WER ≤25%, QWK ≥0.80, false-high-conf <2%, ≤$0.08/page, P95 <10 s | None | Own targets | **M.** Useful as targets; not evidence. |
| Bangla script inventory | 11 vowels, 39 consonants, 10 digits, ~16 kar, 280+ conjuncts | None | None | **M/H.** Standard linguistic description (conjunct counts vary by source). |
| Infeasibility conditions | Human QWK <0.60 or WER >50% | None | None | **M.** Sensible threshold logic. |

---

## Recommended architecture

**Components (Deliverables 14, 20, 24):**
- **Client:** a Flutter mobile scan app with "embedded C++ OpenCV WebAssembly binaries" for edge deskew and quality checks, an offline-first SQLite batch queue (from the risk register), and a desktop web admin.
- **Ingress:** NGINX API gateway with TLS 1.3, then a RabbitMQ asynchronous queue with a job-tracking ID that clients poll.
- **Compute:** a Kubernetes GPU cluster with KEDA autoscaling. It runs CPU preprocessing workers, YOLOv8 layout workers, HTR inference on vLLM or TensorRT-LLM (INT8/FP8), and Python SymPy verification workers.
- **Data:** PostgreSQL, S3-compatible object storage (local, in Bangladesh), and HMAC-SHA256 append-only audit logs.

**Models per stage:**

| Stage | Model/tool |
|---|---|
| Quality gate / preprocessing | OpenCV (Laplacian variance, CLAHE, Sauvola, homography, Radon deskew) |
| Layout | YOLOv8-Doc (primary), LayoutLMv3, Layout-Parser |
| Template segmentation (MVP) | Template negative subtraction (Gradescope-style) |
| English HTR | TrOCR-Large |
| Bengali HTR | GraDeT-HTR (fine-tuned); Phase 3 for production |
| Math OCR | Mathpix API (buy); SimpleTex / Pix2Text as alternatives |
| Math verification | SymPy (SageMath, Z3 mentioned) |
| Subjective | Qwen2.5-VL-72B self-hosted with JSON-schema constraints; GPT-4o / Claude 3.5 Sonnet as fallback |
| Synonym/alternative matching | BanglaBERT embeddings, cosine ≥0.82 |
| Diagram | SAM-2 / CLIP / VLMs (experimental, excluded from MVP) |
| Confidence | Composite C_total (OCR log-prob, layout IoU, semantic variance, rubric cosine) |

**Deterministic vs AI split:**
- **Deterministic:** document alignment, template subtraction, math AST equivalence, step-wise deductions, total summation, grade boundaries, and audit logging.
- **AI:** stroke transcription, layout parsing, answer clustering, semantic concept matching, and confidence estimation.
- LLMs may classify error types but never set deductions.

**HITL points:**
- All C_total ≥0.85 results still go through teacher one-click batch approval, so no mark is final without a human.
- <0.85 goes to a focus queue with highlights. <0.50 goes to full manual grading.
- Human review is mandatory for Bengali literature essays, diagrams and appeals.
- Risk TR-01 says to "enforce 100% human review for Bengali scripts".

**Deployment:** cloud-native microservices with local BD data residency, enterprise ZDR API contracts, and self-hosted fallback nodes (Qwen2.5-VL) for API outages.

---

## Model-by-model notes

- **TrOCR-Large (Handwritten), Microsoft.**
  - Claimed: end-to-end line HTR, "IAM WER <4.5%", 300–700 ms/line, MIT license, English production-ready.
  - Bangla: not claimed.
  - Failure modes: cursive, illegible writing. It is line-level and needs line segmentation.
  - **[Analyst note]** The original TrOCR is English-only (RoBERTa/UniLM decoder); Bangla requires a new decoder/tokenizer. It is self-hosted, so privacy is fine.
- **GraDeT-HTR.**
  - Claimed: decoder-only transformer with a grapheme-cluster tokenizer for conjuncts; WER ~22–28%; 400–900 ms/line; open source; to be fine-tuned locally.
  - Failure modes: complex joint characters. Production use is deferred to Phase 3.
  - **[Analyst note]** This is the most Bangla-specific model named, but its maturity (code, weights, license) was not verified.
- **Flor Gated-CNN / CRNN.** Baselines behind the 36–48% WER figures. Classical HTR architectures.
- **Qwen2.5-VL-7B.**
  - Claimed: dynamic resolution, grounding, "high Latin/Math OCR; moderate Bengali HTR", 1.2–2.5 s/page, $0.80–1.20 per 1k pages self-hosted, fully local.
  - **[Analyst note]** Its Bangla handwriting quality is asserted without a benchmark.
- **Qwen2.5-VL-72B.** The recommended **primary subjective grader**, self-hosted.
  - **[Analyst note]** A 72B VLM needs multi-GPU serving (e.g. 2–4× 80 GB at FP16, fewer with quantisation). That contradicts "cost efficiency" at small scale. The 72B weights ship under the Qwen license, not Apache-2.0; verify commercial terms.
- **Qwen3-VL-30B / 72B.** Claimed SOTA spatial/STEM reasoning, $4–8 per 1k pages via API.
  - **[Analyst note]** To my knowledge the Qwen3-VL family was released as 2B/4B/8B/32B dense plus 30B-A3B and 235B-A22B MoE. A "Qwen3-VL-72B" does not appear to exist; 72B is a Qwen2.5-VL size. Treat as a naming error.
- **Claude 3.5 Sonnet.** Claimed "SOTA rubric comprehension, low hallucination", Latin HTR SOTA, Bengali moderate, $15–30 per 1k requests, ZDR.
  - It is called "fine-tuned" in the QWK claim.
  - **[Analyst note]** Claude 3.5 Sonnet was not publicly fine-tunable and has since been superseded/deprecated by newer Claude models. Treat the model choice as outdated as of Sept 2026.
- **GPT-4o.** Claimed prompt alignment, JSON outputs, robustness to blur and tilt, $12–25 per 1k requests, enterprise SLA. It is the fallback grader. **[Analyst note]** It is also superseded by newer OpenAI models; check availability.
- **AWS Textract / Google Cloud Document AI.** Listed for English HTR only. **[Analyst note]** No BD data residency: no AWS or GCP region exists in Bangladesh, which conflicts with the report's own residency claim.
- **Mathpix API.** Claimed 97.8% handwritten math, 200–500 ms/expression, $20–40 per 1k pages, bought for the MVP.
  - Privacy: external API, so images leave BD. Not addressed beyond ZDR.
  - Failure modes: non-standard notation causes syntax errors.
- **SimpleTex, Pix2Text.** Alternative math OCR. SimpleTex is a Chinese commercial service. Pix2Text is open source and is the build-fallback.
- **SymPy / SageMath / Z3.** Deterministic equivalence checking, <50 ms/expression, "100%".
  - Failure mode: needs clean LaTeX.
  - **[Analyst note]** "100% accuracy" applies only to the algebra once the input is correct. LaTeX→SymPy parsing (`parse_latex`) is fragile and is the real accuracy bottleneck.
- **LayoutLMv3.** Layout segmentation. **[Analyst note]** The Microsoft LayoutLMv3 weights are under CC BY-NC-SA 4.0 (non-commercial), a licensing risk the report does not mention.
- **YOLOv8-Doc.** Page region anchoring (primary). **[Analyst note]** This is not an official Ultralytics model name; it presumably means a YOLOv8 fine-tuned on document layout. Ultralytics YOLOv8 is AGPL-3.0, which matters for closed SaaS.
- **Layout-Parser.** An open-source toolkit.
- **SAM-2, CLIP.** Diagram localisation; correctness verification is "not reliable". Experimental.
- **BanglaBERT.** Multilingual/Bangla embeddings for synonym matching with cosine ≥0.82.
  - **[Analyst note]** BanglaBERT (csebuetnlp) is an ELECTRA discriminator. Its raw [CLS]/mean-pooled cosine similarities are not calibrated for semantic similarity without sentence-level fine-tuning, and the fixed 0.82 threshold is arbitrary.
- **Calibrated deep ensembles / temperature scaling.** Confidence, "pilot-ready".
- **vLLM / TensorRT-LLM.** Inference servers with INT8/FP8.
- **Gradescope (Turnitin).** Competitor: template alignment, answer grouping, and teacher grading of clusters.

---

## Bangla-specific findings

- **Script complexity:** 11 vowels, 39 consonants, 10 numerals, ~16 kar, phala modifiers, 280+ juktakkhor, and a matra headline. Handwriting brings overlap, broken headlines, cursive transformations and non-standard ligatures.
- **Datasets named:**
  - CMATERdb, Ekush and BanglaLekha-Isolated: isolated characters, 97.32–98.40% top-1.
  - BN-HTRd: document-level HTR and line segmentation.
  - BanglaWriting: word/line level.
  - No exam-script dataset exists; the report proposes building one of 50k pages from more than 500 writers across all 8 divisions.
- **CER/WER:** full-page CER 12.83–18.68% and WER 36.01–48.63% (Gated-CNN, CRNN, Transformer). GraDeT-HTR ~22–28% WER on domain corpora.
  - Commonly corrupted: negation words ("না", "নয়"), scientific terms and numbers. **[Analyst note]** Negation corruption is the most grading-relevant failure, because it flips meaning.
- **Conjuncts:** named as the main cause of high WER. GraDeT's grapheme tokenizer targets them.
- **Mixed Bangla-English:** students write English terms in Bangla script and Latin variables inside Bangla sentences. Unified VLMs handle switching better than classical OCR, but WER rises 10–15% (15–25% overall).
- **LLM Bangla comprehension:** not benchmarked. The report only asserts that concept matching works via BanglaBERT. There are no Bangla-specific QWK figures.
- **Policy consequences:**
  - Bengali HTR is "unviable" for autonomous grading, with 100% human review for Bengali scripts (TR-01).
  - Bengali literature is excluded from the MVP; automation there is only 20–35%.
  - The Bengali gate is WER ≤25% for automated short text.
- **Numerals:** Bengali digits (০–৯) appear in the character inventory, but the ">99% digit accuracy" claim is not tied to Bengali numerals.

---

## Math-specific findings

- **Math OCR:** Mathpix (primary, bought), SimpleTex and Pix2Text. Claimed 95.5–98.5% expression-level accuracy (97.8% Mathpix) across algebra, trigonometry, calculus and matrices.
- **Step extraction:** an "intermediate step-parsing module" evaluates each derivation line when the final answer fails. Line segmentation of derivations is not specified.
- **Symbolic verification:** LaTeX → SymPy AST → `simplify(student − rubric) = 0`. SageMath and Z3 are also listed.
  - **[Analyst note]** The worked example ("2x+5=15 ⟹ x=5" vs "(4x+10)/2 = 15 ⟹ 2x=10") mixes equations and implications. Equation-level equivalence needs solution-set comparison, not `simplify(a−b)`, and the report glosses over this.
- **Partial credit:** deterministic step-wise rubric rules. If step 3 has an arithmetic error but steps 1–2 are correct, partial credit follows the rubric. The LLM only labels the error type.
- **Chemistry:** a `deterministic_chemistry_parser` is referenced in the rubric JSON but never specified.
- **Risk TR-03:** LaTeX syntax errors. Mitigations are regex sanitisation and a "fallback to Mathpix API". **[Analyst note]** That fallback is circular, since Mathpix is already the primary.
- **Automation claim:** STEM 65–80% of grading effort.
- **Gates:** math LaTeX ≥96% (Go/No-Go) and >95% (Phase 0).

---

## Risks identified

| ID | Risk | Probability | Impact | Mitigation (as given) | Residual |
|---|---|---|---|---|---|
| TR-01 | High WER in Bengali HTR (36–48%) | High | Severe | 100% human review for Bengali scripts (C_total <0.85) | Medium |
| TR-02 | LLM hallucination / bias (verbosity, invented concept matches) | Medium | High | JSON-schema-constrained decoding plus RAG concept verification | Low |
| TR-03 | Math LaTeX parsing syntax errors | Medium | Medium | Regex sanitisation; fallback to Mathpix API | Low |
| TR-04 | Cloud API outage / latency | Low | High | Self-hosted Qwen2.5-VL fallback nodes | Low |
| TR-05 | Network disruption in remote institutions | High | Medium | Offline-first mobile scan app with local SQLite batch queue | Low |

Additional risks in the text:
- **Privacy:** student PII leakage, cross-tenant leakage in multi-school SaaS, and vendors retraining on scripts.
- **Model:** hallucination, verbosity bias, neatness bias, and OCR word corruption changing meaning.
- **Data:** collection is "highly difficult" because of fragmentation, consent requirements and teacher annotation cost.

---

## Assumptions

1. Fixed-template answer sheets are available (the MVP depends on template subtraction).
2. Enterprise ZDR contracts are obtainable from OpenAI, Anthropic and Google, and satisfy BD law.
3. BD law requires in-country storage (stated as fact; see critical assessment).
4. Teacher review costs $0.15/page, and 25% of pages need focused review.
5. 5 pages per student (scalability table).
6. Composite-confidence weights can be calibrated from historical grading data, which does not yet exist.
7. GraDeT-HTR can be fine-tuned to ≤25% WER on local exam scripts.
8. Human inter-rater QWK in BD is ≥0.60, and in practice about 0.75–0.85.
9. VLMs grading clean transcripts reach QWK ~0.80–0.84.
10. Mathpix accuracy on BD student handwriting matches vendor claims.
11. Answer clustering (Gradescope-style) transfers to BD exam formats.

---

## Recommendations

1. Build only an **AI-assisted, HITL system**. No autonomous grading.
2. The MVP covers **STEM and English exams, Grades 9–12**, on fixed-template sheets: Mathpix → SymPy, TrOCR for English, exact match for objective items, answer clustering, and a confidence-routed review queue.
3. Do **not** build first: Bengali literature essay auto-grading, diagram evaluation, un-templated homework, or real-time grading.
4. Keep scoring, aggregation, grade boundaries and audit deterministic. LLMs only classify.
5. Encode rubrics as structured JSON (concepts, weights, aliases, penalties).
6. Run experiments 1, 3, 4 and 6 (Bengali HTR, Mathpix+SymPy, VLM concept agreement, human IRR) before investing heavily.
7. Use Go/No-Go gates: English WER ≤6%, math ≥96%, Bengali WER ≤25%, QWK ≥0.80, false-high-confidence <2%, ≤$0.08/page, P95 <10 s.
8. Buy Mathpix initially. Fine-tune GraDeT-HTR. Self-host Qwen2.5-VL-72B for subjective grading with commercial fallback. Build the review UI in-house.
9. Local data residency, PII redaction before inference, ZDR contracts, AES-256/TLS 1.3, and hash-chained audit logs.
10. An offline-first capture app for low-connectivity schools.

---

## Open questions

- (From the report) What is the real WER of GraDeT-HTR trained on rural BD secondary exam scripts? What is the teacher adoption/override rate in batch review?
- **[Analyst note]** Further questions:
  - Is the BanglaBERT cosine approach valid for Bangla paraphrase?
  - Do the Personal Data Protection Ordinance 2025 residency provisions apply to exam scripts, and do they permit cross-border processing under ZDR? The report asserts both residency and use of US APIs.
  - What confidence-weight calibration data exists before launch?
  - How are answer clusters formed for handwritten Bangla?
  - Does the "one-click approval" of high-confidence batches produce rubber-stamping?
  - SSC/HSC MCQs are already machine-read via OMR. Does the platform target board exams or internal school exams?

---

## Critical assessment

**Unrealistic or unsupported accuracy claims**
- The "Production-Ready" labels on math OCR (95.5–98.5%) and English HTR (WER 3–8%) rest on vendor pages and blogs, not on student-script benchmarks. Mathpix "97.8%" is **vendor marketing presented as fact**.
- "Symbolic Verification: 100%" conflates the algebra engine with end-to-end accuracy. Accuracy is bounded by LaTeX extraction and parsing.
- "Calibration 88–94%" and "image quality gate 94–98.5%" are undefined metrics with no source.
- QWK 0.72–0.86 is attributed to "fine-tuned Claude 3.5 Sonnet / GPT-4o". The report never explains what fine-tuning is meant; no Claude 3.5 Sonnet fine-tuning was generally available.
- To the report's credit, it does **not** claim 99% Bangla HTR. Its Bangla numbers (CER 12.8–18.7%, WER 36–48%) are the most conservative and credible of the three docs.

**Outdated or doubtful model names**
- "Qwen3-VL-30B / 72B": 72B does not match the known Qwen3-VL sizes.
- Claude 3.5 Sonnet and GPT-4o are outdated as of Sept 2026.
- "YOLOv8-Doc" is not an official model.
- TrOCR's IAM result is reported as WER when the paper reports CER.

**Citation quality**
- Dangling `[cite: 4]` and `[cite: 17]` markers with no numbered list.
- Heavy reliance on blogs (F22 Labs, nullmirror, beanbag.ai, debuggercafe, Medium), Reddit, and a Scribd-hosted paper.
- Gradescope content is well supported by official Gradescope guides. The Bangla HTR baselines are reasonably supported by BN-HTRd and survey papers.

**Internal contradictions**
- **Mathpix cost:** "$0.015/page" in Deliverable 01 vs "$20–40 per 1k pages" in Deliverable 02.
- **Bengali routing:** "100% human review for Bengali scripts" (TR-01) contradicts routing Bengali to GraDeT-HTR in the production pipeline with confidence-based review, and the Bengali WER ≤25% gate "for automated short-text processing".
- **Subjective grading "Hybrid" choice:** it recommends self-hosted Qwen2.5-VL-72B primary "for cost efficiency", yet the cost model lists VLM inference as the second-largest cost and a 72B model needs expensive multi-GPU serving. At 10k pages/month, APIs would be cheaper.
- **Data residency vs APIs:** it requires all scripts to be stored in BD while routing images to US-hosted Mathpix/OpenAI/Anthropic/Google APIs (ZDR ≠ residency) and naming AWS Textract and GCP.
- **Scale:** "microservices + Kubernetes + KEDA + RabbitMQ + 32×H100" in the recommended infrastructure, while the MVP targets 5 pilot schools and 10,000 exams.
- **Scope:** "Grades 9–12" MVP but "Canvas, Moodle" connectors (rare in BD schools).

**Over-engineering**
- Kubernetes GPU autoscaling, a microservices topology, a 32×H100 sizing and a 5,000-rps peak are premature for a pilot of a few thousand pages.
- A self-hosted 72B VLM before any data exists.
- A training data target of 50k Bangla pages before the pipeline is validated.
- **[Analyst note]** A single GPU box or pure API calls plus a Postgres-backed job queue would suffice for Phases 0–2.

**Vendor claims as fact:** Mathpix, SimpleTex, the Qwen blog, and ZDR guarantees ("must never be retained") are treated as contractual certainties.

**Legal claim:** it asserts that the "Personal Data Protection Act / Ordinance of Bangladesh" requires local data residency. It cites the bdlaws page for the 2025 Ordinance, but the specific localisation obligations for exam scripts were not quoted. Verify with counsel.

---

## Confidence level + Relevance to product decisions

**Confidence: Medium.** The overall shape is well reasoned and matches the Gradescope precedent: HITL, deterministic math, conservative Bangla stance, and a STEM/English-first MVP. The Bangla HTR error ranges are the most defensible numbers of the three documents. Most other numbers (costs, latencies, automation percentages, calibration, GPU sizing) are unsourced estimates. The model choices are dated (Claude 3.5 Sonnet, GPT-4o, and the questionable "Qwen3-VL-72B").

**Relevance: High** for:
1. MVP scope: STEM/English, templated sheets, Bangla essays excluded.
2. The deterministic-vs-AI boundary.
3. The Go/No-Go gate framework and the experiment list, which are directly reusable.
4. The data-collection plan and annotation cost structure.
5. The finding that answer clustering plus teacher grading (Gradescope model) is a proven, trust-building alternative to autonomous LLM grading.

**Lower relevance:** the infrastructure blueprint (over-built) and specific vendor/model picks (dated, to be re-benchmarked).
