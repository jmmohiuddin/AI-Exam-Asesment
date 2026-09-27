# V2 — State of the Art: AI/OCR for Grading Handwritten Bangla/English Exam Scripts (incl. Math)

**Verification date (all "accessed" dates):** 2026-09-27
**Method:** Web search (Exa) and direct fetches of vendor docs, arXiv/ACL/NeurIPS pages, and product pages. Several domains (arxiv.org, openai.com, docs.cloud.google.com, learn.microsoft.com, docs.aws.amazon.com) were blocked for direct fetch in this environment. For those, content came from the Exa fetch/search index of the same URL. Where a table rendered only as icons, or a number could not be seen, the item is marked **UNVERIFIED**. No numbers were invented.

**Status legend:** VERIFIED = seen on the cited primary source. PARTIAL = seen but truncated or indirect. UNVERIFIED = not confirmed. CONFLICT = sources disagree.

---

## Executive summary (for product decisions)

1. **Handwritten Bangla OCR is not production-ready off the shelf.**
   - The best published Bangla HTR system (GraDeT-HTR, EMNLP 2025 demo) reports **6.19% CER / 14.20% WER** on BN-HTRd. On the harder Bongabdo set it reports **8.68% CER / 23.56% WER**.
   - In the same paper, **Gemini 2.5 Flash scored 19.39% CER / 32.49% WER** on BN-HTRd and **37.42% / 56.39%** on Bongabdo.
   - Azure Document Intelligence does **not** list Bengali for handwriting. It does not list Bengali for printed Read either.
   - AWS Textract handwriting covers only the English alphabet.
   - Mathpix handles printed Bengali only. Its handwriting languages are English, Hindi and Latin-alphabet languages.
   - Google lists Bengali for OCR and says "50 handwritten languages". Whether Bengali is one of those 50 could not be confirmed (UNVERIFIED).
2. **Handwritten math recognition is close to solved for single expressions, not for full solutions.**
   - A fine-tuned 3B VLM (Uni-MuMER, NeurIPS 2025) reaches **79.74% average ExpRate** on CROHME 14/16/19.
   - Zero-shot Gemini 2.5 Flash reaches **55.32%** and GPT-4o **48.81%**.
   - Multi-line student work is harder. A new 2026 benchmark (OmniHandwritingOCR) reports sharp drops on complex multi-line formulas and "hallucinated corrections".
3. **LLM grading of handwritten STEM work is useful as assisted grading, not autonomous grading.**
   - GPT-4o on a probability exam, with answer key and rubric: exact-score accuracy **46.7%**, correlation **0.62**, MAE 7.7% of question points.
   - GPT-5 on a calculus exam: unfiltered agreement was "moderate". Human-level accuracy was reached only after confidence filtering, which sent **~70% of items to humans**.
   - A 2026 multi-stage ensemble pipeline (GPT-5.2 / Gemini-3 Pro) reached **~8-point mean absolute difference** with a **~17% manual-review trigger rate**.
4. **Targets to plan against.** Human–human QWK is typically **0.61–0.85** on ASAP essay sets and **0.82** on TOEFL Junior. The widely used automated-scoring bar is QWK ≥ 0.70 and within 0.10 of human–human (PARTIAL).
5. **Cost is not the bottleneck.** A 1500×2000 page costs roughly **$0.003–$0.05 per page per model call**, depending on model, and about half that with batch (arithmetic in Q6). OCR accuracy, calibration and injection resistance are the real constraints.

---

## Q1. Bangla handwritten text recognition (HTR)

### Verified facts

**Datasets**

- **BN-HTRd** (Rahman et al.; arXiv 2206.08977; CRC Press 2023; Mendeley CC-BY-4.0).
  - 786–788 full-page images from ~150 writers.
  - 14,383 lines, 108,181 words, 23,115 unique words, 574,203 characters.
  - The BN-DRISHTI paper extended it with 200k+ annotations.
  - Sources: https://huggingface.co/datasets/shaoncsecu/BN-HTRd_Splitted ; https://arxiv.org/html/2306.09351 (accessed 2026-09-27).
- **BanglaWriting** (Mridha et al., Data in Brief 2020/21). 260 single-page samples from 260 writers, 21,234 words, 32,787 characters, 5,470 unique words, word-level bounding boxes. https://pmc.ncbi.nlm.nih.gov/articles/PMC7744928/ (accessed 2026-09-27).
- **Bongabdo** (Ghosh, IEEE SILCON 2023; UCI dataset 894).
  - Full-page Bangla handwriting from 49 contributors, 111 samples.
  - Includes strike-throughs, Bangla–English code-switching and multi-paragraph pages.
  - https://archive.ics.uci.edu/dataset/894/bongabdo ; https://www.kaggle.com/datasets/ayanwap7/bongabdo1429 (accessed 2026-09-27).
- **BanglaLekha-Isolated** (Biswas et al., 2017). 84 classes (50 basic characters, 10 numerals, 24 compounds), 166,105 isolated character images. https://pmc.ncbi.nlm.nih.gov/articles/PMC5382023/ (accessed 2026-09-27).
- **CMATERdb.** Isolated-character accuracy is saturated. BanglaNet (arXiv 2401.08035) reports 98.40% (CMATERdb, 231 classes) and 97.65% (BanglaLekha-Isolated). https://arxiv.org/pdf/2401.08035 (accessed 2026-09-27). **Isolated-character accuracy does not predict page-level exam OCR.**

**Best reported CER/WER (2023–2026)**

**GraDeT-HTR** (Hasan et al., EMNLP 2025 System Demos). Grapheme tokenizer, decoder-only transformer, 87M parameters.

- Word-level pipeline with a text-detection front end:
  - BN-HTRd: **CER 6.19% / WER 14.20%**
  - Bongabdo: **CER 8.68% / WER 23.56%**
- If images where word detection failed are filtered out, BN-HTRd drops to CER 4.58%.
- Line-level variants were much worse: **CER 26.17–38.34%** on BN-HTRd and **46.91–65.04%** on Bongabdo.
- Comparison systems in the same paper: **Gemini 2.5 Flash** CER 19.39% / WER 32.49% (BN-HTRd) and 37.42% / 56.39% (Bongabdo). A footnote says Gemini 2.5 Pro was "slightly better" but was not used because of free-tier limits.
- Sources: https://aclanthology.org/2025.emnlp-demos.52.pdf ; https://arxiv.org/html/2509.18081v1 ; weights at https://github.com/mahmudulyeamim/GraDeT-HTR (accessed 2026-09-27).

**YOLO + EfficientNet-B4 grapheme pipeline** (Discover AI, 2025). On in-house data, with Word2Vec spelling correction, CER **2.47%** (10.37% without correction). Google Cloud Vision had CER **13.89%** on the same data. https://link.springer.com/article/10.1007/s44163-025-00251-7 (accessed 2026-09-27). The in-house data and conditions are not comparable to public benchmarks.

**Multimodal LLMs on Bangla / Indic handwriting**

- **GraDeT-HTR paper (above):** the only head-to-head of a frontier VLM against a specialized model on public Bangla HTR data that was found.
- **KhatianDoc** (arXiv 2609.03597, 2026-09-03).
  - 107 real handwritten Bangladeshi land records (RS Khatians).
  - Six MLLMs (8B–72B+) were tested. 39.3% of QA categories got zero correct answers from every model.
  - This shows domain-specific Bengali handwritten documents remain hard for MLLMs.
  - https://arxiv.org/abs/2609.03597 (accessed 2026-09-27).
- **Devanagari (printed real scans) stress test** (arXiv 2606.29213).
  - Gemini 2.5 Flash chrF++ 86.3, Claude Opus 4.7 82.2, Qwen3-VL-8B 75.2, GPT-5.5 58.5.
  - Takeaway: "English OCR ranking does not transfer to Indic scripts."
  - This is printed Hindi, not handwritten Bangla. Use it only as directional evidence.
  - https://arxiv.org/pdf/2606.29213 ; https://github.com/Aditya-PS-05/devanagari-ocr-benchmark (accessed 2026-09-27).
- **Bangla semantic grading system** (arXiv 2606.11931, June 2026). Uses GraDeT-HTR as its HTR front end rather than a VLM, which suggests a Bangla-specific HTR stage is the current practitioner choice. https://arxiv.org/html/2606.11931 (accessed 2026-09-27).

### Conflicting evidence

- Prompt design swings VLM OCR accuracy a lot. CoRSAL-OCR (2026) reports up to **6× CER reduction** from a detailed generic prompt versus a minimal one (Bodo/Garo, printed archival). https://aclanthology.org/2026.computel-1.14.pdf (accessed 2026-09-27). So the Gemini 2.5 Flash Bangla figures above may understate a well-prompted current model.
- On Bongabdo, a generic website OCR (Imagetotext.info, CER 14.36%) beat Gemini 2.5 Flash (37.42%). This hints at VLM failure modes such as hallucination and skipping on messy full pages, not just recognition errors.

### Unverified

- CER of **current** frontier models (Gemini 3.x, GPT-5.5/5.6, Claude Opus 5 / 5.5, Sonnet 5) on BN-HTRd, BanglaWriting or Bongabdo. No published benchmark found as of 2026-09-27.
- Any dataset of real Bangladeshi **exam answer scripts** (SSC/HSC/university) with transcriptions. None found.
- Numeric results of BanglaWild (arXiv 2608.03884, scene text, 15 VLMs). The page was found but no CER figures were retrieved.

### Implications for product design

- Treat Bangla handwriting transcription as the **largest single risk**.
- A realistic starting assumption for zero-shot VLM transcription of real Bangla exam pages is **CER in the 10–35% range**. This is inferred from the ~19–37% Gemini 2.5 Flash figures plus newer-model improvement, and is **not verified**.
- The best specialized system reaches ~6–9% CER on curated datasets, not on exam scripts.
- Plan a **must-run in-house benchmark**: 300–500 real, consented Bangla/English exam pages, double-transcribed. Compare 2–3 frontier VLMs and GraDeT-HTR.
- Design grading so it does not depend on verbatim transcription:
  - grade directly from the image with rubric criteria;
  - route low-legibility regions to humans;
  - never auto-deduct for "spelling" judged from OCR output.

---

## Q2. Commercial OCR support for handwritten Bangla

### Verified facts

- **Azure AI Document Intelligence v4.0 (Read / Layout).**
  - Handwritten languages: English, Chinese Simplified, French, German, Italian, Japanese, Korean, Portuguese, Spanish, Russian, Thai, Arabic (12).
  - **Bengali is not in the handwritten list.** It is also **not in the printed-text list** (it appears only in the language-*detection* list).
  - https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/language-support/ocr (accessed 2026-09-27 via Exa).
- **Google Cloud Vision OCR.** Bengali (`bn`, Beng script) is in the "Supported languages … prioritized and regularly evaluated" list for `TEXT_DETECTION` / `DOCUMENT_TEXT_DETECTION`. https://cloud.google.com/vision/docs/languages (accessed 2026-09-27).
- **Google Document AI Enterprise Document OCR.**
  - Lists Bangla/Bengali (`bn`). The processor "extract[s] text, including handwritten text … in more than 200 languages".
  - Google's OCR overview says "200+ languages, **50 handwritten languages**".
  - Processor versions: `pretrained-ocr-v2.1-2024-08-07` (GA); regions include `asia-south1`.
  - https://cloud.google.com/document-ai/docs/languages ; https://cloud.google.com/use-cases/ocr (accessed 2026-09-27).
- **AWS Textract.** "Amazon Textract can detect printed text and handwriting from the Standard English alphabet and ASCII symbols"; printed-text extraction covers English, German, French, Spanish, Italian and Portuguese. **No Bengali.** https://aws.amazon.com/textract/faqs/ ; https://docs.aws.amazon.com/textract/latest/dg/textract-best-practices.html (accessed 2026-09-27).
- **Mathpix.** Printed Asian languages include Bengali. Handwritten languages: "Hindi, English, All other Latin alphabet languages". "Math handwriting recognition with English & Hindi". **No Bengali handwriting.** https://mathpix.com/language-support (accessed 2026-09-27).
- Independent evidence: Google Cloud Vision had **13.89% CER** on in-house Bangla handwriting (Springer 2025, Q1).

### Unverified

- **Whether Bengali is one of Google Document AI's 50 handwriting languages.** The "Handwriting supported" column renders as icons that could not be read, and the direct page fetch was blocked. Confirm manually at https://cloud.google.com/document-ai/docs/languages.

### Implications

- For Bangla handwriting, only Google (unconfirmed handwriting status) and frontier VLMs are candidates among hyperscalers.
- Azure, AWS and Mathpix are **out** for Bangla handwriting. They remain usable for English-only pages (Azure/AWS) or English/Hindi math (Mathpix).

---

## Q3. Handwritten math recognition

### Verified facts

**Benchmarks**

- CROHME training set: 8,836 expressions. Test sets: 986 (2014), 1,147 (2016), 1,199 (2019).
- HME100K: 74,502 train and 24,607 test images, real-scene photos.
- Sources: https://arxiv.org/pdf/2401.00435 ; https://openreview.net/pdf?id=oHbVboLXz6 (accessed 2026-09-27).

**Specialized models (ExpRate, exact match)**

- **ICAL (2024):** 60.63 / 58.79 / 60.51 on CROHME 14/16/19; 69.06 on HME100K. https://arxiv.org/pdf/2405.09032v4.pdf
- **PosFormer:** ~61.2 average on CROHME. https://arxiv.org/html/2505.23566

**Fine-tuned VLM (Uni-MuMER, NeurIPS 2025 spotlight)**

- Base model: Qwen2.5-VL-3B, trained on ~1.6M samples.
- CROHME14 **82.05**, CROHME16 **77.94**, CROHME19 **79.23**; average **79.74%** ExpRate (82.86% ExpRate@CDM).
- Newer checkpoints: Qwen3.5-2B reaches 83.98 / 81.17 / 80.15 on CROHME 14/16/19, 70.43 on HME100K, and 51.84 on MathWriting.
- Sources: https://proceedings.neurips.cc/paper_files/paper/2025/file/bb992de895e886c2be79985835cb0ea4-Paper-Conference.pdf ; https://github.com/BFlameSwift/Uni-MuMER (accessed 2026-09-27).

**Zero-shot frontier models** (same paper, CROHME average ExpRate)

| Model | Average ExpRate |
|---|---|
| Gemini 2.5 Flash | 55.32 |
| GPT-4o | 48.81 |
| Qwen2.5-VL-72B | 56.40 |

**Multi-line / student work**

- OmniHandwritingOCR (arXiv 2608.18586, CIKM 2026): 77.57K images including newly collected student writing and difficulty-stratified multi-line formulas.
- Finding: "performance drops sharply on complex multi-line formulas … several generative models hallucinate plausible but visually unsupported corrections".
- https://arxiv.org/abs/2608.18586 (accessed 2026-09-27).

**Mathpix pricing** (https://mathpix.com/pricing/api, accessed 2026-09-27)

| Service | Price |
|---|---|
| Image OCR `v3/text` | $0.002/image (0–1M); $0.0015 above 1M |
| Documents (`v3/pdf`) | $0.005/page |
| Files API batch | $0.0015/page |
| Setup fee | $19.99 one-time |

- Images with **more than 12 rows of text may be billed at the per-page PDF rate**.
- Default image retention is 30 days, with an opt-out that deletes within 24h.

**Open source**

- **pix2tex** targets block LaTeX equations. Per the texify README, it is "trained on im2latex" and "hallucinates more on text". https://github.com/lukas-blecher/LaTeX-OCR
- **texify** is archived and deprecated; its functionality moved to `surya` (`surya_latex_ocr`). https://github.com/VikParuchuri/texify (accessed 2026-09-27)
- **Uni-MuMER** weights are open (above) and are the strongest open HMER option found.

### Unverified

- CROHME / HME100K / MathWriting scores for **current** frontier models (GPT-5.x, Gemini 3.x, Claude Opus 5 / 5.5).
- Mathpix accuracy on student full-page solutions.
- Current accuracy of TrOCR for math. It is an English text-line HTR model and was not evaluated here.

### Implications

- For math, a two-track approach looks most defensible:
  1. a frontier VLM for layout and step extraction;
  2. a specialist check on extracted expressions (Uni-MuMER-class model or Mathpix for English/Hindi), with CAS verification (Q8).
- Expect **about 20% expression-level error even for the best single-expression model**, and more on multi-line work. Grading must therefore tolerate recognition noise, for example by crediting method when the final expression is ambiguous and routing to a human.

---

## Q4. LLM-based short-answer / essay grading

### Verified facts

**Handwritten exams**

- **Caraeni, Scarlatos & Lan 2024** (arXiv 2411.05231). GPT-4o, 18 students × 5 probability questions = 90 samples.

  | Prompt | Accuracy | Pearson r | MAE |
  |---|---|---|---|
  | No context | 42.2% | 0.28 | 0.094 |
  | + correct answer | 43.3% | 0.55 | 0.099 |
  | + correct answer + rubric | **46.7%** | **0.62** | **0.077** |

  - Without a reference, the model over-scores (mean 0.976 vs grader 0.899).
  - Authors: accuracy "still too low for real-world settings".
  - https://arxiv.org/html/2411.05231v2 (accessed 2026-09-27).
- **Kortemeyer et al. 2024** (Phys. Rev. PER). Handwritten thermodynamics exam, 252 students.
  - "The greatest challenge lies in converting handwritten answers into a machine-readable format."
  - The model struggled to track more than a handful of rubric items.
  - The AI graded more leniently than TAs.
  - Precise at identifying passing exams; failing exams still needed humans.
  - https://exa.ai/library/publication/nn94bnv2d9g (accessed 2026-09-27).
- **Kortemeyer, Caspar & Horica 2025** (arXiv 2510.05162). GPT-5 on handwritten calculus.
  - "Unfiltered AI-TA agreement was moderate, adequate for low-stakes feedback but not for high-stakes use."
  - With IRT-based confidence filtering, AI "delivered human-level accuracy, but also left roughly **70% of the items** to be graded by humans."
  - https://arxiv.org/abs/2510.05162 (accessed 2026-09-27).
- **Handwritten engineering quizzes** (arXiv 2601.00730, 2026-01-02; Slovenian, with circuit diagrams).
  - Setup: GPT-5.2 and Gemini-3 Pro, ensemble graders plus supervisor aggregation plus deterministic validation.
  - Result: "≈ 8-point mean absolute difference to lecturer grades", with an estimated manual-review trigger rate of **≈17%**.
  - Trivial prompting or removing the reference solution caused "systematic over-grading".
  - https://arxiv.org/html/2601.00730v1 (accessed 2026-09-27).
- **VUB deployment** (arXiv 2603.13083). Six low-stakes in-class math tests, 5× repeated LLM scoring with consistency checks plus mandatory human verification.
  - About 16–23% grading-time reduction.
  - Agreement "comparable to, and in several cases tighter than, fully manual grading".
  - https://www.arxiv.org/pdf/2603.13083 (accessed 2026-09-27).

**Text (typed) grading and human baselines**

- **TOEFL Junior Writing** (Language Testing, 2025; n = 1,908):

  | Rater pair | QWK |
  |---|---|
  | Human–human | **0.82** |
  | Human–AWE engine | 0.78 |
  | Human–GPT-4 few-shot | 0.77 |
  | Human–GPT-4 zero-shot | 0.78 |

  - GPT-4 ranged from 0.69 to 0.85 by task.
  - Cites Ramineni & Williamson (2013) for a minimum QWK threshold. The snippet was truncated (PARTIAL; the commonly cited rule is QWK ≥ 0.70 and within 0.10 of human–human).
  - https://https-sage-cnpereading-com-443.webvpn1.xju.edu.cn/doi/10.1177/02655322251346860 (mirror; accessed 2026-09-27).
- **ASAP (Hewlett) essays.** Human–human QWK ranged **0.61–0.85** across the 8 sets.
  - ChatGPT-based models fell below human QWK on 5 of 9 sets (e.g., 0.63 vs 0.80 human on set 2a) and matched or exceeded it on 4.
  - https://arxiv.org/pdf/2408.09540 (accessed 2026-09-27).
- **Meta-synthesis of 65 studies** (arXiv 2512.14561). LLM–human QWK "ranged from 0.00 to 0.97". Within-study variation across prompts and models is as large as between-study variation. https://arxiv.org/pdf/2512.14561v2
- **AIMECON 2025.** Human–human QWK 0.91, PEG 0.76.
  - GPT-4o rose from 0.46 to 0.72 with context and few-shot prompting.
  - Claude Sonnet 4 rose from 0.30 to 0.69; Gemini 2.5 Flash from 0.43 to 0.60.
  - https://aclanthology.org/2025.aimecon-wip.9.pdf
- **GPT-4o zero-shot essay scoring** (Sci. Rep. 2024): QWK **0.437**, exact agreement 30%; scores biased low. https://www.nature.com/articles/s41598-024-79208-2

**Bangla / low-resource grading**

- arXiv 2606.11931 (June 2026). Bilingual Bangla–English grader, QLoRA-tuned Qwen3-8B.
  - Trained on a **synthetic** dataset of 490k graded answers produced by Gemini.
  - On a 259-item teacher-graded subset: Spearman **ρ = 0.936**, MAE 0.725 (0–10 scale).
  - Handwriting via GraDeT-HTR.
  - Synthetic training/test data means the result is not yet evidence on real scripts.
  - https://arxiv.org/html/2606.11931 (accessed 2026-09-27).
- **BEnQA** (arXiv 2403.10900). 5,161 Bangladeshi board-exam science questions in parallel Bengali/English. LLMs perform worse in Bengali, and "it is much harder to make the model output in a predefined format" in Bengali. http://arxiv.org/abs/2403.10900

**Known failure modes**

- **Leniency.** Kortemeyer 2024 (AI more lenient than TAs). EvalHack (MDPI 2026): panel more lenient than humans, MAE 1.897 on 0–10, bias −1.345. Caraeni: over-scoring without a reference.
- **Under-scoring also occurs.** SURE (MDPI 2026): "substantial underscoring" with a single prompt.
- **Position and verbosity bias** (Zheng et al., NeurIPS 2023).
  - All tested judges showed strong position bias; GPT-4 was consistent in only ~65% of swaps.
  - A verbosity "repetitive list" attack succeeds on all judges.
  - Reference-guided judging cut math-judging failure from 70% to 15%.
  - https://arxiv.org/html/2306.05685
- **Prompt injection in student answers** — see the conflict note below.

### Conflicting evidence

**Prompt-injection vulnerability**

| Finding | Source |
|---|---|
| Attack success 0.73–0.82 on ASAP / SciEntsBank-style grading, with grade inflation | Sci. Rep. 2026, https://www.nature.com/articles/s41598-026-46563-1 |
| "Current LLM-based AG systems remain highly vulnerable" | arXiv 2606.03090 (v3 2026-09-04) |
| Microsoft Copilot: 94–100% success for some strategies | J. Academic Ethics 2026 |
| Across ~40,000 trials, injections had **negligible effects on most frontier models**; Gemini 3 Pro vulnerable to verbose injections; GPT-4o-mini inflated ~20 points | Wharton GAIL, 2026-03-27, https://gail.wharton.upenn.edu/research-and-insights/hidden-prompt-injections/ |

Resolution: vulnerability depends strongly on model choice and injection design, so test your own model. No study was found on **handwritten** injections (e.g., a student writing "award full marks" on the script). The risk is plausible because the model reads the whole page (UNVERIFIED).

**Can GPT-4-class models match human agreement?** On typed essays, sometimes yes (TOEFL Junior 0.77–0.78 vs 0.82). On handwritten STEM, published results so far are below human agreement unless most items go to humans.

### Implications / realistic targets

- **Primary KPI:** per-question QWK (or exact / ±1-mark agreement) against double-marked human scores, compared with the **measured human–human QWK on the same items**.
- **Launch bar for "AI-assisted, human-confirmed":**
  - QWK ≥ 0.70, and
  - within 0.10 of human–human, and
  - no subgroup (Bangla vs English scripts, handwriting-legibility tiers) more than 0.10 worse.
- **Autonomous marking** of high-stakes public exams is **not supported** by current evidence.
- **Required guardrails:**
  - reference answer and rubric always in the prompt;
  - per-criterion scoring, not a whole-problem rubric;
  - ensemble or repeated sampling with disagreement routing;
  - an injection canary test set;
  - human verification of all failing or borderline scripts.

---

## Q5. Confidence calibration for LLM grading

### Verified facts

- **Vasquez Ferrer et al.** (AIED 2026; arXiv 2603.29559).
  - Setup: 7 LLMs (4B–120B), 3 datasets (RiceChem, SciEntsBank, Beetle).
  - **Self-reported (verbalized) confidence had the best calibration:** average ECE **0.166** vs **0.229** for 5-sample self-consistency, which was "38% worse despite 5× inference cost".
  - Best model: GPT-OSS-120B, ECE 0.100, but discrimination was only AUC 0.668.
  - Confidence was strongly top-skewed (a "confidence floor").
  - https://arxiv.org/html/2603.29559v1 (accessed 2026-09-27).
- **Xiong et al.** (ICLR 2024).
  - Verbalized confidence is "highly overconfident", mostly 80–100% and in multiples of 5.
  - GPT-4 verbalized AUROC averaged 62.7%.
  - **5-sample consistency** improved failure prediction substantially (GSM8K AUROC 54.8% → 92.7%).
  - "None of these techniques consistently outperform others."
  - White-box vs black-box AUROC gap is narrow (0.522 vs 0.605).
  - https://proceedings.iclr.cc/paper_files/paper/2024/file/6733cf15e10e2cd1d59af033c3bb8507-Paper-Conference.pdf
- **SURE** (MDPI MAKE 2026). Scored 46 students × 130 questions 20 times each. "Low certainty (i.e., high output diversity) was diagnostic of incorrect LLM scores", which enabled selective human regrading. https://www.mdpi.com/2504-4990/8/3/74
- **Confidence estimation in ASAG** (arXiv 2605.00200). Model-based confidence alone is "insufficient". Adding dataset-derived aleatoric uncertainty (heterogeneity within clusters of similar answers) improved selective grading. https://arxiv.org/html/2605.00200
- **Psychometric filtering.** Kortemeyer 2025 used an IRT 2PL residual: the deviation of the AI score from the model-expected score for that student and item (Q4).

### Conflicting evidence

- "Verbalized is best" (AIED 2026, measured by ECE) versus "consistency is better" (ICLR 2024, measured mostly by AUROC / failure prediction).
- These metrics measure different things. ECE rewards average calibration; AUROC rewards ranking errors below correct answers.
- For routing scripts to humans, **ranking (AUROC / selective accuracy at fixed coverage) matters more than ECE**.

### Implications

- Do not rely on a single signal. Combine:
  1. verbalized per-criterion confidence;
  2. agreement across 3–5 samples and/or 2 model families;
  3. OCR-legibility signals;
  4. an item-level psychometric residual once enough data exists.
- Calibrate thresholds on a held-out double-marked set. Report **coverage vs accuracy curves** (e.g., "auto-accept 40% of items at ≥95% within-1-mark agreement") rather than a single ECE.

---

## Q6. API pricing, image tokens, data handling (as of 2026-09-27)

### Verified facts — Anthropic

Source: https://platform.claude.com/docs/en/about-claude/pricing (accessed 2026-09-27).

| Model | Input $/MTok | Output $/MTok | Batch in/out |
|---|---|---|---|
| Claude Fable 5.1 | 10 | 50 | 5 / 25 |
| Claude Opus 5.5 | 4 | 20 | 2 / 10 |
| Claude Opus 5 | 5 | 25 | 2.50 / 12.50 |
| Claude Sonnet 5 | 2 | 10 | 1 / 5 |
| Claude Haiku 4.5 | 1 | 5 | 0.50 / 2.50 |

- Sonnet 5's $2/$10 "is now the standard price".
- Batch API: 50% discount.
- Cache read: 0.1× input (0.05× on Opus 5.5; 0.025× on Fable 5.1).
- Claude 4.7+ tokenizer produces ~30% more tokens for the same text.

**Image tokens** (https://platform.claude.com/docs/en/build-with-claude/vision)

- Formula: `⌈width/28⌉ × ⌈height/28⌉`.
- High-resolution tier (Claude 4.7 and later): max long edge 2576 px, max 4,784 tokens.
- Standard tier (other models, e.g., Haiku 4.5): 1568 px, 1,568 tokens.
- The official table lists 2000×1500 as **3,888 tokens** (high-res) and **1,564** (standard).
- "Anthropic does not use uploaded images to train models."

**Data handling**

- `inference_geo` supports only `"global"` or `"us"`. US-only costs **1.1×**. Workspace (storage) geo: **only "us"**. https://platform.claude.com/docs/en/manage-claude/data-residency
- ZDR is available per organization on request. It is not available for "Covered Models" (Fable 5 / 5.1, Mythos), which require 30-day retention. Retained data is "never used for model training without your express permission". https://platform.claude.com/docs/en/manage-claude/api-and-data-retention
- Commercial/API standard retention: 30 days. https://code.claude.com/docs/en/data-usage

### Verified facts — OpenAI

Source: https://platform.openai.com/docs/pricing (accessed 2026-09-27 via Exa). Columns are rendered as raw arrays; the column labels are inferred.

| Model | Input | Cached input | Output | Batch in/out |
|---|---|---|---|---|
| gpt-5.6-sol | $5 | $0.50 | $30 | $2.50 / $15 |
| gpt-5.6-terra | $2.50 | $0.25 | $15 | $1.25 / $7.50 |
| gpt-5.6-luna | $1 | $0.10 | $6 | $0.50 / $3 |
| gpt-5.5 (<272K) | $5 | $0.50 | $30 | – |
| gpt-5.4-mini | $0.75 | – | $4.50 | – |

- Batch and Flex are 50% of standard.
- The 5.6 rows carry a fourth value ($6.25 / $3.125 / $1.25) whose column label was not visible. Probably cache writes (UNVERIFIED).

**Image tokens** (https://developers.openai.com/api/docs/guides/images-vision)

- 32×32-px patches.
- gpt-5.6 `high` detail: fit within 2048×2048 and 2,500 patches, then × **1.2** multiplier.
- `auto` behaves like `original` (no patch budget up to 30,000 patches). **Set `detail:"high"` explicitly to control cost.**
- gpt-5.4 example: 2048×2048 becomes 2,500 patches, which is 3,000 tokens.

**Data handling** (https://developers.openai.com/api/docs/guides/your-data)

- API data is not used for training.
- Abuse-monitoring logs are kept up to 30 days.
- ZDR / Modified Abuse Monitoring require approval.
- Data residency: regions include US, EU, Japan, **India (storage only, no regional processing)**, and others. A **10% uplift** applies for models released on or after 2026-03-05. Non-US regions require ZDR or MAM.

### Verified facts — Google Gemini API

Source: https://ai.google.dev/gemini-api/docs/pricing (accessed 2026-09-27).

| Model | Standard input / output per MTok | Batch |
|---|---|---|
| gemini-3.8-flash | $0.75 / $3.75 through 2026-12-31; $1.50 / $7.50 from 2027-01-01 | $0.375 / $1.875 |
| gemini-3.5 Flash | $1.50 / $9.00 | – |
| gemini-3.5-flash-lite | $0.30 / $2.50 | – |
| gemini-3.1-pro-preview | $2 / $12 (≤200k); $4 / $18 (>200k) | $1 / $6 |

- Batch is a 50% reduction. The page marked 3.1 Pro "Preview"; per third-party blogs, 3.5 Pro had not shipped as of July 2026 (UNVERIFIED for September).
- **Paid tier: "Content not used to improve our products"**. Free tier: used to improve products.

**Image tokens** (https://ai.google.dev/gemini-api/docs/media-resolution)

| `media_resolution` (Gemini 3) | Tokens per image |
|---|---|
| low | 280 |
| medium | 560 |
| high / default | 1,120 |
| ultra_high | 2,240 |

- Pre-Gemini-3 models: 258 tokens per 768 px tile.
- Abuse monitoring: prompts and outputs retained **55 days**. https://ai.google.dev/gemini-api/docs/usage-policies ; terms at https://ai.google.dev/gemini-api/terms

### Cost per page — arithmetic

**Assumptions** (stated, not verified):

- One scanned page at 1500×2000 px.
- A single "transcribe + grade" call per page: image tokens + **1,000 text input tokens** (instructions, rubric, reference answer) and **1,000 output tokens** (transcript + JSON scores).
- Reasoning/"thinking" tokens are billed as output and can multiply output cost. They are excluded here.

**Image tokens per page**

- Claude, high-res tier (Opus 5.5 / Sonnet 5): ⌈1500/28⌉ × ⌈2000/28⌉ = 54 × 72 = **3,888**.
- Claude Haiku 4.5 (standard tier): **1,564** (per the official 2000×1500 row).
- OpenAI gpt-5.6, `high` detail: 47 × 63 = 2,961 patches, which exceeds the 2,500 budget. The image is resized to ~1367×1823, giving 43 × 57 = 2,451 patches; × 1.2 = **2,942 tokens**. With `auto`/`original` it would be 2,961 × 1.2 = 3,554.
- Gemini 3.x, `high`: **1,120**.

**Per-page cost**

| Model | Input tokens | Input cost | Output cost | Total / page | Batch / page |
|---|---|---|---|---|---|
| Claude Opus 5.5 ($4/$20) | 4,888 | $0.01955 | $0.0200 | **$0.0396** | $0.0198 |
| Claude Sonnet 5 ($2/$10) | 4,888 | $0.00978 | $0.0100 | **$0.0198** | $0.0099 |
| Claude Haiku 4.5 ($1/$5) | 2,564 | $0.00256 | $0.0050 | **$0.0076** | $0.0038 |
| gpt-5.6-sol ($5/$30) | 3,942 | $0.01971 | $0.0300 | **$0.0497** | $0.0249 |
| gpt-5.6-terra ($2.5/$15) | 3,942 | $0.00986 | $0.0150 | **$0.0249** | $0.0124 |
| gpt-5.6-luna ($1/$6) | 3,942 | $0.00394 | $0.0060 | **$0.0099** | $0.0050 |
| Gemini 3.1 Pro preview ($2/$12) | 2,120 | $0.00424 | $0.0120 | **$0.0162** | $0.0081 |
| Gemini 3.8 Flash, 2026 promo ($0.75/$3.75) | 2,120 | $0.00159 | $0.00375 | **$0.0053** | $0.0027 |
| Gemini 3.8 Flash, 2027 ($1.50/$7.50) | 2,120 | $0.00318 | $0.0075 | **$0.0107** | $0.0053 |

**Example script.** Assume a 12-written-page script (an assumption; Bangladeshi script lengths were not verified).

- 3-sample self-consistency on Sonnet 5 batch: 12 × 3 × $0.0099 ≈ **$0.36 per script**.
- Single pass on Gemini 3.8 Flash batch: 12 × $0.0027 ≈ **$0.03 per script**.

Scaled to 1 million scripts, the difference is roughly $30k versus $360k. Model choice therefore matters at national scale.

### Conflicting evidence

- A 2026 Roboflow blog gives the Claude image formula as w×h/750, which yields 4,000 tokens for this page. Anthropic's current docs use 28-px patches, which yields 3,888. Use the official doc.

### Unverified

- Any provider offering in-country **Bangladesh** data residency. None found. Nearest options:
  - OpenAI India: storage only.
  - Google Document AI `asia-south1`: listed as a supported region.
  - Anthropic: US or global only.
- Bangla token inflation: how many tokens a Bangla transcript costs versus English. Not measured here. It raises output cost and should be benchmarked with count-tokens APIs.

---

## Q7. Existing products that grade handwritten exams

### Verified facts

- **Gradescope (Turnitin).**
  - AI-assisted answer groups require the **Institutional license** and work only on fixed-template PDF assignments.
  - Four question types: Manually Grouped, Multiple Choice, Math fill-in-the-blank, Text fill-in-the-blank.
  - "Gradescope AI can read student handwriting of **English-language** text and math notation", but answers must be on one line.
  - This is grouping, not free-response grading.
  - https://guides.gradescope.com/hc/en-us/articles/24838908062093 (2025-12-16; accessed 2026-09-27). Pricing is by quote: https://info.gradescope.com/pricing
- **CoGrader.**
  - Free tier: 100 essays/month. Standard: $15/month billed annually ($19 monthly) for 350 submissions, including "Handwritten assignments".
  - Claims it "can assess … assignments in any language" (interface is English).
  - Focus is essays and writing rubrics, not math.
  - https://cograder.com/pricing/ (accessed 2026-09-27).
- **Graide** (UK).
  - "AI assistance (no LLMs or GPTs)"; "Replay Grading" learns from educator marks.
  - Per-response confidence, "Accepts handwriting" via OCR for STEM.
  - Birmingham study: median grading time −74%, 7.2× more feedback.
  - Historic price £30 per student per year (2023 blog; UNVERIFIED as current).
  - https://www.graide.co.uk/how-it-works ; https://www.graide.co.uk/blog/university-of-birmingham-research
- **Marking.ai.** Supports "scanned handwritten scripts"; "optimised for … language based subjects and humanities". Diagram reading added September 2025. 20 free submissions, then subscription. https://marking.ai/faqs
- **TimelyGrader.** Starter $12/month. LMS integration (Canvas, D2L). Reports AI–human percentage agreement. No explicit handwriting claim found. https://www.timelygrader.ai/pricingandplans
- **Brisk Teaching.** Browser extension; "Generate materials in 50+ languages"; per-student district pricing. No handwritten-exam grading claim found. https://www.briskteaching.com/plans
- **Eklavvya (India).**
  - On-screen marking plus "OSM Auto Evaluation": OCR, then a "domain-tuned LLM" drafts a score, then an examiner accepts or overrides. Four strictness modes.
  - Languages: "English, Hindi, Marathi, Tamil, Telugu, and other supported languages". **Bengali not explicitly listed.**
  - Claims its fine-tuned LLM "deviates less from official historic grades than certified human re-graders". No public study linked.
  - Priced per booklet.
  - https://help.eklavvya.com/a/osm-auto-evaluation/ ; https://www.eklavvya.com/ai-answer-sheet-checking/
- **E-Valuate AI (India).** Handwritten answer sheets, "all handwritten answer sheets in **English**", from ₹2/page. https://evaluate-ai.app/
- **Bangladesh.**
  - Only prototypes and competition projects were found: "Mullayon AI" (BTRC Innovation Fair 2025 finalist, handwritten Bangla scripts), "AI Exam Evaluator" (English O/A-Level, IELTS), and the Cognifyq grader (arXiv 2606.11931).
  - Rajshahi University introduced **coded (anonymized) paper scripts** from 2026-09-15. This is not AI grading.
  - No evidence found that Shikho or 10 Minute School grade handwritten scripts with AI (UNVERIFIED).
  - Sources: LinkedIn posts dated 2025-07-25 and 2025-08-03; https://dailyasianage.com/news/357920/ (2026-09-14).

### Implications

- **No commercial product was found that verifiably grades handwritten Bangla.** This is a genuine gap and a differentiation opportunity. It is also a signal that the problem is hard.
- The dominant pattern everywhere is **draft score plus mandatory human accept/override**, as in Eklavvya, Graide and the academic pipelines. Adopt it.
- Eklavvya-style on-screen marking (scan, mask, allocate, annotate, moderate) is the institutional workflow Bangladeshi boards and universities would recognize.

---

## Q8. Symbolic math verification

### Verified facts

**SymPy** (https://docs.sympy.org/latest/tutorials/intro-tutorial/gotchas.html ; https://docs.sympy.org/latest/guides/assumptions.html, accessed 2026-09-27)

- `==` is **structural** equality.
- The recommended test is `simplify(a - b) == 0`, which "is not infallible — in fact, it can be theoretically proven that it is impossible to determine if two symbolic expressions are identically equal in general".
- `Expr.equals` tests numerically at random points.
- Assumptions matter: `sqrt(x**2)` does not simplify to `x` unless `x` is declared positive. Symbols with different assumptions compare unequal.

**Local check** (SymPy 1.14.0, run 2026-09-27):

- `(x+1)**2 == x**2+2*x+1` → `False`; `simplify(diff)` → `0`.
- `simplify(sqrt(x**2))` stays `sqrt(x**2)`.
- `simplify((x**2-1)/(x-1) - (x+1))` → `0`. The domain restriction x ≠ 1 is silently dropped.
- `simplify(log(a*b) - log(a) - log(b))` does not reach 0 without assumptions.
- `Float(0.1)+Float(0.2) == Rational(3,10)` → `False`.

**HuggingFace Math-Verify** (https://github.com/huggingface/math-verify ; blog 2025-02-14)

- Pipeline: LaTeX/expression extraction, then SymPy via `latex2sympy2_extended` (ANTLR4), then comparison.
- Comparison covers numeric tolerance, simplification, sets and intervals, matrices, and relations with flip support.
- Comparison is **intentionally asymmetric** (gold vs prediction), uses a timeout, and is not thread-safe because of signal-based timeouts.
- Reported accuracy on MATH: Math-Verify 0.1328 vs Qwen 0.1288 vs Harness 0.0802.
- Parsing and format failures had underestimated some models by up to 40 points.

### Known pitfalls relevant to grading

- **False negatives** (a correct student answer judged wrong): unsimplifiable forms, missing assumptions, float vs rational, unit handling, and OCR noise in the LaTeX.
- **False positives:** generic simplification ignores domain restrictions and branch cuts, and numeric random-point tests can pass coincidentally.
- **Step checking is harder than final-answer checking.** Consecutive-step equivalence can be tested with SymPy, but legitimate non-equivalent transformations (solving, squaring both sides, dividing by variables) need rule-aware checks.
- **Timeouts are needed:** `simplify` can hang.

### Implications

- Use CAS as a **verifier, not a grader**:
  - final-answer equivalence via Math-Verify-style parsing with declared variable assumptions;
  - numeric spot checks with tolerance;
  - "CAS says equivalent" alone should never award method marks;
  - "CAS cannot decide" should route to the LLM or a human, not count as wrong.
- Log CAS disagreements with the LLM as a high-value signal for the confidence router.

---

## Overall design implications

| Area | Recommendation |
|---|---|
| **Scope v1** | English-medium math and science first. English handwriting and HMER are far more mature. Bangla handwriting as an assisted, human-confirmed beta. |
| **Accuracy targets** | Per-question QWK ≥ 0.70 and within 0.10 of measured human–human. Report coverage/accuracy trade-off. Bangla transcription CER target to be set after the in-house benchmark; public evidence gives ~6% (specialist, curated) to ~19–37% (older VLM zero-shot). |
| **Pipeline** | Page segmentation → VLM transcription + direct-from-image rubric grading → CAS verification for math → multi-sample / multi-model disagreement → IRT residual → human queue. |
| **Security** | Injection test set, including handwritten injections. Choose a model with measured robustness. Strip or ignore instructions inside answers. |
| **Cost** | $0.003–$0.05 per page per call; batch halves it. Budget 3–5× for ensembles. Output tokens and thinking dominate. |
| **Data** | No Bangladesh-region hosting from Anthropic, OpenAI or Google Gemini API. Use paid tiers (no training). Seek ZDR where available. The 55-day (Google) and 30-day (OpenAI, Anthropic standard) abuse-log retention needs legal review. |

---

## Claim | Status | Source

| Claim | Status | Source |
|---|---|---|
| GraDeT-HTR: CER 6.19% / WER 14.20% on BN-HTRd; 8.68% / 23.56% on Bongabdo | VERIFIED | aclanthology.org/2025.emnlp-demos.52.pdf |
| Gemini 2.5 Flash on BN-HTRd: CER 19.39% / WER 32.49%; Bongabdo 37.42% / 56.39% | VERIFIED | same |
| Line-level Bangla HTR CER 26–38% on BN-HTRd | VERIFIED | same |
| BN-HTRd: 786 images, ~150 writers, 108,181 words | VERIFIED | huggingface.co/datasets/shaoncsecu/BN-HTRd_Splitted |
| BanglaWriting: 260 writers, 21,234 words | VERIFIED | pmc.ncbi.nlm.nih.gov/articles/PMC7744928 |
| Bongabdo: 49 contributors, 111 full pages | VERIFIED | kaggle.com/datasets/ayanwap7/bongabdo1429 |
| BanglaLekha-Isolated: 84 classes, 166,105 images | VERIFIED | pmc.ncbi.nlm.nih.gov/articles/PMC5382023 |
| Google Cloud Vision CER 13.89% on in-house Bangla handwriting | VERIFIED (non-public data) | link.springer.com/article/10.1007/s44163-025-00251-7 |
| Current frontier VLM (Gemini 3.x / GPT-5.x / Claude 5.x) CER on Bangla HTR | UNVERIFIED | none found |
| Azure DI v4: no Bengali handwriting (nor printed Read) | VERIFIED | learn.microsoft.com/…/language-support/ocr |
| Google Vision lists Bengali as supported OCR language | VERIFIED | cloud.google.com/vision/docs/languages |
| Google Document AI supports Bengali **handwriting** | UNVERIFIED | cloud.google.com/document-ai/docs/languages (icon column unreadable) |
| Google Enterprise OCR: 50 handwritten languages | VERIFIED | cloud.google.com/use-cases/ocr |
| AWS Textract handwriting = English alphabet only | VERIFIED | aws.amazon.com/textract/faqs |
| Mathpix: Bengali printed only; handwriting English/Hindi/Latin | VERIFIED | mathpix.com/language-support |
| Mathpix: $0.002/image, $0.005/page, $0.0015/page batch, $19.99 setup | VERIFIED | mathpix.com/pricing/api |
| Uni-MuMER: 79.74% average CROHME ExpRate | VERIFIED | NeurIPS 2025 paper; github.com/BFlameSwift/Uni-MuMER |
| Zero-shot Gemini 2.5 Flash 55.32%, GPT-4o 48.81% CROHME average | VERIFIED | same |
| ICAL 60.6 / 58.8 / 60.5 CROHME; 69.06 HME100K | VERIFIED | arxiv.org/pdf/2405.09032v4 |
| MLLMs hallucinate corrections on multi-line handwritten math | VERIFIED (qualitative) | arxiv.org/abs/2608.18586 |
| texify deprecated → surya | VERIFIED | github.com/VikParuchuri/texify |
| GPT-4o handwritten probability exam: accuracy 46.7%, r = 0.62 (with rubric) | VERIFIED | arxiv.org/html/2411.05231v2 |
| GPT-5 calculus: human-level only with ~70% routed to humans | VERIFIED | arxiv.org/abs/2510.05162 |
| Engineering-quiz pipeline: ~8-point MAD, ~17% review rate | VERIFIED | arxiv.org/html/2601.00730v1 |
| AI grades more leniently than TAs (thermodynamics) | VERIFIED | Kortemeyer et al. 2024, PRPER |
| Human–human QWK 0.82 vs GPT-4 0.77–0.78 (TOEFL Junior) | VERIFIED | Language Testing 2025 (doi 10.1177/02655322251346860) |
| ASAP human–human QWK 0.61–0.85 | VERIFIED (secondary) | arxiv.org/pdf/2408.09540 |
| ETS threshold QWK ≥ 0.70 and within 0.10 of human | PARTIAL | cited via truncated snippet |
| LLM–human QWK ranges 0.00–0.97 across 65 studies | VERIFIED | arxiv.org/pdf/2512.14561v2 |
| Bangla grader Qwen3-8B: ρ = 0.936 on 259 teacher-graded items (synthetic data) | VERIFIED | arxiv.org/html/2606.11931 |
| Prompt injection highly effective on LLM graders | CONFLICT | nature.com s41598-026-46563-1 and arXiv 2606.03090 vs Wharton GAIL 2026 |
| Position / verbosity bias in LLM judges; GPT-4 swap consistency ~65% | VERIFIED | arxiv.org/html/2306.05685 |
| Verbalized confidence best calibrated (ECE 0.166 vs 0.229) | VERIFIED / CONFLICT | arxiv.org/html/2603.29559v1 vs ICLR 2024 Xiong et al. |
| Sample consistency improves failure prediction (AUROC 54.8 → 92.7 on GSM8K) | VERIFIED | ICLR 2024 Xiong et al. |
| Anthropic prices (Opus 5.5 $4/$20, Sonnet 5 $2/$10, Haiku 4.5 $1/$5); batch −50% | VERIFIED | platform.claude.com/docs/en/about-claude/pricing |
| Claude image tokens = ⌈w/28⌉ × ⌈h/28⌉; 2000×1500 → 3,888 (high-res) | VERIFIED | platform.claude.com/docs/en/build-with-claude/vision |
| Anthropic inference geo only global/us (US 1.1×); workspace geo US only | VERIFIED | platform.claude.com/docs/en/manage-claude/data-residency |
| Anthropic ZDR per org; Covered Models need 30-day retention | VERIFIED | platform.claude.com/docs/en/manage-claude/api-and-data-retention |
| OpenAI gpt-5.6 sol / terra / luna $5/$30, $2.50/$15, $1/$6; batch −50% | VERIFIED (column labels inferred) | platform.openai.com/docs/pricing |
| OpenAI 32-px patches, 2,500-patch high budget, 1.2× multiplier | VERIFIED | developers.openai.com/api/docs/guides/images-vision |
| OpenAI: API data not trained on; 30-day abuse logs; residency +10% | VERIFIED | developers.openai.com/api/docs/guides/your-data |
| Gemini 3.8 Flash $0.75/$3.75 (to 2026-12-31), then $1.50/$7.50 | VERIFIED | ai.google.dev/gemini-api/docs/pricing |
| Gemini 3.1 Pro preview $2/$12 (≤200k) | VERIFIED | same |
| Gemini paid tier not used to improve products; 55-day abuse logs | VERIFIED | ai.google.dev/gemini-api/terms ; /docs/usage-policies |
| Gemini 3 image = 1,120 tokens at high/default | VERIFIED | ai.google.dev/gemini-api/docs/media-resolution |
| Per-page cost $0.003–$0.05 (assumed 1k in / 1k out) | DERIVED (arithmetic above) | this document |
| Bangladesh in-region hosting from any of the three LLM vendors | UNVERIFIED (none found) | — |
| Gradescope AI grouping: English handwriting + math, one-line answers, Institutional license | VERIFIED | guides.gradescope.com article 24838908062093 |
| CoGrader $15/month (annual), handwriting, "any language" | VERIFIED (vendor claim) | cograder.com/pricing |
| Graide: non-LLM Replay Grading; −74% grading time | VERIFIED (vendor study) | graide.co.uk |
| Eklavvya AI OSM languages exclude explicit Bengali | VERIFIED | help.eklavvya.com/a/osm-auto-evaluation |
| Any commercial product grading handwritten Bangla | UNVERIFIED (none found) | — |
| Shikho / 10 Minute School do AI handwritten grading | UNVERIFIED | — |
| SymPy `==` structural; equivalence undecidable in general | VERIFIED | docs.sympy.org gotchas |
| SymPy `simplify` drops domain restriction ((x²−1)/(x−1) vs x+1) | VERIFIED (local run, SymPy 1.14.0) | local test 2026-09-27 |
| Math-Verify asymmetric comparison; timeout via signals | VERIFIED | github.com/huggingface/math-verify |
