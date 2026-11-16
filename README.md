# Flakewatch
Flakewatch finds flaky CI jobs: jobs that fail, then pass
when someone re-runs them on the same commit.
Status: early work. It scans recent GitHub Actions runs,
finds runs that passed only after a re-run, and confirms each
one by checking that attempt 1 failed on the same commit.
## Run it
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python flakewatch.py psf/requests 100

Set GITHUB_TOKEN to avoid GitHub's low anonymous rate limit.
## Test it
    python -m pytest