"""
Language-aware curriculum dispatcher.

For backward compatibility, CEFR_LEVELS remains a module-level constant.
All curriculum queries accept a ``target_language`` parameter (e.g. "en-GB",
"es-ES", "it-IT", "pt-PT") to resolve the correct language module.
"""

from __future__ import annotations

import sys

from app.data._types import CEFRLevel, CurriculumUnit  # noqa: F401

CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

_LANG_MODULES: dict[str, str] = {
    "en-GB": "app.data.en_GB.curriculum",
    "en-US": "app.data.en_US.curriculum",
    "de": "app.data.de.curriculum",
    "es": "app.data.es.curriculum",
    "fr": "app.data.fr.curriculum",
    "it": "app.data.it.curriculum",
    "ja": "app.data.ja.curriculum",
    "ko": "app.data.ko.curriculum",
    "pt": "app.data.pt.curriculum",
    "xh": "app.data.xh.curriculum",
    "zh": "app.data.zh.curriculum",
}

_CACHE: dict[str, object] = {}

_I18N = {
    "en-GB": {
        "lesson_title": "{title} - Lesson {n}",
        "test_unit_title": "Level {level} Completion Test",
        "test_title": "Level {level} Completion Test",
        "test_objectives": [
            "Review all grammar topics from this level",
            "Complete the assessment to unlock the next level",
        ],
    },
    "en-US": {
        "lesson_title": "{title} - Lesson {n}",
        "test_unit_title": "Level {level} Completion Test",
        "test_title": "Level {level} Completion Test",
        "test_objectives": [
            "Review all grammar topics from this level",
            "Complete the assessment to unlock the next level",
        ],
    },
    "es-ES": {
        "lesson_title": "{title} - Lección {n}",
        "test_unit_title": "Examen de nivel {level}",
        "test_title": "Examen de nivel {level}",
        "test_objectives": [
            "Repasar todos los temas de gramática de este nivel",
            "Completar la evaluación para desbloquear el siguiente nivel",
        ],
    },
    "it-IT": {
        "lesson_title": "{title} - Lezione {n}",
        "test_unit_title": "Test di livello {level}",
        "test_title": "Test di livello {level}",
        "test_objectives": [
            "Ripassare tutti gli argomenti di grammatica di questo livello",
            "Completare la valutazione per sbloccare il livello successivo",
        ],
    },
    "pt-PT": {
        "lesson_title": "{title} - Lição {n}",
        "test_unit_title": "Exame de nível {level}",
        "test_title": "Exame de nível {level}",
        "test_objectives": [
            "Rever todos os tópicos de gramática deste nível",
            "Concluir a avaliação para desbloquear o próximo nível",
        ],
    },
    "fr-FR": {
        "lesson_title": "{title} - Leçon {n}",
        "test_unit_title": "Test de niveau {level}",
        "test_title": "Test de niveau {level}",
        "test_objectives": [
            "Revoir tous les thèmes de grammaire de ce niveau",
            "Réussir l'évaluation pour débloquer le niveau suivant",
        ],
    },
    "de-DE": {
        "lesson_title": "{title} - Lektion {n}",
        "test_unit_title": "Niveautest {level}",
        "test_title": "Niveautest {level}",
        "test_objectives": [
            "Alle Grammatikthemen dieses Niveaus wiederholen",
            "Die Prüfung bestehen, um das nächste Niveau freizuschalten",
        ],
    },
    "ja-JP": {
        "lesson_title": "{title} - レッスン {n}",
        "test_unit_title": "{level} レベル修了テスト",
        "test_title": "{level} レベル修了テスト",
        "test_objectives": [
            "このレベルの文法項目を復習する",
            "評価を完了して次のレベルを解放する",
        ],
    },
    "ko-KR": {
        "lesson_title": "{title} - 레슨 {n}",
        "test_unit_title": "{level} 레벨 완료 테스트",
        "test_title": "{level} 레벨 완료 테스트",
        "test_objectives": [
            "이 레벨의 모든 문법 항목을 복습하기",
            "평가를 완료하여 다음 레벨 잠금 해제하기",
        ],
    },
    "zh-CN": {
        "lesson_title": "{title} - 第 {n} 课",
        "test_unit_title": "{level} 等级完成测试",
        "test_title": "{level} 等级完成测试",
        "test_objectives": [
            "复习本等级的所有语法项目",
            "完成评估以解锁下一个等级",
        ],
    },
    "xh-ZA": {
        "lesson_title": "{title} - Isifundo {n}",
        "test_unit_title": "Uvavanyo lokugqiba inqanaba {level}",
        "test_title": "Uvavanyo lokugqiba inqanaba {level}",
        "test_objectives": [
            "Phinda zonke izihloko zeli nqanaba",
            "Gqiba uvavanyo lwencoko lweentsuku ezilishumi elinesine",
        ],
    },
}


def get_supported_cefr_levels(target_language: str = "en-GB") -> list[str]:
    """Return only the CEFR levels with real curriculum content."""
    curriculum = get_curriculum(target_language)
    return [level for level in CEFR_LEVELS if curriculum.get(level)]


def get_next_supported_cefr_level(level: str, target_language: str = "en-GB") -> str | None:
    """Return the next content-backed level, never a placeholder level."""
    levels = get_supported_cefr_levels(target_language)
    if level not in levels:
        return None
    index = levels.index(level)
    return levels[index + 1] if index + 1 < len(levels) else None


def _resolve_module(target_language: str) -> object:
    module_name = _LANG_MODULES.get(target_language) or _LANG_MODULES.get(
        target_language.split("-")[0], "app.data.en_GB.curriculum"
    )

    if module_name not in _CACHE:
        __import__(module_name)
        _CACHE[module_name] = sys.modules[module_name]

    return _CACHE[module_name]


def get_curriculum(target_language: str) -> dict:
    """Return the full CURRICULUM dict for the given target language."""
    mod = _resolve_module(target_language)
    return mod.CURRICULUM


def get_curriculum_units(level: str, target_language: str = "en-GB") -> list:
    """Return curriculum units for a CEFR level in the given target language."""
    curriculum = get_curriculum(target_language)
    return curriculum.get(level, [])


def distribute_units(
    units: list[CurriculumUnit],
    total_weeks: int,
    days_per_week: int,
    target_language: str = "en-GB",
) -> list[dict]:
    """Distribute curriculum units across lesson slots."""
    i18n = _I18N.get(target_language) or _I18N.get(target_language.split("-")[0], _I18N["en-GB"])

    total_slots = total_weeks * days_per_week
    lesson_slots = max(1, total_slots - 1)

    lesson_types_per_unit = [lt for u in units for lt in u.lesson_types]

    if not lesson_types_per_unit:
        return []

    slots: list[dict] = []
    lessons_seen_by_unit: dict[str, int] = {}

    for slot in range(lesson_slots):
        # Spread the available sessions across every unit. This matters for
        # short intensive plans, where walking each unit's full lesson-type
        # list before advancing can leave the final competencies untouched.
        unit_index = min((slot * len(units)) // lesson_slots, len(units) - 1)
        unit = units[unit_index]
        lt_list = unit.lesson_types
        unit_lesson_number = lessons_seen_by_unit.get(unit.id, 0)
        lt = lt_list[unit_lesson_number % len(lt_list)] if lt_list else "grammar"

        slots.append(
            {
                "week": slot // days_per_week + 1,
                "day": slot % days_per_week + 1,
                "unit_id": unit.id,
                "unit_title": unit.title,
                "lesson_type": lt,
                "title": i18n["lesson_title"].format(
                    title=unit.title, n=unit_lesson_number + 1
                ),
                "objectives": (unit.competency_checklist[:2] if unit.competency_checklist else []),
                "estimated_minutes": 25,
                "grammar_points": (unit.grammar_points[:2] if unit.grammar_points else []),
                "vocabulary_set_ids": (
                    unit.vocabulary_set_ids[:1] if unit.vocabulary_set_ids else []
                ),
            }
        )
        lessons_seen_by_unit[unit.id] = unit_lesson_number + 1

    last_unit = units[-1]
    level = units[0].level
    slots.append(
        {
            "week": total_weeks,
            "day": days_per_week,
            "unit_id": "completion-test",
            "unit_title": i18n["test_unit_title"].format(level=level),
            "lesson_type": "review",
            "title": i18n["test_title"].format(level=level),
            "objectives": i18n["test_objectives"],
            "estimated_minutes": 45,
            "grammar_points": last_unit.grammar_points,
            "vocabulary_set_ids": [],
        }
    )

    return slots
