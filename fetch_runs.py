import requests
URL = "https://api.github.com/repos/psf/requests/actions/runs"
params = {"per_page": 5}
response = requests.get(URL, params=params, timeout=15)
if response.status_code != 200:
    print(f"Request failed: HTTP {response.status_code}")
    print(response.text[:300])
    raise SystemExit(1)
data = response.json()
runs = data.get("workflow_runs", [])
if not runs:
    print("No workflow runs found.")
    raise SystemExit(0)
for run in runs:
    name = run["name"]
    conclusion = run.get("conclusion") or run.get("status")
    attempt = run["run_attempt"]
    sha = run["head_sha"][:7]
    created = run["created_at"]
    print(f"{name}  |  {conclusion}  |  attempt {attempt}  |  {sha}  |  {created}")