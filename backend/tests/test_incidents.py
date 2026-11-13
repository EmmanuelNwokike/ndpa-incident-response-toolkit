from datetime import datetime, timezone

def _incident_payload():
    return {
        "title": "Test incident",
        "description": "Synthetic test incident",
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "reporter": "tester",
        "affected_system": "email",
        "personal_data_involved": True,
        "affected_data_categories": ["contact"],
        "affected_people_estimate": 5,
        "severity": "Medium",
    }

def test_create_incident(client):
    r = client.post("/incidents", json=_incident_payload())
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Test incident"
    assert data["stage"] == "Detection"
    assert data["id"] is not None

def test_create_rejects_missing_fields(client):
    r = client.post("/incidents", json={"title": "x"})
    assert r.status_code == 422

def test_persistence_across_requests(client):
    r = client.post("/incidents", json=_incident_payload())
    iid = r.json()["id"]
    r2 = client.get(f"/incidents/{iid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == iid

def test_stage_sequence(client):
    r = client.post("/incidents", json=_incident_payload())
    iid = r.json()["id"]
    for stage in ["Triage", "Containment", "Investigation", "Reporting"]:
        r = client.patch(f"/incidents/{iid}", json={"stage": stage})
        assert r.status_code == 200, r.text
        assert r.json()["stage"] == stage

def test_invalid_stage_transition(client):
    r = client.post("/incidents", json=_incident_payload())
    iid = r.json()["id"]
    r = client.patch(f"/incidents/{iid}", json={"stage": "Reporting"})
    # skipping allowed? forward-only allows skip; but invalid stage rejected
    assert r.status_code in (200, 409)
    # invalid stage value rejected
    r = client.patch(f"/incidents/{iid}", json={"stage": "Foo"})
    assert r.status_code == 422

def test_action_persists(client):
    r = client.post("/incidents", json=_incident_payload())
    iid = r.json()["id"]
    r = client.post(f"/incidents/{iid}/actions", json={"stage": "Detection", "action": "Record initial incident report", "owner": "Security Analyst", "outcome": "Incident recorded"})
    assert r.status_code == 201
    r2 = client.get(f"/incidents/{iid}")
    assert len(r2.json()["actions"]) == 1
    assert r2.json()["actions"][0]["action"] == "Record initial incident report"

def test_list_filter(client):
    client.post("/incidents", json=_incident_payload())
    r = client.get("/incidents")
    assert r.status_code == 200
    assert len(r.json()) >= 1
    r = client.get("/incidents", params={"q": "Test"})
    assert len(r.json()) >= 1