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

"""Markov chain bigram generator for onomatopoeic sequences.

Defines `MarkovChain`, a class that can be trained on a corpus of onomatopoeic
sequences and then generate new ones by walking the resulting Markov chain.

Corpus are defined in `src/futurizer/lang/*.py` in the `onomatopoeia_corpus` variable.
"""

import random


class MarkovChain:
    """Chain generator for onomatopoeic sequences.

    Each token in the corpus is mapped to the list of tokens
    that follow it. Generation walks that graph randomly.
    """

    def __init__(self, corpus: list[str], rng: random.Random | None = None):
        self.chain: dict[str, list[str]] = {}
        self.rng = rng if rng is not None else random.Random()
        self._train(corpus)

    def _train(self, corpus: list[str]) -> None:
        for sequence in corpus:
            tokens = sequence.split()
            for i in range(len(tokens) - 1):
                self.chain.setdefault(tokens[i], []).append(tokens[i + 1])

    def generate(self, length: int = 3) -> str:
        """Return a hyphen-joined onomatopoeia of at most *length* tokens.

        The actual length may be shorter if the walk reaches a leaf node
        (a token with no recorded successors). Falls back to 'ZANG' on
        an empty chain.
        """

        if not self.chain:
            return "ZANG"

        current = self.rng.choice(list(self.chain.keys()))
        result = [current]
        for _ in range(length - 1):
            successors = self.chain.get(current)
            if not successors:
                break
            current = self.rng.choice(successors)
            result.append(current)

        return "-".join(result)
