import requests
URL = "https://api.github.com/repos/psf/requests/actions/runs"
def format_run(run):
    """Turn one workflow run (a dict from the API) into one line of text."""
    name = run["name"]
    conclusion = run.get("conclusion") or run.get("status")
    attempt = run["run_attempt"]
    sha = run["head_sha"][:7]
    created = run["created_at"]
    return f"{name}  |  {conclusion}  |  attempt {attempt}  |  {sha}  |  {created}"
def main():
    response = requests.get(URL, params={"per_page": 5}, timeout=15)
    if response.status_code != 200:
        print(f"Request failed: HTTP {response.status_code}")
        print(response.text[:300])
        raise SystemExit(1)
    runs = response.json().get("workflow_runs", [])
    if not runs:
        print("No workflow runs found.")
        return
    for run in runs:
        print(format_run(run))
if __name__ == "__main__":
    main()