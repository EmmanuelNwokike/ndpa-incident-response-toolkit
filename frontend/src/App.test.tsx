import { render, screen } from "@testing-library/react";
import { vi, test, expect } from "vitest";
import App from "./App";

vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => [] }));

test("renders sidebar navigation", () => {
  render(<App />);
  expect(screen.getByText("NDPA Toolkit")).toBeInTheDocument();
  expect(screen.getAllByText("Dashboard").length).toBeGreaterThan(0);
  expect(screen.getByText("Playbook")).toBeInTheDocument();
});
