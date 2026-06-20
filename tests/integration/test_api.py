import random

import futurizer


def test_same_seed_same_output():
    out1 = futurizer.futurize("Nel mezzo del cammin di nostra vita", seed=66)
    out2 = futurizer.futurize("Nel mezzo del cammin di nostra vita", seed=66)
    # Same seed must produce identical output
    assert out1 == out2


def test_different_seeds_different_output():
    out1 = futurizer.futurize("Nel mezzo del cammin di nostra vita", seed=66)
    out2 = futurizer.futurize("Nel mezzo del cammin di nostra vita", seed=99)
    # Different seeds must produce different output
    assert out1 != out2


def test_does_not_touch_global_random_state():
    random.seed(1)
    x = random.random()
    futurizer.futurize("Nel mezzo del cammin di nostra vita", seed=66)
    random.seed(1)
    y = random.random()
    # futurize() must not touch global random state
    assert x == y


def test_empty_input_returns_empty():
    assert futurizer.futurize("") == ""
    assert futurizer.futurize("   ") == ""


def test_unsupported_language_raises():
    try:
        futurizer.futurize("test", lang="zz")
        assert False
    except futurizer.UnsupportedLanguageError:
        # futurize() must raise UnsupportedLanguageError for unsupported languages
        pass


def test_languages_contains_defaults():
    langs = futurizer.languages()
    assert "it" in langs
    assert "en" in langs 


def test_english_lang():
    out = futurizer.futurize(
        "To be, or not to be, that is the question",
        lang="en",
        seed=1,
    )
    assert isinstance(out, str) and len(out) > 0
