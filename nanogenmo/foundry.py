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

"""Futurize `Le avventure di Pinocchio`.

Carves the book out of the Project Gutenberg text, then forges it into chrome
chapter by chapter, with a noise level that follows a fixed curve.
"""

import re
import textwrap
from itertools import pairwise
from pathlib import Path

from futurizer import futurize

_CHAPTER_HEADING = re.compile(r"^[ \t]*([IVXLC]+)\.[ \t]*$", re.MULTILINE)
_IMAGE_CAPTION = re.compile(
    r"^[ \t]*\[Illustrazione:.*?\][ \t]*(?:\n|$)",
    re.MULTILINE | re.DOTALL,
)
_WIDTH = 88

# (chapter, noise): the level is interpolated linearly between the anchors
_NOISE_ANCHORS = (
    (1, 0.10),  # the talking piece of wood
    (9, 0.20),  # the puppet theatre, Mangiafoco
    (15, 0.35),  # the assassins, the hanging
    (19, 0.30),  # the Field of Miracles
    (27, 0.35),  # the fight at school
    (30, 0.45),  # Toyland
    (32, 0.60),  # the donkey
    (35, 0.55),  # the Dogfish
    (36, 0.50),  # the finale
)


def carve(text: str) -> str:
    """Strip Gutenberg boilerplate, title page, image captions and final index."""

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Keep what lies between the START and END markers
    text = text.partition("*** START OF")[2].partition("\n")[2]
    text = text.partition("*** END OF")[0]

    first_chapter = _CHAPTER_HEADING.search(text)
    if first_chapter:
        text = text[first_chapter.start() :]

    text = text[: text.rindex("FINE.") + len("FINE.")]
    text = _IMAGE_CAPTION.sub("\n\n", text)
    text = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text)
    return text.strip() + "\n"


def roll(text: str) -> str:
    """Wrap every verse at the page width, indenting the continuation lines."""

    return "\n".join(
        textwrap.fill(
            line,
            width=_WIDTH,
            subsequent_indent="    ",
            break_long_words=False,
            break_on_hyphens=False,
        )
        for line in text.split("\n")
    )


def din(chapter: int) -> float:
    """Return the noise level of a chapter, interpolating between anchors."""

    for (c0, n0), (c1, n1) in pairwise(_NOISE_ANCHORS):
        if c0 <= chapter <= c1:
            return n0 + (n1 - n0) * (chapter - c0) / (c1 - c0)

    raise ValueError(f"chapter {chapter} is outside the noise curve")


def forge(text: str, seed: int = 2026) -> str:
    """Futurize each chapter with its own noise level and seed.

    A title page goes first. The closing "FINE." is centered on the page width
    and the chapter numerals become ruled headings, since the engine would
    mangle both.

    The default seed is the year of the bicentenary of Carlo Collodi's birth.
    """

    textures = "~-=*#"  # from wood grain to rivets, as the noise grows

    parts = _CHAPTER_HEADING.split(text.rpartition("FINE.")[0].rstrip(" "))[1:]
    chapters = list(zip(parts[::2], parts[1::2], strict=True))
    expected = _NOISE_ANCHORS[-1][0]
    if len(chapters) != expected:
        raise ValueError(f"expected {expected} chapters, found {len(chapters)}")

    top = textures[0] * _WIDTH
    cover = "\n".join(
        line.center(_WIDTH).rstrip()
        for line in (
            "from wood TO CHROME",
            'after Carlo Collodi, "Le avventure di Pinocchio"',
        )
    )

    out = []
    for number, (numeral, chapter) in enumerate(chapters, start=1):
        noise = din(number)
        futurized = futurize(chapter, noise=noise, seed=seed + number)
        # The title is the first paragraph after the numeral
        title, _, verses = futurized.lstrip("\n").partition("\n\n")
        rule = textures[min(round(noise * 100) // 15, len(textures) - 1)] * _WIDTH
        label = f"CAPITOLO {numeral}".center(_WIDTH).rstrip()
        out.append(f"{rule}\n{label}\n{roll(title)}\n{rule}\n\n{roll(verses)}")

    ending = "FINE.".center(_WIDTH).rstrip()
    return f"{top}\n{cover}\n{top}\n\n" + "\n".join(out) + f"\n{ending}\n"


if __name__ == "__main__":
    corpus = Path(__file__).parent / "corpus"
    processed = corpus / "processed"
    processed.mkdir(parents=True, exist_ok=True)

    wood = carve((corpus / "raw" / "pinocchio.txt").read_text(encoding="utf-8"))
    (processed / "wood.txt").write_text(wood, encoding="utf-8")

    chrome = forge(wood)
    (processed / "chrome.txt").write_text(chrome, encoding="utf-8")

    chrome = forge(wood)
    (processed / "chrome.txt").write_text(chrome, encoding="utf-8")

    print("wc -w:", len(chrome.split()))
    print("alphanumeric sequences:", len(re.findall(r"\w+", chrome)))
