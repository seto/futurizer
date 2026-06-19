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

"""Public library API for Futurizer.

This is the single supported entry point for using Futurizer as a library,
as opposed to the CLI in `cli.py`, which is a thin wrapper around this
module. It resolves language codes to language data and manages the
random seed, delegating to the engine package, which stays agnostic to
language codes, CLI concerns, and seeding policy.
"""

import importlib
import random

from .engine.compositor import futurize as _engine_futurize

DEFAULT_LANG = "it"
DEFAULT_NOISE = 0.15

_LANGUAGES: dict[str, tuple[str, str]] = {
    "it": ("Italiano", "futurizer.lang.it"),
    "en": ("English", "futurizer.lang.en"),
}


class FuturizerError(Exception):
    """Base class for all errors raised by the Futurizer public API."""


class UnsupportedLanguageError(FuturizerError):
    """Raised when a language code has no registered language data."""


def languages() -> dict[str, str]:
    """Return a mapping of supported language code to display name."""

    return {code: name for code, (name, _) in _LANGUAGES.items()}


def futurize(text: str, lang: str = DEFAULT_LANG, noise: float = DEFAULT_NOISE, seed: int | None = None) -> str:
    """Transform plain text into futurist-style output.

    Args:
        text: The text to transform. Line breaks are preserved as verse
            boundaries; an empty or whitespace-only string returns "".
        lang: A supported language code (see `languages()`).
        noise: Intensity of additional onomatopoeic bursts and
            Markov-generated line corruption. Core syntax destruction
            is always active and not governed by this parameter.
        seed: Optional seed for reproducible output. Two calls with the
            same text, lang, noise, and seed always produce the same
            result; omit it for non-reproducible randomness. Does not
            touch the global `random` module state.

    Raises:
        UnsupportedLanguageError: If `lang` has no registered language data.
    """

    lang_data = _load_lang_data(lang)
    rng = random.Random(seed)

    return _engine_futurize(text, lang_data=lang_data, noise=noise, rng=rng)


def _load_lang_data(lang: str) -> dict:
    try:
        _, module_path = _LANGUAGES[lang]
    except KeyError:
        supported = ", ".join(sorted(_LANGUAGES))
        raise UnsupportedLanguageError(
            f"Unsupported language '{lang}'. Available: {supported}"
        ) from None

    module = importlib.import_module(module_path)

    return module.LANG_DATA

