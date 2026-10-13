
"""CLI: isolate audit <tests-dir>"""

import argparse
import json
import sys
from pathlib import Path

from isolate import __version__
from isolate.audit import audit


def cmd_audit(args):
    try:
        report = audit(args.tests_dir, quiet=args.quiet)
    except Exception as e:
        print("error: " + str(e), file=sys.stderr)
        sys.exit(2)

    print()
    print("=== Results ===")
    print("  isolated:        " + str(report.isolated))
    print("  order-dependent: " + str(report.order_dependent))
    print("  polluter:        " + str(report.polluter))
    print("  broken:          " + str(report.broken))
    print()

    problems = report.order_dependent + report.polluter
    if problems > 0:
        print("=== Problems ===")
        for a in report.audits:
            if a.verdict != "isolated":
                print("  [" + a.verdict + "] " + a.test_id)
                print("      " + a.reason)
        print()

    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
        print("JSON: " + args.json)

    if problems > 0 and args.fail_on_problems:
        sys.exit(1)


def cmd_version(args):
    print("isolate " + __version__)


def main():
    parser = argparse.ArgumentParser(prog="isolate")
    parser.add_argument("--version", action="version", version="isolate " + __version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("audit", help="find order-dependent tests")
    p.add_argument("tests_dir")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--json", help="write JSON results here")
    p.add_argument("--fail-on-problems", action="store_true")
    p.set_defaults(func=cmd_audit)

    pv = sub.add_parser("version")
    pv.set_defaults(func=cmd_version)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
