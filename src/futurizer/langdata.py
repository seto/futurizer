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

"""Shared types describing the shape of language data.

Defines `Pos`, the closed set of part-of-speech tags produced by the tagger,
and the `TypedDict` hierarchy behind `LangData`, the structure each module in
`src/futurizer/lang/` must expose as `LANG_DATA`.

The engine reads optional keys with `.get()` and a default, so a language may
omit them. Declaring them as optional here keeps mypy aligned with that
behavior rather than imposing stricter requirements.
"""

from typing import Literal, NotRequired, TypedDict

Pos = Literal["VERB", "NOUN", "ADJ", "ADV", "PREP", "ART", "CONJ", "PRON", "OTHER"]


class TaggerRules(TypedDict, total=False):
    """Function-word sets and suffix lists used by the rule-based POS tagger."""

    articles: set[str]
    preps: set[str]
    conjunctions: set[str]
    pronouns: set[str]
    verb_suffixes: list[str]
    adj_suffixes: list[str]
    adv_suffixes: list[str]
    noun_suffixes: list[str]


class Rules(TypedDict, total=False):
    """Morphological rewrite rules."""

    verb_to_infinitive: list[tuple[str, str]]


class Thresholds(TypedDict, total=False):
    """Probability cut-offs for the stochastic transformations.

    The `*_upto` values are cumulative upper bounds on a single roll in [0, 1);
    `adj_drop` is a plain probability.
    """

    verb_elongate_upto: float
    verb_repeat_upto: float
    noun_prefix_upto: float
    noun_plain_upto: float
    adj_drop: float


class LangData(TypedDict):
    """Complete language data bundle, exposed by each language module."""

    name: str
    code: str
    tagger_rules: TaggerRules
    rules: Rules
    mechanical_words: list[str]
    onomatopoeia_corpus: list[str]
    noise_sequences: NotRequired[list[str]]
    burst_separators: NotRequired[list[str]]
    thresholds: NotRequired[Thresholds]
