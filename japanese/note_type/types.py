# Copyright: Ajatt-Tools and contributors; https://github.com/Ajatt-Tools
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
import enum
import typing

from anki.models import NotetypeNameId


class ChangeImportsAction(enum.Enum):
    remove = enum.auto()
    add = enum.auto()


class RelevantModelSearchResult(typing.NamedTuple):
    """
    A Relevant model is a model AJT Japanese will add its CSS and JS imports.
    The add-on inserts additional JavaScript and CSS code into the card templates
    to enable the display of pitch accent information on mouse hover.
    """

    is_relevant: bool
    nameid: NotetypeNameId
