import pytest


@pytest.mark.asyncio
async def test_create_task(client):
    payload = {"title": "Test", "description": "Test desc", "status": "created"}
    response = await client.post("/tasks/", json=payload)  # <- await!
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_read_task(client):
    payload = {"title": "Read", "description": "Desc", "status": "created"}
    resp_create = await client.post("/tasks/", json=payload)
    task_id = resp_create.json()["id"]

    resp = await client.get(f"/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Read"


@pytest.mark.asyncio
async def test_update_task(client):
    payload = {"title": "Old", "description": "Old desc", "status": "created"}
    resp_create = await client.post("/tasks/", json=payload)
    task_id = resp_create.json()["id"]

    update_payload = {"title": "New", "status": "in_progress"}
    resp = await client.put(f"/tasks/{task_id}", json=update_payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "New"
    assert data["status"] == "in_progress"


@pytest.mark.asyncio
async def test_delete_task(client):
    payload = {"title": "Del", "description": "Desc", "status": "created"}
    resp_create = await client.post("/tasks/", json=payload)
    task_id = resp_create.json()["id"]

    resp = await client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 200

    resp_get = await client.get(f"/tasks/{task_id}")
    assert resp_get.status_code == 404

    resp = await client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_deleted_task(client):
    payload = {"title": "Del", "description": "Desc", "status": "created"}
    resp_create = await client.post("/tasks/", json=payload)
    task_id = resp_create.json()["id"]

    resp = await client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 200

    payload = {"title": "Del", "description": "deleted", "status": "created"}
    resp = await client.put(f"/tasks/{task_id}", json=payload)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_read_deleted_task(client):
    payload = {"title": "Del", "description": "Desc", "status": "created"}
    resp_create = await client.post("/tasks/", json=payload)
    task_id = resp_create.json()["id"]

    resp = await client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 200

    resp = await client.get(f"/tasks/{task_id}")
    assert resp.status_code == 404
