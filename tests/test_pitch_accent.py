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


@pytest.mark.parametrize(
    "word,  pitch_number,  part_of_speech,  expected_type,  expected_description",
    [
        ("たべる", "1", PartOfSpeech.verb, PitchType.kifuku, "kifuku-1"),
        ("たべる", "2", PartOfSpeech.verb, PitchType.kifuku, "kifuku-2"),
        ("たべる", "3", PartOfSpeech.verb, PitchType.kifuku, "kifuku-3"),
        ("あける", "3", PartOfSpeech.verb, PitchType.kifuku, "kifuku-3"),
        ("高い", "2", PartOfSpeech.i_adjective, PitchType.kifuku, "kifuku-2"),
        ("美しい", "3", PartOfSpeech.i_adjective, PitchType.kifuku, "kifuku-3"),
        ("あける", "0", PartOfSpeech.verb, PitchType.heiban, "heiban"),
        ("電話", "1", PartOfSpeech.noun, PitchType.atamadaka, "atamadaka"),
        ("納屋", "0", PartOfSpeech.noun, PitchType.heiban, "heiban"),
    ],
)
def test_kifuku_pitch_handling_in_pitch_param(
    word: str,
    pitch_number: str,
    part_of_speech: PartOfSpeech,
    expected_type: PitchType,
    expected_description: str,
) -> None:
    """Test that kifuku pitch type is handled correctly in PitchParam.from_symbol."""
    param = PitchParam.from_symbol(word, pitch_number, part_of_speech)
    assert param.type == expected_type
    assert param.describe() == expected_description


@pytest.mark.parametrize(
    "raw_headword,  katakana_reading,  pitch_number,  part_of_speech,  expected_description",
    [
        ("食べる", "タベル", "1", PartOfSpeech.verb, "タベル:kifuku-1"),
        ("食べる", "タベル", "2", PartOfSpeech.verb, "タベル:kifuku-2"),
        ("食べる", "タベル", "3", PartOfSpeech.verb, "タベル:kifuku-3"),
        ("食べる", "タベル", "0", PartOfSpeech.verb, "タベル:heiban"),
        ("高い", "タカイ", "2", PartOfSpeech.i_adjective, "タカイ:kifuku-2"),
        ("高い", "タカイ", "0", PartOfSpeech.i_adjective, "タカイ:heiban"),
        ("電話", "デンワ", "1", PartOfSpeech.noun, "デンワ:atamadaka"),
        ("電話", "デンワ", "2", PartOfSpeech.noun, "デンワ:nakadaka-2"),
        ("納屋", "なや", "0", PartOfSpeech.noun, "なや:heiban"),
        ("納屋", "なや", "1", PartOfSpeech.noun, "なや:atamadaka"),
    ],
)
def test_kifuku_pitch_handling_in_pitch_accent_entry(
    raw_headword: str,
    katakana_reading: str,
    pitch_number: str,
    part_of_speech: PartOfSpeech,
    expected_description: str,
) -> None:
    """Test that kifuku pitch type is handled correctly in PitchAccentEntry.from_formatted."""
    entry = PitchAccentEntry.from_formatted(
        FormattedEntry(
            raw_headword=raw_headword,
            katakana_reading=katakana_reading,
            pitch_number=pitch_number,
            html_notation=katakana_reading, # doesn't matter in this test.
        ),
        part_of_speech,
    )
    assert entry.describe_pitches() == expected_description
