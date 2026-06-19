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

"""Futurist transformation pipeline.

Exposes `futurize`, the single public entry point that transforms
plain text into futurist-style output.
"""

import random
import re

from .markov import MarkovChain
from .transformer import FuturistTransformer

_SEPARATORS = ["×", ">", "/", "+", "—", "::"]
_PREFIX_NOISE_RATIO = 0.3


def futurize(
    text: str,
    lang_data: dict,
    noise: float,
    rng: random.Random | None = None,
) -> str:
    """Transform plain text into futurist-style output.

    Each line is parsed, POS-tagged, transformed, composed with
    futurist separators, and optionally corrupted with onomatopoeia.

    If `rng` is omitted, a fresh random.Random() is used internally;
    pass one to make output reproducible without touching global state.
    """

    lang_rules = lang_data["tagger_rules"]
    rng = rng if rng is not None else random.Random()
    transformer = FuturistTransformer(lang_data, rng=rng)
    markov = transformer.markov

    parsed_verses = _parse(text)
    output_verses = []
    for tokens in parsed_verses:
        if not tokens:
            output_verses.append("")
            continue

        words = [(tok, typ) for tok, typ in tokens if typ == "word"]
        if not words:
            output_verses.append("")
            continue

        transformed = []
        for word, _ in words:
            pos = _tag(word, lang_rules)
            result = transformer.transform(word, pos)
            transformed.append(result)

        verse = _compose(transformed, lang_data, noise=noise, rng=rng)
        verse = _corrupt(verse, markov, lang_data, noise=noise, rng=rng)
        output_verses.append(verse)

    return "\n".join(output_verses)


def _parse(text: str) -> list[list[tuple[str, str]]]:
    """Tokenize text into verses, preserving line structure.

    Returns a list of verses; each verse is a list of (token, type) tuples
    where type is one of 'word', 'punct', or 'space'.
    """

    verses = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            verses.append([])
            continue

        tokens = []
        for m in re.finditer(r"[^\W\d_]+|\d+|[.,;:!?\"'()«»\-–—\/]|\s+", line):
            tok = m.group()
            if tok.strip() == "":
                tokens.append((tok, "space"))
            elif re.match(r"[^\W\d_]+|\d+", tok):
                tokens.append((tok, "word"))
            else:
                tokens.append((tok, "punct"))

        verses.append(tokens)

    return verses


def _tag(word: str, lang_rules: dict) -> str:
    """Return the POS tag for a word using suffix rules.

    Returns one of: 'VERB', 'NOUN', 'ADJ', 'ADV', 'PREP', 'ART', 'CONJ',
    'PRON', 'OTHER'. Lookup order: function-word lists, then suffix rules,
    then heuristic vowel-ending fallbacks.
    """

    w = word.lower()

    if w in lang_rules.get("articles", set()):
        return "ART"
    if w in lang_rules.get("preps", set()):
        return "PREP"
    if w in lang_rules.get("conjunctions", set()):
        return "CONJ"
    if w in lang_rules.get("pronouns", set()):
        return "PRON"

    verb_suffixes = lang_rules.get("verb_suffixes", [])
    adj_suffixes = lang_rules.get("adj_suffixes", [])
    adv_suffixes = lang_rules.get("adv_suffixes", [])
    noun_suffixes = lang_rules.get("noun_suffixes", [])

    for sfx in verb_suffixes:
        if w.endswith(sfx) and len(w) > len(sfx) + 2:
            return "VERB"
    for sfx in adv_suffixes:
        if w.endswith(sfx) and len(w) > len(sfx) + 2:
            return "ADV"
    for sfx in adj_suffixes:
        if w.endswith(sfx) and len(w) > len(sfx) + 1:
            return "ADJ"
    for sfx in noun_suffixes:
        if w.endswith(sfx) and len(w) > len(sfx) + 1:
            return "NOUN"

    if len(w) > 3:
        # Verb infinitives truncated by apocope (poetic/archaic register):
        # "cantar" → "cantare", "veder" → "vedere", "partir" → "partire"
        if w.endswith(("ar", "er", "ir")):
            return "VERB"

        # Typical nouns/adjectives for the Italian language
        if w.endswith(("a", "e", "i", "o")):
            return "NOUN"

    return "OTHER"


def _compose(
    tokens_transformed: list[str],
    lang_data: dict,
    noise: float,
    rng: random.Random,
) -> str:
    """Assemble transformed tokens with futurist separators.

    Injects random onomatopoeic bursts between tokens at the
    rate specified by noise.
    """

    cleaned = [t for t in tokens_transformed if t]
    if not cleaned:
        return ""

    burst_seps = lang_data.get("burst_separators", [])

    parts = []
    for i, tok in enumerate(cleaned):
        parts.append(tok)
        if i < len(cleaned) - 1:
            sep = rng.choice(_SEPARATORS)
            parts.append(sep)
            if burst_seps and rng.random() < noise:
                burst = rng.choice(burst_seps)
                parts.append(burst)
                parts.append(rng.choice(_SEPARATORS))

    return " ".join(parts)


def _corrupt(
    verse: str,
    markov: MarkovChain,
    lang_data: dict,
    noise: float,
    rng: random.Random,
) -> str:
    """Inject onomatopoeic noise at the start or end of a verse.

    Prefix noise (a sequence from the corpus) occurs at `noise * _PREFIX_NOISE_RATIO`
    probability; suffix noise (a Markov-generated sequence) at `noise`.
    Prefixes are less frequent because they disrupt the reading flow more aggressively.
    """

    if not verse:
        return verse

    noise_seqs = lang_data.get("noise_sequences", [])

    if noise_seqs and rng.random() < (noise * _PREFIX_NOISE_RATIO):
        verse = f"{rng.choice(noise_seqs)} > {verse}"

    if rng.random() < noise:
        verse = f"{verse} > {markov.generate(rng.randint(2, 4))}"

    return verse
