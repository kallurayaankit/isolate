
"""Run tests, once alone and once as a suite."""

import subprocess
import time


def run_one(test_id, timeout=30):
    start = time.time()
    try:
        r = subprocess.run(
            ["pytest", test_id, "-q", "--no-header", "-x"],
            capture_output=True, text=True, timeout=timeout,
        )
        duration = (time.time() - start) * 1000
        if r.returncode == 0:
            return True, "", duration
        lines = [l for l in r.stdout.splitlines() if l.strip()]
        err = lines[-1] if lines else "failed"
        return False, err[:300], duration
    except subprocess.TimeoutExpired:
        return False, "timeout", timeout * 1000


def run_suite(tests_dir, timeout=300):
    start = time.time()
    try:
        r = subprocess.run(
            ["pytest", str(tests_dir), "-q", "--no-header"],
            capture_output=True, text=True, timeout=timeout,
        )
        duration = (time.time() - start) * 1000
        passed = r.returncode == 0
        lines = [l for l in r.stdout.splitlines() if l.strip()]
        err = "" if passed else (lines[-1] if lines else "failed")
        return passed, err[:300], duration
    except subprocess.TimeoutExpired:
        return False, "timeout", timeout * 1000
