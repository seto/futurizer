# Changelog

## Version 0.1.0

First published version. Released on the anniversary of Alfred Nobel's will (27 November
1895). He invented dynamite: `DINAMITE` is in the word list, but here no prizes will be
awarded.

### Features

- **Syntax demolition.** Function words (articles, prepositions, conjunctions, pronouns)
  are deleted, and adjectives and adverbs are dropped half of the time; the surviving
  adverbs keep an exclamation mark.
- **Verbs to the infinitive,** elongated, repeated or fused with onomatopoeia.
- **Noun industrialization.** Nouns are fused with factory and war vocabulary.
- **Acoustic noise.** Onomatopoeic bursts between tokens and Markov-generated noise on
  the verses, controlled by the `noise` level.
- **Reproducible.** A `seed` gives the same output on every run, without touching the
  global random state.
- **Italian and English,** with language-specific word lists and rules: elisions,
  grave-accent spellings, passato remoto endings and irregular verbs for Italian;
  contractions and reflexive pronouns for English.
- **CLI and library.** `futurize` reads a file or standard input, and
  `futurizer.futurize()` does the same from Python.
- **No dependencies.** Pure Python 3.11+, fully typed.
