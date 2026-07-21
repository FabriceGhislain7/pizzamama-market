import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { AuthContext } from "./authContext";
import { LoginPage } from "./LoginPage";
import type { AuthContextValue } from "./authContext";

function renderLogin(loginFn = vi.fn()) {
  const value: AuthContextValue = {
    user: null,
    isAuthenticated: false,
    login: loginFn,
    logout: vi.fn(),
  };
  return render(
    <AuthContext.Provider value={value}>
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    </AuthContext.Provider>,
  );
}

describe("LoginPage", () => {
  it("renders username and password fields", () => {
    renderLogin();
    expect(screen.getByLabelText("Username")).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
  });

  it("calls login with credentials on submit", async () => {
    const user = userEvent.setup();
    const loginFn = vi.fn().mockResolvedValue(undefined);
    renderLogin(loginFn);

    await user.type(screen.getByLabelText("Username"), "mario");
    await user.type(screen.getByLabelText("Password"), "pass123");
    await user.click(screen.getByRole("button", { name: /accedi/i }));

    expect(loginFn).toHaveBeenCalledWith("mario", "pass123");
  });

  it("shows error message on login failure", async () => {
    const user = userEvent.setup();
    const loginFn = vi.fn().mockRejectedValue(new Error("Credenziali errate"));
    renderLogin(loginFn);

    await user.type(screen.getByLabelText("Username"), "x");
    await user.type(screen.getByLabelText("Password"), "y");
    await user.click(screen.getByRole("button", { name: /accedi/i }));

    expect(await screen.findByText(/errore/i)).toBeInTheDocument();
  });
});
