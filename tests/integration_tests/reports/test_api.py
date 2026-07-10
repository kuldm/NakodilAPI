import asyncio


async def test_get_ping(ac):
    response = await ac.get("/ping")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


async def test_get_user_report(ac):
    user_id = 1
    response = await ac.post(f"/reports/{user_id}")
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["job_id"] == 1
    assert res["status"] == "running"


async def test_get_status_job(ac):
    create_response = await ac.post("/reports/1")
    assert create_response.status_code == 200
    job_id = create_response.json()["job_id"]

    response = await ac.get(f"/reports/jobs/{job_id}")
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["job_id"] == 1
    assert res["status"] == "running"
    await asyncio.sleep(5)

    response = await ac.get(f"/reports/jobs/{job_id}")
    assert response.status_code == 200
    res = response.json()
    print(res)
    assert isinstance(res, dict)
    assert res["job_id"] == 1
    assert res["status"] == "done"
    assert "result" in res

    # assert res["status"] == "done"
