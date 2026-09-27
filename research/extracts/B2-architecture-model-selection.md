# Technical Research Report: System Architecture and AI Model Selection for Automated Examination Assessment in Bangladesh

- **Drive ID:** `1f0nDi9XXEqvcUYYkFqnK4OdLQT6_zhSQv1KUEXRcEsY`
- **Topic:** Architecture topology selection (six options, A–F), a capability map of 26 functions, Bangla HTR approach comparison, the LLM/VLM model landscape with pricing, domain subsystems (math, objective, subjective, diagram), a composite confidence score with three routing bands, benchmark methodology, Total Cost of Assessment (TCA) modelling, compliance, and an "AI Model & Architecture Decision Memo" with about 40 direct answers, a 10-pipeline experiment plan and an MVP→production migration path.
- **Method (as presented):** A desk synthesis presented as "empirical evaluation" and "weighted multi-criteria analysis". It includes a scorecard (1–5) and a cost model for 1,000 exams / 8,000 pages.
  - Sources cited: LLM price aggregators (anotherwrapper.com, aimodelcalculator.com, aifreeapi.com "Gemini API pricing 2026"), arXiv (2604.09717, 2606.11931 on semantic grading in a low-resource language, 2609.05143 on a HITL framework for AI-assisted scoring, 2609.10572, 2508.02442 on LLM reliability for scoring, 2512.14561 on LLM–human rater agreement), PMC (CompoundDenseNet), Frontiers (ViT for Bangla characters), a Scribd copy of "Bangla Handwritten Word Recognition Using Fine-Tuned TrOCR", Atlantis Press, the IIP Series review, the eklavvya.com blog (answer-sheet OCR), an ORF article on the CBSE OSM controversy, Hugging Face paper search pages, a Turkish OCR/VLM benchmark (ResearchGate), a ResearchGate paper on India's Digital Personal Data Protection Act 2023, and the privacy policy of a BD business school.
  - Inline markers such as `[cite: 1, 6]` and `[cite: 1, 5, 6]` point to no numbered list. The "Source Reference" column in the Bangla HTR table is **empty** in every row.
  - **[Analyst note]** The document says "empirical tests show…" but reports no experiment. All scorecard and cost figures are modelled or assumed.
- **Coverage:** The full document was read (about 67k characters, ending in the reference list). It is not truncated.

---

## Main findings

1. **The capability map has 26 capabilities (A–Z)** with an execution mechanism and a recommended tool for each:
   - A. Image understanding: Gemini 2.0 Flash / Qwen2.5-VL.
   - B. IQA: OpenCV.
   - C/E. General and English HTR: TrOCR-Large (Handwritten).
   - D. Bangla HTR: fine-tuned GraDeT-HTR / TrOCR-Bangla.
   - F. Mixed-language: fine-tuned multilingual TrOCR.
   - G. Math notation: Mathpix API / fine-tuned Nougat.
   - H. Diagram: OpenCV + Gemini 2.5 Flash.
   - I. Tables: TATR / LayoutLMv3.
   - J. Layout: YOLOv8-Doc / LayoutLMv3.
   - K. Question detection: spatial bounding-box parser.
   - L. Answer segmentation: OpenCV slicing.
   - M. Q–A mapping: positional graph associator.
   - N. Marking-scheme interpretation: Gemini 2.5 Pro / Claude 3.5 Sonnet.
   - O. Rubric understanding: Gemini 2.0 Flash / Claude 3.5 Sonnet.
   - P. Objective evaluation: Python regex + Levenshtein.
   - Q. Subjective evaluation: Gemini 2.0 Flash / 2.5 Pro.
   - R. Partial credit: Gemini 2.0 Flash / Claude 3.5 Sonnet.
   - S. Alternative answers: OpenAI text-embedding-3-large + LLM pass.
   - T. Math reasoning: SymPy/CAS.
   - U. Feedback: Gemini 2.0 Flash.
   - V. Confidence: deterministic formula.
   - W. Error propagation: rules.
   - X. Verification: GPT-4o / Gemini 2.5 Pro.
   - Y. Routing: rules.
   - Z. Results: PostgreSQL.
   - **Deterministic:** B, K, L, M, P, T, V, W, Y, Z. **AI:** A, C–J, N, O, Q, R, S, U, X.
2. **Six topologies compared:**
   - A: a single general-purpose VLM (GPT-4o / Gemini 2.0 Flash) does everything. Rejected for error propagation, token cost, context degradation, lack of auditability and prompt injection.
   - B: chained general LLMs.
   - C: a specialised pipeline.
   - **D: C plus HITL and confidence routing. RECOMMENDED.**
   - E: dynamic routing (Flash-Lite for easy items; Gemini 2.5 Pro / Claude 3.5 Sonnet / o3-mini for hard ones).
   - F: a dual-frontier ensemble with auto-accept at δ ≤0.5 marks. It costs **+200–250%** and doubles latency, so it is viable only for edge cases.
3. **Bangla script and HTR claims:**
   - 11 vowels, 39 consonants, **300+ juktakkhor**, and a matra.
   - "General-purpose OCR on handwritten Bangla yields CER >40%."
   - Proposed HTR flow: matra removal and baseline normalisation → ViT encoder → cross-attention with grapheme/ligature priors → autoregressive decoder outputting Unicode plus token log-likelihoods.
4. **Bangla HTR comparison table.** The source column is blank in every row.

   | Model | Dataset | Accuracy | CER |
   |---|---|---|---|
   | CompoundDenseNet | BanglaLekha-Isolated | 98.50% (isolated) | ~1.5% |
   | BanglaNet (Inception-ResNet-DenseNet) | CMATERdb | 98.40% | ~1.6% |
   | ViT (Patch6) | CMATERdb 3.1.2 | 98.26% | ~1.74% |
   | Fine-tuned TrOCR (ViT + RoBERTa) | "Real-world 132 Test Grid" | 62.88% full-word | 10.89% word-level |
   | **GraDeT-HTR** | "BN-HTRd / Exam Scripts" | **71.20% line-level** | **~8.40%** |
   | Google Cloud Vision API | handwritten Bangla forms | 45–65% | 20–35% |
   | Tesseract v5 (Bangla) | — | <30% | >45% |
   | **Qwen2.5-VL-7B-Instruct** | "Complex Document Scans" | ~75% contextual | **6.5–12.0%** (failure mode: hallucinated words when smudged) |

5. **Claim:** fine-tuned open-source transformer HTR (TrOCR, GraDeT) "outperform broad commercial APIs" because contextual language modelling resolves juktakkhor ambiguity.
6. **Four cascade options:**
   - A: direct multimodal. High vision-token cost ("258+ tokens per patch"), no inspectable transcript, hallucinations.
   - B: OCR → text-only LLM. Cheap, but a dropped "না" cascades.
   - **C: dual-path hybrid.** The LLM gets HTR text plus the image crop and audits visually on low confidence.
   - **D: HTR JSON** (text, alternative candidates, bboxes) plus crops → multimodal LLM.
   - C and D are rated most reliable.
7. **Model landscape table.** Prices are per 1M input/output tokens.

   | Model | Version | Context / output | Price in / out | TPS | Role |
   |---|---|---|---|---|---|
   | Gemini 2.0 Flash | Dec 2024/2025 | 1M / 8K | $0.10 / $0.40 | ~183 | **Primary workhorse** |
   | Gemini 2.5 Flash | "Jan 2026" | 1M / 8K | $0.15 / $0.60 | ~150 | Secondary router, diagrams |
   | Gemini 2.5 Pro | — | "2M / 8K" | $1.25 / $10.00 | ~60 | Reasoning specialist |
   | Claude 3.5 Sonnet | claude-3-5-sonnet-20241022 | 200K / 8K | $3 / $15 | ~100 | High-tier evaluator, math proofs, audits (fine-tuning "partner hosted AWS Bedrock") |
   | GPT-4o | gpt-4o-2024-11-20 | 128K / 16K | $2.50 / $10 | ~80 | Verifier |
   | GPT-4o mini | 2024-07-18 | — | $0.15 / $0.60 | ~140 | Low-cost router |
   | DeepSeek V3 | Dec 2024 | 64K / 8K | $0.14 / $0.28 | ~65 | Text-only grader post-HTR; "exceptional Bangla" |
   | DeepSeek R1 | Jan 2025 | 64K | $0.55 / $2.19 | ~35 | Math/logic audit |
   | Qwen2.5-VL-7B-Instruct | Jan 2025 | 32K / 4K | Self-hosted | ~45 (A10G) | Self-hosted OCR guard |
   | Fine-tuned TrOCR (custom) | — | — | — | ~250 wpm | Core HTR engine |

8. **Price argument:** Claude 3.5 Sonnet at "$18 blended per 1M" is unsustainable for first-pass grading. Gemini Flash at "0.50–0.75 blended" gives a **97% reduction**. Reasoning models are reserved for escalations.
9. **Math subsystem:** math-HTR → LaTeX → SymPy `Simplify(E_student − E_solution) = 0`. On failure, a line-by-line symbolic diff locates the error step. **An LLM receives the symbolic diff and applies the rubric for partial credit** (unlike B1, where deductions are purely deterministic).
10. **Objective subsystem:** regex, dictionary and Levenshtein (D_L ≤ threshold). Objective items make up "up to 30% of standard exam papers", with zero API cost, sub-millisecond latency and zero variance.
11. **Subjective subsystem:** normalise HTR artefacts, embed the rubric as an array of criteria, and require JSON output with **point allocations mapped to sentence citations**.
12. **Diagram subsystem:** OpenCV bounding boxes, arrow directions and geometry, plus a VLM (Gemini 2.5 Flash / Claude 3.5 Sonnet) comparing against a master diagram with keypoint prompts (e.g. "verify labelled stamen, anther, filament").
13. **Confidence:**
    - Formula: **ACS = w1·C_HTR + w2·C_Layout + w3·C_Semantic + w4·(1 − Disagreement)**, with Σw = 1.
    - Bands:
      - **ACS ≥0.88: auto-accept with no human.**
      - **0.70–0.88:** secondary verification with a different model (Gemini 2.0 Flash primary, GPT-4o verifier). If |ΔM| ≤0.5 marks, the average is accepted.
      - **<0.70:** teacher queue with uncertainty drivers ("Uncertain HTR on line 3").
14. **Benchmark:**
    - ≥300 real scripts: 40% Bangla, 40% English, 20% mixed.
    - Subjects: SSC/HSC Physics, Chemistry, Mathematics, Higher Mathematics, Biology, English, Bangla, General Science.
    - Legibility: 30% high, 40% moderate, 30% poor.
    - Edge cases: cross-outs, out-of-order answers, blue/black ink, marginal notes, erased pencil.
    - MMLU/GSM8K are dismissed as irrelevant.
15. **Human baseline:** QWK, MAE and RMSE. Targets: **human QWK ≥0.78 for essays, ≥0.92 for STEM**. The AI need only match the human–human level.
16. **TCA formula:** `N_pages·(C_ingest + C_HTR) + N_in·P_in + N_out·P_out + R_human·C_teacher + C_infra`.
17. **Cost model** (8 pages and 10 questions per script: 2 objective, 4 short, 2 math proofs, 2 essays; teacher review $0.15/script):

    | Architecture | Cost per 1,000 scripts | Per script | Escalation rate |
    |---|---|---|---|
    | A: Claude 3.5 Sonnet direct | $349.50 | $0.3495 | 25% |
    | A-Lite: Gemini 2.0 Flash direct | $57.60 | $0.0576 | 32% |
    | C | $35.80 | $0.0358 | 14% |
    | **D** | **$28.90** | **$0.0289** | **8%** |
    | F: Claude + GPT-4o on all items | $153.20 | $0.1532 | 4% |

    - D is a **91.7% reduction** vs A.
    - "Human review labour is the single largest financial driver."
18. **Compliance:**
    - "Bangladesh Data Protection Act (BDPA) & ICT Act": exam scripts are sensitive personal data; storage must be on local cloud or data centres inside BD; **7-year retention** in encrypted read-only form, then purge.
    - Threats: handwritten prompt injection (mitigated by isolating student text as JSON data) and silent vendor model drift (mitigated by pinning snapshots such as `gemini-2.0-flash-001` and `gpt-4o-2024-11-20` and regression-testing on a locked 50-script set).
19. **Scorecard** (1–5; QWK / cost per script / latency per page):

    | Option | Score | QWK | Cost/script | Latency/page |
    |---|---|---|---|---|
    | A (GPT-4o direct) | 2.10 | ≈0.62 | $0.35 | 12.4 s |
    | B (chained) | 2.88 | ≈0.76 | $0.18 | 18.2 s |
    | C | 4.52 | ≈0.84 | $0.035 | 3.2 s |
    | **D** | **4.82** | **≥0.89** | $0.028 | 3.8 s |
    | F | 2.95 | ≈0.86 | $0.15 | 22.0 s |

20. **Selected component matrix:**

    | Function | Primary | Fallback |
    |---|---|---|
    | Layout | YOLOv8-Doc / LayoutLMv3 | OpenCV contours |
    | Bangla HTR | Fine-tuned TrOCR / GraDeT-HTR | Self-hosted Qwen2.5-VL-7B |
    | English HTR | TrOCR-Large | Google Cloud Vision |
    | Objective | Regex / string engine | — |
    | Math | Math-HTR + SymPy | DeepSeek R1 via API |
    | Subjective | **Gemini 2.0 Flash (JSON)** | Gemini 2.5 Flash / GPT-4o mini |
    | High-risk verification | Gemini 2.5 Pro / Claude 3.5 Sonnet | GPT-4o |
    | Tabulation | PostgreSQL | — |

21. **Decision-memo answers:**
    - Multiple models plus deterministic engines. OCR before the LLM. Image plus OCR both go to the LLM for subjective and diagram items.
    - No frontier model on the first pass. Multi-model verification only in the medium band. **No ensemble on all items.**
    - **No RAG:** inject the full marking scheme into context.
    - **Fine-tune HTR only, not LLMs.** Open source for HTR, layout and on-prem OCR. Commercial Gemini API for prose.
    - Self-host YOLOv8 and TrOCR "to meet BDPA data sovereignty".
    - Route by subject and question type. Cascade: Flash → reasoning model → human.
    - "Model agreement within 0.5 marks on a 10-mark essay gives **QWK ≥0.91**."
    - Target **85–90% auto-acceptance**, 10–15% to humans.
    - Cost ≈$0.0028 per answer, $0.0289 per 8-page script, $28.90 per 1,000 students.
    - Simplest validating architecture: open-source TrOCR → Gemini 2.0 Flash → human queue for ACS <0.80.
    - Switch trigger: a VLM with **CER <3.0% on handwritten Bangla at <$0.20/1M tokens** justifies moving to direct multimodal ingestion.
    - Infeasibility trigger: a regulatory ban on cloud LLM APIs for educational records forcing 100% on-prem on low-resource hardware.
    - Vendor lock-in: an internal `AIProvider` abstraction.
22. **Experiment plan:**
    - 300 anonymised SSC/HSC scripts from Dhaka and Chittagong. Three senior teachers grade and transcribe.
    - **10 parallel pipelines:** direct GPT-4o, direct Gemini 2.0 Flash, direct Claude 3.5 Sonnet, Tesseract→Flash, fine-tuned TrOCR→Flash, fine-tuned TrOCR→2.5 Pro, GraDeT→SymPy/Flash, GraDeT→Flash plus image audit, Architecture D, and Architecture F.
    - Metrics: CER, WER, QWK, MAE, RMSE, cost, latency and forced-review %.
23. **Evidence hierarchy** (Tier 1 highest):
    - Tier 1: independent Bangla exam-script benchmarks.
    - Tier 2: peer-reviewed AES/QWK work.
    - Tier 3: open VLM benchmarks (Qwen2.5-VL, LightOnOCR).
    - Tier 4: provider docs and pricing.
    - Tier 5: vendor marketing.
24. **Migration path:**
    - **MVP:** fine-tuned TrOCR on a single GPU instance, Gemini 2.0 Flash via API, SymPy, and ACS <0.82 to humans.
    - **Production:** self-hosted YOLOv8-Doc, an enterprise Gemini 2.0 Flash instance with GPT-4o-mini failover, ACS <0.88 threshold "reducing human review to 10–15%", and backups on BDPA-compliant local storage.

---

## Quantitative claims table

| Claim | Value | Source cited | Source type | Credibility H/M/L + why |
|---|---|---|---|---|
| General OCR CER on handwritten Bangla | >40% | None | None | **M.** Directionally right for Tesseract-style engines. |
| CompoundDenseNet isolated accuracy | 98.50% | PMC article (in refs) | Peer-reviewed | **H** for isolated characters; irrelevant to line HTR. |
| BanglaNet CMATERdb | 98.40% | Empty column | Peer-reviewed (likely) | **M.** |
| ViT CMATERdb 3.1.2 | 98.26% | Frontiers (in refs) | Peer-reviewed | **M/H.** |
| Fine-tuned TrOCR Bangla word-level | 62.88% word; 10.89% CER | Scribd document | Unknown / grey literature | **L.** Scribd copy; the "132 test grid" is tiny. |
| GraDeT-HTR | 71.2% line-level, CER ~8.4% | Empty column | Unknown | **L/M.** Numbers not traceable; "Exam Scripts" dataset is probably mislabelled (GraDeT was not evaluated on BD exam scripts). |
| Google Cloud Vision on BN handwriting | 45–65% word; CER 20–35% | None | None | **L.** Unsourced. |
| Tesseract v5 BN handwriting | <30% word; CER >45% | None | None | **M.** Plausible. |
| Qwen2.5-VL-7B BN | CER 6.5–12% | None | None | **L.** "Complex document scans" does not mean Bangla handwriting; unsourced. |
| Gemini 2.0 Flash price | $0.10 / $0.40 per M; 1M/8K | Aggregator sites | Blog / aggregator | **H** for the historical list price. **[Analyst note]** Model likely deprecated by Sept 2026. |
| Gemini 2.5 Flash | $0.15 / $0.60; released "Jan 2026" | aifreeapi.com | Blog | **L.** GA was mid-2025 and GA list price was higher ($0.30 / $2.50 to my knowledge); $0.15/$0.60 was preview pricing. The release date is wrong. |
| Gemini 2.5 Pro | $1.25 / $10; "2M / 8K" | Aggregator | Blog | **M.** Price matches ≤200k-token tier; context was 1M and max output 64K to my knowledge. |
| Claude 3.5 Sonnet | $3 / $15; 200K / 8K | Aggregator | Blog | **H** for historical price. **[Analyst note]** Deprecated/retired model. |
| GPT-4o 2024-11-20 | $2.50 / $10; 128K / 16K | Aggregator | Blog | **H** historical. |
| GPT-4o mini | $0.15 / $0.60 | Aggregator | Blog | **H** historical. |
| DeepSeek V3 | $0.14 / $0.28; 64K | Aggregator | Blog | **M/L.** $0.14/$0.28 was promotional; standard pricing was higher. "Exceptional Bangla" is unsupported. |
| DeepSeek R1 | $0.55 / $2.19 | Aggregator | Blog | **H** historical. |
| Throughput (TPS) | 183 / 150 / 60 / 100 / 80 / 140 / 65 / 35 / 45 | None | None | **L.** Variable; unsourced. |
| Vision tokens | "258+ tokens per patch" | None | Official docs (implicit) | **M.** Matches Gemini's 258 tokens per image tile. |
| Ensemble cost uplift | +200–250%, 2× latency | None | None | **M.** Arithmetic logic. |
| Objective share of paper | up to 30% | None | None | **M.** SSC/HSC MCQ share is about 25–30% but it is OMR-marked. |
| Human QWK targets | ≥0.78 essays, ≥0.92 STEM | arXiv 2512.14561, 2508.02442 (refs) | Preprint | **M.** Reasonable targets, not measured. |
| Scorecard QWK | A≈0.62, B≈0.76, C≈0.84, D≥0.89, F≈0.86 | `[cite: 1, 6]` dangling | None | **L.** No experiment run; D exceeds the human essay target. |
| Agreement → QWK | ≥0.91 when 2 models agree ≤0.5 marks | "Empirical tests" | None | **L.** No test described; selection effect (only agreeing items). |
| Cost per script | A $0.3495; A-Lite $0.0576; C $0.0358; D $0.0289; F $0.1532 | `[cite: 1, 6]` | Own model | **M** as arithmetic (verified); **L** as prediction (escalation rates assumed). |
| Escalation rates | 25 / 32 / 14 / 8 / 4% | None | None | **L.** Assumed. |
| Human review cost | $0.15 per script review | None | None | **L.** For an 8-page script, $0.15 implies seconds of teacher time; B1 uses $0.15 per page. |
| Cost reductions | 97% (Flash vs Sonnet); 91.7% (D vs A) | Own arithmetic | None | **M.** Arithmetic correct. |
| Auto-accept rate | 85–90% | None | None | **L.** Aspirational. |
| Cost per answer | $0.0028 | Own arithmetic | None | **M** arithmetic; **L** reality. |
| Latency | C 3.2 s, D 3.8 s, A 12.4 s, B 18.2 s, F 22 s per page | None | None | **L.** Unmeasured. |
| Confidence bands | ≥0.88 auto; 0.70–0.88 verify; <0.70 human; MVP <0.82; "highest reliability" <0.80 | None | None | **L.** Design parameters, internally inconsistent (see critical assessment). |
| Retention | 7 years | None | None | **L.** Not traced to any BD statute. |
| Benchmark size | 300 scripts; 40/40/20 language; 30/40/30 legibility | None | Own design | **M.** Reasonable pilot size. |
| Switch trigger | VLM CER <3.0% on handwritten Bangla at <$0.20/M | None | Own rule | **M.** Useful decision rule. |
| Regression set | 50 locked scripts | None | Own design | **M.** |

---

## Recommended architecture

**Architecture D: specialised pipeline plus HITL and dynamic routing.**

1. **Ingest and preprocess (deterministic):** OpenCV IQA (Laplacian variance, contrast).
2. **Layout:** YOLOv8-Doc / LayoutLMv3 (self-hosted), falling back to OpenCV contour heuristics. Tables via TATR.
3. **Question detection, segmentation and Q–A mapping (deterministic):** spatial bbox parser, OpenCV slicing, positional graph associator.
4. **HTR (self-hosted):**
   - Bangla: fine-tuned TrOCR / GraDeT-HTR, falling back to Qwen2.5-VL-7B.
   - English: TrOCR-Large, falling back to Google Cloud Vision.
   - Mixed: multilingual TrOCR.
   - Math: Mathpix API / fine-tuned Nougat.
   - Output: structured JSON (text, alternative candidates, bboxes, token log-likelihoods). This is cascade option C/D.
5. **Evaluation:**
   - Objective: regex/Levenshtein.
   - Math: SymPy equivalence, then a line-by-line symbolic diff, then an LLM applying the rubric for partial credit. DeepSeek R1 is the fallback.
   - Subjective: **Gemini 2.0 Flash** with a JSON schema and sentence citations, plus the image crop for audit. Falls back to Gemini 2.5 Flash / GPT-4o mini.
   - Diagrams: OpenCV plus Gemini 2.5 Flash / Claude 3.5 Sonnet keypoint prompts.
   - Alternative answers: text-embedding-3-large plus an LLM pass.
   - Feedback: Gemini 2.0 Flash.
6. **Confidence and routing:** ACS formula.
   - ≥0.88: **auto-accept** with no human.
   - 0.70–0.88: second model (GPT-4o), averaged if |Δ| ≤0.5.
   - <0.70: teacher queue.
   - Escalation cascade: Flash → Gemini 2.5 Pro / Claude 3.5 Sonnet → human.
7. **Results:** PostgreSQL (ACID). Audit via pinned model versions and a regression suite.
8. **Cross-cutting:**
   - An `AIProvider` abstraction.
   - Model snapshot pinning.
   - Prompt-injection isolation: student text is only ever passed as JSON data.
   - Local BD storage.
   - Self-hosted HTR and layout for "sovereignty". Cloud Gemini API for grading.

**MVP:** fine-tuned TrOCR on one GPU → Gemini 2.0 Flash API → SymPy → human queue for ACS <0.82.

**Production:** self-hosted YOLOv8-Doc, an enterprise Gemini 2.0 Flash instance with GPT-4o-mini failover, and threshold ACS <0.88.

**No RAG. No ensemble on all items. No LLM fine-tuning.**

---

## Model-by-model notes

- **Gemini 2.0 Flash (Google).**
  - Claims: primary workhorse, "high Bangla text comprehension", native JSON schema, 1M context, $0.10/$0.40, fine-tunable on Vertex.
  - Privacy: cloud API with no BD region. This conflicts with the doc's own BDPA local-storage claim unless "storage" is read narrowly.
  - Failure modes: in direct-vision mode, 32% escalation ("vision uncertainty").
  - **[Analyst note]** By Sept 2026 this model is likely deprecated. Google announced retirement of the Gemini 2.0 series after the 2.5 GA. The choice must be re-benchmarked on current Flash-tier models.
- **Gemini 2.0 Flash-Lite.** Easy-item router in Architecture E.
- **Gemini 2.5 Flash.** Secondary router and diagram validation. The release date ("Jan 2026") and pricing are doubtful (see table).
- **Gemini 2.5 Pro.** Reasoning specialist for essays and humanities, marking-scheme interpretation, and verification. "2M context" is doubtful.
- **Claude 3.5 Sonnet (claude-3-5-sonnet-20241022).**
  - Claims: "superior spatial vision; excellent logical extraction". High-tier evaluator for complex math proofs and edge-case audits.
  - Direct-image grading cost $0.35/script with 25% escalation.
  - **[Analyst note]** Retired/deprecated model. Also, "fine-tuning via Bedrock" was offered for Claude 3 Haiku, not 3.5 Sonnet.
- **GPT-4o (gpt-4o-2024-11-20).** Verifier in the medium band and ensemble. "High multilingual competence." Direct vision gives QWK ≈0.62 (scorecard, unsourced).
- **GPT-4o mini.** Low-cost router and failover for Flash.
- **o3-mini.** High-complexity routing option in E. **[Analyst note]** Text-only (no image input), so it is unusable for vision audits.
- **DeepSeek V3 / R1.**
  - V3: text-only grader after HTR, "exceptional Bangla translation and logic" (unsupported).
  - R1: math/logic audit and SymPy fallback.
  - Open weights, self-hostable.
  - **[Analyst note]** The DeepSeek API is hosted in China, which has privacy and residency implications for minors' data. Self-hosting R1 (671B MoE) is very expensive. Using an LLM as a *fallback* for SymPy undermines the determinism principle.
- **Qwen2.5-VL-7B-Instruct.** Self-hosted OCR guard and Bangla HTR fallback, 32K context, ~45 tps on A10G. Bangla CER 6.5–12% (unsourced). It hallucinates words on smudges.
- **Fine-tuned TrOCR / "TrOCR-Bangla" / multilingual TrOCR.** Core HTR engine at ~250 wpm. Bangla fine-tune gives 62.88% word accuracy and 10.89% CER (Scribd source). **[Analyst note]** A multilingual TrOCR for code-switched text is not an existing off-the-shelf model; it would need to be built.
- **GraDeT-HTR.** Line-level 71.2% and CER ~8.4% (unsourced). The recommended Bangla HTR engine alongside TrOCR.
- **CompoundDenseNet, BanglaNet, ViT-Patch6.** Isolated-character classifiers at ~98%. Not usable for line HTR.
- **Google Cloud Vision API.** Bangla handwriting CER 20–35%. English HTR fallback. Cloud, non-BD.
- **Tesseract v5.** Bangla handwriting CER >45%. Baseline in pipeline 4.
- **Mathpix API.** Math-HTR. Accuracy is not quantified in this doc.
- **Nougat (fine-tuned).** Math OCR alternative. **[Analyst note]** Meta's Nougat was trained on typeset academic PDFs, not handwriting, which makes it a poor fit. Its license (CC-BY-NC for weights) is also restrictive.
- **TATR (Table Transformer), LayoutLMv3, YOLOv8-Doc.** Layout and tables. **[Analyst note]** Same licensing caveats as B1: LayoutLMv3 is non-commercial and YOLOv8 is AGPL.
- **text-embedding-3-large (OpenAI).** Alternative-answer paraphrase matching. Bangla quality is not evaluated.
- **SymPy / CAS.** Deterministic math equivalence and step diff.
- **LightOnOCR.** Mentioned only in the evidence hierarchy (Tier 3).
- **PostgreSQL.** Tabulation.

---

## Bangla-specific findings

- **Script:** 11 vowels, 39 consonants, "over 300" juktakkhor (2–4 fused consonants), and a matra. Handwriting causes connected matra lines, variable stroke order and size, and high intra-class variability.
- **Pre-processing proposal:** matra removal and baseline normalisation before a ViT encoder, with grapheme/ligature priors in cross-attention and token log-likelihoods for confidence. **[Analyst note]** Explicit matra removal is a classical segmentation-era technique; modern end-to-end HTR usually does not need it. This is a plausible-sounding but unvalidated design.
- **Datasets:** BanglaLekha-Isolated, CMATERdb (3.1.2), BN-HTRd, a "Real-world 132 Test Grid", "Handwritten Bangla Forms" and "Complex Document Scans". Only the first three are identifiable public datasets.
- **CER landscape (as claimed):** isolated ~1.5–1.7%; fine-tuned TrOCR 10.89%; GraDeT ~8.4%; Qwen2.5-VL-7B 6.5–12%; Google Vision 20–35%; Tesseract >45%; general OCR >40%.
- **Conjuncts:** contextual LM decoding "resolves visual ambiguity in handwritten Juktakkhor using sentence-level semantics". **[Analyst note]** LM priors can also *hallucinate* plausible but wrong words. For grading, this is a double-edged sword: it corrects spelling the student actually got wrong.
- **Negation risk:** dropping "না" is named as the top model risk. Cascade options C/D (image audit) are the mitigation.
- **Mixed script:** benchmark mix of 40% Bangla, 40% English, 20% code-switched. A fine-tuned multilingual TrOCR is proposed.
- **LLM Bangla comprehension:** asserted only. Gemini 2.0 Flash has "high Bangla text comprehension" and DeepSeek V3 "exceptional Bangla translation". No Bangla grading QWK is reported. arXiv 2606.11931 ("Semantic grading of written answers in low-resource language") is cited but no numbers are extracted.
- **Decision rule:** switch to direct VLM ingestion only if Bangla handwriting CER <3.0% at <$0.20/M tokens.

---

## Math-specific findings

- **Math OCR:** "math-specialised HTR" (Mathpix API / fine-tuned Nougat) → normalised LaTeX.
- **Symbolic verification:** SymPy/CAS via algebraic simplification, polynomial expansion and matrix evaluation: `Simplify(E_student − E_solution) = 0`.
- **Step extraction and diff:** line-by-line symbolic subtraction locates the first erroneous step.
- **Partial credit:** **an LLM receives the step-by-step symbolic diff and applies the rubric**. This is a hybrid: the CAS locates the error, the LLM allocates marks. It contrasts with B1 (deterministic deductions) and B3 (programmatic rule engine).
- **Why not LLMs:** matrices, fractions, radicals and integration limits cause tokenisation problems and "arithmetic hallucination".
- **Fallback:** DeepSeek R1 via API when math-HTR/SymPy fails. **[Analyst note]** This reintroduces the non-determinism the design is meant to avoid.
- **Routing:** STEM → math-HTR + SymPy. Claude 3.5 Sonnet is the "high-tier evaluator" for complex proofs.
- **Human STEM baseline target:** QWK ≥0.92.
- **Cost model:** two math proofs per 10-question HSC paper.
- No math OCR accuracy numbers are given in this document.

---

## Risks identified

The document has no formal risk register. The risks below are compiled from the text; probability and impact are not quantified unless noted.

| Risk | Probability | Impact | Mitigation (as given) |
|---|---|---|---|
| HTR drops Bangla negation ("না"), cascading grading errors | Not given ("biggest model risk") | High | Dual-path cascade (image crop plus HTR text); confidence routing |
| Hallucinated credit on incorrect math steps | Not given | High | SymPy verification; LLM given only symbolic diffs |
| Vendor API deprecation / silent model updates | Not given | High (score drift) | Pin snapshot versions (`gemini-2.0-flash-001`, `gpt-4o-2024-11-20`); 50-script regression suite; AIProvider abstraction |
| Primary model outage | Not given | Medium | Failover gemini-2.0-flash → gpt-4o-mini / self-hosted qwen2.5-vl |
| Handwritten prompt injection | Not given | High | System prompt isolation; student text only as JSON data variables |
| Single-model error propagation, token cost, context degradation | High (Architecture A) | High | Specialised pipeline (C/D) |
| Ensemble cost blow-up | Certain if applied to all items | +200–250% cost | Use ensemble only in the 0.70–0.88 band |
| RAG retrieval failure / latency | Not given | Medium | Don't use RAG; inject the full rubric |
| HTR throughput on very illegible cursive | "Technical unknown" | — | Not given |
| ACS calibration stability across subjects | "Technical unknown" | — | Not given |
| Regulatory ban on cloud LLM APIs for education records | Not given | Infeasibility | None; named as the infeasibility trigger |
| PII in scripts (names, rolls, registration codes) | Certain | High | Classify as sensitive; local storage; 7-year encrypted retention then purge |

---

## Assumptions

1. Fine-tuned TrOCR/GraDeT will outperform commercial OCR on BD exam handwriting, based on unsourced CER tables.
2. Gemini Flash-tier models deliver "comparable structured-output accuracy" to Claude 3.5 Sonnet for rubric grading.
3. Escalation rates: 8% for D, 14% for C, 25% for A, 32% for A-Lite, 4% for F.
4. Teacher review costs $0.15 per *script* (8 pages).
5. An HSC paper is 8 handwritten pages and 10 questions (2 objective, 4 short, 2 math proofs, 2 essays).
6. Model-agreement signals correlate with correctness strongly enough to auto-accept averaged scores.
7. BDPA mandates local storage and 7-year retention.
8. Self-hosting HTR plus a cloud Gemini API satisfies BD data sovereignty.
9. Human–human QWK in BD will be around 0.78 for prose and 0.92 for STEM.
10. Pinned snapshot model versions remain available long enough for exam cycles.
11. Full rubric-in-context is better than RAG. This is likely true, given that rubrics are small.

---

## Recommendations

1. Adopt **Architecture D**: a specialised pipeline plus deterministic engines, confidence routing and HITL. Reject single-model and full-ensemble designs.
2. OCR/HTR before the LLM. Give the LLM both the transcript and the image crop (cascade C/D) for subjective and diagram items.
3. Deterministic handling of objective items (regex/Levenshtein), math (SymPy), totals (PostgreSQL) and routing.
4. Gemini 2.0 Flash for the first-pass subjective grade and feedback. Gemini 2.5 Pro / Claude 3.5 Sonnet for escalations. GPT-4o as the medium-band verifier.
5. Fine-tune HTR (TrOCR/GraDeT) on local Bangla handwriting. Do **not** fine-tune LLMs. Do **not** use RAG.
6. Self-host layout and HTR. Use commercial APIs for prose grading behind an `AIProvider` abstraction. Pin model versions and regression-test.
7. Build a 300-script gold benchmark (40/40/20 language; 30/40/30 legibility; three-teacher ground truth) and run the 10-pipeline comparison before committing.
8. Targets: human-level QWK (≥0.78 prose, ≥0.92 STEM) and 85–90% auto-acceptance.
9. MVP threshold ACS <0.82 to humans. Production <0.88.
10. Treat exam scripts as sensitive PII. Store locally, retain 7 years encrypted, isolate prompts from student text.

---

## Open questions

- (From the report) HTR throughput on extremely illegible cursive. Long-term ACS calibration stability across subjects.
- **[Analyst note]** Further questions:
  - How is C_Semantic ("softmax probability or logit bias") obtained from closed APIs that do not expose calibrated probabilities?
  - How are ACS weights fitted before any labelled data exists?
  - Does sending transcripts or crops to the Gemini API (with no BD region) satisfy the law this doc says requires local storage?
  - Is auto-accept without any human sign-off acceptable to BD schools, boards and parents? The ORF article on the CBSE OSM controversy, cited here, suggests public-trust risk.
  - Which current Gemini/Claude/OpenAI models replace the deprecated ones, at what price?
  - Where is the 7-year retention requirement codified?

---

## Critical assessment

**Unrealistic or unsupported accuracy claims**
- **Scorecard QWK ≥0.89 for Architecture D** exceeds the report's own human essay baseline (0.78). It is presented as an "empirical" score with no experiment. Treat it as fabricated precision.
- "Model agreement within 0.5 marks gives QWK ≥0.91" is attributed to "empirical tests" that are never described. It is also a biased subset metric: agreement cases are the easy ones.
- The Bangla HTR table's source column is **empty**. The GraDeT "Exam Scripts" dataset label and the Qwen2.5-VL-7B "6.5–12% CER" on "Complex Document Scans" are not attributable. The Qwen figure would make a general 7B VLM competitive with specialised HTR, which contradicts the doc's own conclusion that specialised HTR wins.
- "Gemini Flash delivers comparable structured-output accuracy" to Claude 3.5 Sonnet is asserted without evidence.

**Outdated or wrong model details**
- Gemini 2.0 Flash is the primary workhorse, but was likely retired by Sept 2026.
- Claude 3.5 Sonnet is retired.
- GPT-4o and GPT-4o mini are superseded.
- Gemini 2.5 Flash's "Jan 2026" release and $0.15/$0.60 price are inconsistent with GA timing and pricing to my knowledge.
- Gemini 2.5 Pro's "2M context / 8K output" is doubtful.
- DeepSeek V3's promo price is quoted as standard.
- Nougat is for printed PDFs, not handwriting.
- o3-mini has no vision.

**Legal citation problem**
- It names a "Bangladesh Data Protection Act (BDPA)" but cites a ResearchGate paper on **India's Digital Personal Data Protection Act 2023**, plus a BD business school's privacy policy.
- The 7-year retention and local-storage mandates are unsourced.
- **[Analyst note]** Bangladesh's instrument is the Personal Data Protection Ordinance 2025 (as B1 cites). The requirements must be verified against its actual text.

**Internal contradictions**
- **Threshold logic is inverted.** The MVP uses a "conservative" threshold of ACS <0.82 to humans, while production moves to ACS <0.88 "reducing human review to 10–15%". Raising the escalation threshold *increases* the items sent to humans. Likewise, the "highest-reliability" option uses ACS <0.80, which is *less* conservative than the default 0.88.
- The ACS bands say ≥0.88 is auto-accepted and escalation to Pro/Sonnet happens at "<0.88", but the medium band routes to GPT-4o averaging, not Pro/Sonnet. Two different escalation targets are described for the same band.
- "Self-host HTR to meet BDPA data sovereignty" while sending text and images to the Gemini cloud API.
- It says "no ensemble", yet the medium band averages two models: a partial ensemble, which it concedes.
- It says "deterministic math", yet an LLM allocates partial credit and DeepSeek R1 is the math fallback.
- Latency of 3.2–3.8 s/page for a multi-stage pipeline with cloud LLM calls is claimed without measurement. The same doc claims the "sub-minute" requirement.

**Cost realism**
- The $0.15 teacher cost per *8-page script* underprices human review about 8× relative to B1 ($0.15 per *page*). Since the doc itself says human review dominates cost, this assumption drives the headline "$0.0289/script".
- Escalation rates (8% for D) are assumed, not measured. They are the key sensitivity.

**Over-engineering and complexity**
- Relatively restrained on infrastructure: a single-GPU MVP, and it explicitly rejects full ensembles.
- The 26-capability map with separate models for tables (TATR), diagrams, feedback, embeddings and verification is broad for an MVP.
- Recommending HTR fine-tuning in the MVP presumes labelled local data that does not yet exist.

**Fabricated-looking citations**
- `[cite: 1, 6]` and `[cite: 1, 5, 6]` markers with no list.
- Price aggregator blogs used as pricing sources rather than official docs, although the doc's own evidence hierarchy ranks official docs as Tier 4.
- A Scribd-hosted paper.
- A Turkish OCR benchmark and an Indian DPDP paper used for BD claims.

---

## Confidence level + Relevance to product decisions

**Confidence: Medium-Low.** The architectural reasoning is sound and useful:
- Why a specialised pipeline beats a monolith.
- Cascade options C/D (HTR transcript plus image crop).
- Deterministic objective and math handling.
- No RAG for small rubrics.
- Snapshot pinning and regression testing.
- The AIProvider abstraction.
- The 10-pipeline bake-off.
- The human-baseline-first evaluation philosophy.

However, nearly all quantitative outputs (scorecard QWK, escalation rates, latencies, cost per script) are unmeasured model outputs presented as empirical. The model shortlist is dated, and there are notable legal-citation errors.

**Relevance: High** for:
1. The architecture pattern (D) and routing and cascade design.
2. The experiment design: a 300-script gold set, three-teacher ground truth, and the 10-pipeline comparison including "direct VLM" baselines. This is the most actionable piece across all three docs.
3. Operational practices: version pinning, a regression set, prompt-injection isolation.
4. The explicit decision rule to switch to direct VLM ingestion if Bangla CER <3%.

**Low relevance:** specific model picks and prices (they must be re-sourced from current official pricing), and the headline cost per script (it depends on an under-priced human review assumption).
