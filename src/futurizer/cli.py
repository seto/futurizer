#!/usr/bin/env python3

# Copyright (C) 2026  Roberto Matarazzo
#
# This file is part of Futurizer.
#
# Futurizer is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Futurizer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Futurizer.  If not, see <https://www.gnu.org/licenses/>.

"""Command-line interface for Futurizer.

This module can be executed from the command line using the following command
from the `src` directory:

    python -m futurizer input.txt -l it --noise 0.25

CLI arguments:
- `input`: The .txt file to transform.
- `-l` or `--lang`: The language code of the text (defaults to "it").
- `--noise`: Corruption noise level (defaults to 0.15).
- `--seed`: Random seed for reproducibility.

For more details, run with `-h` or `--help`.
"""

import argparse
import random
import sys

from .engine.compositor import futurize


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    ap = argparse.ArgumentParser(
        prog="futurize",
        description="Transform a plain text file into futurist-style output.",
    )
    ap.add_argument(
        "input",
        help="path to the file to transform, supported formats: .txt",
    )
    ap.add_argument(
        "-l",
        "--lang",
        choices=["it", "en"],
        default="it",
        help="language code (default: it)",
    )
    ap.add_argument(
        "--noise",
        type=float,
        default=0.15,
        help="corruption noise level (default: 0.15)",
    )
    ap.add_argument(
        "--seed",
        type=int,
        default=None,
        help="random seed for reproducibility",
    )

    args = ap.parse_args(argv)

    if args.seed is not None:
        random.seed(args.seed)

    try:
        if args.lang == "it":
            from .lang.it import LANG_DATA
        elif args.lang == "en":
            from .lang.en import LANG_DATA

    except ImportError:
        print(f"Error: language data for '{args.lang}' not found.", file=sys.stderr)
        return 1

    try:
        with open(args.input, encoding="utf-8") as f:
            text = f.read()

    except FileNotFoundError:
        print(f"Error: file {args.input} not found.", file=sys.stderr)
        return 1

    except UnicodeDecodeError:
        print("Error: file not readable as UTF-8.", file=sys.stderr)
        return 1

    if not text.strip():
        print("Error: file is empty.", file=sys.stderr)
        return 1

    print(futurize(text, lang_data=LANG_DATA, noise=args.noise))
    return 0


if __name__ == "__main__":
    sys.exit(main())
