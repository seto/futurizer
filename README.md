<h1 align="center">Futurizer</h1>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0+-blue.svg" alt="License: AGPL-3.0-or-later"></a>
  <a href="https://pypi.org/project/futurizer/"><img src="https://img.shields.io/pypi/v/futurizer.svg?maxAge=86400&color=blue" alt="Version"></a>
  <a href="https://pypi.org/project/futurizer"><img src="https://img.shields.io/pypi/pyversions/futurizer.svg" alt="Supported Versions"></a>
  <a href="https://github.com/seto/futurizer/actions"><img src="https://github.com/seto/futurizer/workflows/CI/badge.svg" alt="CI"></a>
  <a href="https://www.mypy-lang.org/"><img src="https://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code_style-black-000000.svg" alt="Code Style: Black"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Linting: Ruff"></a>
</p>

**Futurizer** is a rule-based linguistic transformation engine that deconstructs plain
text, crushes its syntax, and rebuilds it as a high-velocity, industrialized stream of
consciousness inspired by the Futurist manifestos of 1909 and 1912.

By passing standard prose or classic poetry through its pipelines, Futurizer strips away
grammatical bureaucracy, injects mechanical jargon, and introduces stochastic
onomatopoeic noise driven by internal Markov chains.

## Features

- **Syntax Demolition:** Automated removal of function words (articles, prepositions,
  conjunctions, pronouns) to let nouns stand naked and raw; adjectives and adverbs are
  dropped half of the time.
- **Verbal Infinitivization & Echoes:** Verbs are forcibly mutated into their infinitive
  forms, dynamically elongated (`URLAREEEEE`), repeated as mechanical loops
  (`SALIRE + SALIRE`), or fused with raw sound.
- **Noun Industrialization:** Most nouns are fused with heavy industry and military
  jargon, as a prefix or a suffix chosen at random.
- **Stochastic Typographic Noise:** Base typographic separators (`×`, `>`, `/`, `+`,
  `—`, `::`) connect every token regardless of setting. A fine-tunable noise factor
  additionally controls the chance of extra onomatopoeic bursts (`ZANG`, `TUMB`,
  `CRACK`, language-specific) and of noise at the edges of each line: a fixed sequence
  at the start, a Markov-generated one at the end.
- **Reproducible Chaos:** Full support for pseudorandom seeding to recreate the exact
  same destruction across different runs.

## The Two Layers of Destruction

Futurizer operates on two conceptually distinct layers:

1. **Syntactic Demolition (Always Active):** Following the radical manifestos, the
   destruction of syntax (removal of function words, infinitivization of verbs, and the
   50% adjective and adverb drop rate) is an absolute stylistic baseline. It cannot be
   turned off.
2. **Acoustic Noise (Parameter Driven):** Base typographic separators connect every
   token regardless of setting. The `--noise` parameter controls only the additional
   interference layered on top: the chance of onomatopoeic bursts inserted between
   tokens, plus a fixed noise sequence at the start of a line and a Markov-generated one
   at the end.

## Installation

```bash
pip install futurizer
```

## Usage

### Command-line

```bash
futurize input.txt
```

Alternatively, you can pipe text directly through standard input:

```bash
cat input.txt | futurize -
```

### Library

```python
from futurizer import futurize

# Basic usage
output = futurize(text)

# With explicit language, noise level and seed
output = futurize(text, lang="en", noise=0.3, seed=77)
```

To see the list of supported languages:

```python
from futurizer import languages

print(languages())
```

Unsupported language codes raise `futurizer.UnsupportedLanguageError`.

## Options

| Option         | Description                                                            | Default         |
| -------------- | ---------------------------------------------------------------------- | --------------- |
| `input`        | Path to the input text file. Use `-` for standard input.               | **(required)**  |
| `-l`, `--lang` | Language of the input text. See [Language support](#language-support). | `it`            |
| `--noise`      | See [Noise control](#the-two-layers-of-destruction).                   | `0.15`          |
| `--seed`       | Random seed for reproducibility.                                       | `None` (random) |

## Language Support

The engine utilizes language-specific collections containing part-of-speech suffix
heuristics, short word lists, verb lemmatization patterns, and targeted industrial
glossaries.

- Italian (it): Built around classic Italian literary texts, loaded with mechanical
  terms from early 20th-century aviation, automotive, and heavy metallurgy industries.
- English (en): Tuned to a raw, angular cadence inspired by early modern industrial
  imagery, Anglo-American Vorticism, and the mechanical din of Wyndham Lewis's _BLAST_
  magazine.

## Historical Note

Futurizer plays with the typographic aesthetic of Italian Futurism — onomatopoeias,
_parole in libertà_, fragmented syntax — as found in works like Marinetti's Zang Tumb
Tumb (1914) and Palazzeschi's playful nonsense verse.

[Futurism](https://en.wikipedia.org/wiki/Futurism) was an avant-garde movement that
influenced Dada, Russian Constructivism, and concrete poetry. Its founder, Marinetti,
was among the founders of the first Fascist movement in 1919 and later supported the
regime, and the 1909 manifesto itself glorifies war and militarism. This is documented
history, not something this project celebrates.

The interest here is in the formal and parodic experiment: what happens when you run
classic prose and verse (or a corporate buzzword soup) through a machine that thinks
like a Futurist manifesto.

## NaNoGenMo 2026

[`nanogenmo/`](https://github.com/seto/futurizer/tree/master/nanogenmo) runs Futurizer
on Collodi's _Le avventure di Pinocchio_ for
[NaNoGenMo](https://github.com/NaNoGenMo/2026) 2026: the novel, its PDF edition and the
script that makes them. It is not part of the installed package.

## License

This program is licensed under the
[GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html)
(AGPL-3.0+).  
See the [LICENSE](https://github.com/seto/futurizer/blob/master/LICENSE) file for
details.

## Changelog

See [CHANGES.md](https://github.com/seto/futurizer/blob/master/CHANGES.md) for release
notes.
