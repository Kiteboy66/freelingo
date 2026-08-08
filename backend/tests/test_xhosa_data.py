from __future__ import annotations

from app.data.assessment_bank import get_assessment_bank
from app.data.curriculum import (
    distribute_units,
    get_curriculum_units,
    get_next_supported_cefr_level,
    get_supported_cefr_levels,
)
from app.data.grammar import get_grammar_topics
from app.data.phrasebook import get_phrasebook_categories
from app.data.vocabulary import get_vocabulary_sets
from app.services.language_helpers import (
    get_iso639,
    get_language_name,
    get_language_script,
    uses_word_spacing,
)


def test_xhosa_pack_exposes_only_content_backed_a1() -> None:
    assert get_supported_cefr_levels("xh-ZA") == ["A1"]
    assert len(get_curriculum_units("A1", "xh-ZA")) == 8
    assert get_curriculum_units("A2", "xh-ZA") == []
    assert get_next_supported_cefr_level("A1", "xh-ZA") is None


def test_xhosa_pack_has_conversation_sprint_content() -> None:
    grammar = get_grammar_topics("xh-ZA")
    vocabulary = get_vocabulary_sets("xh-ZA")
    phrasebook = get_phrasebook_categories("xh-ZA")
    bank = get_assessment_bank("xh-ZA")

    assert len(grammar) >= 12
    assert len(vocabulary) >= 12
    assert len(phrasebook) == 8
    assert len(bank) == 24
    assert {question.skill for question in bank} == {"grammar", "vocabulary", "reading"}
    assert {question.difficulty for question in bank} == {"A1"}


def test_xhosa_two_week_plan_has_thirteen_lessons_and_final_check() -> None:
    units = get_curriculum_units("A1", "xh-ZA")
    slots = distribute_units(units, total_weeks=2, days_per_week=7, target_language="xh-ZA")

    assert len(slots) == 14
    assert slots[0]["week"] == 1
    assert slots[-1]["week"] == 2
    assert slots[-1]["unit_id"] == "completion-test"
    assert slots[-1]["title"] == "Uvavanyo lokugqiba inqanaba A1"
    assert {slot["unit_id"] for slot in slots[:-1]} == {
        f"a1-unit-{number}" for number in range(1, 9)
    }


def test_xhosa_language_metadata() -> None:
    assert get_language_name("xh-ZA") == "isiXhosa"
    assert get_iso639("xh-ZA") == "xh"
    assert get_language_script("xh-ZA") == "latin"
    assert uses_word_spacing("xh-ZA") is True
