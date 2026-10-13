
"""Find tests in a directory."""

import re
import subprocess


COLLECT_RE = re.compile(r"^(?P<file>[^:]+)::(?P<name>[^\s]+)")


def discover(tests_dir):
    result = subprocess.run(
        ["pytest", str(tests_dir), "--collect-only", "-q", "--no-header"],
        capture_output=True, text=True, timeout=60,
    )
    test_ids = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if COLLECT_RE.match(line):
            test_ids.append(line)
    return test_ids
