import { useEffect, useState } from "react";
import * as api from "./api";
import { LayoutDashboard, FileText, BookOpen, ClipboardCheck, FileBarChart, Gamepad2, Lightbulb, Loader2 } from "lucide-react";

const STAGES = ["Detection", "Triage", "Containment", "Investigation", "Reporting"];
const INCIDENT_ROLES = ["System Administrator", "Incident Response Manager", "Security Analyst", "IT Support Officer", "Data Protection Officer (DPO)", "Compliance Officer"];
type View = "dashboard" | "incidents" | "playbook" | "assessment" | "reports" | "tabletop" | "lessons";

const severityColor = (s: string) => s === "High" ? "bg-red-100 text-red-700" : s === "Medium" ? "bg-amber-100 text-amber-700" : s === "Low" ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-600";

export default function App() {
  const [view, setView] = useState<View>("dashboard");
  const [incidents, setIncidents] = useState<any[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  const loadList = async () => {
    setLoading(true);
    try { setIncidents(await api.listIncidents()); setError(""); }
    catch (e: any) { setError(e.message); }
    finally { setLoading(false); }
  };
  useEffect(() => { loadList(); }, []);

  const selectIncident = async (id: number) => {
    try { const inc = await api.getIncident(id); setSelectedId(id);
      setIncidents((prev) => prev.map((x) => x.id === id ? inc : x));
    } catch (e: any) { setError(e.message); }
  };

  const nav = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "incidents", label: "Incidents", icon: FileText },
    { id: "playbook", label: "Playbook", icon: BookOpen },
    { id: "assessment", label: "Notification Assessment", icon: ClipboardCheck },
    { id: "reports", label: "Reports & Templates", icon: FileBarChart },
    { id: "tabletop", label: "Tabletop Exercises", icon: Gamepad2 },
    { id: "lessons", label: "Lessons Learned", icon: Lightbulb },
  ] as const;

  return (
    <div className="flex min-h-screen bg-[#F5F7FA]">
      {mobileOpen && <div className="fixed inset-0 bg-black/40 z-40 md:hidden" onClick={() => setMobileOpen(false)} />}
      <aside className={`w-64 bg-[#142238] text-white shrink-0 flex flex-col z-50 ${mobileOpen ? "fixed inset-y-0 left-0" : "hidden md:flex"}`}>
        <div className="p-5 border-b border-white/10 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-bold">NDPA Toolkit</h1>
            <p className="text-xs text-white/60">Incident Response</p>
          </div>
          <button className="md:hidden text-white" onClick={() => setMobileOpen(false)} aria-label="Close navigation">✕</button>
        </div>
        <nav className="p-3 space-y-1 flex-1">
          {nav.map((n) => {
            const Icon = n.icon;
            return (
              <button key={n.id} onClick={() => { setView(n.id as View); setMobileOpen(false); }}
                className={`w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm ${view === n.id ? "bg-[#2563EB] text-white" : "text-white/80 hover:bg-white/10"}`}>
                <Icon size={18} /> {n.label}
              </button>
            );
          })}
        </nav>
      </aside>
      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button className="md:hidden" onClick={() => setMobileOpen(true)} aria-label="Open navigation">☰</button>
            <h2 className="text-lg font-semibold text-[#142238]">{nav.find((n) => n.id === view)?.label}</h2>
          </div>
          <div className="text-xs text-gray-500">Nigerian SME Incident Toolkit</div>
        </header>
        <main className="flex-1 p-6 overflow-auto">
          {error && <div className="mb-3 text-red-600 text-sm">{error}</div>}
          {loading && <div className="mb-3 text-gray-500 text-sm flex items-center gap-2"><Loader2 size={14} className="animate-spin" /> Loading...</div>}
          {view === "dashboard" && <Dashboard incidents={incidents} />}
          {view === "incidents" && <IncidentsView incidents={incidents} onRefresh={loadList} setError={setError} />}
          {view === "playbook" && <PlaybookView />}
          {view === "assessment" && <AssessmentView incidents={incidents} selectedId={selectedId} onSelect={selectIncident} />}
          {view === "reports" && <ReportsView incidents={incidents} selectedId={selectedId} onSelect={selectIncident} />}
          {view === "tabletop" && <TabletopView />}
          {view === "lessons" && <LessonsView incidents={incidents} selectedId={selectedId} onSelect={selectIncident} />}
        </main>
      </div>
    </div>
  );
}

function Dashboard({ incidents }: any) {
  const byStage: Record<string, number> = {};
  STAGES.forEach((s) => (byStage[s] = 0));
  incidents.forEach((i: any) => { if (byStage[i.stage] !== undefined) byStage[i.stage]++; });
  const bySeverity: Record<string, number> = {};
  incidents.forEach((i: any) => { const k = i.severity || "Unspecified"; bySeverity[k] = (bySeverity[k] || 0) + 1; });
  const recent = [...incidents].sort((a, b) => b.id - a.id).slice(0, 5);
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <Kpi label="Total incidents" value={incidents.length} />
        {STAGES.map((s) => <Kpi key={s} label={s} value={byStage[s]} />)}
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-white border rounded-lg p-4">
          <h3 className="font-semibold text-[#142238] mb-3">Severity distribution</h3>
          {Object.keys(bySeverity).length === 0 && <Empty text="No data" />}
          {Object.entries(bySeverity).map(([k, v]) => (
            <div key={k} className="flex justify-between py-1 text-sm border-b last:border-0"><span>{k}</span><span className="font-medium">{v}</span></div>
          ))}
        </div>
        <div className="bg-white border rounded-lg p-4">
          <h3 className="font-semibold text-[#142238] mb-3">Recent activity</h3>
          {recent.length === 0 && <Empty text="No incidents" />}
          {recent.map((i: any) => (
            <div key={i.id} className="py-1 text-sm border-b last:border-0 flex justify-between">
              <span>#{i.id} {i.title}</span><span className="text-gray-500">{i.stage}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function Kpi({ label, value }: any) {
  return (
    <div className="bg-white border rounded-lg p-4">
      <div className="text-xs text-gray-500">{label}</div>
      <div className="text-2xl font-bold text-[#142238]">{value}</div>
    </div>
  );
}

function Empty({ text }: any) { return <div className="text-gray-400 text-sm">{text}</div>; }

function IncidentsView({ incidents, onRefresh, setError }: any) {
  const [form, setForm] = useState({ title: "", description: "", detected_at: new Date().toISOString().slice(0, 16), reporter: "", affected_system: "", severity: "", personal_data_involved: false, affected_data_categories: "", affected_people_estimate: "" });
  const [err, setErr] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [advancing, setAdvancing] = useState<number | null>(null);
  const [detailId, setDetailId] = useState<number | null>(null);

  const submit = async (e: any) => {
    e.preventDefault();
    try {
      await api.createIncident({
        title: form.title, description: form.description, detected_at: form.detected_at + ":00",
        reporter: form.reporter, affected_system: form.affected_system, severity: form.severity || null,
        personal_data_involved: form.personal_data_involved,
        affected_data_categories: form.affected_data_categories.split(",").map((s: string) => s.trim()).filter(Boolean),
        affected_people_estimate: form.affected_people_estimate ? Number(form.affected_people_estimate) : null,
      });
      setForm({ ...form, title: "", description: "" });
      setShowForm(false);
      onRefresh();
    } catch (e: any) { setErr(e.message); }
  };

  const advance = async (id: number, stage: string) => {
    if (advancing) return;
    setAdvancing(id);
    try { await api.updateIncident(id, { stage }); await onRefresh(); }
    catch (e: any) { setError(e.message); }
    finally { setAdvancing(null); }
  };

  const detail = incidents.find((i: any) => i.id === detailId);

  if (detail) return <IncidentDetail incident={detail} onBack={() => setDetailId(null)} onRefresh={onRefresh} />;

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-[#142238]">Incidents</h2>
        <button className="bg-[#2563EB] text-white px-4 py-2 rounded-md text-sm" onClick={() => setShowForm(!showForm)}>{showForm ? "Cancel" : "New Incident"}</button>
      </div>
      {err && <div className="text-red-600 text-sm">{err}</div>}
      {showForm && (
        <form onSubmit={submit} className="bg-white border rounded-lg p-4 space-y-3">
          <input className="border p-2 w-full rounded" placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
          <textarea className="border p-2 w-full rounded" placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} required />
          <input type="datetime-local" className="border p-2 w-full rounded" value={form.detected_at} onChange={(e) => setForm({ ...form, detected_at: e.target.value })} required />
          <input className="border p-2 w-full rounded" placeholder="Reporter" value={form.reporter} onChange={(e) => setForm({ ...form, reporter: e.target.value })} required />
          <input className="border p-2 w-full rounded" placeholder="Affected system" value={form.affected_system} onChange={(e) => setForm({ ...form, affected_system: e.target.value })} required />
          <select className="border p-2 w-full rounded" value={form.severity} onChange={(e) => setForm({ ...form, severity: e.target.value })} required>
            <option value="" disabled>Select severity</option>
            <option value="High">High</option><option value="Medium">Medium</option><option value="Low">Low</option>
          </select>
          <input className="border p-2 w-full rounded" placeholder="Affected data categories (comma)" value={form.affected_data_categories} onChange={(e) => setForm({ ...form, affected_data_categories: e.target.value })} />
          <input className="border p-2 w-full rounded" placeholder="Affected people estimate" value={form.affected_people_estimate} onChange={(e) => setForm({ ...form, affected_people_estimate: e.target.value })} />
          <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={form.personal_data_involved} onChange={(e) => setForm({ ...form, personal_data_involved: e.target.checked })} /> Personal data involved</label>
          <button className="bg-[#2563EB] text-white px-4 py-2 rounded-md text-sm" type="submit">Create</button>
        </form>
      )}
      <div className="bg-white border rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="p-3 text-left">ID</th><th className="p-3 text-left">Title</th><th className="p-3 text-left">Severity</th><th className="p-3 text-left">Stage</th><th className="p-3 text-left">Reporter</th><th className="p-3 text-left">Detected</th><th className="p-3"></th>
            </tr>
          </thead>
          <tbody>
            {incidents.length === 0 && <tr><td colSpan={7} className="p-4 text-gray-400 text-center">No incidents yet.</td></tr>}
            {incidents.map((i: any) => (
              <tr key={i.id} className="border-t hover:bg-gray-50 cursor-pointer" onClick={() => setDetailId(i.id)}>
                <td className="p-3">#{i.id}</td>
                <td className="p-3 font-medium">{i.title}</td>
                <td className="p-3"><span className={`px-2 py-0.5 rounded text-xs ${severityColor(i.severity)}`}>{i.severity || "Unspecified"}</span></td>
                <td className="p-3">{i.stage}</td>
                <td className="p-3">{i.reporter}</td>
                <td className="p-3 text-gray-500">{new Date(i.detected_at).toLocaleDateString()}</td>
                <td className="p-3">
                  {STAGES.indexOf(i.stage) < STAGES.length - 1 ? (
                    <button className="bg-green-600 text-white px-2 py-1 rounded text-xs" disabled={advancing === i.id} onClick={(e) => { e.stopPropagation(); advance(i.id, STAGES[STAGES.indexOf(i.stage) + 1]); }}>
                      {advancing === i.id ? "..." : "Advance"}
                    </button>
                  ) : <span className="text-xs text-gray-400">Final</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function IncidentDetail({ incident, onBack, onRefresh }: any) {
  const [tab, setTab] = useState("overview");
  const [note, setNote] = useState("");
  const [definitions, setDefinitions] = useState<any>(null);
  const [action, setAction] = useState({ stage: incident.stage, action: "", owner: "", outcome: "", remarks: "" });
  const [answers, setAnswers] = useState("{}");
  const [report, setReport] = useState<any>(null);
  const [lesson, setLesson] = useState({ root_cause: "", improvement: "", follow_up: "" });
  const [evidence, setEvidence] = useState({ description: "", source: "", collected_by: "", notes: "" });
  const [err, setErr] = useState("");
  useEffect(() => { api.getActionDefinitions().then(setDefinitions).catch(() => {}); }, []);

  const wrap = (fn: () => Promise<void>) => async () => { try { await fn(); } catch (e: any) { setErr(e.message); } };
  const submitNote = wrap(async () => { await api.updateIncident(incident.id, { notes: note }); setNote(""); await onRefresh(); });
  const submitAction = wrap(async () => { await api.addAction(incident.id, action); setAction({ stage: incident.stage, action: "", owner: "", outcome: "", remarks: "" }); await onRefresh(); });
  const submitAssessment = wrap(async () => { let a: any; try { a = JSON.parse(answers); } catch { a = {}; } await api.createAssessment(incident.id, { answers: a, reviewer: "reviewer" }); await onRefresh(); });
  const genReport = wrap(async () => { const r = await api.getReport(incident.id); setReport(r); await onRefresh(); });
  const genNotif = wrap(async () => { const r = await api.getNotificationDraft(incident.id); setReport({ id: report?.id, draft_text: r.draft_text }); });
  const saveReport = wrap(async () => { if (report?.id) { await api.updateReport(incident.id, report.id, report.draft_text); await onRefresh(); } });
  const submitLesson = wrap(async () => { await api.addLesson(incident.id, lesson); setLesson({ root_cause: "", improvement: "", follow_up: "" }); await onRefresh(); });
  const submitEvidence = wrap(async () => { await api.addEvidence(incident.id, evidence); setEvidence({ description: "", source: "", collected_by: "", notes: "" }); await onRefresh(); });

  const tabs = ["overview", "actions", "evidence", "assessment", "report", "lessons", "timeline"];

  return (
    <div className="space-y-4">
      <button className="text-[#2563EB] text-sm" onClick={onBack}>← Back to incidents</button>
      <div className="bg-white border rounded-lg p-4">
        <h2 className="text-xl font-bold text-[#142238]">#{incident.id} {incident.title}</h2>
        <div className="text-sm text-gray-600 mt-1">Stage: <b>{incident.stage}</b> | Severity: <span className={`px-2 py-0.5 rounded text-xs ${severityColor(incident.severity)}`}>{incident.severity || "Unspecified"}</span></div>
        <p className="text-sm text-gray-700 mt-2">{incident.description}</p>
      </div>
      {err && <div className="text-red-600 text-sm">{err}</div>}
      <div className="flex gap-2 flex-wrap">
        {tabs.map((t) => (
          <button key={t} onClick={() => setTab(t)} className={`px-3 py-1.5 rounded-md text-sm capitalize ${tab === t ? "bg-[#2563EB] text-white" : "bg-white border"}`}>{t}</button>
        ))}
      </div>

      {tab === "overview" && (
        <div className="bg-white border rounded-lg p-4 text-sm space-y-1">
          <div><b>Reporter:</b> {incident.reporter}</div>
          <div><b>Affected system:</b> {incident.affected_system}</div>
          <div><b>Personal data involved:</b> {String(incident.personal_data_involved)}</div>
          <div><b>Affected categories:</b> {(incident.affected_data_categories || []).join(", ") || "None"}</div>
          <div><b>Affected people:</b> {incident.affected_people_estimate ?? "Unknown"}</div>
          <div><b>Detected at:</b> {new Date(incident.detected_at).toLocaleString()}</div>
        </div>
      )}

      {tab === "actions" && (
        <div className="bg-white border rounded-lg p-4 space-y-3">
          <div className="flex flex-col gap-2">
            <select className="border p-2 rounded text-sm" value={action.stage} onChange={(e) => setAction({ stage: e.target.value, action: "", owner: action.owner, outcome: "", remarks: action.remarks })}>
              {STAGES.slice(0, STAGES.indexOf(incident.stage) + 1).map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
            <select className="border p-2 rounded text-sm" value={action.action} onChange={(e) => setAction({ ...action, action: e.target.value, outcome: "" })} required>
              <option value="" disabled>Select action</option>
              {(definitions?.actions?.[action.stage] ? Object.keys(definitions.actions[action.stage]) : []).map((a: string) => <option key={a} value={a}>{a}</option>)}
            </select>
            <select className="border p-2 rounded text-sm" value={action.owner} onChange={(e) => setAction({ ...action, owner: e.target.value })} required>
              <option value="" disabled>Select action owner</option>
              {INCIDENT_ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
            </select>
            <select className="border p-2 rounded text-sm" value={action.outcome} onChange={(e) => setAction({ ...action, outcome: e.target.value })} required>
              <option value="" disabled>Select outcome</option>
              {(definitions?.actions?.[action.stage]?.[action.action] || []).map((o: string) => <option key={o} value={o}>{o}</option>)}
            </select>
            <textarea className="border p-2 rounded text-sm" rows={3} maxLength={2000} placeholder="Enter additional observations, challenges encountered, evidence references, or follow-up actions." value={action.remarks} onChange={(e) => setAction({ ...action, remarks: e.target.value })} />
            <button className="bg-[#2563EB] text-white px-3 py-1.5 rounded-md text-sm w-fit" onClick={submitAction}>Add Action</button>
          </div>
          <ul className="list-disc ml-6 text-sm space-y-1">
            {(incident.actions || []).map((a: any) => <li key={a.id}>[{a.stage}] {a.action} — {a.owner || "n/a"} ({a.outcome || "n/a"}){a.remarks ? ` Remarks: ${a.remarks}` : ""}</li>)}
          </ul>
          {(incident.actions || []).length === 0 && <div className="text-gray-400 text-sm">No actions recorded.</div>}
        </div>
      )}

      {tab === "evidence" && (
        <div className="bg-white border rounded-lg p-4 space-y-3">
          <div className="flex flex-col gap-2">
            <input className="border p-2 rounded text-sm" placeholder="description" value={evidence.description} onChange={(e) => setEvidence({ ...evidence, description: e.target.value })} />
            <input className="border p-2 rounded text-sm" placeholder="source" value={evidence.source} onChange={(e) => setEvidence({ ...evidence, source: e.target.value })} />
            <input className="border p-2 rounded text-sm" placeholder="collected by" value={evidence.collected_by} onChange={(e) => setEvidence({ ...evidence, collected_by: e.target.value })} />
            <input className="border p-2 rounded text-sm" placeholder="notes" value={evidence.notes} onChange={(e) => setEvidence({ ...evidence, notes: e.target.value })} />
            <button className="bg-[#2563EB] text-white px-3 py-1.5 rounded-md text-sm w-fit" onClick={submitEvidence}>Add Evidence</button>
          </div>
          <ul className="list-disc ml-6 text-sm space-y-1">
            {(incident.evidence || []).map((e: any) => <li key={e.id}>{e.description} — source: {e.source || "n/a"}, by: {e.collected_by || "n/a"}</li>)}
          </ul>
          {(incident.evidence || []).length === 0 && <div className="text-gray-400 text-sm">No evidence recorded.</div>}
        </div>
      )}

      {tab === "assessment" && (
        <div className="bg-white border rounded-lg p-4 space-y-3">
          <p className="text-sm text-gray-600">Rule-based review aid only. Results are "Needs review"; no legal reportability is determined.</p>
          <textarea className="border p-2 w-full rounded text-sm" rows={4} value={answers} onChange={(e) => setAnswers(e.target.value)} />
          <button className="bg-[#2563EB] text-white px-3 py-1.5 rounded-md text-sm" onClick={submitAssessment}>Submit Assessment</button>
          {(incident.assessments || []).map((a: any) => (
            <div key={a.id} className="border p-2 rounded text-sm"><b>{a.outcome}</b> — missing: {(a.missing_questions || []).join(", ") || "none"}</div>
          ))}
        </div>
      )}

      {tab === "report" && (
        <div className="bg-white border rounded-lg p-4 space-y-3">
          <div className="flex gap-2">
            <button className="bg-gray-600 text-white px-3 py-1.5 rounded-md text-sm" onClick={genReport}>Generate Incident Report</button>
            <button className="bg-gray-500 text-white px-3 py-1.5 rounded-md text-sm" onClick={genNotif}>Generate Notification Draft</button>
          </div>
          {report && (
            <div>
              <textarea className="border p-2 w-full rounded text-xs" rows={14} value={report.draft_text} onChange={(e) => setReport({ ...report, draft_text: e.target.value })} />
              {report.id && <button className="bg-[#2563EB] text-white px-3 py-1.5 rounded-md text-sm mt-2" onClick={saveReport}>Save draft</button>}
            </div>
          )}
          {!report && (incident.reports || []).length > 0 && <pre className="bg-gray-50 p-2 text-xs whitespace-pre-wrap rounded">{incident.reports[incident.reports.length - 1].draft_text}</pre>}
        </div>
      )}

      {tab === "lessons" && (
        <div className="bg-white border rounded-lg p-4 space-y-3">
          <div className="space-y-2">
            <input className="border p-2 w-full rounded text-sm" placeholder="root cause" value={lesson.root_cause} onChange={(e) => setLesson({ ...lesson, root_cause: e.target.value })} />
            <input className="border p-2 w-full rounded text-sm" placeholder="improvement" value={lesson.improvement} onChange={(e) => setLesson({ ...lesson, improvement: e.target.value })} />
            <input className="border p-2 w-full rounded text-sm" placeholder="follow up" value={lesson.follow_up} onChange={(e) => setLesson({ ...lesson, follow_up: e.target.value })} />
            <button className="bg-[#2563EB] text-white px-3 py-1.5 rounded-md text-sm" onClick={submitLesson}>Add Lesson</button>
          </div>
          <ul className="list-disc ml-6 text-sm space-y-1">
            {(incident.lessons || []).map((l: any) => <li key={l.id}>{l.root_cause || "-"} → {l.improvement || "-"}</li>)}
          </ul>
          {(incident.lessons || []).length === 0 && <div className="text-gray-400 text-sm">No lessons recorded.</div>}
        </div>
      )}

      {tab === "timeline" && (
        <div className="bg-white border rounded-lg p-4">
          <ul className="list-disc ml-6 text-xs space-y-1">
            {(incident.audit_events || []).map((a: any) => <li key={a.id}>{new Date(a.timestamp).toLocaleString()} — {a.event_type}: {a.details || ""}</li>)}
          </ul>
          {(incident.audit_events || []).length === 0 && <div className="text-gray-400 text-sm">No events recorded.</div>}
        </div>
      )}

      {tab === "overview" && (
        <div className="bg-white border rounded-lg p-4">
          <div className="flex gap-2">
            <button className="bg-gray-600 text-white px-3 py-1.5 rounded-md text-sm" onClick={submitNote}>Add note</button>
            <input className="border p-2 flex-1 rounded text-sm" value={note} onChange={(e) => setNote(e.target.value)} placeholder="note" />
          </div>
        </div>
      )}
    </div>
  );
}

function PlaybookView() {
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState("");
  const [open, setOpen] = useState<Record<string, boolean>>({});
  useEffect(() => { api.getPlaybook().then(setData).catch((e: any) => setErr(e.message)); }, []);
  if (err) return <div className="text-red-600">{err}</div>;
  if (!data) return <div>Loading...</div>;
  return (
    <div className="space-y-3">
      <h2 className="text-2xl font-bold text-[#142238]">Incident Response Playbook</h2>
      {Object.entries(data).map(([stage, steps]: any) => (
        <div key={stage} className="bg-white border rounded-lg">
          <button className="w-full flex items-center justify-between p-4 text-left" onClick={() => setOpen({ ...open, [stage]: !open[stage] })}>
            <span className="font-semibold text-[#142238]">{stage}</span>
            <span className="text-gray-400">{open[stage] ? "−" : "+"}</span>
          </button>
          {open[stage] && (
            <div className="p-4 border-t">
              <p className="text-sm text-gray-600 mb-2">Recommended actions for the {stage} stage.</p>
              <ol className="list-decimal ml-6 text-sm space-y-1">{steps.map((st: string, idx: number) => <li key={idx}>{st}</li>)}</ol>
              <p className="text-xs text-gray-500 mt-2">Document all actions and outcomes for audit history.</p>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

function AssessmentView({ incidents, selectedId, onSelect }: any) {
  const [questions, setQuestions] = useState<any[]>([]);
  const [ruleVersion, setRuleVersion] = useState("");
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [result, setResult] = useState<any>(null);
  const [err, setErr] = useState("");
  const [step, setStep] = useState(0);
  useEffect(() => { api.getAssessmentQuestions().then((d: any) => { setQuestions(d.questions || []); setRuleVersion(d.rule_version || ""); }).catch((e: any) => setErr(e.message)); }, []);
  const submit = async () => {
    if (!selectedId) { setErr("Select an incident first"); return; }
    try { const r = await api.createAssessment(selectedId, { answers, reviewer: "reviewer" }); setResult(r); setErr(""); }
    catch (e: any) { setErr(e.message); }
  };
  const q = questions[step];
  return (
    <div className="space-y-3">
      <h2 className="text-2xl font-bold text-[#142238]">Breach Notification Assessment</h2>
      <p className="text-sm text-gray-600">Rule-based review aid only. Result is "Needs review"; not a legal determination.</p>
      <select className="border p-2 rounded" value={selectedId ?? ""} onChange={(e) => onSelect(Number(e.target.value))}>
        <option value="">Select incident</option>
        {incidents.map((i: any) => <option key={i.id} value={i.id}>#{i.id} {i.title}</option>)}
      </select>
      {questions.length > 0 && (
        <div className="bg-white border rounded-lg p-4 space-y-3">
          <div className="text-xs text-gray-500">Question {step + 1} of {questions.length}</div>
          <label className="block text-sm font-medium">{q?.text}</label>
          <p className="text-xs text-gray-500">{q?.explanation}</p>
          <input className="border p-2 w-full rounded text-sm" value={answers[q?.id] ?? ""} onChange={(e) => setAnswers({ ...answers, [q.id]: e.target.value })} />
          <div className="flex gap-2">
            <button className="bg-gray-200 px-3 py-1.5 rounded text-sm" disabled={step === 0} onClick={() => setStep(step - 1)}>Back</button>
            {step < questions.length - 1 && <button className="bg-[#2563EB] text-white px-3 py-1.5 rounded text-sm" onClick={() => setStep(step + 1)}>Next</button>}
            {step === questions.length - 1 && <button className="bg-[#2563EB] text-white px-3 py-1.5 rounded text-sm" onClick={submit}>Submit</button>}
          </div>
        </div>
      )}
      {err && <div className="text-red-600 text-sm">{err}</div>}
      {result && (
        <div className="bg-white border rounded-lg p-4 text-sm">
          <div className="font-semibold">Outcome: {result.outcome}</div>
          <div>Missing: {(result.missing_questions || []).join(", ") || "none"}</div>
          <div className="text-gray-500">Rule version: {result.rule_version || ruleVersion}</div>
          <p className="text-xs text-gray-500 mt-2">Requires human/legal review; not a final legal determination.</p>
        </div>
      )}
    </div>
  );
}

function ReportsView({ incidents, selectedId, onSelect }: any) {
  const [report, setReport] = useState<any>(null);
  const [err, setErr] = useState("");
  const gen = async () => {
    if (!selectedId) { setErr("Select an incident first"); return; }
    try { const r = await api.getReport(selectedId); setReport(r); setErr(""); }
    catch (e: any) { setErr(e.message); }
  };
  const genNotif = async () => {
    if (!selectedId) { setErr("Select an incident first"); return; }
    try { const r = await api.getNotificationDraft(selectedId); setReport({ id: report?.id, draft_text: r.draft_text }); setErr(""); }
    catch (e: any) { setErr(e.message); }
  };
  const save = async () => {
    if (!report?.id) return;
    try { await api.updateReport(selectedId, report.id, report.draft_text); setErr(""); }
    catch (e: any) { setErr(e.message); }
  };
  return (
    <div className="space-y-3">
      <h2 className="text-2xl font-bold text-[#142238]">Reports & Templates</h2>
      <select className="border p-2 rounded" value={selectedId ?? ""} onChange={(e) => onSelect(Number(e.target.value))}>
        <option value="">Select incident</option>
        {incidents.map((i: any) => <option key={i.id} value={i.id}>#{i.id} {i.title}</option>)}
      </select>
      <div className="flex gap-2">
        <button className="bg-gray-600 text-white px-4 py-2 rounded-md text-sm" onClick={gen}>Generate Incident Report</button>
        <button className="bg-gray-500 text-white px-4 py-2 rounded-md text-sm" onClick={genNotif}>Generate Notification Draft</button>
      </div>
      {err && <div className="text-red-600 text-sm">{err}</div>}
      {report && (
        <div className="space-y-3">
          <div className="bg-gray-50 border rounded-lg p-3">
            <h3 className="font-semibold text-sm mb-1">Report preview</h3>
            <pre className="text-xs whitespace-pre-wrap">{report.draft_text}</pre>
          </div>
          <div>
            <label className="text-sm font-medium">Editable draft</label>
            <textarea className="border p-2 w-full rounded text-xs" rows={16} value={report.draft_text} onChange={(e) => setReport({ ...report, draft_text: e.target.value })} />
            {report.id && <button className="bg-[#2563EB] text-white px-4 py-2 rounded-md text-sm mt-2" onClick={save}>Save draft</button>}
          </div>
        </div>
      )}
    </div>
  );
}

function TabletopView() {
  const [scenarios, setScenarios] = useState<any[]>([]);
  const [runs, setRuns] = useState<any[]>([]);
  const [responses, setResponses] = useState<Record<string, string>>({});
  const [err, setErr] = useState("");
  useEffect(() => { api.getTabletop().then(setScenarios).catch((e: any) => setErr(e.message)); api.listTabletopRuns().then(setRuns).catch(() => {}); }, []);
  return (
    <div className="space-y-3">
      <h2 className="text-2xl font-bold text-[#142238]">Tabletop Exercises</h2>
      {err && <div className="text-red-600 text-sm">{err}</div>}
      {scenarios.map((sc: any) => (
        <div key={sc.id} className="bg-white border rounded-lg p-4">
          <h3 className="font-semibold mb-1">{sc.title}</h3>
          <p className="text-sm text-gray-700 mb-3">{sc.description}</p>
          <div className="grid md:grid-cols-2 gap-3 mb-3">
            <div>
              <h4 className="font-semibold text-sm mb-1">Tasks</h4>
              <ul className="list-disc ml-6 text-sm">{sc.tasks.map((t: string, i: number) => <li key={i}>{t}</li>)}</ul>
            </div>
            <div>
              <h4 className="font-semibold text-sm mb-1">Evaluation checklist</h4>
              <ul className="list-disc ml-6 text-sm">{sc.evaluation_checklist.map((t: string, i: number) => <li key={i}>{t}</li>)}</ul>
            </div>
          </div>
          <textarea className="border p-2 w-full rounded text-sm" rows={4} placeholder="Your response notes..." value={responses[sc.id] || ""} onChange={(e) => setResponses({ ...responses, [sc.id]: e.target.value })} />
          <button className="bg-[#2563EB] text-white px-3 py-1.5 rounded-md text-sm mt-2" onClick={async () => {
            try { await api.createTabletopRun({ scenario_id: sc.id, responses: { notes: responses[sc.id] || "" }, completed: true }); const r = await api.listTabletopRuns(); setRuns(r); alert("Run saved"); }
            catch (e: any) { alert(e.message); }
          }}>Save run</button>
        </div>
      ))}
      {scenarios.length === 0 && <div className="text-gray-400">No scenarios.</div>}
      <div className="bg-white border rounded-lg p-4">
        <h3 className="font-semibold mb-2">Saved runs</h3>
        {runs.length === 0 && <div className="text-gray-400 text-sm">No runs saved.</div>}
        {runs.map((r: any) => (
          <div key={r.id} className="border-b py-2 text-sm">
            <div>Run #{r.id} — {r.scenario_id} — completed: {r.completed_at ? new Date(r.completed_at).toLocaleString() : "in progress"}</div>
            <div className="text-gray-500 text-xs">{JSON.stringify(r.responses_json)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function LessonsView({ incidents, selectedId, onSelect }: any) {
  const [items, setItems] = useState<any[]>([]);
  const [form, setForm] = useState({ root_cause: "", improvement: "", follow_up: "" });
  const [err, setErr] = useState("");
  const [query, setQuery] = useState("");
  const load = async (id: number) => {
    try { setItems(await api.listLessons(id)); } catch (e: any) { setErr(e.message); }
  };
  useEffect(() => { if (selectedId) load(selectedId); }, [selectedId]);
  const add = async () => {
    if (!selectedId) { setErr("Select an incident first"); return; }
    try { await api.addLesson(selectedId, form); setForm({ root_cause: "", improvement: "", follow_up: "" }); load(selectedId); setErr(""); }
    catch (e: any) { setErr(e.message); }
  };
  const filtered = items.filter((l: any) => (l.root_cause || "").toLowerCase().includes(query.toLowerCase()) || (l.improvement || "").toLowerCase().includes(query.toLowerCase()));
  return (
    <div className="space-y-3">
      <h2 className="text-2xl font-bold text-[#142238]">Lessons Learned</h2>
      <select className="border p-2 rounded" value={selectedId ?? ""} onChange={(e) => onSelect(Number(e.target.value))}>
        <option value="">Select incident</option>
        {incidents.map((i: any) => <option key={i.id} value={i.id}>#{i.id} {i.title}</option>)}
      </select>
      <input className="border p-2 w-full rounded text-sm" placeholder="Search lessons..." value={query} onChange={(e) => setQuery(e.target.value)} />
      <div className="bg-white border rounded-lg p-4 space-y-2">
        <input className="border p-2 w-full rounded text-sm" placeholder="root cause" value={form.root_cause} onChange={(e) => setForm({ ...form, root_cause: e.target.value })} />
        <input className="border p-2 w-full rounded text-sm" placeholder="improvement" value={form.improvement} onChange={(e) => setForm({ ...form, improvement: e.target.value })} />
        <input className="border p-2 w-full rounded text-sm" placeholder="follow up" value={form.follow_up} onChange={(e) => setForm({ ...form, follow_up: e.target.value })} />
        <button className="bg-[#2563EB] text-white px-4 py-2 rounded-md text-sm" onClick={add}>Add lesson</button>
      </div>
      {err && <div className="text-red-600 text-sm">{err}</div>}
      <ul className="list-disc ml-6 text-sm space-y-1">
        {filtered.map((l: any) => <li key={l.id}>{l.root_cause || "-"} → {l.improvement || "-"} (follow-up: {l.follow_up || "-"})</li>)}
      </ul>
      {filtered.length === 0 && <div className="text-gray-400 text-sm">No lessons recorded.</div>}
    </div>
  );
}
