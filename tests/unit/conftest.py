import random

import pytest

from futurizer.engine.markov import MarkovChain
from futurizer.lang.en import LANG_DATA as EN_LANG_DATA
from futurizer.lang.it import LANG_DATA as IT_LANG_DATA


@pytest.fixture
def it_lang_data():
    return IT_LANG_DATA


@pytest.fixture
def en_lang_data():
    return EN_LANG_DATA


@pytest.fixture
def rng():
    return random.Random(0)


@pytest.fixture
def it_markov(rng, it_lang_data):
    return MarkovChain(it_lang_data["onomatopoeia_corpus"], rng=rng)
