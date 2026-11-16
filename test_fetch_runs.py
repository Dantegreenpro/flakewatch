from fetch_runs import format_run
SAMPLE_RUN = {
    "name": "Tests",
    "status": "completed",
    "conclusion": "failure",
    "run_attempt": 2,
    "head_sha": "3c7baaa05ab4aa49cc819ce3a819d260de19c157",
    "created_at": "2026-11-15T23:00:16Z",
}
def test_format_run_shows_the_key_fields():
    line = format_run(SAMPLE_RUN)
    assert line == "Tests  |  failure  |  attempt 2  |  3c7baaa  |  2026-11-15T23:00:16Z"
def test_format_run_uses_status_while_running():
    running = dict(SAMPLE_RUN, conclusion=None, status="in_progress")
    assert "in_progress" in format_run(running) 