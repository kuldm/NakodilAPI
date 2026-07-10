from services.reports import JobService, jobs
import services.reports as reports_module


async def test_create_job_returns_running_status():
    jobs.clear()
    reports_module.next_job_id = 1

    service = JobService()
    result = await service.create_job(user_id=1)

    assert result == {"job_id": 1, "status": "running"}
    assert jobs[1]["job_id"] == 1
    assert jobs[1]["status"] == "running"
