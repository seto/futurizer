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

"""Typeset `chrome.txt` as a PDF, the way a typewriter would.

A4, Courier 12 pt at 10 characters per inch (pica) and 6 lines per inch: 65 columns
by 58 lines, centered on the page. Every chapter starts on a new page, the color of
the headings goes from wood brown to chrome grey as the book advances, and the words
of the din are set in bold.
"""

import re
import textwrap
from itertools import groupby, pairwise
from pathlib import Path

from futurizer.lang.it import BURST_SEPARATORS, NOISE_SEQUENCES, ONOMATOPOEIA_CORPUS

_RULE = re.compile(r"^[~=*#-]{88}$")
_PIECES = re.compile(r"[^\W_]+|[\W_]+")
_WOOD = (0.55, 0.34, 0.17)
_CHROME = (0.40, 0.45, 0.50)
_BLACK = (0.0, 0.0, 0.0)
_TITLE = "from wood TO CHROME"

# The words of the din, set in bold
_DIN = {
    word
    for sequence in (*ONOMATOPOEIA_CORPUS, *NOISE_SEQUENCES, *BURST_SEPARATORS)
    for word in sequence.split()
}

# 65 columns of Courier 12 pt are 468 pt wide, centered on an A4 page
_WIDTH, _HEIGHT = 595.28, 841.89
_SIZE, _LEADING, _MARGIN_Y, _COLUMNS = 12, 12, 72, 65
_MARGIN_X = (_WIDTH - _COLUMNS * 0.6 * _SIZE) / 2
_PER_PAGE = int((_HEIGHT - 2 * _MARGIN_Y) // _LEADING)

Run = tuple[str, int, tuple[float, float, float]]  # text, font number, color
Line = tuple[Run, ...]


def _escape(line: str) -> bytes:
    data = line.encode("cp1252", errors="replace")
    return data.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def tint(t: float) -> tuple[float, float, float]:
    """Return the color between wood (t = 0) and chrome (t = 1)."""

    r, g, b = (a + (c - a) * t for a, c in zip(_WOOD, _CHROME, strict=True))
    return r, g, b


def ink(text: str) -> Line:
    """Split a verse into runs, inking the words of the din in bold."""

    pieces = [
        (piece, 2 if piece in _DIN else 1, _BLACK) for piece in _PIECES.findall(text)
    ]
    return tuple(
        ("".join(run[0] for run in group), font, color)
        for (font, color), group in groupby(pieces, key=lambda run: run[1:])
    )


def flow(lines: list[str]) -> list[str]:
    """Rejoin the verses wrapped in the text file and wrap them at the page width."""

    verses: list[str] = []
    for line in lines:
        # Continuation lines are indented: they belong to the verse above
        if line.startswith("    ") and verses and verses[-1]:
            verses[-1] += " " + line.strip()
        else:
            verses.append(line)

    out: list[str] = []
    for verse in verses:
        if verse.strip() == "FINE.":
            out.append("FINE.".center(_COLUMNS))
        else:
            out += textwrap.wrap(
                verse,
                _COLUMNS,
                subsequent_indent="  ",
                break_long_words=False,
                break_on_hyphens=False,
            ) or [""]
    return out


def typeset(text: str) -> list[list[Line]]:
    """Split the novel into pages: the cover, then every chapter on its own."""

    lines = text.rstrip("\n").split("\n")
    starts = [
        i
        for i in range(len(lines) - 1)
        if _RULE.match(lines[i]) and lines[i + 1].strip().startswith("CAPITOLO")
    ]

    pages: list[list[Line]] = []
    for k, (a, b) in enumerate(pairwise([0, *starts, len(lines)])):
        block = lines[a:b]
        while not block[-1].strip():
            block.pop()

        head = next(i for i in range(1, len(block)) if _RULE.match(block[i])) + 1
        styled: list[Line]
        if k == 0:
            top, title, subtitle, bottom = block[:head]
            before, mark, after = title.strip().center(_COLUMNS).partition("TO CHROME")
            styled = [
                ((top[0] * _COLUMNS, 2, _WOOD),),
                ((before, 2, _WOOD), (mark + after, 2, _CHROME)),
                (("", 1, _BLACK),),
                *[
                    ((t.center(_COLUMNS), 2, _BLACK),)
                    for t in textwrap.wrap(subtitle.strip(), _COLUMNS)
                ],
                ((bottom[0] * _COLUMNS, 2, _CHROME),),
            ]
            styled = [(("", 1, _BLACK),)] * 20 + styled
        else:
            color = tint((k - 1) / (len(starts) - 1))
            rule, label, *title, _ = block[:head]
            heading = [
                rule[0] * _COLUMNS,
                label.strip().center(_COLUMNS),
                "",
                *textwrap.wrap(" ".join(t.strip() for t in title), _COLUMNS),
                rule[0] * _COLUMNS,
            ]
            styled = [((t, 2, color),) for t in heading]
        styled += [ink(t) for t in flow(block[head:])]

        pages += [styled[i : i + _PER_PAGE] for i in range(0, len(styled), _PER_PAGE)]

    return pages


def bind(pages: list[list[Line]]) -> bytes:
    """Assemble the PDF: two Courier fonts and one content stream per page."""

    count = len(pages)
    kids = b" ".join(b"%d 0 R" % (3 + 2 * n) for n in range(1, count + 1))
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [%s] /Count %d >>" % (kids, count),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier "
        b"/Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold "
        b"/Encoding /WinAnsiEncoding >>",
    ]
    page_object = (
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %g %g] "
        b"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents %d 0 R >>"
    )

    for number, page in enumerate(pages, start=1):
        content = [
            b"BT",
            b"%g TL" % _LEADING,
            b"%g %g Td" % (_MARGIN_X, _HEIGHT - _MARGIN_Y),
        ]
        current = None
        for line in page:
            for text, font, color in line:
                if (font, color) != current:
                    content.append(b"/F%d %g Tf %g %g %g rg" % (font, _SIZE, *color))
                    current = (font, color)
                content.append(b"(%s) Tj" % _escape(text))
            content.append(b"T*")

        label = str(number).encode()
        x = (_WIDTH - len(label) * 0.6 * 8) / 2
        content += [
            b"ET",
            b"BT /F1 8 Tf 0.45 g 1 0 0 1 %g %g Tm (%s) Tj ET"
            % (x, _MARGIN_Y / 2, label),
        ]
        stream = b"\n".join(content)

        objects.append(page_object % (_WIDTH, _HEIGHT, 4 + 2 * number))
        objects.append(
            b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream)
        )

    objects.append(b"<< /Title (%s) >>" % _TITLE.encode("ascii"))

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (number, body)

    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    for offset in offsets:
        out += b"%010d 00000 n \n" % offset
    out += b"trailer\n<< /Size %d /Root 1 0 R /Info %d 0 R >>\n" % (
        len(objects) + 1,
        len(objects),
    )
    out += b"startxref\n%d\n%%%%EOF\n" % xref
    return bytes(out)


def main():
    processed = Path(__file__).parent / "corpus" / "processed"
    text = (processed / "chrome.txt").read_text(encoding="utf-8")

    lost = {c for c in text if c.encode("cp1252", errors="replace") == b"?"} - {"?"}
    if lost:
        raise SystemExit(f"not available in Courier: {''.join(sorted(lost))}")

    (processed / "chrome.pdf").write_bytes(bind(typeset(text)))


if __name__ == "__main__":
    main()
