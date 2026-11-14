from futurizer.engine.compositor import _tag


def test_articles_tagged(it_lang_data):
    rules = it_lang_data["tagger_rules"]
    for word in ("il", "lo", "la", "un", "una"):
        assert _tag(word, rules) == "ART", f"'{word}' should be ART"


def test_preps_tagged(it_lang_data):
    rules = it_lang_data["tagger_rules"]
    for word in ("di", "a", "da", "in", "con"):
        assert _tag(word, rules) == "PREP", f"'{word}' should be PREP"


def test_conjunctions_tagged(it_lang_data):
    rules = it_lang_data["tagger_rules"]
    for word in ("e", "ma", "però", "quindi"):
        assert _tag(word, rules) == "CONJ", f"'{word}' should be CONJ"


def test_verb_suffixes_tagged(it_lang_data):
    rules = it_lang_data["tagger_rules"]
    # Long enough to pass the length guard (len > suffix + 2)
    for word in ("cantando", "correndo", "partivano", "mangiarono"):
        assert _tag(word, rules) == "VERB", f"'{word}' should be VERB"


def test_noun_suffixes_tagged(it_lang_data):
    rules = it_lang_data["tagger_rules"]
    for word in ("nazione", "velocità", "movimento", "potenza"):
        assert _tag(word, rules) == "NOUN", f"'{word}' should be NOUN"


def test_adv_suffix_tagged(it_lang_data):
    rules = it_lang_data["tagger_rules"]
    assert _tag("velocemente", rules) == "ADV"


def test_apocope_infinitives_tagged(it_lang_data):
    # Poetic/archaic truncated infinitives: cantar, veder, partir
    rules = it_lang_data["tagger_rules"]
    for word in ("cantar", "veder", "partir"):
        assert _tag(word, rules) == "VERB", f"'{word}' should be VERB"


def test_vowel_ending_fallback_tagged_as_noun(it_lang_data):
    # Common nouns not covered by specific suffixes should fall
    # through to the vowel-ending heuristic and be tagged NOUN.
    rules = it_lang_data["tagger_rules"]
    for word in ("casa", "porta", "libro", "treno"):
        assert _tag(word, rules) == "NOUN", f"'{word}' should be NOUN"


def test_short_unknown_word_tagged_as_other(it_lang_data):
    rules = it_lang_data["tagger_rules"]
    # 3 chars or fewer, no suffix match, no vowel fallback
    assert _tag("xyz", rules) == "OTHER"


def test_elision_stems_tagged_as_function_words(it_lang_data):
    rules = it_lang_data["tagger_rules"]
    expected = {
        "dell": "ART",
        "nell": "ART",
        "d": "PREP",
        "c": "PRON",
        "quand": "CONJ",
    }
    for word, pos in expected.items():
        assert _tag(word, rules) == pos, f"'{word}' should be {pos}"


def test_grave_accent_variants_tagged(it_lang_data):
    rules = it_lang_data["tagger_rules"]
    expected = {"perchè": "CONJ", "nè": "CONJ", "sè": "PRON"}
    for word, pos in expected.items():
        assert _tag(word, rules) == pos, f"'{word}' should be {pos}"


def test_italian_past_historic_accented_endings_tagged_as_verbs(it_lang_data):
    rules = it_lang_data["tagger_rules"]
    for word in ("gridò", "domandò", "andò", "sentì", "partì"):
        assert _tag(word, rules) == "VERB", f"'{word}' should be VERB"


def test_short_accented_words_not_verbs(it_lang_data):
    # The length guard keeps "ciò", "lì" and "sì" out; "così" and "perciò"
    # are listed as function words so the new suffixes do not catch them.
    rules = it_lang_data["tagger_rules"]
    for word in ("ciò", "lì", "sì"):
        assert _tag(word, rules) != "VERB", f"'{word}' should not be VERB"
    for word in ("così", "perciò"):
        assert _tag(word, rules) == "CONJ", f"'{word}' should be CONJ"
