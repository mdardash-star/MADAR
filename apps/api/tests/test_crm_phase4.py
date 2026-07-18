"""
PH4-001 CRM Leads
PH4-002 CRM Pipelines & Stages
PH4-003 CRM Opportunities
PH4-004 CRM Activities
PH4-005 CRM Notes
All acceptance criteria verified via API smoke tests.
"""

import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _fresh_company_id() -> int:
    """Register a unique company for each test that writes data and return its id."""
    slug = f"crm-test-{uuid.uuid4().hex[:8]}"
    resp = client.post(
        "/companies/register",
        json={
            "company_name": f"CRM Test Co {slug}",
            "company_slug": slug,
            "admin_email": f"admin+{slug}@example.com",
            "admin_password": "Test1234!",
            "admin_full_name": "Test Admin",
        },
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["company"]["id"]


COMPANY_ID = 1


# ── PH4-001 CRM Leads ─────────────────────────────────────────────────────────

def test_leads_list_is_accessible() -> None:
    response = client.get("/api/v1/crm/leads", params={"company_id": COMPANY_ID})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_leads_create_and_update_status() -> None:
    cid = _fresh_company_id()
    resp = client.post(
        "/api/v1/crm/leads",
        json={
            "company_id": cid,
            "full_name": "Test Lead",
            "email": "lead@test.com",
            "status": "new",
        },
    )
    assert resp.status_code == 201
    lead_id = resp.json()["id"]

    # Update status → contacted
    upd = client.put(f"/api/v1/crm/leads/{lead_id}", json={"status": "contacted"})
    assert upd.status_code == 200
    assert upd.json()["status"] == "contacted"

    # Soft-delete
    del_resp = client.delete(f"/api/v1/crm/leads/{lead_id}")
    assert del_resp.status_code == 200


def test_leads_filter_by_status() -> None:
    cid = _fresh_company_id()
    # Create a 'qualified' lead
    create_resp = client.post(
        "/api/v1/crm/leads",
        json={"company_id": cid, "full_name": "Qualified Lead", "status": "qualified"},
    )
    assert create_resp.status_code == 201

    listed = client.get(
        "/api/v1/crm/leads",
        params={"company_id": cid, "status": "qualified"},
    )
    assert listed.status_code == 200
    results = listed.json()
    assert all(r["status"] == "qualified" for r in results)


# ── PH4-002 CRM Pipelines & Stages ───────────────────────────────────────────

def test_pipelines_create_and_list() -> None:
    cid = _fresh_company_id()
    resp = client.post(
        "/api/v1/crm/pipelines",
        json={"company_id": cid, "name": "Main Pipeline", "is_default": True},
    )
    assert resp.status_code == 201
    pipeline_id = resp.json()["id"]

    listed = client.get("/api/v1/crm/pipelines", params={"company_id": cid})
    assert listed.status_code == 200
    assert any(p["id"] == pipeline_id for p in listed.json())


def test_stages_create_and_list() -> None:
    cid = _fresh_company_id()
    # Create a pipeline first
    pipe = client.post(
        "/api/v1/crm/pipelines",
        json={"company_id": cid, "name": "Stages Test Pipeline"},
    )
    assert pipe.status_code == 201
    pipeline_id = pipe.json()["id"]

    # Add 3 stages
    for seq, name in [(10, "Prospecting"), (20, "Proposal"), (30, "Closed Won")]:
        s = client.post(
            "/api/v1/crm/stages",
            json={
                "company_id": cid,
                "pipeline_id": pipeline_id,
                "name": name,
                "sequence": seq,
                "probability": seq / 30 * 100,
                "is_won": name == "Closed Won",
            },
        )
        assert s.status_code == 201

    stages = client.get(
        f"/api/v1/crm/pipelines/{pipeline_id}/stages",
        params={"company_id": cid},
    )
    assert stages.status_code == 200
    assert len(stages.json()) == 3


# ── PH4-003 CRM Opportunities ────────────────────────────────────────────────

def test_opportunities_create_and_move_stage() -> None:
    cid = _fresh_company_id()
    # Bootstrap pipeline + 2 stages
    pipe = client.post(
        "/api/v1/crm/pipelines",
        json={"company_id": cid, "name": "Opp Pipeline"},
    )
    assert pipe.status_code == 201
    pipeline_id = pipe.json()["id"]

    s1 = client.post(
        "/api/v1/crm/stages",
        json={"company_id": cid, "pipeline_id": pipeline_id, "name": "Stage 1", "sequence": 10},
    )
    s2 = client.post(
        "/api/v1/crm/stages",
        json={"company_id": cid, "pipeline_id": pipeline_id, "name": "Stage 2", "sequence": 20, "probability": 60.0},
    )
    assert s1.status_code == 201
    assert s2.status_code == 201
    stage1_id = s1.json()["id"]
    stage2_id = s2.json()["id"]

    # Create opportunity
    opp = client.post(
        "/api/v1/crm/opportunities",
        json={
            "company_id": cid,
            "name": "Big Deal",
            "pipeline_id": pipeline_id,
            "stage_id": stage1_id,
            "expected_value": 50000.0,
            "expected_close_date": "2026-12-31",
        },
    )
    assert opp.status_code == 201
    opp_id = opp.json()["id"]

    # Move to stage 2
    moved = client.put(f"/api/v1/crm/opportunities/{opp_id}", json={"stage_id": stage2_id})
    assert moved.status_code == 200
    assert moved.json()["stage_id"] == stage2_id

    # List by pipeline
    listed = client.get(
        "/api/v1/crm/opportunities",
        params={"company_id": cid, "pipeline_id": pipeline_id},
    )
    assert listed.status_code == 200
    assert any(o["id"] == opp_id for o in listed.json())


# ── PH4-004 CRM Activities ───────────────────────────────────────────────────

def test_activities_create_and_complete() -> None:
    cid = _fresh_company_id()
    # Create a lead to link
    lead = client.post(
        "/api/v1/crm/leads",
        json={"company_id": cid, "full_name": "Activity Test Lead"},
    )
    assert lead.status_code == 201
    lead_id = lead.json()["id"]

    act = client.post(
        "/api/v1/crm/activities",
        json={
            "company_id": cid,
            "subject": "Follow-up call",
            "activity_type": "call",
            "lead_id": lead_id,
            "due_date": "2026-08-01",
            "status": "planned",
        },
    )
    assert act.status_code == 201
    act_id = act.json()["id"]

    # Complete the activity
    done = client.put(
        f"/api/v1/crm/activities/{act_id}",
        json={"status": "done", "outcome": "Lead expressed interest"},
    )
    assert done.status_code == 200
    assert done.json()["status"] == "done"

    # List by lead
    listed = client.get(
        "/api/v1/crm/activities",
        params={"company_id": cid, "lead_id": lead_id},
    )
    assert listed.status_code == 200
    assert any(a["id"] == act_id for a in listed.json())


# ── PH4-005 CRM Notes ────────────────────────────────────────────────────────

def test_notes_create_and_retrieve_by_lead() -> None:
    cid = _fresh_company_id()
    lead = client.post(
        "/api/v1/crm/leads",
        json={"company_id": cid, "full_name": "Note Test Lead"},
    )
    assert lead.status_code == 201
    lead_id = lead.json()["id"]

    note = client.post(
        "/api/v1/crm/notes",
        json={"company_id": cid, "lead_id": lead_id, "content": "Initial discovery call completed."},
    )
    assert note.status_code == 201
    note_id = note.json()["id"]

    notes = client.get("/api/v1/crm/notes", params={"company_id": cid, "lead_id": lead_id})
    assert notes.status_code == 200
    assert any(n["id"] == note_id for n in notes.json())
