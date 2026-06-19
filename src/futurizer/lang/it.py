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

"""Italian language data for Futurizer.

Provides POS tagger rules, verb inflection, mechanical vocabulary,
onomatopoeia corpus, and noise sequences.
"""

TAGGER_RULES = {
    "articles": {
        "il", "lo", "la", "i", "gli", "le", "l",
        "un", "uno", "una",
        "del", "dello", "della", "dei", "degli", "delle",
        "al", "allo", "alla", "ai", "agli", "alle",
        "dal", "dallo", "dalla", "dai", "dagli", "dalle",
        "nel", "nello", "nella", "nei", "negli", "nelle",
        "sul", "sullo", "sulla", "sui", "sugli", "sulle",
        "col", "coi",
    },
    "preps": {
        "di", "a", "da", "in", "con", "su", "per", "tra", "fra",
        "gl", "de", "ne",
    },
    "conjunctions": {
        "e", "ed", "o", "od", "ma", "però", "se", "che", "come",
        "quando", "mentre", "perché", "quindi", "dunque", "né",
    },
    "pronouns": {
        "io", "tu", "lui", "lei", "noi", "voi", "loro",
        # NOTE: "lo", "la", "le", "li" are also articles; the lookup order in
        # _tag() checks "articles" first, so clitic usage ("lo vedo") is
        # always tagged ART, never PRON. Accepted: article usage is far more frequent.
        "mi", "ti", "si", "ci", "vi", "lo", "la", "li", "le",
        "me", "te", "sé", "mio", "tuo", "suo",
    },
    "verb_suffixes": [
        "isco", "isce", "iamo", "iate", "iscono",
        "avo", "avi", "ava", "avamo", "avate", "avano",
        "evo", "evi", "eva", "evamo", "evate", "evano",
        "ivo", "ivi", "iva", "ivamo", "ivate", "ivano",
        "arono", "erono", "irono", "ettero",
        "erò", "erai", "erà", "eremo", "erete", "eranno",
        "irò", "irai", "irà", "iremo", "irete", "iranno",
        "arò", "arai", "arà", "aremo", "arete", "aranno",
        "ando", "endo",
        "ato", "uto", "ito",
        "are", "ere", "ire",
        "ano", "ono", "amo",
        "asse", "esse", "isse",
    ],
    "adj_suffixes": [
        "oso", "osa", "osi", "ose",
        "ale", "ali",
        "ile", "ili",
        "ivo", "iva", "ivi", "ive",
        "ato", "ata", "ati", "ate",
        "uto", "uta", "uti", "ute",
        "ente", "enti",
        "ante", "anti",
        "iero", "iera",
        "evole", "evoli",
    ],
    "adv_suffixes": [
        "mente",
    ],
    "noun_suffixes": [
        "zione", "zioni",
        "ità", "tà",
        "ismo", "ismi",
        "ista", "isti",
        "ezza", "ezze",
        "aggio", "aggi",
        "ore", "ori",
        "ura", "ure",
        "iere", "ieri",
        "mento", "menti",
        "anza", "anze",
        "enza", "enze",
    ],
}

# Each tuple is suffix_to_strip, suffix_to_append, it is applied in order
# from most specific to least specific to avoid premature matches
VERB_TO_INFINITIVE = [
    ("are", "are"), ("ere", "ere"), ("ire", "ire"),  # Pass-through: already infinitive
    ("ando", "are"), ("endo", "ere"),
    ("ato", "are"), ("uto", "ere"), ("ito", "ire"),
    ("arono", "are"), ("erono", "ere"), ("irono", "ire"),
    ("ettero", "ere"),
    ("ava", "are"), ("avi", "are"), ("avo", "are"),
    ("avano", "are"), ("avate", "are"), ("avamo", "are"),
    ("eva", "ere"), ("evi", "ere"), ("evo", "ere"),
    ("evano", "ere"), ("evate", "ere"), ("evamo", "ere"),
    ("iva", "ire"), ("ivi", "ire"), ("ivo", "ire"),
    ("ivano", "ire"), ("ivate", "ire"), ("ivamo", "ire"),
    ("isco", "ire"), ("isce", "ire"), ("iscono", "ire"),
    # NOTE: "-iamo" is the 1st person plural present tense ending shared
    # by all three conjugations (-are, -ere, -ire), so it does not provide any
    # signal about which infinitive to reconstruct.
    # We default to "-are" because it is the productive conjugation in Italian
    # (almost all neologisms are -are), making it the safest bet on unseen text.
    # Approximate estimate, not measured on a corpus.
    ("iamo", "are"),
    ("erò", "ere"), ("erai", "ere"), ("erà", "ere"),
    ("arò", "are"), ("arai", "are"), ("arà", "are"),
    ("irò", "ire"), ("irai", "ire"), ("irà", "ire"),
    ("ano", "are"), ("amo", "are"),
    ("ono", "ere"),
    ("ar", "are"), ("er", "ere"), ("ir", "ire"),
    # NOTE: Heuristic fallback: Reached when a verb form doesn't match 
    # any more specific suffix above, either because none applies, or
    # because it does but fails that suffix's length guard (len(w) > len(sfx) + 2).
    # That guard is flat regardless of pattern length, so it penalizes
    # the longer, safer compound patterns (avamo/avate/avano/evamo/...,
    # 5 chars, near-zero false-positive risk) just as hard as the
    # shorter, more ambiguous ones (amo/ano/ono). Any verb with a
    # 1-2 letter stem at imperfect plural falls through here even when
    # a perfectly correct compound pattern exists for it: "amavamo"
    # (← amare, stem "am-") needs len > 7 for ("avamo", "are") and has
    # exactly 7, so it's rejected and matched instead by the shorter
    # ("amo", "are"), yielding "AMAVARE" instead of "AMARE". Same
    # mechanism hits "stava"/"dava" (stems "st-"/"d-"). Not confined to
    # rare irregulars or to long words, it's a property of stem length,
    # and it can misfire on common regular forms too. It still earns its
    # place for genuinely unmatched longer forms, e.g. "cresce" (3rd
    # singular of "crescere", not covered by "-isce") correctly becomes
    # "CRESCERE" via the bare "e" rule.
    ("a", "are"), ("e", "ere"), ("o", "are"),
]

MECHANICAL_WORDS = [
    "ACCIAIO", "PISTONE", "TURBINA", "CILINDRO", "CARBURATORE",
    "BENZINA", "GASOLIO", "MOSCHETTO", "GRANATA", "PROIETTILE",
    "MITRAGLIATRICE", "ELICA", "AEROPLANO", "LOCOMOTIVA", "DINAMO",
    "VOLANO", "INGRANAGGIO", "BULLONE", "FUCILE", "CANNONE",
    "FIAMMA", "FOLGORE", "VAPORE", "SCINTILLA", "LAMPO",
    "TUONO", "ESPLOSIONE", "VORTICE", "BAGLIORE", "INCENDIO",
    "800HP", "1000RPM", "MAX", "ULTRA", "IPER",
    "VELOCITÀ", "POTENZA", "IMPULSO", "FORZA", "IMPATTO",
    "FERRO", "RAME", "PIOMBO", "CROMO", "TITANIO",
    "TRAC", "CRACK", "BANG", "SLAM", "HIT",
]

# Onomatopoeic sequences for training the Markov chain,
# extracted and inspired by Italian futurist poets
ONOMATOPOEIA_CORPUS = [
    "ZANG TUMB TUMB TUMB TARARÀ",
    "TUMB TUUUM TUMB TUUUM TUMB",
    "ZANG ZANG ZANG TUMB TUMB",
    "CRACK BOOOM SSSSHHH ZANG",
    "TATATATA TARARÀ TUMB ZANG",
    "FFFFF SSSSS ZANG TUMB CRACK",
    "BRRR RRRRR ZANG TUMB TUMB",
    "FISCHIO FISCHIO TUMB TUMB ZANG",
    "RRRR RRRR TATATATA BOOM",
    "SCRETCH CRACK ZANG TUMB",
    "CLOFF CLOP CLOCH",
    "CLOFFETE CLOPPETE CLOCCHETE",
    "ZANG CRACK BOOM TUMB SSSSS",
    "TUMB ZANG FISCHIO CRACK BOOM",
    "BOOM BOOM CRACK SSSSS ZANG",
    "RATATATA BOOM CRACK TUMB ZANG",
    "SCREECH CRACK BOOM ZANG TUMB",
    "SHHH SHHH BOOM CRACK TUMB",
    "SLAM BANG CRACK TUMB ZANG",
    "VROOM VROOM CRACK ZANG TUMB",
    "FISCHIO SSSSS CRACK BOOM ZANG",
    "CLANG CLANG TUMB CRACK BOOM",
    "TUMB TUMB ZANG CRACK BOOM RRRR TATATATA",
    "BOOM CRACK ZANG TUMB SSSSS FISCHIO RRRR",
    "ZANG TUMB CRACK BOOM SHHH TATATATA FFFFF",
    "CRACK BOOM ZANG TUMB RRRR SSSSS BANG",
    "CLOFF CLOP CLOCH CHCHCH"
]

NOISE_SEQUENCES = [
    "ZANG TUMB TUMB",
    "CRACK BOOM SSSSS",
    "TATATATA CRACK",
    "RRRR BOOM",
    "FISCHIO FISCHIO ZANG",
    "SSSSS BANG CRACK",
    "VROOM CRACK",
    "CLANG ZANG TUMB",
    "BOOM RATATATA",
    "FFFFF SSSSS ZANG",
]

BURST_SEPARATORS = ["ZANG", "TUMB", "CRACK", "SSSSS", "BRRR", "CLOFF", "CLOP", "CLOCH"]

TRANSFORMATION_THRESHOLDS = {
    "verb_elongate": 0.35,
    "verb_repeat": 0.65,
    "noun_prefix": 0.40,
    "noun_plain": 0.70,
    "adj_drop": 0.50,
}

LANG_DATA = {
    "name": "Italiano",
    "code": "it",
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
