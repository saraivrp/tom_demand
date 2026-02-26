import os
import shutil
import time
from pathlib import Path
from typing import Optional

from fastapi.testclient import TestClient

from src.api.main import app


def _headers(role: str = "executor", api_key: Optional[str] = None):
    headers = {"X-Role": role}
    if api_key:
        headers["X-API-Key"] = api_key
    return headers


def test_workflow_validate_and_prioritize():
    client = TestClient(app)

    validate_resp = client.post(
        "/api/v1/workflows/validate",
        json={
            "ideas_path": "data/input/ideas20260224.csv",
            "ra_weights_path": "data/input/weights_ra.csv",
            "rs_weights_path": "data/input/weights_rs.csv",
            "bg_rs_weights_path": "data/input/weights_bg_rs.csv",
        },
        headers=_headers(role="viewer"),
    )
    assert validate_resp.status_code == 200
    assert validate_resp.json()["ideas_count"] > 0

    prioritize_resp = client.post(
        "/api/v1/workflows/prioritize",
        json={
            "ideas_path": "data/input/ideas20260224.csv",
            "ra_weights_path": "data/input/weights_ra.csv",
            "rs_weights_path": "data/input/weights_rs.csv",
            "bg_rs_weights_path": "data/input/weights_bg_rs.csv",
            "output_dir": "/tmp/tom_demand_test_out",
            "method": "sainte-lague",
        },
        headers=_headers(role="executor"),
    )
    assert prioritize_resp.status_code == 200
    body = prioritize_resp.json()
    assert "sainte-lague" in body["methods_executed"] or "mixed" in body["methods_executed"]


def test_reference_data_upsert_and_list(tmp_path: Path):
    ideas_copy = tmp_path / "ideas.csv"
    shutil.copy("data/input/ideas20260224.csv", ideas_copy)

    client = TestClient(app)

    list_resp = client.get(
        f"/api/v1/reference-data/ideas?path={ideas_copy}&limit=3&offset=0",
        headers=_headers(role="viewer"),
    )
    assert list_resp.status_code == 200
    assert list_resp.json()["total"] >= 3

    upsert_resp = client.post(
        "/api/v1/reference-data/upsert",
        json={
            "path": str(ideas_copy),
            "key_column": "ID",
            "row": {"ID": "ZZZ_TEST_ID", "Name": "Test Idea Name"},
        },
        headers=_headers(role="editor"),
    )
    assert upsert_resp.status_code == 200

    check_resp = client.get(
        f"/api/v1/reference-data/ideas?path={ideas_copy}&limit=10000&offset=0",
        headers=_headers(role="viewer"),
    )
    assert check_resp.status_code == 200
    ids = [row.get("ID") for row in check_resp.json()["rows"]]
    assert "ZZZ_TEST_ID" in ids

    upload_resp = client.post(
        "/api/v1/reference-data/upload-ideas",
        files={"file": ("ideas_upload.csv", b"ID;Name\nA1;Uploaded idea\n", "text/csv")},
        headers=_headers(role="viewer"),
    )
    assert upload_resp.status_code == 200
    uploaded = upload_resp.json()
    assert uploaded["path"].endswith(".csv")
    assert os.path.exists(uploaded["path"])


def test_jobs_and_auth_enforcement(monkeypatch):
    monkeypatch.setenv("AUTH_ENABLED", "true")
    monkeypatch.setenv("API_KEY", "secret")
    monkeypatch.setenv("AUDIT_LOG_PATH", "/tmp/tom_demand_audit_test.jsonl")

    client = TestClient(app)

    denied = client.post(
        "/api/v1/workflows/prioritize",
        json={
            "ideas_path": "data/input/ideas20260224.csv",
            "ra_weights_path": "data/input/weights_ra.csv",
            "rs_weights_path": "data/input/weights_rs.csv",
            "bg_rs_weights_path": "data/input/weights_bg_rs.csv",
            "output_dir": "/tmp/tom_demand_test_out_auth",
        },
        headers=_headers(role="executor"),
    )
    assert denied.status_code == 401

    submit = client.post(
        "/api/v1/jobs/workflows/validate",
        json={
            "ideas_path": "data/input/ideas20260224.csv",
            "ra_weights_path": "data/input/weights_ra.csv",
            "rs_weights_path": "data/input/weights_rs.csv",
            "bg_rs_weights_path": "data/input/weights_bg_rs.csv",
        },
        headers=_headers(role="viewer", api_key="secret"),
    )
    assert submit.status_code == 200
    job_id = submit.json()["job_id"]

    status = None
    for _ in range(20):
        poll = client.get(f"/api/v1/jobs/{job_id}", headers=_headers(role="viewer", api_key="secret"))
        assert poll.status_code == 200
        status = poll.json()["status"]
        if status in ("completed", "failed"):
            break
        time.sleep(0.05)

    assert status == "completed"
    assert os.path.exists("/tmp/tom_demand_audit_test.jsonl")
