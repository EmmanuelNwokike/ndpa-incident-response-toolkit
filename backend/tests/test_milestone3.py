from datetime import datetime, timezone

def _payload():
    return {
        "title": "M3 incident",
        "description": "Synthetic",
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "reporter": "tester",
        "affected_system": "email",
        "severity": "High",
        "personal_data_involved": True,
        "affected_data_categories": ["contact"],
        "affected_people_estimate": 3,
    }

def test_evidence_and_timeline(client):
    r = client.post("/incidents", json=_payload())
    iid = r.json()["id"]
    r = client.post(f"/incidents/{iid}/evidence", json={"description": "log file", "source": "mail server", "collected_by": "analyst", "notes": "synthetic"})
    assert r.status_code == 201
    r = client.get(f"/incidents/{iid}/evidence")
    assert r.status_code == 200 and len(r.json()) == 1
    r = client.get(f"/incidents/{iid}")
    assert "audit_events" in r.json()
    assert len(r.json()["audit_events"]) >= 1

def test_notification_draft(client):
    r = client.post("/incidents", json=_payload())
    iid = r.json()["id"]
    r = client.get(f"/incidents/{iid}/notification-draft")
    assert r.status_code == 200
    assert "DRAFT BREACH NOTIFICATION" in r.json()["draft_text"]
    assert "MISSING INFORMATION" in r.json()["draft_text"]

def test_tabletop_run_persistence(client):
    r = client.post("/tabletop/runs", json={"scenario_id": "scenario-1", "responses": {"notes": "done"}, "completed": True})
    assert r.status_code == 201
    rid = r.json()["id"]
    assert r.json()["completed_at"] is not None
    r = client.get(f"/tabletop/runs/{rid}")
    assert r.status_code == 200
    r = client.get("/tabletop/runs")
    assert len(r.json()) >= 1
    r = client.patch(f"/tabletop/runs/{rid}", json={"scenario_id": "scenario-1", "responses": {"notes": "updated"}, "evaluation": {"score": 1}, "completed": True})
    assert r.status_code == 200
    assert r.json()["responses_json"]["notes"] == "updated"

def test_decision_tree_needs_review(client):
    r = client.post("/incidents", json=_payload())
    iid = r.json()["id"]
    r = client.post(f"/incidents/{iid}/assessment", json={"answers": {}, "reviewer": "rev"})
    assert r.status_code == 201
    assert r.json()["outcome"] == "Needs review"

def test_report_draft_edit(client):
    r = client.post("/incidents", json=_payload())
    iid = r.json()["id"]
    r = client.get(f"/incidents/{iid}/report")
    assert r.status_code == 200
    assert "INCIDENT REPORT DRAFT" in r.json()["draft_text"]
    rid = r.json()["id"]
    r = client.patch(f"/incidents/{iid}/report/{rid}", json={"draft_text": "edited draft"})
    assert r.status_code == 200
    assert r.json()["draft_text"] == "edited draft"


def test_invalid_severity_rejected(client):
    payload = {
        "title": "t", "description": "d", "detected_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "reporter": "r", "affected_system": "s", "severity": "Critical",
    }
    r = client.post("/incidents", json=payload)
    assert r.status_code == 422


def test_transition_beyond_reporting_rejected(client):
    payload = {
        "title": "t", "description": "d", "detected_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "reporter": "r", "affected_system": "s",
    }
    r = client.post("/incidents", json=payload)
    iid = r.json()["id"]
    for st in ["Triage", "Containment", "Investigation", "Reporting"]:
        r = client.patch(f"/incidents/{iid}", json={"stage": st})
        assert r.status_code == 200
    r = client.patch(f"/incidents/{iid}", json={"stage": "Reporting"})
    assert r.status_code in (200, 409)
    r = client.patch(f"/incidents/{iid}", json={"stage": "Detection"})
    assert r.status_code == 409

def test_audit_event_on_transition(client):
    payload = {
        "title": "t", "description": "d", "detected_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "reporter": "r", "affected_system": "s",
    }
    r = client.post("/incidents", json=payload)
    iid = r.json()["id"]
    r = client.patch(f"/incidents/{iid}", json={"stage": "Triage"})
    assert r.status_code == 200
    r = client.get(f"/incidents/{iid}")
    events = r.json()["audit_events"]
    assert any("Detection -> Triage" in (e.get("details") or "") for e in events)

def test_owner_validation(client):
    payload = {
        "title": "t", "description": "d", "detected_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "reporter": "r", "affected_system": "s",
    }
    r = client.post("/incidents", json=payload)
    iid = r.json()["id"]
    r = client.post(f"/incidents/{iid}/actions", json={"stage": "Detection", "action": "act", "owner": "NotARole", "outcome": "ok"})
    assert r.status_code == 422
    r = client.post(f"/incidents/{iid}/actions", json={"stage": "Detection", "action": "Record initial incident report", "owner": "Security Analyst", "outcome": "Incident recorded"})
    assert r.status_code == 201
