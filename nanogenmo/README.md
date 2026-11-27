# from wood TO CHROME

A [NaNoGenMo](https://github.com/NaNoGenMo/2026) 2026 entry: Carlo Collodi's _Le
avventure di Pinocchio_, futurized chapter by chapter with [Futurizer](../README.md),
the rule-based engine in this repository that demolishes syntax the way the Futurist
manifestos asked.

The novel can be found in [`corpus/processed/chrome.txt`](corpus/processed/chrome.txt).
A PDF edition of it is in [`corpus/processed/chrome.pdf`](corpus/processed/chrome.pdf);
the word counts below refer to the text file.

## Numbers

Words are counted as space-separated tokens, as `wc -w` does: **63,901**. The Futurist
separators (`×`, `>`, `/`, `+`, `—`, `::`) are tokens of their own, so the count without
them is also given.

| Counting                                                        | Words  |
| --------------------------------------------------------------- | ------ |
| `wc -w`                                                         | 63,901 |
| Alphanumeric sequences, separators excluded (`VOLPE-LAMPO` = 2) | 52,517 |

## How it was made

- **Source:** Project Gutenberg ebook 52484 (R. Bemporad & figlio edition, 1902), kept
  unmodified in `corpus/raw/pinocchio.txt`.
- **Engine:** function words are deleted, verbs go to the infinitive, most nouns are
  fused with factory and war vocabulary, adjectives and adverbs are dropped half of the
  time (the surviving adverbs keep an exclamation mark), and a small Markov chain adds
  onomatopoeic noise.
- **Carving:** `foundry.carve` removes the Gutenberg boilerplate, the title page, the
  image captions and the final index.
- **Forging:** `foundry.forge` futurizes each of the 36 chapters with its own noise
  level and seed (2026 + the chapter number). The noise follows a fixed curve: 0.10 in
  the first chapter (the wood), up to 0.60 at the donkey (chapter XXXII), 0.50 in the
  finale, with peaks at the assassins, Toyland and the Dogfish.
- **Layout:** chapter numerals become headings whose rules go from `~` (wood grain) to
  `#` (rivets) as the noise grows; verses are wrapped at 88 columns and the closing
  `FINE.` is kept as it is, centered.
- **Typesetting:** `press` sets the text the way a typewriter would: A4, Courier 12 pt
  (10 characters per inch, 6 lines per inch, 65 columns), one chapter per page, with the
  headings fading from wood brown to chrome grey and the words of the din in bold. It
  has no third-party dependencies and its output is the same on every run.

The seed is 2026, the year of the bicentenary of Collodi's birth (24 November 1826). It
was picked after trying a few, because with it the novel opens with `CROMO-LEGNO`
("chrome-wood", the title in two words) and brings it back near the end, in the mirror
scene.

## Reproducing it

From the repository root:

```bash
pip install -e .
python -m nanogenmo.foundry   # the novel (chrome.txt)
python -m nanogenmo.press     # the PDF edition (chrome.pdf)
```

Made with Python 3.14.10. The generated novel is committed, so reproducing it is
optional: the `random` module does not guarantee the same sequence across Python
versions.

## Known glitches

The machine reads words mostly by their endings, so look-alikes sometimes get the wrong
treatment: `subito` ("at once") becomes `SUBIRE` ("to undergo"), and `lontano` ("far")
becomes `LONTARE`, a verb that does not exist. They stay: the rules are meant to work on
any text, not just on this book, so ambiguous forms are not patched one by one, and the
glitches are considered part of the game.

## License

The code is licensed under AGPL-3.0+ (see [LICENSE](../LICENSE)).  
Collodi's text is in the public domain.  
The generated novel is released under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
