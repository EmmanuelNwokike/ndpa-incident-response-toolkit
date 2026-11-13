import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { vi, test, expect } from "vitest";
import App from "./App";

const inc = { id: 1, title: "t", description: "d", detected_at: "2026-01-01T00:00:00", created_at: "2026-01-01T00:00:00", reporter: "r", affected_system: "s", incident_type: null, severity: null, stage: "Detection", personal_data_involved: false, affected_data_categories: [], affected_people_estimate: null, actions: [], assessments: [], reports: [], lessons: [], audit_events: [], evidence: [] };

test("advance button moves stage", async () => {
  let stage = "Detection";
  const fetchMock = vi.fn().mockImplementation((url: string, opts?: any) => {
    if (url.endsWith("/incidents") && (!opts || !opts.method)) {
      return Promise.resolve({ ok: true, json: async () => [{ ...inc, stage }] });
    }
    if (url.includes("/incidents/1") && opts?.method === "PATCH") {
      stage = "Triage";
      return Promise.resolve({ ok: true, json: async () => ({ ...inc, stage }) });
    }
    return Promise.resolve({ ok: true, json: async () => [] });
  });
  vi.stubGlobal("fetch", fetchMock);
  render(<App />);
  fireEvent.click(screen.getByText("Incidents"));
  const btn = await screen.findByText("Advance");
  fireEvent.click(btn);
  await waitFor(() => expect(screen.getAllByText("Triage").length).toBeGreaterThan(0));
});
