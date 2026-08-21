"""Run the full test suite.

The test suit can be executed from the command line using the following
command from the root of the project:

    python tests/run.py [options]

Extra pytest arguments are forwarded as-is, e.g.:
    python tests/run.py -k test_cache
    python tests/run.py --no-cov -x
"""

import sys

import pytest


def main():
    extra = sys.argv[1:]
    args = [
        "--cov=futurizer",
        "--cov-report=term-missing",
        *extra,
    ]
    return pytest.main(args)


if __name__ == "__main__":
    sys.exit(main())
