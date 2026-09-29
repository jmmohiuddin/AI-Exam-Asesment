/** Roster and consent (FR-ORG-03, FR-ORG-06). */
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router";
import { beforeEach, describe, expect, it } from "vitest";
import { RosterPage } from "./RosterPage";
import { SessionProvider } from "../auth/SessionProvider";
import { setAccessToken } from "../api/tokenStore";
import { MOCK_ACCESS_TOKEN, setMockConsents } from "../mocks/handlers";
import { i18n } from "../i18n";

function renderRoster() {
  setAccessToken(MOCK_ACCESS_TOKEN);
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/roster"]}>
        <SessionProvider>
          <RosterPage />
        </SessionProvider>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

function csvFile(text: string, name = "class-9.csv"): File {
  return new File([text], name, { type: "text/csv" });
}

const GOOD_CSV = [
  "Roll,Name (EN),Class,Group,Version,Shift,Section",
  "101,Karim Uddin,9,Science,BM,Day,A",
  "102,Fatema Akter,9,Science,BM,Day,A",
].join("\n");

const CSV_WITH_A_MISSING_ROLL = [
  "Roll,Name (EN),Class,Group,Version,Shift,Section",
  ",Karim Uddin,9,Science,BM,Day,A",
].join("\n");

beforeEach(async () => {
  await i18n.changeLanguage("en");
});

describe("RosterPage", () => {
  it("lists the students on the roll", async () => {
    renderRoster();

    expect(await screen.findByText("Karim Uddin")).toBeInTheDocument();
    expect(screen.getByText(/9-A-101/)).toBeInTheDocument();
  });

  it("shows a student who has consented to nothing as consented to nothing", async () => {
    renderRoster();

    // Awaited per box: the consent state is a second request, so the row renders
    // before the checkboxes exist.
    for (const type of ["CT-1", "CT-2", "CT-3"]) {
      const box = await screen.findByRole("checkbox", {
        name: new RegExp(type),
      });
      expect(box).not.toBeChecked();
    }
  });

  it("says that a student without CT-2 is marked without AI", async () => {
    renderRoster();

    expect(await screen.findByText("Marked without AI")).toBeInTheDocument();
  });

  it("stops saying so once CT-2 is recorded", async () => {
    const user = userEvent.setup();
    renderRoster();

    await user.click(await screen.findByRole("checkbox", { name: /CT-2/ }));

    await waitFor(() =>
      expect(screen.queryByText("Marked without AI")).not.toBeInTheDocument(),
    );
  });

  it("reflects a consent that was already on file", async () => {
    setMockConsents({ "CT-1": true, "CT-2": true });
    renderRoster();

    expect(await screen.findByRole("checkbox", { name: /CT-2/ })).toBeChecked();
    expect(screen.getByRole("checkbox", { name: /CT-3/ })).not.toBeChecked();
  });

  it("withdrawing a consent unticks it", async () => {
    setMockConsents({ "CT-2": true });
    const user = userEvent.setup();
    renderRoster();
    const box = await screen.findByRole("checkbox", { name: /CT-2/ });
    expect(box).toBeChecked();

    await user.click(box);

    await waitFor(() => expect(box).not.toBeChecked());
  });
});

describe("RosterPage import", () => {
  it("reports what a clean file would do without importing it", async () => {
    const user = userEvent.setup();
    renderRoster();
    const input = await screen.findByLabelText("Choose a roster file");

    await user.upload(input, csvFile(GOOD_CSV));

    expect(
      await screen.findByText(/Ready to import 2 rows/),
    ).toBeInTheDocument();
    expect(screen.getByText(/Nothing has been saved yet/)).toBeInTheDocument();
  });

  it("offers the import button only once the file is clean", async () => {
    const user = userEvent.setup();
    renderRoster();
    const input = await screen.findByLabelText("Choose a roster file");

    await user.upload(input, csvFile(CSV_WITH_A_MISSING_ROLL));

    expect(
      await screen.findByRole("button", { name: "Import these students" }),
    ).toBeDisabled();
  });

  it("shows each problem against the row it came from", async () => {
    const user = userEvent.setup();
    renderRoster();
    const input = await screen.findByLabelText("Choose a roster file");

    await user.upload(input, csvFile(CSV_WITH_A_MISSING_ROLL));

    expect(await screen.findByText("Roll is required.")).toBeInTheDocument();
  });

  it("imports the students when confirmed", async () => {
    const user = userEvent.setup();
    renderRoster();
    const input = await screen.findByLabelText("Choose a roster file");
    await user.upload(input, csvFile(GOOD_CSV));

    await user.click(
      await screen.findByRole("button", { name: "Import these students" }),
    );

    expect(
      await screen.findByText(/2 students added, 0 updated/),
    ).toBeInTheDocument();
  });

  it("refuses a file whose header it cannot read, rather than importing blanks", async () => {
    const user = userEvent.setup();
    renderRoster();
    const input = await screen.findByLabelText("Choose a roster file");

    await user.upload(input, csvFile("x,y\n1,2"));

    expect(
      await screen.findByText(/No column in this file was recognised/),
    ).toBeInTheDocument();
  });

  it("names the columns it ignored", async () => {
    const user = userEvent.setup();
    renderRoster();
    const input = await screen.findByLabelText("Choose a roster file");

    await user.upload(
      input,
      csvFile("Roll,Blood Group,Class,Section\n101,B+,9,A"),
    );

    expect(
      await screen.findByText(/These columns were ignored: Blood Group/),
    ).toBeInTheDocument();
  });
});

describe("RosterPage in Bangla", () => {
  it("shows the report problem in Bangla", async () => {
    await i18n.changeLanguage("bn");
    const user = userEvent.setup();
    renderRoster();
    const input = await screen.findByLabelText("তালিকা ফাইল নির্বাচন করুন");

    await user.upload(input, csvFile(CSV_WITH_A_MISSING_ROLL));

    expect(await screen.findByText("রোল নম্বর দিতে হবে।")).toBeInTheDocument();
  });

  it("shows the row number in Bangla numerals", async () => {
    await i18n.changeLanguage("bn");
    const user = userEvent.setup();
    renderRoster();
    const input = await screen.findByLabelText("তালিকা ফাইল নির্বাচন করুন");

    await user.upload(input, csvFile(CSV_WITH_A_MISSING_ROLL));

    // Scoped to the report table: the student list is on the page too.
    const report = await screen.findByRole("table", {
      name: "তালিকা ফাইলে পাওয়া সমস্যা",
    });
    expect(within(report).getByText("১")).toBeInTheDocument();
  });
});
