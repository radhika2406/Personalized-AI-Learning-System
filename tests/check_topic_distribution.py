
import csv
import pathlib
from collections import Counter, defaultdict

courses_folder = pathlib.Path("courses")

topics_checked = 0
issues = []

for file in courses_folder.rglob("questions.csv"):
    with file.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    topics = defaultdict(list)

    for row in rows:
        topic = row.get("topic") or row.get("topic_id") or "MISSING"
        topics[topic].append(row)

    print(f"\nCourse: {file.parent.name}")

    for topic, questions in sorted(topics.items()):
        difficulty = Counter(
            q.get("difficulty", "").strip().lower()
            for q in questions
        )

        topics_checked += 1

        correct = (
            len(questions) == 6
            and difficulty == {
                "easy": 3,
                "medium": 2,
                "hard": 1
            }
        )

        if correct:
            print(f"  PASS: {topic}")
        else:
            print(f"  FAIL: {topic} - {dict(difficulty)}")
            issues.append((file.parent.name, topic, dict(difficulty)))

print("\n========== FINAL REPORT ==========")
print("Topics checked:", topics_checked)
print("Topics with issues:", len(issues))

if not issues:
    print("RESULT: ALL TOPICS PASSED")
else:
    print("RESULT: ISSUES FOUND")
    for issue in issues:
        print(issue)
