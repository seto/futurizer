<h1 align="center">Futurizer</h1>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-AGPL--3.0+-blue.svg" alt="License: AGPL-3.0-or-later"></a>
  <a href="https://pypi.org/project/futurizer/"><img src="https://img.shields.io/pypi/v/futurizer.svg?maxAge=86400&color=blue" alt="Version"></a>
  <a href="https://pypi.org/project/futurizer"><img src="https://img.shields.io/pypi/pyversions/futurizer.svg" alt="Supported Versions"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code_style-black-000000.svg" alt="Code Style: Black"></a>
</p>

**Futurizer** is a rule-based linguistic transformation engine that deconstructs plain text, crushes its syntax, and rebuilds it as a high-velocity, industrialized stream of consciousness inspired by the 1909 early avant-garde manifestos.

By passing standard prose or classic poetry through its pipelines, Futurizer strips away grammatical bureaucracy, injects mechanical jargon, and introduces stochastic onomatopoeic noise driven by internal Markov chains.

## Features

- **Syntax Demolition:** Automated removal of function words (articles, prepositions, conjunctions, pronouns) to let nouns stand naked and raw.
- **Verbal Infinitivization & Echoes:** Verbs are forcibly mutated into their infinitive forms, dynamically elongated (`URLAREEEEE`), repeated as mechanical loops (`SALIRE + SALIRE`), or fused with raw sound.
- **Noun Industrialization:** Nouns are automatically fused with heavy industry and military jargon using randomized prefix and suffix patterns.
- **Stochastic Typographic Noise:** Inject non-linear typographic separators (`×`, `>`, `/`, `::`) and chaotic bursts (`ZANG`, `TUMB`, `CRACK`) based on a fine-tunable noise factor.
- **Reproducible Chaos:** Full support for pseudorandom seeding to recreate the exact same destruction across different runs.

## Installation

```bash
pip install futurizer
```

## Usage

```bash
futurize input.txt
```

Alternatively, you can pipe text directly through standard input:

```bash
cat input.txt | futurize - 
```

## Options

| Option         | Description                                                            | Default         |
| -------------- | ---------------------------------------------------------------------- | --------------- |
| `input`        | Path to the input text file. Use `-` for standard input.               | **(required)**  |
| `-l`, `--lang` | Language of the input text. See [Language support](#language-support). | `it`            |
| `--noise`      | Probability threshold for onomatopoeic bursts and line corruption.     | `0.15`          |
| `--seed`       | Random seed for reproducibility.                                       | `None` (random) |

## Language Support

The engine utilizes language-specific corpora containing part-of-speech suffix heuristics, verb lemmatization patterns, and targeted industrial glossaries.

- Italian (it): Built around classic Italian literary texts, loaded with mechanical terms from early 20th-century aviation, automotive, and heavy metallurgy industries.

## Historical Note

Futurizer draws on the typographic aesthetic of Italian Futurism — onomatopoeias, _parole in libertà_, fragmented syntax — as found in works like Marinetti's Zang Tumb Tumb (1914) and Palazzeschi's sound poetry.

[Futurism](https://en.wikipedia.org/wiki/Futurism) was an avant-garde movement that influenced Dada, Russian Constructivism, and concrete poetry. Marinetti's later alignment with Italian fascism is a documented historical fact, not something this project celebrates.

The interest here is purely in the formal experiment: what happens when you run nineteenth-century verse, or corporate buzzword soup, through a machine that thinks like a 1909 manifesto.

## License

This program is licensed under the [GNU Affero General Public License v3.0 or later](https://www.gnu.org/licenses/agpl-3.0.html) (AGPL-3.0+).  
See the [LICENSE](LICENSE) file for details.
