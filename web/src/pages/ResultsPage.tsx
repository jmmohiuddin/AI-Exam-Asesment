import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router";
import { getExamResults, type CandidateResult } from "../api/assessment";
import { formatNumber, resolveNumerals, type Numerals } from "../lib/format";
import { FullPageSpinner } from "../components/Spinner/Spinner";
import { ErrorView } from "./ErrorView";
import "./results.css";

export function ResultsPage(): ReactNode {
  const { examId = "" } = useParams();
  const { t, i18n } = useTranslation(["pages", "common"]);
  const numerals = resolveNumerals("auto", i18n.language);
  const query = useQuery({
    queryKey: ["results", examId],
    queryFn: () => getExamResults(examId),
  });

  if (query.isPending) return <FullPageSpinner />;
  if (query.isError)
    return (
      <ErrorView error={query.error} onRetry={() => void query.refetch()} />
    );

  const { candidates, provisional } = query.data;
  const passed = candidates.filter((c) => c.is_pass).length;

  return (
    <main className="review" id="main">
      <header className="review__header">
        <h1>{t("pages:results.title")}</h1>
        <p className="hint">
          {query.data.name} · {query.data.subject_code}
        </p>
      </header>

      {/* Stated before the numbers, not after: a provisional total that looks
          final is the one mistake this screen must not allow. */}
      <p
        className={`banner ${provisional ? "banner--warning" : "banner--info"}`}
        role="status"
      >
        {provisional
          ? t("pages:results.provisional")
          : t("pages:results.final")}
      </p>

      {candidates.length === 0 ? (
        <div className="card stack">
          <p className="hint">{t("pages:results.noCandidates")}</p>
        </div>
      ) : (
        <div className="card">
          <p className="hint">
            {t("pages:results.passCount", {
              passed: formatNumber(passed, { numerals }),
              total: formatNumber(candidates.length, { numerals }),
            })}
          </p>
          <table className="ledger">
            <caption className="visually-hidden">
              {t("pages:results.title")} — {query.data.name}
            </caption>
            <thead>
              <tr>
                <th scope="col">{t("pages:results.columns.roll")}</th>
                <th scope="col">{t("pages:results.columns.name")}</th>
                <th scope="col" className="ledger__num">
                  {t("pages:results.columns.marks")}
                </th>
                <th scope="col" className="ledger__num">
                  {t("pages:results.columns.percent")}
                </th>
                <th scope="col">{t("pages:results.columns.grade")}</th>
                <th scope="col">{t("pages:results.columns.result")}</th>
              </tr>
            </thead>
            <tbody>
              {candidates.map((candidate) => (
                <ResultRow
                  key={candidate.candidate_id}
                  candidate={candidate}
                  numerals={numerals}
                />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}

function ResultRow({
  candidate,
  numerals,
}: {
  candidate: CandidateResult;
  numerals: Numerals;
}): ReactNode {
  const { t } = useTranslation(["pages"]);
  const marks = (value: string): string =>
    formatNumber(Number(value), { numerals });

  return (
    <tr>
      <td>{marks(candidate.roll)}</td>
      <td>
        {candidate.name}
        {candidate.pending_items > 0 ? (
          // Shown on the row, not only in the page banner: one unmarked answer
          // makes this student's total wrong even when the exam looks finished.
          <span className="ledger__pending">
            {/* `count` picks the plural form; `shown` carries the digits, so
                the number is in the same numerals as the rest of the row. */}
            {t("pages:results.pendingItems", {
              count: candidate.pending_items,
              shown: formatNumber(candidate.pending_items, { numerals }),
            })}
          </span>
        ) : null}
      </td>
      <td className="ledger__num">
        {marks(candidate.marks)}
        <span className="ledger__max">/{marks(candidate.max_marks)}</span>
      </td>
      <td className="ledger__num">{marks(candidate.percent)}%</td>
      <td>{candidate.letter}</td>
      <td>
        <span className={`pill ${candidate.is_pass ? "" : "pill--fail"}`}>
          {candidate.is_pass
            ? t("pages:results.pass")
            : t("pages:results.fail")}
        </span>
      </td>
    </tr>
  );
}
