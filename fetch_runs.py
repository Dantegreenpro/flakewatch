import os

import requests

API = "https://api.github.com"


class FetchError(Exception):
    """The GitHub API gave us something we can't use."""


def format_run(run):
    """Turn one workflow run (a dict from the API) into one line of text."""
    name = run["name"]
    conclusion = run.get("conclusion") or run.get("status")
    attempt = run["run_attempt"]
    sha = run["head_sha"][:7]
    created = run["created_at"]
    return f"{name}  |  {conclusion}  |  attempt {attempt}  |  {sha}  |  {created}"


def _headers():
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _get(url, params=None):
    response = requests.get(url, params=params, headers=_headers(), timeout=15)
    if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
        raise FetchError("GitHub rate limit hit. Set GITHUB_TOKEN to raise it.")
    if response.status_code != 200:
        raise FetchError(f"HTTP {response.status_code}: {response.text[:300]}")
    return response.json()


def fetch_runs(repo, limit=100):
    """Fetch up to `limit` completed workflow runs, newest first."""
    runs = []
    page = 1
    while len(runs) < limit:
        per_page = min(100, limit - len(runs))
        data = _get(
            f"{API}/repos/{repo}/actions/runs",
            {"per_page": per_page, "page": page, "status": "completed"},
        )
        batch = data.get("workflow_runs", [])
        if not batch:
            break
        runs.extend(batch)
        page += 1
    return runs[:limit]


def fetch_attempt(repo, run_id, attempt):
    """Fetch one specific attempt of a run."""
    return _get(f"{API}/repos/{repo}/actions/runs/{run_id}/attempts/{attempt}")
