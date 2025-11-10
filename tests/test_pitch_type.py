# Copyright: Ajatt-Tools and contributors; https://github.com/Ajatt-Tools
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
import pytest

from japanese.mecab_controller.basic_types import PartOfSpeech
from japanese.mecab_controller.kana_conv import HIRAGANA, KATAKANA
from japanese.pitch_accents.basic_types import (
    PitchParam,
    PitchType,
    PitchUnknown,
    adjust_if_kifuku,
    count_moras,
    is_verb_or_i_adjective,
    pitch_type_from_pitch_num,
)


@pytest.mark.parametrize(
    "text_case,  expected_mora_count",
    [
        ("あいうえお", 5),
        ("カキクケコ", 5),
        ("にゃ", 1),
        ("あ", 1),
        ("ー", 1),
        ("っ", 1),
        ("とうきょう", 4),
        ("きゃきゅきょ", 3),
    ],
)
def test_count_moras(text_case: str, expected_mora_count: int) -> None:
    assert count_moras(text_case) == expected_mora_count


def test_pitch_type_from_pitch_num() -> None:
    assert pitch_type_from_pitch_num("0", 2) == PitchType.heiban
    assert pitch_type_from_pitch_num("1", 1) == PitchType.atamadaka
    assert pitch_type_from_pitch_num("2", 2) == PitchType.odaka
    assert pitch_type_from_pitch_num("2", 3) == PitchType.nakadaka
    assert pitch_type_from_pitch_num("3", 3) == PitchType.odaka
    assert pitch_type_from_pitch_num("3", 10) == PitchType.nakadaka
    assert pitch_type_from_pitch_num("4", 8) == PitchType.nakadaka
    assert pitch_type_from_pitch_num("?", 8) == PitchType.unknown
