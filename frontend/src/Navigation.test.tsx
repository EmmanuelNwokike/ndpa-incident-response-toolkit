import { render, screen, fireEvent } from "@testing-library/react";
import { vi, test, expect } from "vitest";
import App from "./App";

vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => [] }));

test("navigates to playbook page", async () => {
  render(<App />);
  fireEvent.click(screen.getByText("Playbook"));
  expect(await screen.findByText("Incident Response Playbook")).toBeInTheDocument();
});

test("navigates to tabletop page", async () => {
  render(<App />);
  const btns = screen.getAllByRole("button", { name: "Tabletop Exercises" });
  fireEvent.click(btns[0]);
  expect(await screen.findByText("No scenarios.")).toBeInTheDocument();
});

test("shows empty state on incidents page", async () => {
  render(<App />);
  fireEvent.click(screen.getAllByText("Incidents")[0]);
  expect(await screen.findByText("No incidents yet.")).toBeInTheDocument();
});
