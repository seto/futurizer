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

"""English language data for Futurizer.

Provides POS tagger rules, verb inflection, mechanical vocabulary,
onomatopoeia corpus, and noise sequences tailored for industrial aesthetics.
"""

from ..langdata import LangData, TaggerRules, Thresholds

# NOTE: _parse splits contractions at the apostrophe ("don't" → "don", "t"),
# so the pronoun set also lists the clitic stems ("s", "ll", "re", ...) and the
# stems of "n't" forms that are not words on their own ("isn", "doesn", ...).
# "won", "don", "can" and "haven" are real words too, so they are left alone.
TAGGER_RULES: TaggerRules = {
    "articles": {
        "the", "a", "an",
    },
    "preps": {
        "of", "to", "in", "for", "on", "with", "at", "by", "from",
        "up", "about", "into", "over", "after", "through", "out",
        "under", "between", "against", "during", "without",
    },
    "conjunctions": {
        "and", "but", "or", "yet", "so", "nor",
        # NOTE: the archaic conjunction "for" ("for he was tired") is
        # deliberately absent: it is tagged PREP, whose lookup runs first.
        "because", "although", "since", "unless", "while",
        "whereas", "if", "than", "whether",
    },
    "pronouns": {
        "i", "you", "he", "she", "it", "we", "they",
        "me", "him", "her", "us", "them",
        "my", "your", "his", "its", "our", "their",
        "mine", "yours", "hers", "ours", "theirs",
        "myself", "yourself", "himself", "herself",
        "itself", "oneself",
        "ourselves", "yourselves", "themselves",
        # Contraction stems: it's, I'm, don't, we're, they've, you'll, I'd
        "s", "m", "d", "t", "re", "ve", "ll",
        # Stems of n't forms that are not words on their own: isn't, doesn't
        "isn", "aren", "wasn", "weren", "hasn", "hadn", "doesn", "didn",
        "wouldn", "couldn", "shouldn", "mustn", "needn",
    },
    "verb_suffixes": [
        "ing", "ed", "es", "eth",
        "ize", "ise", "ate", "ify",
    ],
    "adj_suffixes": [
        "able", "ible", "al", "ful", "ic", "ive", "less", "ous",
        "ish", "ent", "ant", "en", "y",
    ],
    "adv_suffixes": [
        "ly", "wise", "ward", "wards",
    ],
    "noun_suffixes": [
        "tion", "sion", "ment", "ness", "ity", "ty", "ance", "ence",
        "er", "or", "ist", "ism", "ship", "hood", "age", "th",
    ],
}

# NOTE: Each tuple is suffix_to_strip, suffix_to_append, it is applied in order
# from most specific to least specific. English morphology is simpler
# than Italian but highly prone to silent -e dropping (e.g., igniting → ignite).
# We deliberately do NOT attempt to restore the silent "e" for "-ing"/"-ed":
# distinguishing "hoping" (← hope) from "jumping" (← jump) requires either
# a dictionary or a consonant-doubling heuristic, both disproportionate for
# a suffix-rule list. Silent-e verbs come out truncated instead
# (EXPLODE → EXPLOD), which reads as a Marinetti-style "parola troncata"
# rather than a spelling error.
VERB_TO_INFINITIVE: list[tuple[str, str]] = [
    ("ying", "ie"),
    ("ing", ""),
    ("ied", "y"),
    ("ed", ""),
    ("ies", "y"),
    ("es", ""),
    ("s", ""),
]

MECHANICAL_WORDS: list[str] = [
    "STEEL", "PISTON", "TURBINE", "CYLINDER", "CARBURETOR",
    "GASOLINE", "DIESEL", "MUSKET", "GRENADE", "BULLET",
    "MACHINEGUN", "PROPELLER", "AEROPLANE", "LOCOMOTIVE", "DYNAMO",
    "FLYWHEEL", "GEAR", "BOLT", "RIFLE", "CANNON",
    "FLAME", "LIGHTNING", "STEAM", "SPARK", "FLASH",
    "THUNDER", "EXPLOSION", "VORTEX", "GLARE", "FIRE",
    "800HP", "1000RPM", "MAX", "ULTRA", "HYPER",
    "SPEED", "VELOCITY", "POWER", "IMPULSE", "FORCE", "IMPACT",
    "IRON", "COPPER", "LEAD", "CHROME", "TITANIUM",
    "CLANG", "CRACK", "BANG", "SLAM", "HIT", "WHIZZ",
]

# Onomatopoeic sequences for training the Markov chain,
# heavily inspired by Vorticist typography, industrial din,
# and BLAST magazine
ONOMATOPOEIA_CORPUS: list[str] = [
    "BLAST HUM CLICK CLACK CHUFF",
    "CHUFF CHUFF CHUFF THUB THUB",
    "CRACK BOOM WHIZZ CLANG BANG",
    "RATATATA TICK TOCK CLATTER SHHH",
    "VROOM VROOM SCREECH SMASH",
    "BANG ZAP POW CRUNCH CLINK",
    "WHIRR WHIRR HUMMM DRONE BLIP",
    "BLAST BLAST RATATATA BOOM CHUFF",
    "CLICK CLACK WHIRR SCREECH SMASH",
    "CLANG CLANG THUB CRACK BOOM",
    "TICK TOCK TICK TOCK CLATTER DRONE",
    "SHHH SHHH BOOM CRACK HUMMM",
    "SLAM BANG CRACK THUB VROOM",
    "VROOM VROOM CRACK BLIP HUMMM",
    "WHIRR SHHH CRACK BOOM ZAP",
    "CLINK CLANG THUB CRACK BOOM",
    "THUB THUB WHIRR CRACK BOOM RATATATA",
    "BOOM CRACK BLAST THUB SHHH WHIRR",
    "BLAST THUB CRACK BOOM SHHH RATATATA",
    "CRACK BOOM BLAST THUB RATATATA SHHH BANG",
    "CLICK CLACK CLATTER CHCHCH",
]

NOISE_SEQUENCES: list[str] = [
    "BLAST HUM CLACK",
    "CHUFF CHUFF THUB",
    "CRACK BOOM WHIZZ",
    "RATATATA CLANG",
    "VROOM SCREECH",
    "WHIRR HUMMM BLIP",
    "CLANG BLAST THUB",
    "BOOM RATATATA",
    "SHHH CLATTER BANG",
]

BURST_SEPARATORS: list[str] = [
    "BLAST", "THUB", "CRACK", "BOOM", "SHHH", "CHUFF", "BLIP", "ZAP"
]

TRANSFORMATION_THRESHOLDS: Thresholds = {
    "verb_elongate_upto": 0.35,
    "verb_repeat_upto": 0.65,
    "noun_prefix_upto": 0.40,
    "noun_plain_upto": 0.70,
    "adj_drop": 0.50,
    "adv_drop": 0.50,
}

LANG_DATA: LangData = {
    "name": "English",
    "code": "en",
    "tagger_rules": TAGGER_RULES,
    "rules": {
        "verb_to_infinitive": VERB_TO_INFINITIVE,
    },
    "mechanical_words": MECHANICAL_WORDS,
    "onomatopoeia_corpus": ONOMATOPOEIA_CORPUS,
    "noise_sequences": NOISE_SEQUENCES,
    "burst_separators": BURST_SEPARATORS,
    "thresholds": TRANSFORMATION_THRESHOLDS,
}
