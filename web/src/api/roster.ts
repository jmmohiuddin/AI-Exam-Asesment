/** Roster endpoints (/v1/schools/{id}/roster-imports, /v1/students). */

import { apiFetch } from "./client";

export type ConsentType = "CT-1" | "CT-2" | "CT-3";
export type ConsentMethod = "paper_form" | "digital" | "verbal_recorded";

export interface Student {
  id: string;
  student_uid: string;
  name_bn: string;
  name_en: string;
  guardian_mobile: string | null;
  status: string;
}

export interface Enrolment {
  section_id: string;
  academic_year_id: string;
  roll: string;
  fourth_subject_code: string | null;
}

export interface StudentRow {
  student: Student;
  enrolment: Enrolment | null;
}

/** One reason one row cannot be imported. Both messages are always present. */
export interface RowProblem {
  row_number: number;
  field: string;
  code: string;
  message_en: string;
  message_bn: string;
  severity: "error" | "warning";
  value: string;
  /** Other rows carrying the same value, for duplicates. */
  conflicts_with: number[];
}

export interface ImportReport {
  row_count: number;
  accepted_count: number;
  error_count: number;
  is_committable: boolean;
  problems: RowProblem[];
}

export interface RosterImport {
  id: string;
  school_id: string;
  academic_year_id: string;
  filename: string;
  state: "validated" | "committed" | "discarded";
  row_count: number;
  accepted_count: number;
  error_count: number;
  report: ImportReport;
  students_created: number;
  students_updated: number;
  sections_created: number;
  created_at: string;
  committed_at: string | null;
}

export interface CommitOutcome {
  import_id: string;
  students_created: number;
  students_updated: number;
  sections_created: number;
  enrolments_created: number;
  enrolments_updated: number;
}

/** A spreadsheet row, still as text: the server does every conversion. */
export interface RawRosterRow {
  row_number: number;
  roll?: string;
  student_uid?: string;
  name_bn?: string;
  name_en?: string;
  class_level?: string;
  group_code?: string;
  version?: string;
  shift?: string;
  section?: string;
  fourth_subject_code?: string;
  guardian_mobile?: string;
}

export interface AcademicYear {
  id: string;
  year: number;
  starts_on: string;
  ends_on: string;
  is_current: boolean;
}

export function listAcademicYears(schoolId: string): Promise<AcademicYear[]> {
  return apiFetch<AcademicYear[]>(`/schools/${schoolId}/academic-years`);
}

export function listStudents(
  schoolId: string,
  sectionId?: string,
): Promise<StudentRow[]> {
  const query = sectionId ? `?section_id=${encodeURIComponent(sectionId)}` : "";
  return apiFetch<StudentRow[]>(`/schools/${schoolId}/students${query}`);
}

/** Validate a file. Writes nothing: the report says what a commit would do. */
export function validateRosterImport(
  schoolId: string,
  body: {
    academic_year_id: string;
    filename: string;
    rows: RawRosterRow[];
  },
): Promise<RosterImport> {
  return apiFetch<RosterImport>(`/schools/${schoolId}/roster-imports`, {
    method: "POST",
    body,
  });
}

export function commitRosterImport(importId: string): Promise<CommitOutcome> {
  return apiFetch<CommitOutcome>(`/roster-imports/${importId}/commit`, {
    method: "POST",
  });
}

export interface Consent {
  id: string;
  consent_type: ConsentType;
  granted: boolean;
  method: ConsentMethod;
  evidence_ref: string | null;
  note: string | null;
  recorded_at: string;
  superseded_at: string | null;
}

export interface ConsentState {
  student_id: string;
  current: Consent[];
  /** Stated by the server so no client can get "absence means no" wrong. */
  capture_allowed: boolean;
  ai_allowed: boolean;
}

export function getConsents(studentId: string): Promise<ConsentState> {
  return apiFetch<ConsentState>(`/students/${studentId}/consents`);
}

export function putConsent(
  studentId: string,
  body: {
    consent_type: ConsentType;
    granted: boolean;
    method: ConsentMethod;
    evidence_ref?: string | null;
    note?: string | null;
  },
): Promise<ConsentState> {
  return apiFetch<ConsentState>(`/students/${studentId}/consents`, {
    method: "PUT",
    body,
  });
}
