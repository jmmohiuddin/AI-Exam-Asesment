import { useState, type ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useParams } from "react-router";
import {
  decideItem,
  getReviewQueue,
  type CriterionDecision,
  type CriterionDecisionValue,
  type ReviewCard,
  type RubricCriterion,
} from "../api/assessment";
import { FullPageSpinner } from "../components/Spinner/Spinner";
import { ErrorView } from "./ErrorView";
import "./review.css";

const DECISIONS: CriterionDecisionValue[] = [
  "met",
  "partly",
  "not_met",
  "cannot_determine",
];

const DECISION_LABEL: Record<CriterionDecisionValue, string> = {
  met: "Met",
  partly: "Partly",
  not_met: "Not met",
  cannot_determine: "Cannot tell",
};

function criteriaOf(card: ReviewCard): RubricCriterion[] {
  return "criteria" in card.rubric ? card.rubric.criteria : [];
}

/** Start from the AI's decisions so the common case is one click, not many. */
function initialDecisions(
  card: ReviewCard,
): Record<string, CriterionDecisionValue> {
  const seed: Record<string, CriterionDecisionValue> = {};
  for (const criterion of criteriaOf(card)) seed[criterion.id] = "not_met";
  for (const decision of card.ai_decisions)
    seed[decision.criterion_id] = decision.decision;
  for (const scored of card.teacher_score?.criteria ?? [])
    seed[scored.criterion_id] = scored.decision;
  return seed;
}

export function ReviewPage(): ReactNode {
  const { scriptId = "" } = useParams();
  const query = useQuery({
    queryKey: ["review", scriptId],
    queryFn: () => getReviewQueue(scriptId),
    enabled: Boolean(scriptId),
  });

  if (query.isPending) return <FullPageSpinner />;
  if (query.isError)
    return (
      <ErrorView error={query.error} onRetry={() => void query.refetch()} />
    );

  const queue = query.data;
  return (
    <main className="review" id="main">
      <header className="review__header">
        <h1>
          {queue.candidate.name}{" "}
          <span className="review__roll">#{queue.candidate.roll}</span>
        </h1>
        <p className="hint">
          Exam state: {queue.exam_state}
          {queue.script_total ? ` · Script total ${queue.script_total}` : ""}
        </p>
      </header>
      {queue.items.map((card) => (
        <ReviewItem key={card.result_id} card={card} scriptId={scriptId} />
      ))}
    </main>
  );
}

function ReviewItem({
  card,
  scriptId,
}: {
  card: ReviewCard;
  scriptId: string;
}): ReactNode {
  const { t } = useTranslation(["common"]);
  const queryClient = useQueryClient();
  const [decisions, setDecisions] = useState(() => initialDecisions(card));
  const [touched, setTouched] = useState(false);

  const criteria = criteriaOf(card);
  const locked = card.state === "locked";

  const mutation = useMutation({
    mutationFn: (acceptedAi: boolean) =>
      decideItem(card.result_id, {
        decisions: criteria.map<CriterionDecision>((criterion) => ({
          criterion_id: criterion.id,
          decision: decisions[criterion.id] ?? "not_met",
        })),
        accepted_ai: acceptedAi,
      }),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ["review", scriptId] }),
  });

  function choose(criterionId: string, value: CriterionDecisionValue): void {
    setTouched(true);
    setDecisions((current) => ({ ...current, [criterionId]: value }));
  }

  return (
    <article className="card review__item">
      <h2>
        Question {card.item_no}
        <span className="review__marks">
          {card.total ?? "—"} / {card.max_marks}
        </span>
      </h2>

      {/* Question, answer and model answer sit side by side: the teacher compares
          them without navigating away (05 §23). */}
      <div className="review__grid">
        <section>
          <h3>Question</h3>
          <p lang="bn">{card.prompt_bn}</p>
          <p lang="en">{card.prompt_en}</p>
        </section>

        <section>
          <h3>Student answer</h3>
          <p className="review__answer">
            {card.student_answer || <em>Blank</em>}
          </p>
        </section>

        <section>
          <h3>Model answer</h3>
          <p className="review__answer">{card.model_answer ?? t("noValue")}</p>
        </section>
      </div>

      <AiPanel card={card} />

      <section>
        <h3>Rubric</h3>
        {criteria.length === 0 ? (
          <p className="hint">This question has no rubric criteria.</p>
        ) : (
          <ul className="review__criteria">
            {criteria.map((criterion) => (
              <li key={criterion.id}>
                <div className="review__criterion-text">
                  <strong>
                    {criterion.text_en || criterion.text_bn || criterion.id}
                  </strong>
                  <span className="hint"> ({criterion.marks})</span>
                </div>
                <fieldset
                  className="review__choices"
                  disabled={locked || mutation.isPending}
                >
                  <legend className="visually-hidden">
                    Decision for {criterion.text_en || criterion.id}
                  </legend>
                  {DECISIONS.map((value) => (
                    <label key={value} className={`chip chip--${value}`}>
                      <input
                        type="radio"
                        name={`${card.result_id}:${criterion.id}`}
                        value={value}
                        checked={decisions[criterion.id] === value}
                        onChange={() => choose(criterion.id, value)}
                      />
                      {DECISION_LABEL[value]}
                    </label>
                  ))}
                </fieldset>
              </li>
            ))}
          </ul>
        )}
      </section>

      {mutation.isError ? <ErrorBanner error={mutation.error} /> : null}

      {locked ? (
        <p className="banner banner--info">These marks are locked.</p>
      ) : (
        <div className="review__actions">
          <button
            type="button"
            className="button"
            disabled={mutation.isPending || criteria.length === 0}
            onClick={() => mutation.mutate(!touched)}
          >
            {touched ? "Save my decision" : "Accept AI suggestion"}
          </button>
          {card.decided_at ? (
            <span className="hint">{t("states.saved")}</span>
          ) : null}
        </div>
      )}
    </article>
  );
}

function AiPanel({ card }: { card: ReviewCard }): ReactNode {
  if (!card.ai_model) {
    return (
      <p className="banner banner--warning">
        No AI suggestion for this question — mark it from the evidence.
      </p>
    );
  }
  return (
    <section className="review__ai">
      <h3>
        AI suggestion
        <span className="badge badge--ai">{card.ai_model}</span>
        {card.ai_confidence ? (
          <span
            className={`badge ${card.ai_low_confidence ? "badge--low" : "badge--ai"}`}
          >
            confidence {card.ai_confidence}
          </span>
        ) : null}
      </h3>
      {card.ai_low_confidence ? (
        <p className="banner banner--warning">
          Low confidence. Read the answer yourself before deciding.
        </p>
      ) : null}
      {card.ai_rationale ? <p>{card.ai_rationale}</p> : null}
      {card.ai_evidence.length > 0 ? (
        <>
          <h4>Evidence</h4>
          <ul>
            {card.ai_evidence.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </>
      ) : null}
      {card.suggested_score ? (
        <p className="hint">
          Suggested total {card.suggested_score.computed_total} /{" "}
          {card.suggested_score.item_max}
          {card.suggested_score.needs_teacher ? " — needs a teacher" : ""}
        </p>
      ) : null}
    </section>
  );
}

function ErrorBanner({ error }: { error: unknown }): ReactNode {
  const { i18n } = useTranslation();
  const message =
    error && typeof error === "object" && "serverMessage" in error
      ? (
          error as { serverMessage: (l: string) => string | undefined }
        ).serverMessage(i18n.language)
      : null;
  return (
    <p className="banner banner--danger" role="alert">
      {message ?? "That decision could not be saved."}
    </p>
  );
}
