# Flakewatch
Flakewatch finds flaky CI jobs: jobs that fail, then pass
when someone re-runs them on the same commit.
Status: early work. Right now it prints the last 5
GitHub Actions runs for psf/requests.
## Run it
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python fetch_runs.py
## Test it
    python -m pytest