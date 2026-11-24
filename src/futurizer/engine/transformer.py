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

"""Token-level futurist transformations.

Defines `FuturistTransformer`, which maps each POS-tagged token to its
futurist equivalent using randomized stylistic rules.
"""

import random
from typing import assert_never

from ..langdata import LangData, Pos
from .markov import MarkovChain


class FuturistTransformer:
    """Apply futurist transformations to POS-tagged tokens.

    Verbs are elongated, repeated, or fused with onomatopoeia.
    Nouns are uppercased and fused with mechanical vocabulary.
    Adjectives are randomly dropped or kept in uppercase.
    Adverbs are randomly dropped or kept in uppercase with a trailing "!".
    Function words (articles, prepositions, conjunctions, pronouns) are deleted.
    """

    def __init__(self, lang_data: LangData, rng: random.Random | None = None):
        self.rules = lang_data["rules"]
        self.irregular_verbs = lang_data["tagger_rules"].get("irregular_verbs", {})
        self.mechanical_words = lang_data["mechanical_words"]
        self.thresholds = lang_data.get("thresholds", {})
        self.rng = rng if rng is not None else random.Random()
        self.markov = MarkovChain(lang_data["onomatopoeia_corpus"], rng=self.rng)

    def _to_infinitive(self, word: str) -> str:
        """Return the approximate infinitive form of a verb in uppercase.

        Applies the language's verb_to_infinitive suffix rules in order.
        Falls back to the uppercased original if no rule matches.
        """

        w = word.lower()
        for infinitive, forms in self.irregular_verbs.items():
            if w in forms:
                return infinitive.upper()

        for pattern, replacement in self.rules.get("verb_to_infinitive", []):
            if w.endswith(pattern) and len(w) > len(pattern) + 2:
                stem = w[: -len(pattern)]
                return (stem + replacement).upper()

        return word.upper()

    def _futurize_verb(self, word: str) -> str:
        inf = self._to_infinitive(word)
        roll = self.rng.random()

        if roll < self.thresholds.get("verb_elongate_upto", 0.35):
            # Elongated echo: URLARE → URLAREEEEE
            if inf and inf[-1] in "aeiouAEIOU":
                return inf + inf[-1] * self.rng.randint(2, 4)
            return inf + "RRRR"

        if roll < self.thresholds.get("verb_repeat_upto", 0.65):
            # Repetition: SALIRE → SALIRE + SALIRE + SALIRE
            n = self.rng.randint(2, 3)
            return " + ".join([inf] * n)

        ono = self.markov.generate(self.rng.randint(2, 3))
        return f"{inf}-{ono}"

    def _futurize_noun(self, word: str) -> str:
        w = word.upper()
        mech = self.rng.choice(self.mechanical_words)
        roll = self.rng.random()

        if roll < self.thresholds.get("noun_prefix_upto", 0.40):
            return f"{w}-{mech}"
        if roll < self.thresholds.get("noun_plain_upto", 0.70):
            # Uppercase only as the compositor will add separator
            return w

        return f"{mech}-{w}"

    def _futurize_adj(self, word: str) -> str | None:
        if self.rng.random() < self.thresholds.get("adj_drop", 0.50):
            return None

        return word.upper()

    def _futurize_adv(self, word: str) -> str | None:
        if self.rng.random() < self.thresholds.get("adv_drop", 0.50):
            return None

        return word.upper() + "!"

    def transform(self, word: str, pos: Pos) -> str | None:
        match pos:
            case "VERB":
                return self._futurize_verb(word)
            case "NOUN":
                return self._futurize_noun(word)
            case "ADJ":
                return self._futurize_adj(word)
            case "ART" | "PREP" | "CONJ" | "PRON":
                # Function words are deleted per futurist manifesto
                return None
            case "ADV":
                return self._futurize_adv(word)
            case "OTHER":
                return word.upper()
            case _:
                assert_never(pos)
