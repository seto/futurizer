import random

from futurizer.engine.compositor import _corrupt, _parse
from futurizer.engine.compositor import futurize as engine_futurize


def test_parse_token_kinds():
    (tokens,) = _parse("Il 3, treno")
    assert tokens == [
        ("Il", "word"),
        (" ", "space"),
        ("3", "word"),
        (",", "punct"),
        (" ", "space"),
        ("treno", "word"),
    ]


def test_parse_reconstructs_line():
    line = "Il treno, veloce, corre: 3 volte!"
    (tokens,) = _parse(line)
    assert "".join(tok for tok, _ in tokens) == line


def test_parse_preserves_blank_lines():
    verses = _parse("Il treno corre\n\nLa macchina vola")
    assert len(verses) == 3
    assert verses[1] == []


def test_parse_splits_elision_at_apostrophe():
    # The tagger relies on this: it sees "dell" and "albero", not "dell'albero".
    (tokens,) = _parse("dell'albero")
    assert [tok for tok, _ in tokens] == ["dell", "'", "albero"]


def test_engine_futurize_without_rng(it_lang_data):
    # engine_futurize must not crash when rng is omitted (internal fallback)
    out = engine_futurize(
        "Sempre caro mi fu quest'ermo colle",
        lang_data=it_lang_data,
        noise=0.15,
    )
    assert isinstance(out, str) and len(out) > 0


def test_elisions_do_not_leak(it_lang_data):
    # Elision stems ("dell'", "nell'", "c'", ...) must be deleted like any
    # other function word, not survive as isolated tokens.
    text = "Nell'acqua dell'albero c'era un'ombra"
    stems = {"NELL", "DELL", "C"}
    for seed in range(50):
        out = engine_futurize(
            text,
            lang_data=it_lang_data,
            noise=0.0,
            rng=random.Random(seed),
        )
        assert not stems & set(out.upper().split()), f"Elision stem in: {out}"


def test_function_words_deleted(it_lang_data):
    # Articles, prepositions, and conjunctions must be stripped from output.
    # noise=0.0 disables bursts and Markov corruption so the output
    # contains only transformed content tokens, making the check reliable.
    function_words = (
        it_lang_data["tagger_rules"]["articles"]
        | it_lang_data["tagger_rules"]["preps"]
        | it_lang_data["tagger_rules"]["conjunctions"]
    )
    for seed in range(50):
        out = engine_futurize(
            "Sempre caro mi fu quest'ermo colle",
            lang_data=it_lang_data,
            noise=0.0,
            rng=random.Random(seed),
        )
        tokens = out.upper().split()
        for fw in function_words:
            assert fw.upper() not in tokens, f"Function word '{fw}' survived in: {out}"


def test_multiline_preserves_structure(it_lang_data, rng):
    text = "Il treno corre\nLa macchina vola"
    out = engine_futurize(text, lang_data=it_lang_data, noise=0.0, rng=rng)
    # Line structure must be preserved
    assert out.count("\n") == 1


def test_empty_lines_preserved(it_lang_data, rng):
    text = "Il treno corre\n\nLa macchina vola"
    out = engine_futurize(text, lang_data=it_lang_data, noise=0.0, rng=rng)
    # Empty lines must be preserved
    assert out.count("\n") == 2


def test_corrupt_prefix_suffix_distribution(it_markov, it_lang_data, rng):
    # Verifies that _corrupt produces prefix and suffix noise at the
    # rates implied by the formula in its docstring:
    #   prefix probability = noise * _PREFIX_NOISE_RATIO = 0.15 * 0.3 = 0.045
    #   suffix probability = noise = 0.15
    # Since prefix and suffix are now independent (two separate rolls),
    # a verse can receive both; we count each independently.
    N = 100_000
    noise = 0.15
    expected_prefix = noise * 0.3  # _PREFIX_NOISE_RATIO
    expected_suffix = noise
    tolerance = 0.005
    noise_seqs = set(it_lang_data["noise_sequences"])

    prefix_count = suffix_count = 0
    for _ in range(N):
        result = _corrupt("VERSO", it_markov, it_lang_data, noise=noise, rng=rng)
        parts = result.split(" > ")
        has_prefix = parts[0] in noise_seqs
        has_suffix = parts[-1] != "VERSO"
        if has_prefix:
            prefix_count += 1
        if has_suffix:
            suffix_count += 1

    assert (
        abs(prefix_count / N - expected_prefix) < tolerance
    ), f"Prefix rate {prefix_count/N:.4f} deviates from expected {expected_prefix}"
    assert (
        abs(suffix_count / N - expected_suffix) < tolerance
    ), f"Suffix rate {suffix_count/N:.4f} deviates from expected {expected_suffix}"
