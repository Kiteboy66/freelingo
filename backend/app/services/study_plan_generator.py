from __future__ import annotations

from app.data.curriculum import distribute_units, get_curriculum_units
from app.data.xh.guided_course import GUIDED_XHOSA_A1_DAYS
from app.schemas.study_plan import (
    DayPlan,
    GeneratedPlan,
    GenerateStudyPlanRequest,
    WeekPlan,
)
from app.services.language_helpers import get_language_name


async def generate_study_plan(
    request: GenerateStudyPlanRequest,
    target_language: str = "en-GB",
) -> GeneratedPlan:
    """
    Build a curriculum-driven study plan skeleton.
    No LLM call — purely deterministic from the static curriculum.
    LLM is called separately per-lesson when the user opens one for the first time.
    """
    if (
        target_language == "xh-ZA"
        and request.cefr_level == "A1"
        and request.duration_weeks == 2
        and request.days_per_week == 7
    ):
        return _guided_xhosa_sprint_plan()

    lang_name = get_language_name(target_language)
    units = get_curriculum_units(request.cefr_level, target_language)
    lesson_slots = distribute_units(
        units=units,
        total_weeks=request.duration_weeks,
        days_per_week=request.days_per_week,
        target_language=target_language,
    )

    weeks_map: dict[int, list[dict]] = {}
    for slot in lesson_slots:
        w = slot["week"]
        weeks_map.setdefault(w, []).append(slot)

    weekly_plan: list[WeekPlan] = []
    for week_num in sorted(weeks_map):
        slots_in_week = weeks_map[week_num]
        theme = slots_in_week[0]["unit_title"] if slots_in_week else ""
        days = [
            DayPlan(
                day=s["day"],
                lesson_type=s["lesson_type"],
                title=s["title"],
                objectives=s["objectives"],
                estimated_minutes=s["estimated_minutes"],
                unit_id=s["unit_id"],
                grammar_points=s.get("grammar_points", []),
                vocabulary_set_ids=s.get("vocabulary_set_ids", []),
            )
            for s in slots_in_week
        ]
        weekly_plan.append(WeekPlan(week=week_num, theme=theme, days=days))

    return GeneratedPlan(
        title=f"{lang_name} {request.cefr_level} — {request.duration_weeks}-week programme",
        cefr_level=request.cefr_level,
        duration_weeks=request.duration_weeks,
        days_per_week=request.days_per_week,
        ends_with_test=True,
        weekly_plan=weekly_plan,
    )


def _guided_xhosa_sprint_plan() -> GeneratedPlan:
    weekly_plan: list[WeekPlan] = []
    for week_number in (1, 2):
        first_day = (week_number - 1) * 7 + 1
        guided_days = [
            guided for guided in GUIDED_XHOSA_A1_DAYS if first_day <= guided.day < first_day + 7
        ]
        weekly_plan.append(
            WeekPlan(
                week=week_number,
                theme=(
                    "Start speaking from day one"
                    if week_number == 1
                    else "Handle useful everyday conversations"
                ),
                days=[
                    DayPlan(
                        day=((guided.day - 1) % 7) + 1,
                        lesson_type=guided.lesson_type,
                        title=guided.title,
                        objectives=[guided.goal],
                        estimated_minutes=10,
                        unit_id=guided.unit_id,
                        grammar_points=list(guided.grammar_refs),
                        vocabulary_set_ids=[],
                    )
                    for guided in guided_days
                ],
            )
        )

    return GeneratedPlan(
        title="Your 14-day isiXhosa conversation sprint",
        cefr_level="A1",
        duration_weeks=2,
        days_per_week=7,
        ends_with_test=True,
        weekly_plan=weekly_plan,
    )
