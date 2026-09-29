import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router";
import { listExams, listScripts, type Exam } from "../api/assessment";
import { useSession } from "../auth/SessionContext";
import { FullPageSpinner, Spinner } from "../components/Spinner/Spinner";
import { ErrorView } from "./ErrorView";

export function HomePage(): ReactNode {
  const { t } = useTranslation(["pages", "nav", "common"]);
  const session = useSession();
  const query = useQuery({ queryKey: ["exams"], queryFn: listExams });

  if (query.isPending) return <FullPageSpinner />;
  if (query.isError)
    return (
      <ErrorView error={query.error} onRetry={() => void query.refetch()} />
    );

  return (
    <main className="review" id="main">
      <header className="review__header">
        <h1>{t("pages:exams.title")}</h1>
        <p className="hint">
          {session.me?.name}
          {session.activeMembership
            ? ` · ${session.activeMembership.school_name_en}`
            : ""}
        </p>
      </header>

      <nav className="card stack" aria-label={t("pages:roster.title")}>
        <Link to="/roster">{t("pages:roster.title")}</Link>
      </nav>

      {query.data.length === 0 ? (
        <div className="card stack">
          <h2>{t("pages:exams.emptyTitle")}</h2>
          <p className="hint">{t("pages:exams.emptyBody")}</p>
        </div>
      ) : (
        query.data.map((exam) => <ExamRow key={exam.id} exam={exam} />)
      )}

      <button
        type="button"
        className="button button--secondary"
        onClick={() => void session.logout()}
      >
        {t("nav:signOut")}
      </button>
    </main>
  );
}

function ExamRow({ exam }: { exam: Exam }): ReactNode {
  const { t } = useTranslation(["pages"]);
  const scripts = useQuery({
    queryKey: ["scripts", exam.id],
    queryFn: () => listScripts(exam.id),
  });

  return (
    <article className="card stack">
      <h2>
        {exam.name}
        <span className="hint">
          {" "}
          · {exam.subject_code} · Class {exam.class_level} · {exam.state} ·{" "}
          {exam.total_marks} marks
        </span>
      </h2>

      {scripts.isPending ? <Spinner /> : null}
      {scripts.isError ? (
        <p className="hint">Scripts could not be loaded.</p>
      ) : null}
      {scripts.data?.length === 0 ? (
        <p className="hint">No scripts captured yet.</p>
      ) : null}

      <Link to={`/exams/${exam.id}/results`}>{t("pages:results.title")}</Link>

      {scripts.data && scripts.data.length > 0 ? (
        <ul>
          {scripts.data.map((script) => (
            <li key={script.id}>
              <Link to={`/review/${script.id}`}>
                Review script {script.id.slice(0, 8)}
                {script.total_marks ? ` — ${script.total_marks} marks` : ""}
              </Link>
            </li>
          ))}
        </ul>
      ) : null}
    </article>
  );
}
