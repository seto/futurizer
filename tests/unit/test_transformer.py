import copy
import random
from typing import cast

import pytest

from futurizer.engine.transformer import FuturistTransformer
from futurizer.langdata import Pos


class FixedRandom(random.Random):
    def __init__(self, roll: float, randint_value: int = 2):
        super().__init__(0)
        self.roll = roll
        self.randint_value = randint_value

    def random(self) -> float:
        return self.roll

    def randint(self, a: int, b: int) -> int:
        return self.randint_value


def test_function_words_return_none(it_lang_data, rng):
    transformer = FuturistTransformer(it_lang_data, rng=rng)
    for pos in ("ART", "PREP", "CONJ", "PRON"):
        assert (
            transformer.transform("parola", pos) is None
        ), f"POS '{pos}' should return None"


def test_verb_returns_uppercase_string(it_lang_data, rng):
    transformer = FuturistTransformer(it_lang_data, rng=rng)
    result = transformer.transform("correre", "VERB")
    assert isinstance(result, str) and result == result.upper()


def test_noun_returns_uppercase_string(it_lang_data, rng):
    transformer = FuturistTransformer(it_lang_data, rng=rng)
    result = transformer.transform("treno", "NOUN")
    assert isinstance(result, str) and result == result.upper()


def test_adj_drop_rate(it_lang_data):
    # With enough samples the drop rate should be close to the threshold.
    # We use a fixed seed per iteration to isolate randomness.
    threshold = it_lang_data["thresholds"]["adj_drop"]
    tolerance = 0.05
    N = 2_000
    dropped = 0
    for seed in range(N):
        transformer = FuturistTransformer(it_lang_data, rng=random.Random(seed))
        if transformer.transform("veloce", "ADJ") is None:
            dropped += 1
    assert (
        abs(dropped / N - threshold) < tolerance
    ), f"ADJ drop rate {dropped/N:.3f} deviates from threshold {threshold}"


def test_adv_returns_exclamation(it_lang_data, rng):
    transformer = FuturistTransformer(it_lang_data, rng=rng)
    result = transformer.transform("velocemente", "ADV")
    assert result is not None and result.endswith("!")


def test_thresholds_from_lang_data(it_lang_data, rng):
    # Transformer must read thresholds from lang_data, not hardcoded constants
    custom = copy.copy(it_lang_data)
    custom["thresholds"] = {
        **it_lang_data["thresholds"],
        "adj_drop": 0.0,  # never drop
    }

    transformer = FuturistTransformer(custom, rng=rng)
    for seed in range(20):
        transformer.rng = random.Random(seed)
        assert (
            transformer.transform("veloce", "ADJ") is not None
        ), "ADJ should never be dropped with adj_drop=0.0"


def test_to_infinitive_italian_past_historic(it_lang_data, rng):
    transformer = FuturistTransformer(it_lang_data, rng=rng)
    assert transformer._to_infinitive("gridò") == "GRIDARE"
    assert transformer._to_infinitive("sentì") == "SENTIRE"


def test_to_infinitive_future_not_shadowed_by_past_historic(it_lang_data, rng):
    # Rule order matters: ("irò", "ire") must come before the generic
    # ("ò", "are"), otherwise "dormirò" becomes "DORMIRARE".
    transformer = FuturistTransformer(it_lang_data, rng=rng)
    assert transformer._to_infinitive("dormirò") == "DORMIRE"


def test_to_infinitive_falls_back_to_uppercase(it_lang_data, rng):
    transformer = FuturistTransformer(it_lang_data, rng=rng)
    assert transformer._to_infinitive("xyz") == "XYZ"


def test_verb_elongation_appends_vowels(it_lang_data):
    transformer = FuturistTransformer(
        it_lang_data, rng=FixedRandom(roll=0.0, randint_value=3)
    )
    assert transformer.transform("cantare", "VERB") == "CANTAREEEE"


def test_verb_elongation_uses_r_for_non_vowel_ending(it_lang_data):
    transformer = FuturistTransformer(it_lang_data, rng=FixedRandom(roll=0.0))
    assert transformer.transform("xyz", "VERB") == "XYZRRRR"


def test_verb_repeat_branch_repeats_infinitive(it_lang_data):
    transformer = FuturistTransformer(
        it_lang_data, rng=FixedRandom(roll=0.5, randint_value=2)
    )
    assert transformer.transform("cantare", "VERB") == "CANTARE + CANTARE"


def test_unexpected_pos_fails_loudly(it_lang_data, rng):
    transformer = FuturistTransformer(it_lang_data, rng=rng)
    with pytest.raises(AssertionError, match="unreachable"):
        transformer.transform("parola", cast(Pos, "INVALID"))
