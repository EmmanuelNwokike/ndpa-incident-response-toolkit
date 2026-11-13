from datetime import datetime, timezone

def test_report_draft(client):
    payload = {
        "title": "t", "description": "d", "detected_at": datetime.now(timezone.utc).isoformat(),
        "reporter": "r", "affected_system": "s", "severity": "High",
    }
    r = client.post("/incidents", json=payload)
    iid = r.json()["id"]
    r = client.get(f"/incidents/{iid}/report")
    assert r.status_code == 200
    data = r.json()
    assert "INCIDENT REPORT DRAFT" in data["draft_text"]
    assert "MISSING INFORMATION" in data["draft_text"]

def test_lessons(client):
    from datetime import datetime, timezone
    payload = {
        "title": "t", "description": "d", "detected_at": datetime.now(timezone.utc).isoformat(),
        "reporter": "r", "affected_system": "s",
    }
    r = client.post("/incidents", json=payload)
    iid = r.json()["id"]
    r = client.post(f"/incidents/{iid}/lessons", json={"root_cause": "human error", "improvement": "training"})
    assert r.status_code == 201
    r = client.get(f"/incidents/{iid}/lessons")
    assert r.status_code == 200
    assert len(r.json()) == 1

def test_playbook_and_tabletop(client):
    r = client.get("/playbook")
    assert r.status_code == 200
    assert "Detection" in r.json()
    r = client.get("/tabletop/scenarios")
    assert r.status_code == 200
    assert len(r.json()) >= 1

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"