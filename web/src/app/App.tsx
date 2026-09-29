import type { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router";
import { I18nextProvider } from "react-i18next";
import { i18n } from "../i18n";
import { SessionProvider } from "../auth/SessionProvider";
import { RequireAuth } from "../auth/RequireAuth";
import { HomePage } from "../pages/HomePage";
import { LoginPage } from "../pages/LoginPage";
import { ResultsPage } from "../pages/ResultsPage";
import { ReviewPage } from "../pages/ReviewPage";
import { RosterPage } from "../pages/RosterPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Marking data is shared and changes under the teacher's feet; a stale
      // suggestion is worse than a refetch. Auth errors are handled centrally,
      // so retrying them here would only delay the redirect to /login.
      staleTime: 10_000,
      retry: (failureCount, error) => {
        const status = (error as { status?: number }).status;
        if (status !== undefined && status < 500) return false;
        return failureCount < 2;
      },
    },
  },
});

function SkipLink(): ReactNode {
  const { t } = useTranslation();
  return (
    <a className="skip-link" href="#main">
      {t("skipLink")}
    </a>
  );
}

export function App(): ReactNode {
  return (
    <I18nextProvider i18n={i18n}>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <SessionProvider>
            <SkipLink />
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route element={<RequireAuth />}>
                <Route path="/" element={<HomePage />} />
                <Route path="/review/:scriptId" element={<ReviewPage />} />
                <Route
                  path="/exams/:examId/results"
                  element={<ResultsPage />}
                />
                <Route path="/roster" element={<RosterPage />} />
              </Route>
            </Routes>
          </SessionProvider>
        </BrowserRouter>
      </QueryClientProvider>
    </I18nextProvider>
  );
}
