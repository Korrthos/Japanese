# Copyright: Ajatt-Tools and contributors; https://github.com/Ajatt-Tools
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
import enum
import typing

from anki.models import NotetypeNameId


class ChangeImportsAction(enum.Enum):
    remove = enum.auto()
    add = enum.auto()


class RelevantModelSearchResult(typing.NamedTuple):
    is_relevant: bool
    nameid: NotetypeNameId
