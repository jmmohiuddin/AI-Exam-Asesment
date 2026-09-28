/** Assessment endpoints (/v1/exams, /v1/scripts, /v1/item-results). */

import { apiFetch } from "./client";

export type ExamState =
  | "draft"
  | "rubric_locked"
  | "capturing"
  | "processing"
  | "reviewing"
  | "moderation"
  | "marks_locked"
  | "published"
  | "recheck";

export type ItemState =
  | "pending"
  | "unmapped"
  | "processing"
  | "failed"
  | "manual_ready"
  | "evidence_only"
  | "suggested"
  | "confirmed"
  | "edited"
  | "flagged"
  | "moderated"
  | "locked"
  | "recheck";

/** Marks arrive as decimal strings so they never pass through a binary float. */
export type MarkString = string;

export interface Exam {
  id: string;
  name: string;
  subject_code: string;
  class_level: number;
  state: ExamState;
  total_marks: MarkString;
  rubric_locked_at: string | null;
  marks_locked_at: string | null;
}

export interface Script {
  id: string;
  exam_id: string;
  candidate_id: string;
  total_marks: MarkString | null;
}

export interface Candidate {
  id: string;
  roll: string;
  name: string;
}

export type CriterionDecisionValue =
  "met" | "partly" | "not_met" | "cannot_determine";

export interface CriterionDecision {
  criterion_id: string;
  decision: CriterionDecisionValue;
  marks?: MarkString | null;
  ecf_consistent?: boolean;
}

export interface RubricCriterion {
  id: string;
  text_bn: string;
  text_en: string;
  marks: MarkString;
  type: string;
  evidence_expectation: string;
}

export interface RubricPayload {
  item_id: string;
  version: number;
  model_answer: string | null;
  criteria: RubricCriterion[];
  half_marks_allowed: boolean;
}

export interface CriterionScore {
  criterion_id: string;
  decision: CriterionDecisionValue;
  max_marks: MarkString;
  awarded: MarkString;
  ecf_credit: boolean;
}

export interface ItemScore {
  item_id: string;
  item_max: MarkString;
  criteria: CriterionScore[];
  computed_total: MarkString;
  total: MarkString;
  needs_teacher: boolean;
}

export interface ReviewCard {
  result_id: string;
  item_id: string;
  item_no: number;
  prompt_bn: string;
  prompt_en: string;
  max_marks: MarkString;
  state: ItemState;
  student_answer: string;
  model_answer: string | null;
  rubric: RubricPayload | Record<string, never>;
  rubric_version: number | null;
  ai_model: string | null;
  ai_confidence: MarkString | null;
  ai_low_confidence: boolean;
  ai_rationale: string | null;
  ai_evidence: string[];
  ai_decisions: CriterionDecision[];
  suggested_score: ItemScore | null;
  teacher_score: ItemScore | null;
  total: MarkString | null;
  decided_at: string | null;
}

export interface ReviewQueue {
  script_id: string;
  candidate: Candidate;
  exam_state: ExamState;
  script_total: MarkString | null;
  items: ReviewCard[];
}

export interface ReviewDecisionBody {
  decisions: CriterionDecision[];
  deductions_applied?: string[];
  total_override?: { total: MarkString; reason: string } | null;
  accepted_ai: boolean;
}

export function listExams(): Promise<Exam[]> {
  return apiFetch<Exam[]>("/exams");
}

export function getExam(examId: string): Promise<Exam> {
  return apiFetch<Exam>(`/exams/${examId}`);
}

export function listScripts(examId: string): Promise<Script[]> {
  return apiFetch<Script[]>(`/exams/${examId}/scripts`);
}

export function getReviewQueue(scriptId: string): Promise<ReviewQueue> {
  return apiFetch<ReviewQueue>(`/scripts/${scriptId}/review`);
}

export function evaluateScript(scriptId: string): Promise<unknown> {
  return apiFetch(`/scripts/${scriptId}/evaluate`, { method: "POST" });
}

export function decideItem(
  resultId: string,
  body: ReviewDecisionBody,
): Promise<ReviewCard> {
  return apiFetch<ReviewCard>(`/item-results/${resultId}/review`, {
    method: "POST",
    body,
  });
}

export function lockMarks(examId: string): Promise<Exam> {
  return apiFetch<Exam>(`/exams/${examId}/lock-marks`, { method: "POST" });
}

/** True when the teacher still has to decide this item. */
export function isUndecided(card: ReviewCard): boolean {
  return (
    card.state !== "confirmed" &&
    card.state !== "edited" &&
    card.state !== "locked"
  );
}

export interface CandidateResult {
  candidate_id: string;
  roll: string;
  name: string;
  script_id: string | null;
  marks: MarkString;
  max_marks: MarkString;
  percent: MarkString;
  letter: string;
  grade_point: MarkString;
  is_pass: boolean;
  /** Items still to be decided. Non-zero means `marks` is incomplete. */
  pending_items: number;
}

export interface ExamResults {
  exam_id: string;
  name: string;
  subject_code: string;
  state: ExamState;
  max_marks: MarkString;
  /** True until marks are locked: these totals will still change. */
  provisional: boolean;
  candidates: CandidateResult[];
}

export function getExamResults(examId: string): Promise<ExamResults> {
  return apiFetch<ExamResults>(`/exams/${examId}/results`);
}
