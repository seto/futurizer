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

"""
"""

import re

_GUTENBERG_START = re.compile(
    r"^[ \t]*\*{3}\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK\b.*$",
    re.IGNORECASE | re.MULTILINE,
)
_GUTENBERG_END = re.compile(
    r"^[ \t]*\*{3}\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK\b.*$",
    re.IGNORECASE | re.MULTILINE,
)
_CHAPTER_HEADING = re.compile(r"^[ \t]*[IVXLCDM]+\.[ \t]*$", re.MULTILINE)
_BOOK_END = re.compile(r"^[ \t]*FINE\.[ \t]*$", re.MULTILINE)
_IMAGE_CAPTION = re.compile(
    r"^[ \t]*\[(?:illustrazione|illustration|immagine|image)\s*:.*?\][ \t]*(?:\n|$)",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
_BLANK_RUNS = re.compile(r"\n[ \t]*\n(?:[ \t]*\n)+")


def clean(text: str) -> str:
    """Strip Gutenberg boilerplate, title page, image captions and final index."""

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    start = _GUTENBERG_START.search(text)
    if start:
        text = text[start.end() :]

    end = _GUTENBERG_END.search(text)
    if end:
        text = text[: end.start()]

    # The title page precedes the book: start at the first chapter heading
    first_chapter = _CHAPTER_HEADING.search(text)
    if first_chapter:
        text = text[first_chapter.start() :]

    # The index follows the closing "FINE.": keep that line, drop the rest
    book_end = list(_BOOK_END.finditer(text))
    if book_end:
        text = text[: book_end[-1].end()]

    text = _IMAGE_CAPTION.sub("\n\n", text)
    text = _BLANK_RUNS.sub("\n\n", text)
    text = text.strip()
    return f"{text}\n" if text else ""
