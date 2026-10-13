# isolate

[![Tests](https://github.com/kallurayaankit/isolate/actions/workflows/test.yml/badge.svg)](https://github.com/kallurayaankit/isolate/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Find the tests that only pass because of other tests.**

```bash
pip install -e .
isolate audit tests/

The problem

You have 200 tests. They all pass in CI. They all pass locally. Then someone runs one test on its own and it fails. Or reorders the file alphabetically and three tests break. Or enables parallel execution and the whole suite goes red.

Your tests are coupled. They share state through a database row, a module-level dict, a file on disk, a mocked object that leaks. The coupling is invisible because CI always runs them in the same order.

Every test suite has this problem. Most teams never see it because they never look.
What it does

isolate runs each test twice:

    Once as part of the full suite (the normal way)

    Once alone, in its own pytest process, with no other test having run before it

Then it compares the two results. Four possible verdicts:
Verdict	Meaning
isolated	Passes alone and in the suite
order_dependent	Passes in the suite, fails alone — depends on another test
polluter	Passes alone, but the suite fails — probably leaking state
broken	Fails both ways — a real bug in the test

The order_dependent result is the headline. That's a test that's lying to you.
The output
text

$ isolate audit tests/

Found 5 tests
Running the suite once...
  suite: PASS
Running each test alone...
  [1/5] .  test_00_isolated_pass
  [2/5] .  test_01_isolated_pass_too
  [3/5] .  test_02_creates_user
  [4/5] X  test_03_needs_user
  [5/5] .  test_04_another_pass

=== Results ===
  isolated:        4
  order-dependent: 1
  polluter:        0
  broken:          0

=== Problems ===
  [order_dependent] examples/demo_tests/test_demo.py::test_03_needs_user
      passes in suite but FAILS alone - depends on other tests

The . marks tests that are fine. The X marks a test that only passes because test_02_creates_user ran first.
Quickstart
bash

# install
python -m venv .venv
.venv\Scripts\activate          # or source .venv/bin/activate
pip install -e .

# try it on the demo
isolate audit examples/demo_tests

# point it at your own tests
isolate audit path/to/your/tests

# fail CI when problems are found
isolate audit tests --fail-on-problems

# also write JSON
isolate audit tests --json out/audit.json

Verified results

Two runs from real projects:

The demo suite (5 tests, one deliberately order-dependent):
text

isolated:        4
order-dependent: 1

isolate found the bug.

A real 79-test suite (rely):
text

isolated:        79
order-dependent: 0
polluter:        0
broken:          0

isolate correctly reported nothing when there was nothing to report. That's the harder test.
How it works
text

┌─────────────────┐
│  discover.py    │  pytest --collect-only → list of test IDs
└────────┬────────┘
         │
┌────────▼────────┐
│  runner.py      │  pytest <id> -x    → did it pass alone?
│                 │  pytest <dir>      → did the suite pass?
└────────┬────────┘
         │
┌────────▼────────┐
│  audit.py       │  compare → assign verdict → build report
└────────┬────────┘
         │
┌────────▼────────┐
│  cli.py         │  print + optionally exit(1)
└─────────────────┘

No subprocess magic beyond pytest itself. No plugins. No LLM. Just: run the suite, run each test alone, compare.
Installation note

isolate runs pytest in a subprocess. That subprocess uses whatever environment isolate was installed into. If you want to audit a project, isolate needs to share a venv with that project's dependencies — or you install isolate into the project's own venv.

Two ways that work:
bash

# Option A: install the target into isolate's venv
pip install -e /path/to/target

# Option B: install isolate into the target's venv
cd /path/to/target
pip install -e /path/to/isolate
isolate audit tests

What this is not

    Not a flake detector. pulse finds tests that are nondeterministic across identical runs. isolate finds tests that are deterministic but coupled.

    Not a test selector. It runs everything. Twice.

    Not fast on large suites. 200 tests × 1 second each = 200 seconds. It's meant for periodic audits, not every commit.

Status

Early. Works on pytest suites. Roadmap: parallel isolation checks, shuffled-ordering mode (run the suite in 3 random orders, look for flips), shared-state tracer (parse test code for module-level writes and file I/O to guess the coupling).
License

MIT
