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
    signedIn = true;
    return HttpResponse.json({
      status: "ok",
      access_token: MOCK_ACCESS_TOKEN,
      expires_in: 900,
      user: {
        id: "66666666-6666-4666-8666-666666666666",
        name: "Rahim Teacher",
        locale: "en",
      },
      refresh_token: null,
    });
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
];
