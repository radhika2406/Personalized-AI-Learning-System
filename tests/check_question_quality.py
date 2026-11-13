
import csv
import pathlib
from collections import Counter

courses_folder = pathlib.Path("courses")

required_columns = [
    "question_id", "category", "course", "topic",
    "difficulty", "question", "option_a",
    "option_b", "option_c", "option_d",
    "correct", "explanation"
]

valid_answers = {"a", "b", "c", "d"}
all_ids = set()
issues = []
total_questions = 0

for file in courses_folder.rglob("questions.csv"):
    with file.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        missing_columns = [
            col for col in required_columns
            if col not in (reader.fieldnames or [])
        ]

        if missing_columns:
            issues.append(
                f"{file}: Missing columns {missing_columns}"
            )
            continue

        rows = list(reader)

    print(f"\nChecking: {file.parent.name}")

    for line_number, row in enumerate(rows, start=2):
        total_questions += 1
        question_id = (row.get("question_id") or "").strip()

        if not question_id:
            issues.append(f"{file}, row {line_number}: Missing ID")
        elif question_id in all_ids:
            issues.append(
                f"{file}, row {line_number}: Duplicate ID {question_id}"
            )
        else:
            all_ids.add(question_id)

        for field in required_columns:
            if not (row.get(field) or "").strip():
                issues.append(
                    f"{file}, row {line_number}: Empty {field}"
                )

        correct = (row.get("correct") or "").strip().lower()

        if correct not in valid_answers:
            issues.append(
                f"{file}, row {line_number}: Invalid answer key {correct}"
            )

    print("Questions checked:", len(rows))

print("\n========== QUALITY REPORT ==========")
print("Total questions:", total_questions)
print("Unique IDs:", len(all_ids))
print("Total issues:", len(issues))

if not issues:
    print("RESULT: ALL QUALITY CHECKS PASSED")
else:
    print("RESULT: ISSUES FOUND")
    for issue in issues[:100]:
        print("-", issue)
