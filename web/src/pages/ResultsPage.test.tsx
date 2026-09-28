/** The results ledger (FR-RES-01/02/03, FR-ANL-01). */
import { render, screen, within } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter, Route, Routes } from "react-router";
import { describe, expect, it } from "vitest";
import { ResultsPage } from "./ResultsPage";
import { setAccessToken } from "../api/tokenStore";
import {
  MOCK_ACCESS_TOKEN,
  setExamResultsProvisional,
} from "../mocks/handlers";
import { i18n } from "../i18n";

function renderResults() {
  setAccessToken(MOCK_ACCESS_TOKEN);
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/exams/exam-1/results"]}>
        <Routes>
          <Route path="/exams/:examId/results" element={<ResultsPage />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

async function rows(): Promise<HTMLElement[]> {
  const table = await screen.findByRole("table");
  return within(table).getAllByRole("row").slice(1); // drop the header row
}

async function row(index: number): Promise<HTMLElement> {
  const found = (await rows())[index];
  if (!found) throw new Error(`no result row at index ${index}`);
  return found;
}

describe("ResultsPage", () => {
  it("lists every candidate with marks, grade and outcome", async () => {
    renderResults();
    const [first, second] = [await row(0), await row(1)];

    expect(within(first).getByText("Karim Student")).toBeInTheDocument();
    expect(within(first).getByText("A+")).toBeInTheDocument();
    expect(within(first).getByText("Pass")).toBeInTheDocument();
    expect(within(second).getByText("Fatema Akter")).toBeInTheDocument();
    expect(within(second).getByText("F")).toBeInTheDocument();
    expect(within(second).getByText("Fail")).toBeInTheDocument();
  });

  it("warns that provisional totals will still change", async () => {
    renderResults();
    // Queried by text, not by role: the loading spinner is a status region too.
    expect(
      await screen.findByText(/marking is not finished/i),
    ).toBeInTheDocument();
    expect(screen.queryByText(/final totals/i)).not.toBeInTheDocument();
  });

  it("says the totals are final once marks are locked", async () => {
    setExamResultsProvisional(false);
    renderResults();
    expect(await screen.findByText(/final totals/i)).toBeInTheDocument();
    expect(
      screen.queryByText(/marking is not finished/i),
    ).not.toBeInTheDocument();
  });

  it("flags the student whose paper is not fully marked", async () => {
    renderResults();
    const [first, second] = [await row(0), await row(1)];
    expect(within(second).getByText(/still to mark/i)).toBeInTheDocument();
    expect(within(first).queryByText(/still to mark/i)).not.toBeInTheDocument();
  });

  it("counts how many passed", async () => {
    renderResults();
    expect(await screen.findByText(/1 of 2 passed/i)).toBeInTheDocument();
  });

  it("gives the table an accessible name", async () => {
    renderResults();
    expect(await screen.findByRole("table")).toHaveAccessibleName(/Results/i);
  });

  it("renders marks in Bangla numerals when the UI is Bangla", async () => {
    await i18n.changeLanguage("bn");
    renderResults();
    const first = await row(0);
    // 4/5.00 and 80% become ৪/৫ and ৮০%
    expect(within(first).getByText(/৪/)).toBeInTheDocument();
    expect(within(first).getByText(/৮০/)).toBeInTheDocument();
  });

  it("puts the pending count in Bangla numerals too", async () => {
    // The interpolated count is easy to leave in Latin digits while every other
    // number on the row is converted, which looks like a rendering fault.
    await i18n.changeLanguage("bn");
    renderResults();
    const second = await row(1);
    const pending = within(second).getByText(/মূল্যায়ন বাকি/);
    expect(pending).toHaveTextContent("১");
    expect(pending.textContent).not.toMatch(/[0-9]/);
  });
});
