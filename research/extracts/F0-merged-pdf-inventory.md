# F0 — merged.pdf Inventory

**Source:** Google Drive `merged.pdf`, file ID `1pn152ME19dwh55_zzszPULP4M0t-RL8S`. It is 5,698,172 bytes, 569 pages, PDF 1.7, created 2026-09-27 and stored in Drive folder `19NlDgGbMkDcLNastEtomrvGvcuyiQ9Jz`.
**Prepared:** 2026-09-27
**Bottom line:** merged.pdf holds **13 documents**. They are K1–K13 in a different order, and each one is text-identical to its standalone PDF. **K14 is not inside merged.pdf.** No NEW documents were found, so no F1+ extracts were written.

---

## 1. How the file was read (and where the Drive text reader stops)

- **The Drive `read_file_content` result is truncated.** It returned about 152,600 characters, or 3,001 lines of text. It covers:
  - all of K8 (HITL)
  - all of K2 (Workflow)
  - only the **title and Executive Summary of K12 (Business Model)**, which ends at "...an operational gross margin of 64% to 85%, depending..."

  After that come only the hyperlink URLs from the reference lists. The last URL is `https://www.youtube.com/watch?v=UYlUAVnqmKY`. So the Drive text reader covers only about pages 1–80 of 569 (**about 14% of the file**). Anyone who relied on that reader missed K12's body and every document after it.
- **Full extraction used a different route.** The raw PDF was downloaded (`download_file_content`, base64) and the text of **all 569 pages** was extracted locally with pypdfium2, about 782,000 characters. Document boundaries were found from the title pages.
- **Check against the standalone PDFs.** Each segment was compared with its standalone PDF in the Drive research folder `116e3lzhV_3EyMYeT9O9ha95dIcPM3cIg`. After whitespace normalisation, **all 13 segments have byte-identical extracted text**.
- **Blank-looking pages are not missing content.** Pages 37, 79, 112–113, 153–154, 217, 260, 306–307, 352–353, 393–395, 428, 494–495, 538–539 and 569 have no text layer. They are the tail of each document's source list (link icons and "Opens in a new window" markers only) or empty trailing pages. No images exist anywhere in the PDF: 0 image objects.

## 2. Inventory (in order of appearance)

| # | Pages (of 569) | Title as printed on title page | Maps to | Body words (approx.) | Source list begins approx. | Notes |
|---|---|---|---|---|---|---|
| 1 | 1–37 | Architecture and Governance of Human-in-the-Loop AI Assessment Systems: A Framework for High-Stakes and Formative Educational Evaluation | **K8** | 5,000 | p.33 | Identical to standalone PDF (37 pp). |
| 2 | 38–79 | BANGLADESH SCHOOL AND COLLEGE EXAMINATION WORKFLOW: END-TO-END OPERATIONAL WORKFLOW RESEARCH AND PROCESS-MAPPING STUDY | **K2** | 9,700 | p.76 | Identical (42 pp). Title in all caps; sections numbered "SECTION 01…21". |
| 3 | 80–113 | Business Model Architecture, Pricing Strategy, and Unit Economics Blueprint for an AI-Powered Assessment Platform | **K12** | 6,500 | p.107 | Identical (34 pp). The Drive text reader stops inside this document's Executive Summary. |
| 4 | 114–154 | Comprehensive Data Strategy and Governance Framework for AI-Powered Educational Assessment Platforms in Bangladesh and International Jurisdictions | **K9** | 7,300 | p.149 | Identical (41 pp). |
| 5 | 155–217 | Comprehensive Evaluation Framework for AI-Powered Examination Assessment: Accuracy Definitions, Psychometric Metrics, End-to-End Pipeline Decomposition, and System Governance | **K7** | 7,200 | p.214 | Identical (63 pp). Many pages are broken-up math formula fragments (pp.164–200) because equations were rendered as separate glyph runs. |
| 6 | 218–261 | Comprehensive Product Architecture and Strategy Report: AI-Powered Examination Assessment and Academic Intelligence Platform | **K10** | 7,700 | p.258 | Text identical to the standalone "(1).pdf" (43 pp). merged.pdf has **44 pp**: the extra page 261 is blank. [Analyst note] Page 261 is most likely the 1-page blank export `…Platform.pdf` (9 KB, file ID `1SKVMzQaeIULAimlaHRfr4yuH41bMXrST`) that sits beside the real file in the research folder. It is harmless. |
| 7 | 262–307 | Comprehensive Technology Feasibility Research Report: AI-Powered Examination Assessment and Answer-Script Evaluation Platform for Educational Institutions in Bangladesh | **K4** | 6,800 | p.302 | Identical (46 pp). Organised as "Deliverable 01…". |
| 8 | 308–353 | Go-To-Market Strategy Research Report: AI-Powered Examination Assessment Platform | **K13** | 7,500 | p.347 | Identical (46 pp). |
| 9 | 354–395 | Strategic Competitive Intelligence & Opportunity Blueprint: AI-Powered Assessment Platform for Bangladesh & Global EdTech | **K11** | 8,000 | p.386 | Identical (42 pp). The line "Bangla Handwriting Recognition — বাংলা হাতের লেখা OCR" on p.387 is a **reference-list entry** (banglaocr.com), not a separate document. |
| 10 | 396–428 | Systemic Examination Assessment Infrastructure and Operational Problem Discovery Report: Evaluating Evaluation Lifecycles, Institutional Workflows, and Market Readiness in Bangladesh | **K1** | 6,800 | p.424 | Identical (33 pp). |
| 11 | 429–495 | Technical Feasibility and System Risk Analysis: Automated AI-Powered Examination Assessment Platform | **K6** | 10,100 | p.490 | Identical (67 pp). This is the longest document, with sections numbered up to 40. |
| 12 | 496–539 | Technical Research Report: System Architecture and AI Model Selection for Automated Examination Assessment in Bangladesh | **K5** | 7,500 | p.534 | Identical (44 pp). |
| 13 | 540–569 | The Assessment and Examination Ecosystem in Bangladesh Education: Comprehensive Customer Discovery and User Research Report | **K3** | 6,900 | p.567 | Identical (30 pp). "Comprehensive Master Research Synthesis" (p.557) and "Concluding Executive Summary and Strategic Recommendations" (p.565) are **internal sections of K3**, not separate documents. |

**Totals:** 13 documents, 569 pages, about 97,800 words including reference lists.

## 3. Mapping summary

| Known doc | Present in merged.pdf? | Pages |
|---|---|---|
| K1 Systemic Examination Assessment Infrastructure… | Yes | 396–428 |
| K2 Bangladesh School and College Examination Workflow… | Yes | 38–79 |
| K3 The Assessment and Examination Ecosystem… | Yes | 540–569 |
| K4 Comprehensive Technology Feasibility Research Report | Yes | 262–307 |
| K5 Technical Research Report: System Architecture and AI Model Selection | Yes | 496–539 |
| K6 Technical Feasibility and System Risk Analysis | Yes | 429–495 |
| K7 Comprehensive Evaluation Framework… | Yes | 155–217 |
| K8 Architecture and Governance of HITL AI Assessment Systems | Yes | 1–37 |
| K9 Comprehensive Data Strategy and Governance Framework | Yes | 114–154 |
| K10 Comprehensive Product Architecture and Strategy Report | Yes | 218–261 (p.261 blank) |
| K11 Strategic Competitive Intelligence & Opportunity Blueprint | Yes | 354–395 |
| K12 Business Model Architecture, Pricing Strategy, and Unit Economics Blueprint | Yes | 80–113 |
| K13 Go-To-Market Strategy Research Report | Yes | 308–353 |
| **K14** The Problem Space of Academic Operations and Assessment in Bangladesh | **No** | Not in merged.pdf. It is a separate Drive PDF, "The Problem Space of Academic Operations and Assessment in Bangladesh_ A B2B EdTech Problem Discovery and Validation Report.pdf" (ID `1MMF-DKxQk-282NC4W5Kyu92IWzromGb4`, created 2026-09-05, different folder). |

## 4. NEW documents

**None.** No standalone curriculum, Bangla/BLM language, OCR/handwriting, mathematics evaluation, assessment methodology, UX/design or market-sizing report appears in merged.pdf.

[Analyst note] Those topics are covered only as **sections inside the known documents**:
- Bangla handwriting recognition, including Juktakkhor/Kar diacritics and Matra-line segmentation, is covered in K4 (pp.~268–300), K5 (pp.~497–506) and K6 (§11 "Handwritten Mathematics & Symbolic Reasoning Risks", p.453; transcription-error analysis, p.448).
- Mathematics and CAS evaluation is in K5 (p.511) and K6 (pp.453–454).
- Psychometrics and metrics are in K7.
- The NCTB Creative Question (CQ) rubric appears in K8 (p.27), K10 (p.247) and K11 (p.355).
- UX friction is K11 §19 (p.375).

Extractors of K4–K8, K10 and K11 should cover these sections.

## 5. Differences between merged.pdf versions and their standalone versions

- **No material differences.** The extracted text of all 13 segments matches the standalone PDFs in Drive folder `116e3lzhV_3EyMYeT9O9ha95dIcPM3cIg`. There are no extra or missing sections.
- **The only structural difference** is one extra blank page (p.261) after K10.
- **Not checked:** the same folder also holds a native Google Docs version of each of the 13 reports. I did not compare those Google Docs with the PDFs. [Analyst note] If other agents extracted from the Google Docs versions, small differences are possible but were not checked. The PDFs were exported at the same times as the Docs (16:46–17:41 on 2026-09-26 and 04:51–04:53 on 2026-09-27).

## 6. Out-of-scope observation

[Analyst note] The same Drive also contains other research sets that are **not** part of merged.pdf and not about exam-script assessment:
- a School & College **ERP** research series (about 12 PDFs, folder `1iP2QJ0chrLDVHgOkpm1MoCUpzyFBccWl`), including an "Enterprise UX Strategy…" report and a "Comprehensive Problem-Discovery Study…"
- a "NIMIKH" company-strategy series (folder `1BSbC7Ew_-KHHGgVoFCKrZbxDCCv927au`)

They were not extracted. They may be relevant if the product will integrate with or sit beside an ERP.
