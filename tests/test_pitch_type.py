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


@pytest.mark.parametrize(
    "pitch_num_str,  n_moras,  expected_type",
    [
        ("0", 2, PitchType.heiban),
        ("0", 9, PitchType.heiban),
        ("1", 1, PitchType.atamadaka),
        ("1", 9, PitchType.atamadaka),
        ("2", 2, PitchType.odaka),
        ("3", 3, PitchType.odaka),
        ("4", 4, PitchType.odaka),
        ("2", 3, PitchType.nakadaka),
        ("3", 10, PitchType.nakadaka),
        ("4", 8, PitchType.nakadaka),
        ("?", 8, PitchType.unknown),
        ("xxx", 8, PitchType.unknown),
    ],
)
def test_pitch_type_from_pitch_num(pitch_num_str: str, n_moras: int, expected_type: PitchType) -> None:
    assert pitch_type_from_pitch_num(pitch_num_str, n_moras) == expected_type


@pytest.mark.parametrize(
    "pitch_num_str,  n_moras",
    [
        ("-2", 2),
        ("-1", 1),
        ("0", -1),
        ("1", 0),
        ("3", -2),
        ("33", 10),
        ("44", 3),
    ],
)
def test_pitch_type_from_pitch_num_value_error(pitch_num_str: str, n_moras: int):
    with pytest.raises(ValueError):
        pitch_type_from_pitch_num(pitch_num_str, n_moras)
