import { render, screen, fireEvent } from "@testing-library/react";
import { vi, test, expect } from "vitest";
import App from "./App";

const inc = { id: 1, title: "t", description: "d", detected_at: "2026-01-01T00:00:00", created_at: "2026-01-01T00:00:00", reporter: "r", affected_system: "s", incident_type: null, severity: "Low", stage: "Detection", personal_data_involved: false, affected_data_categories: [], affected_people_estimate: null, actions: [], assessments: [], reports: [], lessons: [], audit_events: [], evidence: [] };

vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => [inc] }));

test("mobile hamburger opens sidebar", () => {
  render(<App />);
  const btn = screen.getByLabelText("Open navigation");
  fireEvent.click(btn);
  expect(screen.getByLabelText("Close navigation")).toBeInTheDocument();
});

test("incident detail tab switching", async () => {
  render(<App />);
  const navBtns = screen.getAllByRole("button", { name: "Incidents" });
  fireEvent.click(navBtns[0]);
  const row = await screen.findByText("#1");
  fireEvent.click(row);
  const actionsTab = await screen.findByText("actions");
  fireEvent.click(actionsTab);
  expect(await screen.findByText("Add Action")).toBeInTheDocument();
});
