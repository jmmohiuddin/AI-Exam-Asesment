import { useState, type ChangeEvent, type ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  commitRosterImport,
  getConsents,
  listAcademicYears,
  listStudents,
  putConsent,
  validateRosterImport,
  type ConsentType,
  type RosterImport,
  type RowProblem,
  type StudentRow,
} from "../api/roster";
import { parseRosterCsv } from "../lib/csv";
import { useSession } from "../auth/SessionContext";
import { formatNumber, resolveNumerals, type Numerals } from "../lib/format";
import { FullPageSpinner, Spinner } from "../components/Spinner/Spinner";
import { ErrorView } from "./ErrorView";
import "./roster.css";

/** The three consents, in the order 08 §6.1 lists them. */
const CONSENT_TYPES: ConsentType[] = ["CT-1", "CT-2", "CT-3"];

export function RosterPage(): ReactNode {
  const { t } = useTranslation(["pages", "nav"]);
  const session = useSession();
  const schoolId = session.activeMembership?.school_id ?? "";

  const students = useQuery({
    queryKey: ["students", schoolId],
    queryFn: () => listStudents(schoolId),
    enabled: schoolId !== "",
  });
  const years = useQuery({
    queryKey: ["academic-years", schoolId],
    queryFn: () => listAcademicYears(schoolId),
    enabled: schoolId !== "",
  });
  // An import is filed against one year. The current one is the only sensible
  // default, and without one there is nothing to import into.
  const academicYearId =
    years.data?.find((year) => year.is_current)?.id ??
    years.data?.[0]?.id ??
    "";

  if (schoolId === "") {
    return (
      <main className="review" id="main">
        <header className="review__header">
          <h1>{t("pages:roster.title")}</h1>
        </header>
        <div className="card stack">
          <p className="hint">{t("pages:roster.noSchool")}</p>
        </div>
      </main>
    );
  }

  if (students.isPending) return <FullPageSpinner />;
  if (students.isError)
    return (
      <ErrorView
        error={students.error}
        onRetry={() => void students.refetch()}
      />
    );

  return (
    <main className="review" id="main">
      <header className="review__header">
        <h1>{t("pages:roster.title")}</h1>
        <p className="hint">{t("pages:roster.subtitle")}</p>
      </header>

      {academicYearId === "" ? (
        <div className="card stack">
          <h2>{t("pages:roster.import.title")}</h2>
          <p className="hint">{t("pages:roster.import.noAcademicYear")}</p>
        </div>
      ) : (
        <ImportCard schoolId={schoolId} academicYearId={academicYearId} />
      )}

      {students.data.length === 0 ? (
        <div className="card stack">
          <h2>{t("pages:roster.emptyTitle")}</h2>
          <p className="hint">{t("pages:roster.emptyBody")}</p>
        </div>
      ) : (
        <StudentTable rows={students.data} />
      )}
    </main>
  );
}

// --------------------------------------------------------------------------- import

function ImportCard({
  schoolId,
  academicYearId,
}: {
  schoolId: string;
  academicYearId: string;
}): ReactNode {
  const { t, i18n } = useTranslation(["pages"]);
  const numerals = resolveNumerals("auto", i18n.language);
  const queryClient = useQueryClient();
  const [staged, setStaged] = useState<RosterImport | null>(null);
  const [parseWarning, setParseWarning] = useState<string | null>(null);

  const validate = useMutation({
    mutationFn: (file: File) =>
      file.text().then((text) => {
        const parsed = parseRosterCsv(text);
        if (parsed.headerUnrecognised) {
          throw new Error(t("pages:roster.import.headerUnrecognised"));
        }
        setParseWarning(
          parsed.unknownColumns.length > 0
            ? t("pages:roster.import.unknownColumns", {
                columns: parsed.unknownColumns.join(", "),
              })
            : null,
        );
        return validateRosterImport(schoolId, {
          academic_year_id: academicYearId,
          filename: file.name,
          rows: parsed.rows,
        });
      }),
    onSuccess: setStaged,
  });

  const commit = useMutation({
    mutationFn: (importId: string) => commitRosterImport(importId),
    onSuccess: () => {
      setStaged(null);
      setParseWarning(null);
      void queryClient.invalidateQueries({ queryKey: ["students", schoolId] });
    },
  });

  const onChoose = (event: ChangeEvent<HTMLInputElement>): void => {
    const file = event.target.files?.[0];
    // Clear the input so choosing the same corrected file again still fires.
    event.target.value = "";
    if (file) {
      setStaged(null);
      commit.reset();
      validate.mutate(file);
    }
  };

  return (
    <section className="card stack" aria-labelledby="roster-import-heading">
      <h2 id="roster-import-heading">{t("pages:roster.import.title")}</h2>
      <p className="hint">{t("pages:roster.import.help")}</p>

      <label className="roster__file">
        <span className="visually-hidden">
          {t("pages:roster.import.choose")}
        </span>
        <input
          type="file"
          accept=".csv,text/csv"
          onChange={onChoose}
          disabled={validate.isPending || commit.isPending}
        />
      </label>

      {validate.isPending ? <Spinner /> : null}
      {validate.isError ? (
        <p className="banner banner--warning" role="alert">
          {validate.error.message}
        </p>
      ) : null}
      {parseWarning ? (
        <p className="banner banner--warning" role="status">
          {parseWarning}
        </p>
      ) : null}

      {staged ? (
        <ImportReportView
          staged={staged}
          numerals={numerals}
          committing={commit.isPending}
          onCommit={() => commit.mutate(staged.id)}
        />
      ) : null}

      {commit.isSuccess ? (
        <p className="banner banner--info" role="status">
          {t("pages:roster.import.committed", {
            created: formatNumber(commit.data.students_created, { numerals }),
            updated: formatNumber(commit.data.students_updated, { numerals }),
          })}
        </p>
      ) : null}
      {commit.isError ? (
        <p className="banner banner--warning" role="alert">
          {commit.error.message}
        </p>
      ) : null}
    </section>
  );
}

function ImportReportView({
  staged,
  numerals,
  committing,
  onCommit,
}: {
  staged: RosterImport;
  numerals: Numerals;
  committing: boolean;
  onCommit: () => void;
}): ReactNode {
  const { t, i18n } = useTranslation(["pages"]);
  const count = (value: number): string => formatNumber(value, { numerals });
  const { report } = staged;

  return (
    <div className="roster__report">
      {/* Said before the counts: the whole point of the dry run is that the
          admin knows nothing has been written yet. */}
      <p
        className={`banner ${report.is_committable ? "banner--info" : "banner--warning"}`}
        role="status"
      >
        {report.is_committable
          ? t("pages:roster.import.ready", {
              accepted: count(report.accepted_count),
            })
          : t("pages:roster.import.blocked", {
              errors: count(report.error_count),
            })}
      </p>

      <p className="hint">
        {t("pages:roster.import.counts", {
          rows: count(report.row_count),
          accepted: count(report.accepted_count),
          errors: count(report.error_count),
        })}
      </p>

      {report.problems.length > 0 ? (
        <table className="ledger">
          <caption className="visually-hidden">
            {t("pages:roster.import.problemsCaption")}
          </caption>
          <thead>
            <tr>
              <th scope="col">{t("pages:roster.import.columns.row")}</th>
              <th scope="col">{t("pages:roster.import.columns.field")}</th>
              <th scope="col">{t("pages:roster.import.columns.problem")}</th>
            </tr>
          </thead>
          <tbody>
            {report.problems.map((problem) => (
              <ProblemRow
                key={`${problem.row_number}-${problem.field}-${problem.code}`}
                problem={problem}
                numerals={numerals}
                language={i18n.language}
              />
            ))}
          </tbody>
        </table>
      ) : null}

      <button
        type="button"
        className="button"
        onClick={onCommit}
        disabled={!report.is_committable || committing}
      >
        {committing
          ? t("pages:roster.import.committing")
          : t("pages:roster.import.commit")}
      </button>
    </div>
  );
}

function ProblemRow({
  problem,
  numerals,
  language,
}: {
  problem: RowProblem;
  numerals: Numerals;
  language: string;
}): ReactNode {
  const { t } = useTranslation(["pages"]);
  // The server sends both languages on every problem, so the report reads in
  // the language the admin is using without a second round trip.
  const message = language.startsWith("bn")
    ? problem.message_bn
    : problem.message_en;

  return (
    <tr>
      <td className="ledger__num">
        {formatNumber(problem.row_number, { numerals })}
      </td>
      <td>{problem.field}</td>
      <td>
        {message}
        {problem.conflicts_with.length > 0 ? (
          <span className="hint">
            {" "}
            {t("pages:roster.import.alsoRows", {
              rows: problem.conflicts_with
                .map((row) => formatNumber(row, { numerals }))
                .join(", "),
            })}
          </span>
        ) : null}
      </td>
    </tr>
  );
}

// --------------------------------------------------------------------------- students

function StudentTable({ rows }: { rows: StudentRow[] }): ReactNode {
  const { t, i18n } = useTranslation(["pages"]);
  const numerals = resolveNumerals("auto", i18n.language);

  return (
    <div className="card">
      <p className="hint">
        {t("pages:roster.studentCount", {
          count: rows.length,
          shown: formatNumber(rows.length, { numerals }),
        })}
      </p>
      <table className="ledger">
        <caption className="visually-hidden">{t("pages:roster.title")}</caption>
        <thead>
          <tr>
            <th scope="col">{t("pages:roster.columns.roll")}</th>
            <th scope="col">{t("pages:roster.columns.name")}</th>
            <th scope="col">{t("pages:roster.columns.consent")}</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <StudentRowView
              key={row.student.id}
              row={row}
              numerals={numerals}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}

function StudentRowView({
  row,
  numerals,
}: {
  row: StudentRow;
  numerals: Numerals;
}): ReactNode {
  const { i18n } = useTranslation(["pages"]);
  const name = i18n.language.startsWith("bn")
    ? row.student.name_bn || row.student.name_en
    : row.student.name_en || row.student.name_bn;

  return (
    <tr>
      <td className="ledger__num">
        {row.enrolment
          ? formatNumber(Number(row.enrolment.roll), { numerals })
          : "—"}
      </td>
      <td>
        {name}
        <span className="hint"> · {row.student.student_uid}</span>
      </td>
      <td>
        <ConsentCell studentId={row.student.id} label={name} />
      </td>
    </tr>
  );
}

function ConsentCell({
  studentId,
  label,
}: {
  studentId: string;
  label: string;
}): ReactNode {
  const { t } = useTranslation(["pages"]);
  const queryClient = useQueryClient();
  const query = useQuery({
    queryKey: ["consents", studentId],
    queryFn: () => getConsents(studentId),
  });

  const record = useMutation({
    mutationFn: ({
      consentType,
      granted,
    }: {
      consentType: ConsentType;
      granted: boolean;
    }) =>
      putConsent(studentId, {
        consent_type: consentType,
        granted,
        method: "paper_form",
      }),
    onSuccess: (state) => {
      queryClient.setQueryData(["consents", studentId], state);
    },
  });

  if (query.isPending) return <Spinner />;
  if (query.isError) return <span className="hint">—</span>;

  const granted = new Map(
    query.data.current.map((consent) => [
      consent.consent_type,
      consent.granted,
    ]),
  );

  return (
    <div className="roster__consents">
      {CONSENT_TYPES.map((consentType) => {
        // Absence of a record is a refusal, not an unknown (08 §6.1), so an
        // unrecorded consent renders exactly like a refused one.
        const isGranted = granted.get(consentType) === true;
        return (
          <label key={consentType} className="roster__consent">
            <input
              type="checkbox"
              checked={isGranted}
              disabled={record.isPending}
              onChange={(event) =>
                record.mutate({
                  consentType,
                  granted: event.target.checked,
                })
              }
            />
            <span>
              {consentType}
              <span className="visually-hidden">
                {" "}
                — {t(`pages:roster.consent.${consentType}`)} — {label}
              </span>
            </span>
          </label>
        );
      })}
      {!query.data.ai_allowed ? (
        // The consequence, not just the checkbox: this is why a teacher will see
        // no suggestion on this student's script.
        <span className="roster__l0">{t("pages:roster.consent.noAi")}</span>
      ) : null}
    </div>
  );
}
