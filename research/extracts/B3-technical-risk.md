# Technical Feasibility and System Risk Analysis: Automated AI-Powered Examination Assessment Platform

- **Drive ID:** `1D9ujrUcFGzaUQnW5UJI1zATdvE4OYP_ALV6agPlqMSE`
- **Topic:** Risk-centred feasibility analysis in 40 sections:
  - Executive summary; formal problem definition as seven mappings (T_prep → T_seg → T_htr → T_eval → T_calib → summation → audit); a 21-stage pipeline spec with inputs, outputs, technology, failure modes and requirements.
  - Feasibility matrix; a 12-item RPN risk register.
  - Deep dives on HTR, vision degradation, IQA, layout, Q–A mapping, math, diagrams, rubrics, partial marks, hallucination grounding, conformal abstention, ensembles, infrastructure, security, scalability, unit cost, vendor fallback, data leakage, HITL, solution options, alternative architectures.
  - 14 POC experiments, benchmark design, red-teaming, fault tolerance, observability, build vs buy, open vs proprietary, MVP scope, Go/No-Go, target architecture, a 28-week roadmap, residual risks, open research questions, and 30 direct answers.
- **Method (as presented):** Desk synthesis framed with mathematical formalism: RPN = Severity × Probability × Detectability, and conformal-prediction FDR bounds.
  - Sources cited: arXiv (SCOPE: Selective Conformal Optimized Pairwise LLM Judging 2602.13110; CDM formula-recognition metric 2409.03643; DocSAM 2504.04085; LayoutLMv3 2204.08387; InkFM 2503.23081; an in-the-wild Bengali scene-text benchmark 2608.03884; "Automated Grading of Handwritten Mathematics Using Vision…" 2605.19043; "Conformity Breaks Conformal Prediction" 2609.04445; Image-to-LaTeX 2408.04015; EDocNet; energy-efficiency and token-ops inference papers), Hugging Face paper search, Scribd (Bornonet), MDPI, and ResearchGate (private LLM inference on consumer Blackwell GPUs).
  - Inline `[cite: 1]`, `[cite: 5]`, `[cite: 8, 17]`, `[cite: 10]` and `[cite: 14, 15]` markers point to no numbered list.
- **Coverage:** The full document was read (about 111k characters, ending in the reference list). It is not truncated.

---

## Main findings

1. **Headline thesis:** "an unconstrained, zero-shot VLM approach is technically infeasible for high-stakes assessment". A "constrained, multi-stage hybrid architecture" with anchored templates, specialised extraction, a CAS, rubric engines, conformal abstention and HITL *is* feasible.
2. **Cited empirical anchors:**
   - "Up to **87%** of grading discrepancies [in handwritten math] stem from transcription and visual parsing failures rather than rubric misapplication."
   - "Visual misrecognition accounts for approximately **60%** of transcription errors" in low-resource Indic scripts for SOTA VLMs.
3. **21-stage pipeline with requirements:**
   1. Acquisition: ≥300 DPI, capture <50 ms, rejects >45° perspective.
   2. IQA: Laplacian variance, BRISQUE, OpenCV. <150 ms; false-accept of unreadable images <0.1%.
   3. Preprocessing: Canny, Douglas–Peucker, homography, Sauvola. ≤0.5° skew, <250 ms.
   4. Page sequence: registration anchors, corner QR codes, page classifier. **99.99%** precision, <100 ms.
   5. Student/exam ID: barcode/QR plus numeric HTR for roll numbers. **100% exact match** via checksum digits, <150 ms.
   6. Question segmentation: YOLOv8-Doc, LayoutLMv3, DocSAM. mAP@0.5 ≥0.96, <400 ms.
   7. Q–A mapping: spatial GNN, reading-order transformers, DAG output. 99.5% precision, <100 ms.
   8. HTR: fine-tuned TrOCR (**Swin encoder + BanglaBERT decoder**), LightOnOCR, Mathpix. **Bangla CER <3.0%**, math CDM >95%, <1200 ms/block.
   9. Text and visual features: cross-attention encoders, sentence-transformers. <300 ms.
   10. Math understanding: SymPy, ANTLR, Z3 SMT. AST conversion >98%, <200 ms.
   11. Diagrams: YOLOv8-Segment, ViT aligners. IoU >0.85, <800 ms.
   12. Question intent: fine-tuned BERT taxonomy. >99% accuracy, <50 ms.
   13. Rubric compiler: Claude 3.5 Sonnet / GPT-4o to JSON schema. 99.5% precision, <3 s offline.
   14. Evaluation: SymPy plus **dual-LLM judges**. **QWK κ ≥0.88** vs master teachers, <2500 ms.
   15. Partial marks: programmatic rule engine with carry-forward. 100% precision, <10 ms.
   16. Total: deterministic summation with caps. <1 ms.
   17. Confidence: **SCOPE selective conformal prediction**. FDR α ≤0.02, <30 ms.
   18. Escalation: **Apache Kafka** broker. <100 ms.
   19. HITL UI: <200 ms load, **<15 s per item** teacher resolution.
   20. Persistence: PostgreSQL with RLS. 99.99% availability, <50 ms writes.
   21. Audit: SHA-256 signed, WORM **AWS S3** Object Lock. 100% completeness.
4. **Feasibility by domain:** Bangla HTR **FEASIBLE** (fine-tuned TrOCR + BN-HTRd). English HTR FEASIBLE (TrOCR/LightOnOCR). Math OCR FEASIBLE (Mathpix / Swin). Math reasoning FEASIBLE (SymPy). Short essays FEASIBLE (LLM ensembles plus rubric constraints). Diagrams **HIGH RISK**. Subjective essays **HIGH RISK**.
5. **Zero-shot VLM Bangla handwriting CER "exceeding 12%"** (12.4% in the architecture matrix).
6. **Traditional OCR:** Tesseract v5 CER >35% on handwritten Bangla (38.5% in the options matrix).
7. **Specialised HTR claim:** Swin + BanglaBERT TrOCR achieves **CER <3.0%** when trained on BN-HTRd (**108,147 annotated words across 788 pages**). The options matrix claims "**CER drops from 38.5% to 1.9%**". Architecture B (plain TrOCR + LayoutLMv3) gives CER ~2.8%, Architecture C ~1.9%.
8. **IQA thresholds:**
   - Laplacian variance ≥100.0, image entropy ≥4.5, DPI ≥300.
   - Illumination correction: divide by a Gaussian background (σ = 50) and min-max normalise.
   - Sauvola: W = 15, k = 0.2, R = 128.
   - Non-local-means denoising; homography to A4.
9. **Layout:** LayoutLMv3 fine-tuned on exam scripts into QuestionHeader / AnswerBlock / CrossedOutBlock / DiagramBlock / MarginalNote. A **spatial GNN** links continuation blocks across pages with >99.5% precision.
10. **Math:**
    - Mathpix API or fine-tuned Pix2Tex → LaTeX → SymPy AST in a sandbox.
    - Step validation: `E_step_n − E_step_{n−1} = 0`, then **randomised numeric equivalence testing** if symbolic reduction fails.
    - Example: ∫2x dx = x² + C.
11. **Diagrams:** YOLOv8-Segment → node-edge graph → graph edit distance vs a rubric master graph. Visual confidence <0.85 goes to a human.
12. **Rubric JSON:** `question_id`, `max_score`, `rubric_version`, and `sub_criteria` with types `deterministic_math` (symbolic_target, allow_algebraic_rearrangement), `numeric_verification` (expected_values, tolerance 0.01) and `semantic_text` (required_concepts, negative_concepts). Also `error_propagation_rules` (carry_forward_arithmetic_errors, penalty_max_cap). The example is Boyle's law.
13. **Partial marks:** carry-forward. An early arithmetic slip is penalised once; downstream correct method keeps credit.
14. **Grounding:** each score must cite a character span and an image bbox. An ungrounded justification counts as a hallucination failure and goes to a human.
15. **Conformal abstention (SCOPE):**
    - Non-conformity s(x) combines token entropy, HTR softmax, ensemble variance and CAS errors.
    - Calibrated on N expert-verified scripts to α = 0.02 (a "98% statistical reliability threshold").
    - Commit if s(x) ≤ λ̂, else abstain. The guarantee holds "under exchangeability".
16. **Ensemble:** Claude 3.5 Sonnet, GPT-4o and Gemini Pro judges. A spread ≤0.5 marks gives a weighted average; >0.5 goes to abstention or a human.
17. **Infrastructure:** Apache Kafka plus Redis, stateless workers (visual, HTR/vision, CAS/LLM), Kubernetes HPA on Kafka lag, dynamic batching ("up to 4× throughput"), vLLM / NVIDIA Triton, a LiteLLM router (failover on 500 errors or >3000 ms), Prometheus/Grafana (alerts when teacher override >8.0% or P95 >10 s), AWS KMS, and S3 Object Lock.
18. **Cost cascade:**
    - Stage 1: local TrOCR + OpenCV, 65% of volume at $0.0020/script.
    - Stage 2: Mathpix + SymPy + mid-tier LLM, 25% at $0.0120.
    - Stage 3: multi-LLM ensemble, 10% at $0.0450.
    - Human fallback at $0.0500.
    - Weighted average **$0.0088/script** (arithmetic verified; excludes human cost).
19. **Architecture comparison:**

    | Architecture | Bangla CER | Calibration | P95 latency/script | Cost/script |
    |---|---|---|---|---|
    | A: minimal VLM (GPT-4o / Gemini Pro) | ~12.4% | Uncalibrated, 8–15% error | 18 s | $0.085 |
    | B: modular (TrOCR + LayoutLMv3 + LLM judge) | ~2.8% | 4–8% error | 6.5 s | $0.025 |
    | **C: hybrid (anchored sheets + TrOCR + SymPy + dual LLM + SCOPE)** | **~1.9%** | FDR ≤0.02 | **2.8 s** | **$0.0088** |

20. **14 POCs** (sizes and targets):

    | POC | What | Data | Target | Time |
    |---|---|---|---|---|
    | 01 | TrOCR Bangla | 10k BN-HTRd + local | CER <3%, WER <8% | 3 wk |
    | 02 | Mathpix | 2,500 scripts | CDM ≥95% | 1.5 wk |
    | 03 | SymPy + Z3 | 2,000 derivations | FP step error <0.5% | 2 wk |
    | 04 | YOLOv8-Doc | 3,000 pages | mAP@0.5 ≥0.96 | 2 wk |
    | 05 | SCOPE | 5,000 scripts | FDR ≤0.02 | 2.5 wk |
    | 06 | JSON rubrics, Claude / GPT-4o ensemble | 1,000 essays | κ ≥0.88 | 2 wk |
    | 07 | Injection | 500 adversarial scripts | 0.0% success | 1 wk |
    | 08 | IQA | 1,500 captures | Unreadable accept <0.1% | 1 wk |
    | 09 | GNN mapping | 2,000 scripts | ≥99.5% | 2.5 wk |
    | 10 | Dual-LLM hallucination detection | 1,200 answers | >98% | 2 wk |
    | 11 | vLLM/Triton | Load test | >120 scripts/min/GPU | 1.5 wk |
    | 12 | Cost | 10k scripts | ≤$0.01/script | 1.5 wk |
    | 13 | LiteLLM failover | Fault injection | 99.99% availability | 1 wk |
    | 14 | End-to-end | 500 scripts | P95 <5.0 s/script | 3 wk |

21. **Benchmark:** N = 10,000 scripts, stratified 30% clean / 30% poor / 20% code-switched / 10% degraded / 10% adversarial, across national, English-medium and **madrasah** curricula.
22. **Go/No-Go:**
    - Bangla CER ≤3.0% (halt unconstrained text launch if above; abandon if >5.0%).
    - Conformal FDR α ≤0.02 (redesign if abstention >40%).
    - SymPy false positives ≤0.5% (otherwise restrict to final answers).
    - Cost ≤$0.03/script (abandon if >$0.10).
    - Proceed if human escalation <15%.
23. **Roadmap (28 weeks):**
    - Weeks 1–8: 14 POCs and fine-tuning Swin-TrOCR on BN-HTRd.
    - Weeks 9–16: Kafka/Redis, SCOPE, UIs.
    - Weeks 17–22: pilot at **10 institutions, 20,000 scripts**.
    - Weeks 23–28: multi-tenant, Kubernetes autoscaling, red team.
24. **Direct answers:**
    - Biggest risk: "uncalibrated hallucination plus compound error propagation". The infeasibility risk is loss of trust from silent errors.
    - Humans handle abstentions, diagrams, essays, **5% random audit sampling**, and appeals.
    - Standardised sheets cut downstream failures by "an estimated **80%**".
    - MVP: STEM only (Math, Physics, Chemistry) on anchored forms, MCQ and short answers.
    - Build first: constrained Architecture C for secondary STEM with a mandatory review queue for low confidence.

---

## Quantitative claims table

| Claim | Value | Source cited | Source type | Credibility H/M/L + why |
|---|---|---|---|---|
| Transcription causes most math grading discrepancies | up to 87% | arXiv 2605.19043 (likely) | Preprint | **M.** Plausible and consistent with B1's QWK degradation logic; unverified. |
| Visual misrecognition share in Indic VLM errors | ~60% | arXiv 2608.03884 / HF search (likely) | Preprint | **L/M.** The cited benchmark is **scene text**, not handwriting. |
| Zero-shot VLM Bangla handwriting CER | >12% (12.4%) | None traceable | None | **M/L.** Direction plausible; the precise 12.4% is untraceable. |
| Tesseract Bangla handwriting CER | >35%; 38.5% | `[cite: 1]` dangling | None | **M.** Consistent with B2 (>45%). |
| Fine-tuned TrOCR (Swin + BanglaBERT) Bangla CER | <3.0%; 1.9%; 2.8% | `[cite: 1]` dangling | None | **L.** Far better than any published full-page Bangla HTR result cited elsewhere (B1: 12.8–18.7%; B2: 8.4–10.9%). BanglaBERT is an encoder, not a decoder. Likely conflated with word-level or isolated-character results. |
| BN-HTRd size | 108,147 words, 788 pages | BN-HTRd paper (implicit) | Peer-reviewed / preprint | **H.** Matches the published dataset description to my knowledge. |
| POC-01 WER target | <8% | None | Own target | **L.** Inconsistent with B1's Bengali WER gate of ≤25%. |
| Math CDM | >95% | CDM paper arXiv 2409.03643 | Preprint | **M.** CDM is a real metric; the 95% target is aspirational. |
| Layout mAP@0.5 | ≥0.96; "increases to 0.97" | `[cite: 10]` (EDocNet / DocSAM?) | Preprint | **L/M.** Results on datasheet or document datasets, not exam scripts. |
| Q–A mapping precision (GNN) | ≥99.5% | None | None | **L.** Unsourced; a GNN would need training data that doesn't exist. |
| Page sequence precision | 99.99% | None | Requirement | **M** as a requirement (achievable with QR codes); not evidence. |
| Roll-number exact match | 100% via checksum | None | Requirement | **M.** Only with printed or bubbled IDs and checksums. |
| AST conversion | >98% | None | Requirement | **L.** |
| Question-intent classifier | >99% | None | Requirement | **L.** |
| Rubric parsing precision | 99.5% | None | Requirement | **L.** |
| AI–teacher QWK | κ ≥0.88 | None | Requirement | **L/M.** High for essays; B2 uses 0.78 for essays. |
| Rubric consistency | "increases to 98.5%" | None | None | **L.** Undefined metric. |
| Conformal FDR | α ≤0.02 "certified" / "guaranteed" | SCOPE arXiv 2602.13110 | Preprint | **M** method, **L** as a guarantee. The guarantee is marginal, under exchangeability; SCOPE targets **pairwise** LLM judging; school/regional shift breaks exchangeability (the doc's own citation "Conformity Breaks Conformal Prediction" is relevant). |
| Calibration error (A/B) | 8–15% / 4–8% | None | None | **L.** |
| IQA rejection of degraded scans | >99.5% | None | None | **L.** |
| IQA thresholds | Laplacian ≥100, entropy ≥4.5, DPI ≥300; σ=50; W=15, k=0.2, R=128 | None | Engineering heuristics | **M.** Standard defaults; need device-specific tuning. DPI is ill-defined for phone photos. |
| Standard-sheet failure reduction | ~80% | None | None | **L.** "Estimated", no basis. |
| Dynamic batching | up to 4× throughput; >120 scripts/min/GPU | None | None | **L/M.** Batching gains are real; the specific numbers are unsourced. |
| Cost cascade | $0.0020 / $0.0120 / $0.0450 / human $0.0500; avg $0.0088/script | `[cite: 8, 17]` dangling | Own model | **L.** Arithmetic is right, but 65% of scripts get "TrOCR only" with no evaluation model; human cost excluded; human review at $0.05 is implausibly cheap. |
| Architecture A cost | $0.085/script | `[cite: 8, 17]` | None | **L.** |
| P95 latency | C 2.8 s; B 6.5 s; A 18 s per script; POC-14 <5 s | None | None | **L.** 2.8 s per multi-page script with a dual-LLM ensemble plus Mathpix API is implausible. |
| Teacher resolution | <15 s/item; 20–30 s for CAS/ensemble items; appeals <24 h | None | Requirement | **L/M.** Optimistic for reading a handwritten crop and rubric. |
| Override alert | >8.0% teacher override; P95 >10 s | None | Own threshold | **M.** Reasonable monitoring design. |
| Audit sample | 5% random | None | Own policy | **M.** Sensible. |
| Hallucination detection | >98% (POC-10) | None | Target | **L.** |
| Injection success | 0.0% (POC-07) | None | Target | **M** as a target; zero is unprovable. |
| Availability | 99.99% under failure | None | Target | **L** for a pilot. |
| Benchmark size | 10,000 scripts; 5,000 for SCOPE | None | Own design | **L/M.** Very large for pre-MVP. |
| Pilot | 10 institutions, 20,000 scripts in 6 weeks | None | Plan | **L.** Aggressive. |
| RPN scores | R-01 504, R-04 504, R-08 486, R-05 384, R-03 336, R-07 288, R-06/R-09 280, R-02 252, R-12 224, R-10 126, R-11 96 | None | Own scoring | **M.** Subjective but useful for prioritisation. |

---

## Recommended architecture

**"Architecture C: High-Reliability Hybrid Engine" (Section 36):**

1. **Anchored script upload:** pre-printed templates with corner registration anchors, QR codes, bounded answer boxes and pre-coded sub-questions.
2. **IQA** (Laplacian, entropy, DPI) → preprocessing (homography, NLM denoise, Sauvola, illumination correction). Reject and prompt a recapture on failure.
3. **Page sequencing and ID:** QR/barcode, checksum roll numbers.
4. **Bounded YOLOv8 segmenter** (YOLOv8-Doc; LayoutLMv3 region classes; DocSAM), then **spatial GNN** Q–A mapping.
5. **Text path:** fine-tuned TrOCR (Swin encoder) with BanglaBERT decoder/LM priors, self-hosted on **Triton on NVIDIA L4**.
6. **Math path:** Mathpix LaTeX (Pix2Tex fallback) → SymPy AST verifier (Z3, ANTLR) in an isolated Docker sandbox, with symbolic plus randomised numeric step checks.
7. **Diagram path (post-MVP):** YOLOv8-Segment → graph → graph-edit-distance matching.
8. **Rubric compiler (offline):** Claude 3.5 Sonnet / GPT-4o turn teacher schemes into JSON micro-rubrics.
9. **Dual-LLM ensemble judge:** Claude 3.5 Sonnet + GPT-4o (Gemini Pro as third) via a **LiteLLM** multi-provider router, with grounded evidence spans and bboxes.
10. **Deterministic** partial-mark engine (carry-forward) and summation with caps.
11. **SCOPE conformal gate:** s(x) ≤ λ̂ auto-commits; otherwise the item goes to the teacher review UI.
12. **Persistence:** PostgreSQL with RLS per tenant. Audit via SHA-256 signed WORM S3 Object Lock and AWS KMS.
13. **Infrastructure:** Kafka + Redis queues, stateless workers, Kubernetes HPA GPU autoscaling, vLLM/Triton dynamic batching, Prometheus/Grafana/Alertmanager, a dead-letter queue, idempotency via job hash, MD5 dedup, and page checkpoints.

**Deterministic vs AI split:**
- **Deterministic:** preprocessing, IQA, ID/checksum, CAS, partial marks, summation, audit, routing.
- **AI:** HTR, layout, GNN mapping, rubric compilation, semantic judging, diagram segmentation.
- "Every output that can be validated deterministically must be…overriding LLM judgments."

**HITL triggers:**
- s(x) > λ̂.
- SymPy AST failure.
- IQA failure.
- Ensemble spread >0.5 marks.
- Diagram confidence <0.85.
- Ungrounded justification.
- Detected prompt-injection strings.
- 5% random audit.
- Appeals.

**Unlike B1, auto-committed scores need no teacher sign-off.**

**MVP:** STEM only (Math, Physics, Chemistry) on anchored forms, MCQ and short answers, with a mandatory human queue for low confidence. Excludes humanities essays, freehand biology diagrams, unanchored photos and creative writing.

---

## Model-by-model notes

- **TrOCR (fine-tuned; "Swin Transformer encoder + BanglaBERT decoder").**
  - Claims: Bangla CER <3% (1.9%) with BN-HTRd; the core Bangla/English HTR; self-hosted on Triton on L4. Fails on messy cursive.
  - **[Analyst note]** Canonical TrOCR uses a BEiT/DeiT encoder with a RoBERTa/UniLM decoder. "Swin + BanglaBERT" is a custom VisionEncoderDecoder, not TrOCR. BanglaBERT (ELECTRA discriminator) is not a generative decoder; it would need cross-attention and LM-head adaptation. The CER claims are not credible without a source.
- **BanglaBERT.** Language-model decoding priors for Bangla HTR. See the note above; also check its license.
- **LightOnOCR.** English HTR alternative. **[Analyst note]** A recent (2025) end-to-end OCR VLM from LightOn, mainly for printed documents. No Bangla or handwriting claims were verified.
- **Mathpix API.**
  - Claims: math LaTeX with CDM ≥95% (POC-02). Bought via API.
  - Risks: pricing changes and rate limits.
  - Privacy: external HTTPS endpoint, not addressed for BD residency.
- **Pix2Tex / fine-tuned Pix2Tex; "Swin-Transformer" math OCR.** Fallback math OCR. **[Analyst note]** Pix2Tex (LaTeX-OCR) targets rendered formulas; handwriting performance is weak without fine-tuning.
- **SymPy, ANTLR, Z3 SMT.** AST parsing and step and numeric equivalence. POC-03 target: false-positive step error <0.5%. Docker sandbox.
- **YOLOv8-Doc / YOLOv8-Segment.** Layout and diagram elements. mAP@0.5 ≥0.96. **[Analyst note]** AGPL-3.0 licensing; "YOLOv8-Doc" is not an official model.
- **LayoutLMv3.** Region classification into 5 classes, fine-tuned on exam scripts. **[Analyst note]** CC BY-NC-SA weights: a commercial-use problem.
- **DocSAM.** Instance segmentation for documents (arXiv 2504.04085). Research code.
- **Spatial GNN / reading-order transformers.** Q–A mapping. No specific model named. Needs training data.
- **Fine-tuned BERT taxonomy classifier.** Question intent. No specific model named.
- **Sentence-transformers.** Text embeddings. No specific model named.
- **Claude 3.5 Sonnet.**
  - Roles: rubric compiler, primary LLM judge, and primary provider in the failover diagram (GPT-4o secondary).
  - Selling points claimed: "superior reasoning, zero infra, high multilingual baseline". Stated downsides: cost, lock-in, privacy.
  - **[Analyst note]** Deprecated/retired model as of Sept 2026.
- **GPT-4o.** Second judge and fallback. **[Analyst note]** Superseded.
- **Gemini Pro.** Third judge in the ensemble diagram. Version unspecified.
- **Llama 3.** Listed as an open-source option in the trade-off profile; no role assigned.
- **LiteLLM.** Multi-provider router, with failover on HTTP 500 or >3000 ms.
- **vLLM / NVIDIA Triton.** Serving with dynamic batching, NVIDIA L4 GPUs.
- **SCOPE (Selective Conformal Optimized Pairwise LLM Judging).** The abstention framework.
  - **[Analyst note]** It is designed for *pairwise preference* judging with FDR control, not pointwise mark regression. Adapting it to per-criterion marks is a research task, not an off-the-shelf component. It needs a large labelled calibration set (the doc proposes 5,000 scripts). The guarantee degrades under distribution shift (new schools or curricula), which the doc lists as an open research question.
- **BRISQUE.** No-reference IQA model used in the IQA stage.
- **Apache Kafka, Redis, Kubernetes HPA, Prometheus/Grafana, AWS S3 Object Lock, AWS KMS, PostgreSQL RLS.** Infrastructure. **[Analyst note]** There is no AWS region in Bangladesh, so AWS S3/KMS conflicts with any local-residency requirement (B1/B2). B3 does not discuss BD data law at all.

---

## Bangla-specific findings

- **Orthography:** matra (defeats vertical-projection segmentation), **300+ juktakkhor** (2–4 consonants stacked vertically or horizontally), kar diacritics positioned above, below, left and right (non-linear order), and code-switching (Bangla prose, English terms, algebraic variables and **Bengali numerals** in one sentence).
- **Datasets:** **BN-HTRd** (108,147 words, 788 pages) is the named fine-tuning set. The refs include an "in-the-wild Bengali scene text recognition benchmark" (arXiv 2608.03884) and Bornonet (character recognition). No exam-script corpus exists; the benchmark proposes national, English-medium and madrasah scripts.
- **CER claims:** Tesseract >35% (38.5%); zero-shot VLMs >12% (12.4%); fine-tuned TrOCR (Swin + BanglaBERT) <3.0% (1.9%; 2.8% without the full hybrid).
  - Go/No-Go: CER ≤3.0% to launch unconstrained text; abandon above 5.0%.
  - POC-01 WER target <8%.
- **Conjuncts:** named as risk R-01, with the highest RPN (504, P0 Blocking). Mitigation: a fine-tuned TrOCR with BanglaBERT LM decoding. Residual risk: Medium.
- **Mixed script:** 20% of the benchmark is code-switched. Better data (BN-HTRd fine-tuning) "significantly reduces CER on mixed Bangla-English". **[Analyst note]** BN-HTRd is Bangla-only, so it cannot teach code-switching.
- **LLM Bangla comprehension:** not evaluated. The "high multilingual baseline" of proprietary models is asserted.
- **Residual:** "micro-scale HTR ambiguities between similar Bangla character forms".
- **Open research:** LoRA few-shot adaptation to teacher- or school-specific handwriting.
- **Position:** B3 calls Bangla HTR "FEASIBLE". This is the most optimistic of the three docs and directly contradicts B1 ("unviable for autonomous grading").

---

## Math-specific findings

- **Math OCR:** Mathpix API (primary, bought), then fine-tuned Pix2Tex / Swin-Transformer. Metric: **CDM (Character Detection Matching)** ≥95%. Named failure: misreading superscripts and subscripts.
- **Step extraction:** implicit in "step-by-step equivalence". Each step's expression is compared to the previous one.
- **Symbolic verification:**
  - `E_step_n − E_step_{n−1} = 0` via SymPy, plus randomised complex-value numeric equivalence when symbolic simplification is inconclusive. This is more robust than B1/B2.
  - Z3 SMT and ANTLR grammar compilers.
  - AST conversion >98% (requirement).
  - Sandbox isolation in Docker.
  - **[Analyst note]** Comparing successive steps by subtraction works for expression rewriting but not for equation-solving steps (e.g. 2x = 10 → x = 5 are equivalent equations, but their "expressions" differ). A solution-set or implication check is needed. The doc does not address this.
- **Partial credit:** a deterministic rule engine with **carry-forward** logic (penalise the first arithmetic error once, credit correct downstream method) and `penalty_max_cap`. This is the most exam-realistic partial-credit treatment across the three docs.
- **Numeric verification:** `expected_values` with a 0.01 tolerance, e.g. Boyle's law P1 = 101325, V1 = 0.05, V2 = 0.02.
- **Go/No-Go:** SymPy false-positive step errors >0.5% means restricting auto-scoring to final answers.
- **HITL:** SymPy AST failure sends the item to manual verification (<20 s per item).
- **Residual:** non-standard solution proofs go to humans.
- **Chemistry:** named as MVP scope, but no chemistry parser is specified (e.g. for balancing equations).

---

## Risks identified

**RPN risk register (Probability / Impact / Detectability on 1–10; RPN = product):**

| ID | Risk | Prob | Impact | Det | RPN | Class | Mitigation (as given) | Residual |
|---|---|---|---|---|---|---|---|---|
| R-01 | Bangla handwriting / juktakkhor misreads | 8 | 9 | 7 | 504 | P0 | Fine-tuned TrOCR on BN-HTRd + BanglaBERT LM decoding | Medium |
| R-02 | Uncontrolled captures (skew, blur, light, shadow) | 9 | 7 | 4 | 252 | P1 | Edge IQA (Laplacian, Sauvola) + recapture prompts | Low |
| R-03 | Non-standard layouts, overlapping bboxes | 7 | 8 | 6 | 336 | P0 | Standardised templates with QR anchors + YOLOv8-Doc | Low |
| R-04 | LLM hallucinating algebraic steps | 7 | 9 | 8 | 504 | P0 | Mathpix → SymPy CAS | Low |
| R-05 | Rubric ambiguity, inconsistent partial credit | 8 | 8 | 6 | 384 | P0 | JSON rubric compiler with micro-criteria | Medium |
| R-06 | Penalising valid alternative solutions | 5 | 8 | 7 | 280 | P1 | Graph-based semantic equivalence + CAS | Medium |
| R-07 | Handwritten prompt injection | 4 | 9 | 8 | 288 | P1 | System-prompt isolation; HTR output as data tokens | Low |
| R-08 | Overconfident hallucinated grades bypass abstention | 6 | 9 | 9 | 486 | P0 | SCOPE conformal prediction with certified FDR | Low |
| R-09 | Correlated errors across LLM ensemble | 5 | 7 | 8 | 280 | P1 | Architectural heterogeneity (HTR + CAS + VLMs) | Medium |
| R-10 | Queue latency spikes at national uploads | 7 | 6 | 3 | 126 | P2 | Async serverless queue + autoscaling GPU pools | Low |
| R-11 | API token cost exceeds unit economics | 8 | 6 | 2 | 96 | P2 | Multi-tier routing, local models first | Low |
| R-12 | Silent model drift (curriculum or API updates) | 4 | 8 | 7 | 224 | P1 | CI regression suite on golden datasets | Low |

**Security threats:**
- Prompt injection (High): JSON encapsulation.
- Adversarial micro-print (Medium): frequency-domain / high-pass filtering.
- Cross-tenant exfiltration (Critical): PostgreSQL RLS + KMS.
- Insider audit manipulation (Critical): S3 Object Lock WORM.

**Failure modes (FMEA):**
- API timeout (High): LiteLLM failover.
- GPU OOM crash (High): Kafka requeue + page checkpoint.
- Duplicate ingestion (Medium): MD5 dedup.
- Corrupted upload (Medium): checksum + re-upload.

**Residual risks:** unreadable handwriting (→ human), creative essays (human-assisted pilot), provider outages (latency), teacher rubric inconsistency, and low-end phone cameras.

---

## Assumptions

1. Schools will adopt **pre-printed anchored answer sheets** with QR codes and bounded boxes. This is foundational: R-03 residual "Low" depends on it.
2. BN-HTRd fine-tuning transfers to BD exam handwriting well enough to reach CER <3%.
3. Conformal exchangeability holds between calibration and deployment data.
4. 5,000 expert-verified scripts will be available for calibration and 10,000 for the benchmark.
5. Commercial LLM APIs (Claude, OpenAI, Google) can be used for student data. Privacy and residency are not analysed.
6. Teachers can resolve items in about 15 s.
7. Human review costs $0.05 per escalated item/script.
8. AWS infrastructure (S3 Object Lock, KMS) is acceptable.
9. Ensemble disagreement is informative despite correlated errors (partly acknowledged in R-09).
10. A spatial GNN for Q–A mapping can be trained to 99.5% precision.

---

## Recommendations

1. Do **not** build zero-shot VLM grading. Build a constrained hybrid (Architecture C).
2. **Product design first:** standardised anchored answer sheets with QR codes, registration marks, bounded boxes and pre-coded sub-questions. This is claimed to cut pipeline failures by about 80%.
3. The MVP covers **secondary STEM only** (Math, Physics, Chemistry): MCQ, short answers and bounded derivations. Exclude humanities essays, freehand diagrams, arbitrary photos, creative writing and real-time fully automated scoring.
4. Deterministic verification wherever possible (CAS, units, summation), overriding LLMs.
5. Compile rubrics into JSON micro-rubrics offline, with explicit step dependencies and carry-forward rules.
6. Require evidence grounding (text span plus bbox) for every awarded mark. Ungrounded justifications go to a human.
7. Use **selective conformal prediction** (SCOPE) for abstention, calibrated on held-out expert scripts, and recalibrate for distribution shift.
8. Build HTR and CAS in-house (open source plus fine-tuning). Buy Mathpix and LLM APIs with multi-vendor LiteLLM failover.
9. Run all 14 POCs before full development. Apply the Go/No-Go thresholds (Bangla CER ≤3%, FDR ≤0.02, SymPy FP ≤0.5%, cost ≤$0.03/script).
10. Operations: 5% random audit, red-teaming (injection, adversarial marks, blank or upside-down pages), idempotency, DLQ, telemetry with override-rate alerts (>8%), and SHA-256 leakage exclusion of gold data from training.

---

## Open questions

- (From the report) LoRA few-shot adaptation to atypical Indic handwriting. Dynamic conformal thresholding under distribution shift. Multimodal visual GNNs that parse diagrams into ASTs.
- **[Analyst note]** Further questions:
  - Will BD schools and boards accept custom anchored answer sheets? Boards print their own answer scripts.
  - How are LLM token entropies obtained from closed APIs for s(x)?
  - What labelled data trains the spatial GNN and the LayoutLMv3 5-class model?
  - Data residency and legal basis for sending minors' data to US LLM APIs and AWS: entirely missing.
  - Why does the Stage 1 cost tier (65% of scripts, TrOCR only) commit scores without any evaluation model?
  - How does SCOPE (pairwise) map onto pointwise per-criterion marks?

---

## Critical assessment

**Unrealistic accuracy claims (the most serious across all three docs)**
- **Bangla handwriting CER 1.9% (<3%)**, "CER drops from 38.5% to 1.9%", backed only by a dangling `[cite: 1]`. This is roughly 5–10× better than the full-page Bangla HTR results in B1 (CER 12.8–18.7%) and B2 (GraDeT ~8.4%, TrOCR ~10.9%).
  - **[Analyst note]** Likely conflates isolated-character or word-level accuracy (~98%) with continuous exam-script HTR. It should be treated as **unsupported and probably wrong**. Building a Go/No-Go gate around CER ≤3% may still be a reasonable *target*, but the feasibility verdict ("Bangla HTR FEASIBLE") rests on it.
- "Certified" / "guaranteed" FDR ≤0.02 overstates conformal guarantees: they are marginal and assume exchangeability.
- Stage requirements such as 100% ID exact match, 99.99% page sequencing, 99.5% GNN mapping, >99% intent classification and 99.5% rubric parsing are presented as specs without any feasibility evidence.
- P95 2.8 s per *script* with Mathpix plus a dual-LLM ensemble is implausible.

**Outdated models:** Claude 3.5 Sonnet, GPT-4o and an unspecified "Gemini Pro" are the ensemble judges. All are outdated by Sept 2026.

**Architectural misstatements**
- "TrOCR = Swin + BanglaBERT decoder" is inaccurate. BanglaBERT is an encoder.
- SCOPE is a pairwise-judging method repurposed without discussion.
- LightOnOCR's Bangla handwriting capability is unverified.

**Internal contradictions**
- **Cost vs architecture:** the recommended Architecture C sends every script through a "Dual LLM Ensemble Judge" (Section 36 diagram), but the $0.0088 cost assumes 65% of scripts use only local TrOCR at $0.002, and only 10% hit the ensemble. The Stage 1 tier "commits score" with no grading model at all.
- **Human cost omitted:** the headline average omits human review ($0.05 per escalated item), yet the Go/No-Go threshold is ≤$0.03/script, and abstention rates up to 40% are contemplated.
- **Bangla feasibility vs MVP:** Bangla HTR is "FEASIBLE" (Section 4), yet the MVP excludes humanities and essays and targets STEM only. It is unclear whether Bangla-medium STEM answers are in scope.
- **Scope vs infrastructure:** "Serverless queue" (R-10) vs Kafka + Kubernetes HPA (Sections 18 and 20).
- **Scale vs timeline:** a 10,000-script benchmark plus 5,000-script calibration set within a 28-week plan that also pilots 20,000 scripts at 10 institutions in 6 weeks.
- **Better data:** says BN-HTRd fine-tuning fixes "mixed Bangla-English" CER, but BN-HTRd has no English.

**Over-engineering**
- The most over-engineered of the three docs: Kafka + Redis + Kubernetes HPA + Triton + vLLM + LiteLLM + a spatial GNN + DocSAM + LayoutLMv3 + YOLOv8 + BRISQUE + a Z3 SMT solver + ANTLR + SCOPE conformal prediction + a triple-LLM ensemble + WORM S3 + KMS + Prometheus/Grafana, plus 14 POCs and 99.99% availability targets, for an MVP that grades secondary STEM on anchored sheets.
- It requires custom model training (Swin-TrOCR, the LayoutLMv3 5-class model, a GNN, a BERT intent classifier, YOLOv8-Segment for diagrams) **before any exam data exists**.

**Omissions**
- No Bangladesh data-protection or residency analysis at all, despite AWS and US LLM APIs.
- No teacher-training or adoption discussion beyond UI timings.
- No discussion of how board and school answer-script formats would change to anchored templates.

**Fabricated-looking citations**
- Numeric results carry dangling `[cite: N]` markers.
- Several refs are loosely related: consumer-Blackwell private inference, energy-efficiency models, infographic reconstruction, a mathematical forum platform, datasheet layout (EDocNet), Bengali *scene* text.
- Real and relevant refs (SCOPE, CDM, DocSAM, LayoutLMv3, BN-HTRd facts) are mixed with filler.

**Strengths worth keeping**
- The anchored-template product lever.
- Evidence grounding (span plus bbox) per mark.
- Carry-forward partial credit in the rubric schema.
- Randomised numeric equivalence as a CAS fallback.
- An explicit abstention philosophy.
- 5% random audits.
- An override-rate alert.
- A red-team plan for handwritten prompt injection.
- Idempotency and DLQ basics.
- Concrete, testable Go/No-Go and abandon criteria (CER >5%, abstention >40%, cost >$0.10).

---

## Confidence level + Relevance to product decisions

**Confidence: Low-Medium.** Risk identification is thorough and mostly sensible; the RPN register and the HITL triggers are directly reusable. Its central optimistic claim (Bangla HTR CER <3% / 1.9%, hence "FEASIBLE") is unsupported and contradicted by the other two docs and by the published baselines they cite. Many "requirements" are aspirational numbers dressed as specifications. Cost and latency figures are internally inconsistent with its own recommended architecture.

**Relevance: High** for:
1. The **product-design lever**: anchored, pre-printed answer sheets with QR codes and ID checksums, arguably the single highest-leverage de-risking decision across all three docs.
2. The risk register and HITL trigger list.
3. Rubric JSON design with carry-forward and negative concepts.
4. Evidence-grounded scoring.
5. Abstention via calibrated thresholds. Start with simple held-out calibration of a threshold before attempting SCOPE.
6. Red-team and security items (prompt injection).
7. Abandon/proceed criteria.

**Low relevance:** its infrastructure stack, custom GNN/diagram models, the 28-week timeline and the headline Bangla CER. Treat these as over-engineering or unsupported.
