def test_assessment_missing_returns_needs_review(client):
    from datetime import datetime, timezone
    payload = {
        "title": "t", "description": "d", "detected_at": datetime.now(timezone.utc).isoformat(),
        "reporter": "r", "affected_system": "s",
    }
    r = client.post("/incidents", json=payload)
    iid = r.json()["id"]
    r = client.post(f"/incidents/{iid}/assessment", json={"answers": {}, "reviewer": "rev"})
    assert r.status_code == 201
    assert r.json()["outcome"] == "Needs review"
    assert len(r.json()["missing_questions"]) > 0

def test_assessment_saved(client):
    from datetime import datetime, timezone
    payload = {
        "title": "t", "description": "d", "detected_at": datetime.now(timezone.utc).isoformat(),
        "reporter": "r", "affected_system": "s",
    }
    r = client.post("/incidents", json=payload)
    iid = r.json()["id"]
    answers = {"incident_type": "phishing", "personal_data_involved": True}
    r = client.post(f"/incidents/{iid}/assessment", json={"answers": answers, "reviewer": "rev"})
    assert r.status_code == 201
    assert r.json()["answers_json"] == answers
    assert r.json()["rule_version"] is not None