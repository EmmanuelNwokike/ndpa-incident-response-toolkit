const BASE = "http://localhost:8000";

export async function api(path: string, options?: RequestInit) {
  const res = await fetch(BASE + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export const listIncidents = () => api("/incidents");
export const getIncident = (id: number) => api(`/incidents/${id}`);
export const createIncident = (data: any) => api("/incidents", { method: "POST", body: JSON.stringify(data) });
export const updateIncident = (id: number, data: any) => api(`/incidents/${id}`, { method: "PATCH", body: JSON.stringify(data) });
export const addAction = (id: number, data: any) => api(`/incidents/${id}/actions`, { method: "POST", body: JSON.stringify(data) });
export const createAssessment = (id: number, data: any) => api(`/incidents/${id}/assessment`, { method: "POST", body: JSON.stringify(data) });
export const getReport = (id: number) => api(`/incidents/${id}/report`);
export const updateReport = (id: number, reportId: number, text: string) => api(`/incidents/${id}/report/${reportId}`, { method: "PATCH", body: JSON.stringify({ draft_text: text }) });
export const addLesson = (id: number, data: any) => api(`/incidents/${id}/lessons`, { method: "POST", body: JSON.stringify(data) });
export const listLessons = (id: number) => api(`/incidents/${id}/lessons`);
export const getPlaybook = () => api("/playbook");
export const getTabletop = () => api("/tabletop/scenarios");

export const addEvidence = (id: number, data: any) => api(`/incidents/${id}/evidence`, { method: "POST", body: JSON.stringify(data) });
export const listEvidence = (id: number) => api(`/incidents/${id}/evidence`);
export const getNotificationDraft = (id: number) => api(`/incidents/${id}/notification-draft`);
export const createTabletopRun = (data: any) => api("/tabletop/runs", { method: "POST", body: JSON.stringify(data) });
export const listTabletopRuns = () => api("/tabletop/runs");
export const getActionDefinitions = () => api("/actions/definitions");
export const getAssessmentQuestions = () => api("/assessment/questions");
