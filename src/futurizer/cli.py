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

    python -m futurizer input.txt

CLI arguments:
- `input`: The .txt file to transform, or '-' to read from stdin.
- `-l` or `--lang`: The language code of the text (defaults to "it").
- `--noise`: Corruption noise level (defaults to 0.15).
- `--seed`: Random seed for reproducibility.

For more details, run with `-h` or `--help`.
"""

import argparse
import sys

from . import api

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    ap = argparse.ArgumentParser(
        prog="futurize",
        description="Transform a plain text file into futurist-style output.",
    )
    ap.add_argument(
        "input",
        help="path to the .txt file to transform, or '-' to read from stdin",
    )
    ap.add_argument(
        "-l",
        "--lang",
        choices=sorted(api.languages()),
        default=api.DEFAULT_LANG,
        help=f"language code (default: {api.DEFAULT_LANG})",
    )
    ap.add_argument(
        "--noise",
        type=float,
        default=api.DEFAULT_NOISE,
        help=f"corruption noise level (default: {api.DEFAULT_NOISE})",
    )
    ap.add_argument(
        "--seed",
        type=int,
        default=None,
        help="random seed for reproducibility",
    )

    args = ap.parse_args(argv)

    try:
        if args.input == "-":
            text = sys.stdin.read()
        else:
            with open(args.input, encoding="utf-8") as f:
                text = f.read()

    except FileNotFoundError:
        print(f"Error: file {args.input} not found.", file=sys.stderr)
        return 1

    except UnicodeDecodeError:
        print("Error: input not readable as UTF-8.", file=sys.stderr)
        return 1

    if not text.strip():
        print("Error: input is empty.", file=sys.stderr)
        return 1

    try:
        print(api.futurize(text,lang=args.lang,noise=args.noise,seed=args.seed))
        return 0
    
    except api.UnsupportedLanguageError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
