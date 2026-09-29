/**
 * MSW handlers for component tests and `pnpm dev:mock`.
 *
 * These mirror the real API's shapes, including its RFC 9457 error body, so a
 * test that passes here is exercising the same contract the backend serves.
 * State lives in module scope and is reset between tests by `resetMockState`.
 */

import { http, HttpResponse } from "msw";

export const MOCK_ACCESS_TOKEN = "mock-access-token";
export const MOCK_MOBILE = "+8801712345678";
export const MOCK_PASSWORD = "correct-horse-battery";
export const MOCK_DEVICE_ID = "11111111-1111-4111-8111-111111111111";
export const MOCK_CHALLENGE_ID = "22222222-2222-4222-8222-222222222222";
export const MOCK_OTP_CODE = "123456";

/** Flipped by tests that need the locked-marks view. */
export let examResultsProvisional = true;
export function setExamResultsProvisional(value: boolean): void {
  examResultsProvisional = value;
}
export const MOCK_USER = {
  id: "66666666-6666-4666-8666-666666666666",
  name: "Rahim Teacher",
  locale: "en",
};

/** Must match the school on the membership `/v1/me` returns below. */
export const MOCK_SCHOOL_ID = "88888888-8888-4888-8888-888888888888";
export const MOCK_ACADEMIC_YEAR_ID = "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee";
export const MOCK_STUDENT_ID = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa";

/** Students the roster screen lists. Reset with the rest of the mock state. */
let students = freshStudents();
function freshStudents() {
  return [
    {
      student: {
        id: MOCK_STUDENT_ID,
        student_uid: "9-A-101",
        name_bn: "করিম উদ্দিন",
        name_en: "Karim Uddin",
        guardian_mobile: null,
        status: "active",
      },
      enrolment: {
        section_id: "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
        academic_year_id: MOCK_ACADEMIC_YEAR_ID,
        roll: "101",
        fourth_subject_code: null,
      },
    },
  ];
}

/** Live consent per type for MOCK_STUDENT_ID. Empty means consented to nothing. */
let consents: Record<string, boolean> = {};

function consentState() {
  return {
    student_id: MOCK_STUDENT_ID,
    current: Object.entries(consents).map(([consent_type, granted], index) => ({
      id: `cccccccc-cccc-4ccc-8ccc-00000000000${index}`,
      consent_type,
      granted,
      method: "paper_form",
      evidence_ref: null,
      note: null,
      recorded_at: "2026-09-01T10:00:00Z",
      superseded_at: null,
    })),
    capture_allowed: consents["CT-1"] === true,
    ai_allowed: consents["CT-2"] === true,
  };
}

/** The staged import the roster page is currently showing, if any. */
let stagedImport: Record<string, unknown> | null = null;

const BASE = "/v1";

export const mockExam = {
  id: "11111111-1111-4111-8111-111111111111",
  name: "Biology First Term",
  subject_code: "BIO",
  class_level: 9,
  state: "reviewing",
  total_marks: "5.00",
  rubric_locked_at: "2026-09-01T10:00:00Z",
  marks_locked_at: null,
};

export const mockScript = {
  id: "22222222-2222-4222-8222-222222222222",
  exam_id: mockExam.id,
  candidate_id: "33333333-3333-4333-8333-333333333333",
  total_marks: null as string | null,
};

const rubric = {
  item_id: "q1",
  version: 1,
  model_answer: "Chlorophyll captures sunlight to make glucose.",
  half_marks_allowed: false,
  criteria: [
    {
      id: "c1",
      text_bn: "",
      text_en: "Identifies chlorophyll",
      marks: "3.00",
      type: "concept",
      evidence_expectation: "chlorophyll",
    },
    {
      id: "c2",
      text_bn: "",
      text_en: "Names glucose as a product",
      marks: "2.00",
      type: "final_answer",
      evidence_expectation: "glucose",
    },
  ],
};

function freshCard(): Record<string, unknown> {
  return {
    result_id: "44444444-4444-4444-8444-444444444444",
    item_id: "55555555-5555-4555-8555-555555555555",
    item_no: 1,
    prompt_bn: "সালোকসংশ্লেষণ কাকে বলে?",
    prompt_en: "What is photosynthesis?",
    max_marks: "5.00",
    state: "suggested",
    student_answer: "Plants use chlorophyll to make glucose.",
    model_answer: rubric.model_answer,
    rubric,
    rubric_version: 1,
    ai_model: "fake-marker",
    ai_confidence: "0.900",
    ai_low_confidence: false,
    ai_rationale: "Matched 2 of 2 criteria by expected keywords.",
    ai_evidence: ["c1: matched chlorophyll", "c2: matched glucose"],
    ai_decisions: [
      { criterion_id: "c1", decision: "met" },
      { criterion_id: "c2", decision: "met" },
    ],
    suggested_score: {
      item_id: "q1",
      item_max: "5.00",
      criteria: [],
      computed_total: "5.00",
      total: "5.00",
      needs_teacher: false,
    },
    teacher_score: null,
    total: null,
    decided_at: null,
  };
}

let card = freshCard();
let signedIn = false;

/** Called from the vitest setup file after every test. */
export function resetMockState(): void {
  card = freshCard();
  signedIn = false;
  examResultsProvisional = true;
  students = freshStudents();
  consents = {};
  stagedImport = null;
}

/** Start a test with a student who has already consented to some types. */
export function setMockConsents(next: Record<string, boolean>): void {
  consents = { ...next };
}

/** Start a test with an empty roster. */
export function setMockStudents(next: typeof students): void {
  students = next;
}

function problem(status: number, code: string, messageEn: string) {
  return HttpResponse.json(
    {
      type: `urn:khata:error:${code}`,
      title: code,
      status,
      detail: messageEn,
      code,
      message_bn: messageEn,
      message_en: messageEn,
      support_code: "KH-TESTTEST",
    },
    { status, headers: { "Content-Type": "application/problem+json" } },
  );
}

function requireAuth(request: Request) {
  return request.headers.get("Authorization") === `Bearer ${MOCK_ACCESS_TOKEN}`
    ? null
    : problem(401, "UNAUTHENTICATED", "Please sign in again.");
}

export const handlers = [
  http.post(`${BASE}/auth/login`, async ({ request }) => {
    const body = (await request.json()) as { mobile: string; password: string };
    if (body.mobile !== MOCK_MOBILE || body.password !== MOCK_PASSWORD) {
      return problem(
        401,
        "INVALID_CREDENTIALS",
        "Mobile number or password is incorrect.",
      );
    }
    const known = (body as { device_id?: string }).device_id === MOCK_DEVICE_ID;
    if (!known) {
      return HttpResponse.json({
        status: "otp_required",
        challenge_id: MOCK_CHALLENGE_ID,
        otp_expires_at: new Date(Date.now() + 5 * 60_000).toISOString(),
      });
    }
    signedIn = true;
    return HttpResponse.json({
      status: "ok",
      access_token: MOCK_ACCESS_TOKEN,
      expires_in: 900,
      user: MOCK_USER,
      refresh_token: null,
    });
  }),

  http.post(`${BASE}/auth/otp/verify`, async ({ request }) => {
    const body = (await request.json()) as {
      challenge_id: string;
      code: string;
    };
    if (
      body.challenge_id !== MOCK_CHALLENGE_ID ||
      body.code !== MOCK_OTP_CODE
    ) {
      return problem(400, "OTP_INVALID", "The code is incorrect.");
    }
    signedIn = true;
    return HttpResponse.json({
      status: "ok",
      access_token: MOCK_ACCESS_TOKEN,
      expires_in: 900,
      device_id: MOCK_DEVICE_ID,
      user: MOCK_USER,
      refresh_token: null,
    });
  }),

  http.post(`${BASE}/auth/otp/resend`, async ({ request }) => {
    const body = (await request.json()) as { challenge_id: string };
    return body.challenge_id === MOCK_CHALLENGE_ID
      ? HttpResponse.json({
          challenge_id: MOCK_CHALLENGE_ID,
          otp_expires_at: new Date(Date.now() + 5 * 60_000).toISOString(),
        })
      : problem(400, "OTP_INVALID", "The code is incorrect.");
  }),

  http.post(`${BASE}/auth/refresh`, () =>
    signedIn
      ? HttpResponse.json({ access_token: MOCK_ACCESS_TOKEN, expires_in: 900 })
      : problem(401, "REFRESH_INVALID", "Please sign in again."),
  ),

  http.post(`${BASE}/auth/logout`, () => {
    signedIn = false;
    return new HttpResponse(null, { status: 204 });
  }),

  http.get(`${BASE}/me`, ({ request }) => {
    const denied = requireAuth(request);
    if (denied) return denied;
    return HttpResponse.json({
      id: "66666666-6666-4666-8666-666666666666",
      name: "Rahim Teacher",
      mobile_masked: "+880****5678",
      locale: "en",
      preferences: {},
      platform_role: null,
      memberships: [
        {
          tenant_id: "77777777-7777-4777-8777-777777777777",
          org_name: "Test Model School",
          school_id: "88888888-8888-4888-8888-888888888888",
          school_name_bn: "পরীক্ষা বিদ্যালয়",
          school_name_en: "Test Model School",
          roles: ["exam_coordinator"],
        },
      ],
      active_tenant_id: "77777777-7777-4777-8777-777777777777",
    });
  }),

  http.get(
    `${BASE}/exams`,
    ({ request }) => requireAuth(request) ?? HttpResponse.json([mockExam]),
  ),

  http.get(
    `${BASE}/exams/:examId/scripts`,
    ({ request }) => requireAuth(request) ?? HttpResponse.json([mockScript]),
  ),

  http.get(`${BASE}/exams/:examId/results`, ({ request }) => {
    const denied = requireAuth(request);
    if (denied) return denied;
    return HttpResponse.json({
      exam_id: mockExam.id,
      name: mockExam.name,
      subject_code: mockExam.subject_code,
      state: mockExam.state,
      max_marks: "5.00",
      provisional: examResultsProvisional,
      candidates: [
        {
          candidate_id: mockScript.candidate_id,
          roll: "101",
          name: "Karim Student",
          script_id: mockScript.id,
          marks: "4",
          max_marks: "5.00",
          percent: "80.00",
          letter: "A+",
          grade_point: "5.0",
          is_pass: true,
          pending_items: 0,
        },
        {
          candidate_id: "99999999-9999-4999-8999-999999999999",
          roll: "102",
          name: "Fatema Akter",
          script_id: null,
          marks: "1",
          max_marks: "5.00",
          percent: "20.00",
          letter: "F",
          grade_point: "0.0",
          is_pass: false,
          pending_items: 1,
        },
      ],
    });
  }),

  http.get(`${BASE}/scripts/:scriptId/review`, ({ request }) => {
    const denied = requireAuth(request);
    if (denied) return denied;
    return HttpResponse.json({
      script_id: mockScript.id,
      candidate: {
        id: mockScript.candidate_id,
        roll: "101",
        name: "Karim Student",
      },
      exam_state: mockExam.state,
      script_total: mockScript.total_marks,
      items: [card],
    });
  }),

  http.post(`${BASE}/item-results/:resultId/review`, async ({ request }) => {
    const denied = requireAuth(request);
    if (denied) return denied;
    const body = (await request.json()) as { accepted_ai: boolean };
    card = {
      ...card,
      state: body.accepted_ai ? "confirmed" : "edited",
      total: "5.00",
    };
    return HttpResponse.json(card);
  }),

  http.get(`${BASE}/schools/:schoolId/academic-years`, ({ request }) => {
    const denied = requireAuth(request);
    if (denied) return denied;
    return HttpResponse.json([
      {
        id: MOCK_ACADEMIC_YEAR_ID,
        year: 2026,
        starts_on: "2026-01-01",
        ends_on: "2026-12-31",
        is_current: true,
      },
    ]);
  }),

  http.get(`${BASE}/schools/:schoolId/students`, ({ request }) => {
    const denied = requireAuth(request);
    if (denied) return denied;
    return HttpResponse.json(students);
  }),

  http.post(`${BASE}/schools/:schoolId/roster-imports`, async ({ request }) => {
    const denied = requireAuth(request);
    if (denied) return denied;
    const body = (await request.json()) as {
      filename: string;
      rows: { row_number: number; roll?: string }[];
    };
    // Mirrors the engine closely enough for the screen: a row with no roll is
    // the error the report has to show.
    const problems = body.rows
      .filter((row) => !row.roll)
      .map((row) => ({
        row_number: row.row_number,
        field: "roll",
        code: "required",
        message_en: "Roll is required.",
        message_bn: "রোল নম্বর দিতে হবে।",
        severity: "error" as const,
        value: "",
        conflicts_with: [] as number[],
      }));
    const accepted = body.rows.length - problems.length;
    stagedImport = {
      id: "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
      school_id: MOCK_SCHOOL_ID,
      academic_year_id: MOCK_ACADEMIC_YEAR_ID,
      filename: body.filename,
      state: "validated",
      row_count: body.rows.length,
      accepted_count: accepted,
      error_count: problems.length,
      report: {
        row_count: body.rows.length,
        accepted_count: accepted,
        error_count: problems.length,
        is_committable: accepted > 0 && problems.length === 0,
        problems,
      },
      students_created: 0,
      students_updated: 0,
      sections_created: 0,
      created_at: "2026-09-29T10:00:00Z",
      committed_at: null,
    };
    return HttpResponse.json(stagedImport, { status: 201 });
  }),

  http.post(`${BASE}/roster-imports/:importId/commit`, ({ request }) => {
    const denied = requireAuth(request);
    if (denied) return denied;
    const staged = stagedImport as { accepted_count: number } | null;
    if (!staged || staged.accepted_count === 0) {
      return problem(
        409,
        "ROSTER_IMPORT_NOT_COMMITTABLE",
        "Fix the reported rows and upload the file again.",
      );
    }
    return HttpResponse.json({
      import_id: "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
      students_created: staged.accepted_count,
      students_updated: 0,
      sections_created: 1,
      enrolments_created: staged.accepted_count,
      enrolments_updated: 0,
    });
  }),

  http.get(`${BASE}/students/:studentId/consents`, ({ request }) => {
    const denied = requireAuth(request);
    if (denied) return denied;
    return HttpResponse.json(consentState());
  }),

  http.put(`${BASE}/students/:studentId/consents`, async ({ request }) => {
    const denied = requireAuth(request);
    if (denied) return denied;
    const body = (await request.json()) as {
      consent_type: string;
      granted: boolean;
    };
    consents = { ...consents, [body.consent_type]: body.granted };
    return HttpResponse.json(consentState());
  }),
];
