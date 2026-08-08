"""Conversation-first isiXhosa A1 curriculum."""

from app.data._types import CurriculumUnit

CEFR_LEVELS = ["A1"]

A1_UNITS: list[CurriculumUnit] = [
    CurriculumUnit(
        id="a1-unit-1",
        level="A1",
        unit_number=1,
        title="Izandi nezicofayo",
        grammar_points=["xh-vowels", "xh-clicks"],
        vocabulary_set_ids=["izandi_xh_a1"],
        lesson_types=["listening", "vocabulary"],
        competency_checklist=[
            "Biza izikhamiso a, e, i, o, u ngokucacileyo",
            "Yahlula izandi zika-c, q no-x xa uziva naxa uzithetha",
        ],
        default_weeks=1,
    ),
    CurriculumUnit(
        id="a1-unit-2",
        level="A1",
        unit_number=2,
        title="Imibuliso nempilo",
        grammar_points=["xh-singular-plural-greetings", "xh-subject-concords"],
        vocabulary_set_ids=["imibuliso_xh_a1", "imbeko_xh_a1"],
        lesson_types=["vocabulary", "listening"],
        competency_checklist=[
            "Bulisa umntu omnye neqela ngendlela efanelekileyo",
            "Buza impilo uze uphendule",
        ],
        default_weeks=1,
        prerequisite_unit="a1-unit-1",
    ),
    CurriculumUnit(
        id="a1-unit-3",
        level="A1",
        unit_number=3,
        title="Ukuzazisa",
        grammar_points=["xh-copulative-ngu", "xh-question-words"],
        vocabulary_set_ids=["ukuzazisa_xh_a1"],
        lesson_types=["grammar", "writing"],
        competency_checklist=[
            "Xela igama lakho, indawo ovela kuyo nendawo ohlala kuyo",
            "Buza igama nemvelaphi yomnye umntu",
        ],
        default_weeks=1,
        prerequisite_unit="a1-unit-2",
    ),
    CurriculumUnit(
        id="a1-unit-4",
        level="A1",
        unit_number=4,
        title="Ukucela ukucaciselwa",
        grammar_points=["xh-negation", "xh-polite-requests"],
        vocabulary_set_ids=["ukuqonda_xh_a1"],
        lesson_types=["listening", "grammar"],
        competency_checklist=[
            "Chaza xa ungaqondi",
            "Cela umntu aphinde okanye athethe kancinci",
        ],
        default_weeks=1,
        prerequisite_unit="a1-unit-3",
    ),
    CurriculumUnit(
        id="a1-unit-5",
        level="A1",
        unit_number=5,
        title="Usapho nabantu",
        grammar_points=["xh-noun-classes", "xh-possessives"],
        vocabulary_set_ids=["usapho_xh_a1", "abantu_xh_a1"],
        lesson_types=["vocabulary", "reading"],
        competency_checklist=[
            "Chaza abantu abasondeleyo kuwe ngezivakalisi ezilula",
            "Buza ngomntu okanye ngosapho",
        ],
        default_weeks=1,
        prerequisite_unit="a1-unit-4",
    ),
    CurriculumUnit(
        id="a1-unit-6",
        level="A1",
        unit_number=6,
        title="Ukutya nokusela",
        grammar_points=["xh-present-tense", "xh-polite-requests"],
        vocabulary_set_ids=["ukutya_xh_a1", "amanani_xh_a1"],
        lesson_types=["vocabulary", "listening"],
        competency_checklist=[
            "Cela ukutya okanye isiselo ngembeko",
            "Buza ixabiso uze uqonde amanani alula",
        ],
        default_weeks=1,
        prerequisite_unit="a1-unit-5",
    ),
    CurriculumUnit(
        id="a1-unit-7",
        level="A1",
        unit_number=7,
        title="Iindawo nezithuthi",
        grammar_points=["xh-locatives", "xh-question-words"],
        vocabulary_set_ids=["iindawo_xh_a1", "izithuthi_xh_a1"],
        lesson_types=["reading", "listening"],
        competency_checklist=[
            "Buza indlela okanye indawo",
            "Qonda imiyalelo elula yasekunene, yasekhohlo naphambili",
        ],
        default_weeks=1,
        prerequisite_unit="a1-unit-6",
    ),
    CurriculumUnit(
        id="a1-unit-8",
        level="A1",
        unit_number=8,
        title="Incoko yemihla ngemihla",
        grammar_points=["xh-present-tense", "xh-object-concords", "xh-conversation-turns"],
        vocabulary_set_ids=["ixesha_xh_a1", "incoko_xh_a1"],
        lesson_types=["review", "listening"],
        competency_checklist=[
            "Bamba incoko elula yemizuzu emibini",
            "Bulisa, uzazise, ubuze, uphendule uze uvalelise",
        ],
        default_weeks=1,
        prerequisite_unit="a1-unit-7",
    ),
]

CURRICULUM: dict[str, list[CurriculumUnit]] = {"A1": A1_UNITS}


def get_curriculum_units(level: str) -> list[CurriculumUnit]:
    return CURRICULUM.get(level, [])
