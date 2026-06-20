import random

from futurizer.engine.markov import MarkovChain


def test_generate_returns_string(it_markov):
    result = it_markov.generate(3)
    assert isinstance(result, str) and len(result) > 0


def test_generate_respects_length(it_lang_data, rng):
    # Output tokens (hyphen-separated) should never exceed requested length
    markov = MarkovChain(it_lang_data["onomatopoeia_corpus"], rng=rng)
    for length in (1, 2, 3, 4):
        result = markov.generate(length)
        assert (
            len(result.split("-")) <= length
        ), f"generate({length}) produced more than {length} tokens: {result}"


def test_generate_empty_corpus_returns_fallback(rng):
    markov = MarkovChain([], rng=rng)
    assert markov.generate() == "ZANG"


def test_reproducible_with_same_rng(it_lang_data):
    rng1 = random.Random(7)
    rng2 = random.Random(7)
    m1 = MarkovChain(it_lang_data["onomatopoeia_corpus"], rng=rng1)
    m2 = MarkovChain(it_lang_data["onomatopoeia_corpus"], rng=rng2)
    assert m1.generate(3) == m2.generate(3)
