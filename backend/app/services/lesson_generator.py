import json
import re
from dataclasses import asdict
from typing import Any

from app.data.curriculum import get_curriculum
from app.data.grammar import get_grammar_topic
from app.data.vocabulary import get_vocabulary_set
from app.data.xh.guided_course import get_guided_xhosa_a1_day
from app.schemas.lessons import (
    ExerciseContent,
    FillBlankEvaluation,
    FreeWriteEvaluation,
    LessonContent,
    PronunciationEvaluation,
)
from app.services.language_helpers import get_language_name, get_native_language_name
from app.services.llm_adapter import llm_adapter
from app.services.prompts import lesson as lesson_prompts
from app.services.prompts.common import get_language_prompt_overlay
from app.services.prompts.lesson import (
    build_fill_blank_eval_prompt,
    build_free_write_eval_prompt,
    build_lesson_generation_prompt,
    build_pronunciation_eval_prompt,
    build_regenerate_exercise_prompt,
)

LESSON_GENERATION_PROMPT = lesson_prompts.LESSON_GENERATION_PROMPT
FILL_BLANK_EVAL_PROMPT = lesson_prompts.FILL_BLANK_EVAL_PROMPT
FREE_WRITE_EVAL_PROMPT = lesson_prompts.FREE_WRITE_EVAL_PROMPT
PRONUNCIATION_EVAL_PROMPT = lesson_prompts.PRONUNCIATION_EVAL_PROMPT


def hint_reveals_answer(native_hint: str | None, correct_answer: str | None) -> bool:
    if not native_hint or not correct_answer:
        return False
    hint = native_hint.casefold()
    answers = [part.strip().casefold() for part in correct_answer.split("/")]
    for answer in answers:
        if not answer:
            continue
        if re.search(r"\s", answer) or not answer.replace("'", "").isalnum():
            if answer in hint:
                return True
            continue
        if re.search(rf"(?<!\w){re.escape(answer)}(?!\w)", hint):
            return True
    return False


def get_valid_grammar_slugs(target_language: str = "en-GB") -> set[str]:
    """Return the set of valid grammar slugs for a given target language."""
    curriculum = get_curriculum(target_language)
    return {slug for units in curriculum.values() for unit in units for slug in unit.grammar_points}


def _curated_xhosa_guided_lesson(
    *,
    cefr_level: str,
    week: int,
    day: int,
    native_language: str | None,
) -> LessonContent | None:
    """Return one deterministic, conversation-first isiXhosa sprint lesson."""
    if cefr_level != "A1" or (native_language or "en").split("-")[0] != "en":
        return None

    guided = get_guided_xhosa_a1_day(week, day)
    if guided is None:
        return None

    translations = [phrase.translation for phrase in guided.phrases]
    target_phrases = [phrase.text for phrase in guided.phrases]
    exercises = [
        ExerciseContent(
            type="multiple_choice",
            question=f'Kuthetha ukuthini: "{guided.phrases[0].text}"?',
            native_question=f'What does "{guided.phrases[0].text}" mean?',
            options=translations,
            correct=guided.phrases[0].translation,
            explanation=f"“{guided.phrases[0].text}” uthetha “{guided.phrases[0].translation}”.",
            native_explanation=(
                f"Correct: “{guided.phrases[0].text}” means “{guided.phrases[0].translation}”"
            ),
            native_hint="Say the phrase aloud once, then recall the situation where you used it.",
        ),
        ExerciseContent(
            type="multiple_choice",
            question=f'Uthi njani: "{guided.phrases[1].translation}"?',
            native_question=f"How do you say “{guided.phrases[1].translation}” in isiXhosa?",
            options=target_phrases,
            correct=guided.phrases[1].text,
            explanation=f"Impendulo ngu: “{guided.phrases[1].text}”",
            native_explanation=f"The isiXhosa phrase is “{guided.phrases[1].text}”",
            native_hint="Picture the short conversation, and try to say the answer before revealing the choices.",
        ),
        ExerciseContent(
            type="multiple_choice",
            question=f'Uthi njani: "{guided.phrases[2].translation}"?',
            native_question=f"How do you say “{guided.phrases[2].translation}” in isiXhosa?",
            options=target_phrases,
            correct=guided.phrases[2].text,
            explanation=f"Impendulo ngu: “{guided.phrases[2].text}”",
            native_explanation=f"The isiXhosa phrase is “{guided.phrases[2].text}”",
            native_hint="Try the answer from memory first; the choices are only a check.",
        ),
    ]

    return LessonContent(
        lesson_type=guided.lesson_type,
        title=guided.xhosa_title,
        native_title=guided.title,
        cefr_level=cefr_level,
        unit_id=guided.unit_id,
        explanation={
            "text": guided.xhosa_title,
            "key_points": [phrase.text for phrase in guided.phrases],
            "examples": [],
        },
        native_explanation={
            "text": guided.goal,
            "key_points": [f"{phrase.text} — {phrase.translation}" for phrase in guided.phrases],
            "examples": [],
            "common_traps": [],
            "mini_glossary": [],
        },
        exercises=exercises,
        vocabulary=[
            {
                "word": phrase.text,
                "definition": phrase.translation,
                "translation": phrase.translation,
                "example": phrase.text,
                "example_translation": phrase.translation,
                "reading": phrase.chunks,
                "note": phrase.usage,
            }
            for phrase in guided.phrases
        ],
        grammar_refs=list(guided.grammar_refs),
        learning_flow={
            "version": 1,
            "day": guided.day,
            "goal": guided.goal,
            "coach_note": guided.coach_note,
            "phrases": [asdict(phrase) for phrase in guided.phrases],
            "dialogue": [asdict(line) for line in guided.dialogue],
        },
    )


async def generate_lesson(
    cefr_level: str,
    lesson_type: str,
    topic: str,
    week: int,
    day: int,
    unit_id: str = "",
    grammar_points: list[str] | None = None,
    vocabulary_set_ids: list[str] | None = None,
    target_language: str = "en-GB",
    native_language: str | None = None,
) -> LessonContent:
    if target_language == "xh-ZA":
        curated_lesson = _curated_xhosa_guided_lesson(
            cefr_level=cefr_level,
            week=week,
            day=day,
            native_language=native_language,
        )
        if curated_lesson is not None:
            return curated_lesson

    gp_str = ", ".join(grammar_points) if grammar_points else "none specified"
    vs_str = ", ".join(vocabulary_set_ids) if vocabulary_set_ids else "general"
    target_language_name = get_language_name(target_language)
    native_language_name = get_native_language_name(native_language) if native_language else "none"
    language_prompt_overlay = get_language_prompt_overlay(target_language)
    valid_slugs = get_valid_grammar_slugs(target_language)
    valid_slugs_str = ", ".join(sorted(valid_slugs))
    curriculum_source = json.dumps(
        {
            "grammar": [
                asdict(topic_data)
                for slug in (grammar_points or [])
                if (topic_data := get_grammar_topic(slug, target_language)) is not None
            ],
            "vocabulary": [
                asdict(vocabulary_data)
                for set_id in (vocabulary_set_ids or [])
                if (vocabulary_data := get_vocabulary_set(set_id, target_language)) is not None
            ],
        },
        ensure_ascii=False,
    )
    prompt = build_lesson_generation_prompt(
        cefr_level=cefr_level,
        target_language_name=target_language_name,
        native_language_name=native_language_name,
        lesson_type=lesson_type,
        topic=topic,
        unit_id=unit_id or "—",
        grammar_points=gp_str,
        vocabulary_set_ids=vs_str,
        week=week,
        day=day,
        valid_slugs=valid_slugs_str,
        curriculum_source=curriculum_source,
        language_prompt_overlay=language_prompt_overlay,
    )

    lesson = await llm_adapter.structured_output(
        [{"role": "system", "content": prompt}],
        LessonContent,
    )
    lesson.grammar_refs = [s for s in lesson.grammar_refs if s in valid_slugs]
    # Sanitize fill_blank exercises: question MUST contain ___ (the gapped sentence).
    # If the LLM put the instruction in question and the actual sentence in explanation,
    # swap them so the user always sees the gapped sentence in the UI.
    for ex in lesson.exercises:
        if ex.type == "fill_blank" and "___" not in ex.question:
            if ex.explanation and "___" in ex.explanation:
                ex.question, ex.explanation = ex.explanation, ex.question
        if hint_reveals_answer(ex.native_hint, ex.correct):
            ex.native_hint = None
    return lesson


async def regenerate_exercise(
    *,
    cefr_level: str,
    lesson_type: str,
    topic: str,
    exercise_type: str,
    lesson_explanation: dict[str, Any],
    lesson_vocabulary: list[dict[str, Any]] | None,
    invalid_exercise: dict[str, Any],
    target_language: str = "en-GB",
    native_language: str | None = None,
) -> ExerciseContent:
    target_language_name = get_language_name(target_language)
    native_language_name = get_native_language_name(native_language) if native_language else "none"
    language_prompt_overlay = get_language_prompt_overlay(target_language)
    options_schema = {
        "multiple_choice": '["option 1", "option 2", "option 3", "option 4"]',
        "fill_blank": "null",
        "free_write": '["grading criterion 1", "grading criterion 2"]',
        "pronunciation": '["short pronunciation hint"]',
    }.get(exercise_type, "null")
    prompt = build_regenerate_exercise_prompt(
        cefr_level=cefr_level,
        target_language_name=target_language_name,
        native_language_name=native_language_name,
        lesson_type=lesson_type,
        topic=topic,
        exercise_type=exercise_type,
        lesson_explanation=json.dumps(lesson_explanation or {}, ensure_ascii=False),
        lesson_vocabulary=json.dumps(lesson_vocabulary or [], ensure_ascii=False),
        invalid_exercise=json.dumps(invalid_exercise, ensure_ascii=False),
        options_schema=options_schema,
        language_prompt_overlay=language_prompt_overlay,
    )

    exercise = await llm_adapter.structured_output(
        [{"role": "system", "content": prompt}],
        ExerciseContent,
    )
    if exercise.type != exercise_type:
        raise ValueError("Regenerated exercise type does not match original type")
    if exercise.type == "fill_blank" and "___" not in exercise.question:
        if exercise.explanation and "___" in exercise.explanation:
            exercise.question, exercise.explanation = (
                exercise.explanation,
                exercise.question,
            )
    if hint_reveals_answer(exercise.native_hint, exercise.correct):
        exercise.native_hint = None
    return exercise


async def evaluate_free_write(
    cefr_level: str,
    prompt: str,
    criteria: list[str],
    answer: str,
    target_language: str = "en-GB",
    native_language: str | None = None,
) -> FreeWriteEvaluation:
    target_language_name = get_language_name(target_language)
    native_language_name = (
        get_native_language_name(native_language) if native_language else "English"
    )
    language_prompt_overlay = get_language_prompt_overlay(target_language)
    eval_prompt = build_free_write_eval_prompt(
        cefr_level=cefr_level,
        target_language_name=target_language_name,
        native_language_name=native_language_name,
        prompt=prompt,
        criteria=", ".join(criteria),
        answer=answer,
        language_prompt_overlay=language_prompt_overlay,
    )

    result = await llm_adapter.structured_output(
        [{"role": "system", "content": eval_prompt}],
        FreeWriteEvaluation,
    )
    return result


async def evaluate_pronunciation(
    cefr_level: str,
    target: str,
    transcription: str,
    target_language: str = "en-GB",
    native_language: str | None = None,
) -> PronunciationEvaluation:
    target_language_name = get_language_name(target_language)
    native_language_name = (
        get_native_language_name(native_language) if native_language else "English"
    )
    language_prompt_overlay = get_language_prompt_overlay(target_language)
    eval_prompt = build_pronunciation_eval_prompt(
        cefr_level=cefr_level,
        target_language_name=target_language_name,
        native_language_name=native_language_name,
        target=target,
        transcription=transcription,
        language_prompt_overlay=language_prompt_overlay,
    )
    result = await llm_adapter.structured_output(
        [{"role": "system", "content": eval_prompt}],
        PronunciationEvaluation,
    )
    return result


async def evaluate_fill_blank(
    cefr_level: str,
    question: str,
    correct_answer: str,
    student_answer: str,
    target_language: str = "en-GB",
    native_language: str | None = None,
) -> FillBlankEvaluation:
    target_language_name = get_language_name(target_language)
    native_language_name = (
        get_native_language_name(native_language) if native_language else "English"
    )
    language_prompt_overlay = get_language_prompt_overlay(target_language)
    eval_prompt = build_fill_blank_eval_prompt(
        cefr_level=cefr_level,
        target_language_name=target_language_name,
        native_language_name=native_language_name,
        question=question,
        correct_answer=correct_answer,
        student_answer=student_answer,
        language_prompt_overlay=language_prompt_overlay,
    )
    result = await llm_adapter.structured_output(
        [{"role": "system", "content": eval_prompt}],
        FillBlankEvaluation,
    )
    return result
