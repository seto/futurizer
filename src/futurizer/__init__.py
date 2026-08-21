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

from .api import (
    DEFAULT_LANG,
    DEFAULT_NOISE,
    FuturizerError,
    UnsupportedLanguageError,
    futurize,
    languages,
)

__all__ = [
    "DEFAULT_LANG",
    "DEFAULT_NOISE",
    "FuturizerError",
    "UnsupportedLanguageError",
    "futurize",
    "languages",
]
