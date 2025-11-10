# Copyright: Ajatt-Tools and contributors; https://github.com/Ajatt-Tools
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os.path

import pytest

from japanese.mecab_controller.basic_types import Inflection, PartOfSpeech
from japanese.pitch_accents.basic_types import (
    AccDbParsedToken,
    PitchAccentEntry,
    PitchParam,
    PitchType,
)
from japanese.pitch_accents.common import (
    FormattedEntry,
    files_in_dir,
    split_pitch_numbers,
)
from japanese.pitch_accents.consts import PITCH_DIR_PATH
from japanese.pitch_accents.format_accents import format_entry


@pytest.mark.parametrize(
    "token,  expected_pitches",
    [
        (
            AccDbParsedToken(
                word="楽しかった",
                headword="楽しい",
                katakana_reading="たのしかった",
                part_of_speech=PartOfSpeech.i_adjective,
                inflection_type=Inflection.unknown,
                headword_accents=(
                    PitchAccentEntry.from_formatted(
                        FormattedEntry(
                            raw_headword="楽しい",
                            katakana_reading="たのしい",
                            pitch_number="3",
                            html_notation="たのしい",
                        ),
                        PartOfSpeech.i_adjective,
                    ),
                ),
            ),
            "たのしい:kifuku-3",
        ),
        (
            AccDbParsedToken(
                word="納屋",
                headword="納屋",
                katakana_reading="なや",
                part_of_speech=PartOfSpeech.noun,
                inflection_type=Inflection.dictionary_form,
                headword_accents=(
                    PitchAccentEntry.from_formatted(
                        FormattedEntry(
                            raw_headword="納屋",
                            katakana_reading="なや",
                            pitch_number="0,1",
                            html_notation="なや",
                        ),
                        PartOfSpeech.noun,
                    ),
                ),
            ),
            "なや:heiban,atamadaka",
        ),
        (
            AccDbParsedToken(
                word="食べる",
                headword="食べる",
                katakana_reading="タベル",
                part_of_speech=PartOfSpeech.verb,
                inflection_type=Inflection.dictionary_form,
                headword_accents=(
                    PitchAccentEntry.from_formatted(
                        FormattedEntry(
                            raw_headword="食べる",
                            katakana_reading="タベル",
                            pitch_number="1",
                            html_notation="タベル",
                        ),
                        PartOfSpeech.verb,
                    ),
                ),
            ),
            "タベル:kifuku-1",
        ),
        (
                AccDbParsedToken(
                    word="食べる",
                    headword="食べる",
                    katakana_reading="タベル",
                    part_of_speech=PartOfSpeech.verb,
                    inflection_type=Inflection.dictionary_form,
                    headword_accents=(
                            PitchAccentEntry.from_formatted(
                                FormattedEntry(
                                    raw_headword="食べる",
                                    katakana_reading="タベル",
                                    pitch_number="2",
                                    html_notation="タベル",
                                ),
                                PartOfSpeech.verb,
                            ),
                    ),
                ),
                "タベル:kifuku-2",
        ),
        (
            AccDbParsedToken(
                word="粗末",
                headword="粗末",
                katakana_reading=None,
                part_of_speech=PartOfSpeech.unknown,
                inflection_type=Inflection.dictionary_form,
                headword_accents=[
                    PitchAccentEntry(
                        katakana_reading="ソマツ",
                        pitches=[PitchParam(type=PitchType.atamadaka, number="1", n_moras=3)],
                        katakana_reading_sep="ソマツ",
                    )
                ],
            ),
            "ソマツ:atamadaka",
        ),
    ],
)
def test_pitch_accent_entry(token: AccDbParsedToken, expected_pitches: str) -> None:
    assert token.describe_pitches() == expected_pitches


def test_files_in_dir() -> None:
    assert any(os.path.basename(file) == "__init__.py" for file in files_in_dir(PITCH_DIR_PATH))


def test_split_pitch_numbers() -> None:
    assert split_pitch_numbers("?-1-2") == ["?", "1", "2"]
    assert split_pitch_numbers("1") == ["1"]


@pytest.mark.parametrize(
    "kana,  accent,  expected",
    [
        ("あいうえお", 2, "<low_rise>あ</low_rise><high_drop>い</high_drop><low>うえお</low>"),
        ("あいうえお", 0, "<low_rise>あ</low_rise><high>いうえお</high>"),
        ("あいうえお", 5, "<low_rise>あ</low_rise><high_drop>いうえお</high_drop>"),
        ("あいうえお", 1, "<high_drop>あ</high_drop><low>いうえお</low>"),
        ("あ", 1, "<high_drop>あ</high_drop>"),
        ("あ", 0, "<low_rise>あ</low_rise>"),
    ],
)
def test_format_entry(kana: str, accent: int, expected: str) -> None:
    assert format_entry(list(kana), accent) == expected


