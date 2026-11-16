"""Pure flake-detection logic. No network calls in here, so it is easy to test."""
from collections import Counter


def rerun_candidates(runs):
    """Runs that passed, but only after being re-run (attempt 2 or later).

    The Actions API lists one entry per run, showing the latest attempt.
    A pass on attempt 2+ means someone re-ran it, so it might be a flake.
    """
    return [
        run
        for run in runs
        if run.get("run_attempt", 1) > 1 and run.get("conclusion") == "success"
    ]


def is_flake(first_attempt, latest_attempt):
    """A flake: attempt 1 failed, a later attempt passed, same commit."""
    return (
        first_attempt.get("conclusion") == "failure"
        and latest_attempt.get("conclusion") == "success"
        and first_attempt.get("head_sha") == latest_attempt.get("head_sha")
    )


def find_flakes(runs, get_attempt):
    """Return the runs that are confirmed flakes.

    get_attempt(run_id, attempt_number) returns that attempt's run dict.
    It is passed in so tests can fake it without touching the network.
    """
    flakes = []
    for run in rerun_candidates(runs):
        first = get_attempt(run["id"], 1)
        if is_flake(first, run):
            flakes.append(run)
    return flakes


def summarize(flakes):
    """Count flakes per workflow name, worst first: [(name, count), ...]."""
    return Counter(run["name"] for run in flakes).most_common()
