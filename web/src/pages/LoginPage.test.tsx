/** Sign-in, including the OTP step a new device has to pass (08 §5.2). */
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router";
import { describe, expect, it } from "vitest";
import { LoginPage } from "./LoginPage";
import { SessionProvider } from "../auth/SessionProvider";
import { DEVICE_ID_KEY } from "../auth/device";
import {
  MOCK_DEVICE_ID,
  MOCK_MOBILE,
  MOCK_OTP_CODE,
  MOCK_PASSWORD,
} from "../mocks/handlers";

function renderLogin() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>
        <SessionProvider>
          <LoginPage />
        </SessionProvider>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

async function submitPassword(user: ReturnType<typeof userEvent.setup>) {
  await user.type(screen.getByLabelText(/mobile number/i), MOCK_MOBILE);
  await user.type(screen.getByLabelText(/^password$/i), MOCK_PASSWORD);
  await user.click(screen.getByRole("button", { name: /^sign in$/i }));
}

describe("LoginPage", () => {
  it("asks for a code when the device is unknown", async () => {
    const user = userEvent.setup();
    renderLogin();
    await submitPassword(user);

    expect(
      await screen.findByRole("heading", { name: /verification code/i }),
    ).toBeInTheDocument();
    // No token may exist before the second factor is proven.
    expect(window.localStorage.getItem(DEVICE_ID_KEY)).toBeNull();
  });

  it("signs in with the right code and remembers the device", async () => {
    const user = userEvent.setup();
    renderLogin();
    await submitPassword(user);

    await screen.findByLabelText(/verification code/i);
    await user.type(screen.getByLabelText(/verification code/i), MOCK_OTP_CODE);
    await user.click(screen.getByRole("button", { name: /^verify$/i }));

    await waitFor(() => {
      expect(window.localStorage.getItem(DEVICE_ID_KEY)).toBe(MOCK_DEVICE_ID);
    });
  });

  it("reports a wrong code and clears the field", async () => {
    const user = userEvent.setup();
    renderLogin();
    await submitPassword(user);

    const field = await screen.findByLabelText(/verification code/i);
    await user.type(field, "000000");
    await user.click(screen.getByRole("button", { name: /^verify$/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/incorrect/i);
    expect(field).toHaveValue("");
    expect(window.localStorage.getItem(DEVICE_ID_KEY)).toBeNull();
  });

  it("refuses to submit a short code without calling the server", async () => {
    const user = userEvent.setup();
    renderLogin();
    await submitPassword(user);

    await user.type(await screen.findByLabelText(/verification code/i), "123");
    await user.click(screen.getByRole("button", { name: /^verify$/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/all 6 digits/i);
  });

  it("keeps non-digits out of the code field", async () => {
    const user = userEvent.setup();
    renderLogin();
    await submitPassword(user);

    const field = await screen.findByLabelText(/verification code/i);
    await user.type(field, "12ab34cd56");
    expect(field).toHaveValue("123456");
  });

  it("skips the code when the browser already knows the device", async () => {
    window.localStorage.setItem(DEVICE_ID_KEY, MOCK_DEVICE_ID);
    const user = userEvent.setup();
    renderLogin();
    await submitPassword(user);

    await waitFor(() => {
      expect(
        screen.queryByRole("heading", { name: /verification code/i }),
      ).not.toBeInTheDocument();
    });
  });

  it("lets the user go back and correct the number", async () => {
    const user = userEvent.setup();
    renderLogin();
    await submitPassword(user);

    await screen.findByRole("heading", { name: /verification code/i });
    await user.click(
      screen.getByRole("button", { name: /use a different number/i }),
    );

    expect(await screen.findByLabelText(/mobile number/i)).toBeInTheDocument();
  });

  it("rejects a wrong password before any code is sent", async () => {
    const user = userEvent.setup();
    renderLogin();
    await user.type(screen.getByLabelText(/mobile number/i), MOCK_MOBILE);
    await user.type(screen.getByLabelText(/^password$/i), "wrong-password");
    await user.click(screen.getByRole("button", { name: /^sign in$/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/incorrect/i);
    expect(
      screen.queryByRole("heading", { name: /verification code/i }),
    ).not.toBeInTheDocument();
  });
});
