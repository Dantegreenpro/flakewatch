from detect import find_flakes, is_flake, rerun_candidates, summarize


def make_run(run_id=1, name="Tests", conclusion="success", attempt=1, sha="abc1234"):
    return {
        "id": run_id,
        "name": name,
        "conclusion": conclusion,
        "run_attempt": attempt,
        "head_sha": sha,
    }


def test_rerun_candidates_keeps_only_passes_after_a_rerun():
    runs = [
        make_run(1, attempt=1),                       # passed first try
        make_run(2, attempt=2),                       # passed after re-run
        make_run(3, attempt=2, conclusion="failure"), # still failing
    ]
    assert [r["id"] for r in rerun_candidates(runs)] == [2]


def test_is_flake_needs_fail_then_pass_on_same_commit():
    failed = make_run(conclusion="failure")
    passed = make_run(conclusion="success", attempt=2)
    assert is_flake(failed, passed)


def test_is_flake_false_if_first_attempt_passed():
    assert not is_flake(make_run(conclusion="success"), make_run(attempt=2))


def test_is_flake_false_if_commit_differs():
    failed = make_run(conclusion="failure", sha="aaa")
    passed = make_run(attempt=2, sha="bbb")
    assert not is_flake(failed, passed)


def test_find_flakes_confirms_with_first_attempt():
    runs = [make_run(10, attempt=2), make_run(11, attempt=2)]
    first_attempts = {
        10: make_run(10, conclusion="failure"),  # real flake
        11: make_run(11, conclusion="success"),  # re-run of a pass, not a flake
    }
    flakes = find_flakes(runs, lambda run_id, n: first_attempts[run_id])
    assert [r["id"] for r in flakes] == [10]


def test_summarize_ranks_workflows_worst_first():
    flakes = [make_run(1, "Lint"), make_run(2, "Tests"), make_run(3, "Tests")]
    assert summarize(flakes) == [("Tests", 2), ("Lint", 1)]
