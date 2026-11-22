
"""Generate 20 deterministic fictional learner profiles and quiz attempts.

Run from the repository root:
    python data/generate_learners.py

Creates:
    data/learners.json
    data/quiz_attempts.json
"""

import json
import random
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
os.chdir(PROJECT_ROOT)

from ai_engine.common.schemas import COURSE, TOPICS
from ai_engine.learner_analysis.profile import validate_profile
from assessment.scoring.score_quiz import load_questions, score_quiz


SEED = 42
LEARNER_COUNT = 20
QUESTIONS_PER_ATTEMPT = 6
OUTPUT_DIR = PROJECT_ROOT / "data"

GOALS = [
    "Learn Python programming fundamentals",
    "Prepare for Python coding interviews",
    "Build confidence solving programming problems",
    "Learn Python for data analysis",
    "Strengthen problem-solving skills",
]

INTERESTS = [
    ["programming", "problem-solving"],
    ["data-science", "python"],
    ["automation", "coding"],
    ["software-development", "algorithms"],
    ["beginner-projects", "coding"],
]

LEVELS = ["beginner", "intermediate", "advanced"]
DAILY_MINUTES = [20, 30, 45, 60, 90]
SCENARIOS = ["struggling", "developing", "mixed", "strong", "new"]


def _choose_correct_count(rng, scenario, topic_index, attempt):
    """Choose a realistic number of correct answers out of six."""
    if scenario == "struggling":
        count = rng.randint(0, 2)
    elif scenario == "developing":
        count = rng.randint(2, 4)
    elif scenario == "strong":
        count = rng.randint(5, 6)
    elif scenario == "mixed":
        ranges = [(5, 6), (2, 4), (0, 2)]
        low, high = ranges[topic_index % len(ranges)]
        count = rng.randint(low, high)
    else:
        count = rng.randint(2, 5)

    if attempt > 1:
        count = min(6, count + rng.randint(1, 2))

    return count


def _build_answers(rng, topic_questions, correct_count):
    """Build answers with exactly correct_count correct responses."""
    selected = list(topic_questions)
    rng.shuffle(selected)
    selected = selected[:QUESTIONS_PER_ATTEMPT]

    answers = {}

    for index, question in enumerate(selected):
        question_id = question["question_id"]
        correct_answer = str(question["correct"]).strip().lower()

        if index < correct_count:
            answers[question_id] = correct_answer
        else:
            wrong_choices = [
                choice for choice in ("a", "b", "c", "d")
                if choice != correct_answer
            ]
            answers[question_id] = rng.choice(wrong_choices)

    return answers


def generate_dataset():
    rng = random.Random(SEED)
    question_map = load_questions(COURSE)

    questions_by_topic = {topic: [] for topic in TOPICS}

    for question in question_map.values():
        topic = question.get("topic") or question.get("topic_id")

        if topic in questions_by_topic:
            questions_by_topic[topic].append(question)

    for topic in TOPICS:
        if len(questions_by_topic[topic]) < QUESTIONS_PER_ATTEMPT:
            raise ValueError(
                f"Topic '{topic}' has fewer than "
                f"{QUESTIONS_PER_ATTEMPT} questions."
            )

    learners = []
    quiz_attempts = []

    for learner_index in range(LEARNER_COUNT):
        learner_id = f"synthetic_{learner_index + 1:03d}"
        scenario = SCENARIOS[learner_index % len(SCENARIOS)]

        profile = {
            "learner_id": learner_id,
            "course": COURSE,
            "goal": GOALS[learner_index % len(GOALS)],
            "level": LEVELS[learner_index % len(LEVELS)],
            "daily_minutes": DAILY_MINUTES[
                learner_index % len(DAILY_MINUTES)
            ],
            "interests": INTERESTS[
                learner_index % len(INTERESTS)
            ],
        }

        errors = validate_profile(profile)

        if errors:
            raise ValueError(
                f"Invalid profile for {learner_id}: {errors}"
            )

        learners.append(profile)

        # New learners have completed an initial assessment
        # in only the first two topics.
        learner_topics = TOPICS[:2] if scenario == "new" else TOPICS

        for topic_index, topic in enumerate(learner_topics):
            attempt_number = 1

            correct_count = _choose_correct_count(
                rng, scenario, topic_index, attempt_number
            )

            answers = _build_answers(
                rng,
                questions_by_topic[topic],
                correct_count,
            )

            result = score_quiz(
                learner_id=learner_id,
                topic=topic,
                answers=answers,
                questions=question_map,
                attempt=attempt_number,
                course_id=COURSE,
            )

            quiz_attempts.append(result)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    learners_path = OUTPUT_DIR / "learners.json"
    attempts_path = OUTPUT_DIR / "quiz_attempts.json"

    learners_path.write_text(
        json.dumps(learners, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    attempts_path.write_text(
        json.dumps(quiz_attempts, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Generated {len(learners)} fictional learner profiles.")
    print(f"Saved: {learners_path}")
    print(f"Generated {len(quiz_attempts)} scored quiz attempts.")
    print(f"Saved: {attempts_path}")
    print(f"Course: {COURSE}")
    print(f"Topics: {len(TOPICS)}")


if __name__ == "__main__":
    generate_dataset()
