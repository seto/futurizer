import copy
import random

from futurizer.engine.transformer import FuturistTransformer


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
