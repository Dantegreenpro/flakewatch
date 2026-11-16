import sys

from detect import find_flakes, rerun_candidates, summarize
from fetch_runs import FetchError, fetch_attempt, fetch_runs, format_run


def main(argv):
    repo = argv[1] if len(argv) > 1 else "psf/requests"
    limit = int(argv[2]) if len(argv) > 2 else 100

    try:
        runs = fetch_runs(repo, limit)
        flakes = find_flakes(runs, lambda run_id, n: fetch_attempt(repo, run_id, n))
    except FetchError as error:
        print(f"Error: {error}")
        return 1

    print(f"{repo}: checked {len(runs)} runs, "
          f"{len(rerun_candidates(runs))} passed only after a re-run, "
          f"{len(flakes)} confirmed flaky.")
    for name, count in summarize(flakes):
        print(f"  {count}x  {name}")
    for run in flakes:
        print("   ", format_run(run))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
