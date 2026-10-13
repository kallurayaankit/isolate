
"""The audit: compare suite behavior vs isolated behavior."""

from isolate.discover import discover
from isolate.models import Audit, Report, Verdict
from isolate.runner import run_one, run_suite


def audit(tests_dir, quiet=False):
    test_ids = discover(tests_dir)
    if not test_ids:
        raise ValueError("no tests found in " + str(tests_dir))

    if not quiet:
        print("Found " + str(len(test_ids)) + " tests")
        print("Running the suite once...")

    suite_passed, _, _ = run_suite(tests_dir)

    if not quiet:
        print("  suite: " + ("PASS" if suite_passed else "FAIL"))
        print("Running each test alone...")

    report = Report(suite_count=len(test_ids))

    for i, tid in enumerate(test_ids, start=1):
        alone_passed, _, _ = run_one(tid)

        if suite_passed and alone_passed:
            verdict = Verdict.ISOLATED.value
            reason = "passes alone and in suite"
        elif suite_passed and not alone_passed:
            verdict = Verdict.ORDER_DEPENDENT.value
            reason = "passes in suite but FAILS alone - depends on other tests"
        elif not suite_passed and alone_passed:
            verdict = Verdict.POLLUTER.value
            reason = "passes alone but suite fails - possibly polluting shared state"
        else:
            verdict = Verdict.BROKEN.value
            reason = "fails both alone and in suite"

        report.audits.append(Audit(test_id=tid, verdict=verdict, reason=reason))

        if verdict == Verdict.ISOLATED.value:
            report.isolated += 1
        elif verdict == Verdict.ORDER_DEPENDENT.value:
            report.order_dependent += 1
        elif verdict == Verdict.POLLUTER.value:
            report.polluter += 1
        else:
            report.broken += 1

        if not quiet:
            icon = {
                Verdict.ISOLATED.value: ".",
                Verdict.ORDER_DEPENDENT.value: "X",
                Verdict.POLLUTER.value: "P",
                Verdict.BROKEN.value: "B",
            }[verdict]
            print("  [" + str(i) + "/" + str(len(test_ids)) + "] " + icon + "  " + tid.split("::")[-1])

    return report
