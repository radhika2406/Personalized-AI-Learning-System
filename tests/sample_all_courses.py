
import csv
import pathlib

for file in sorted(pathlib.Path("courses").rglob("questions.csv")):
    with file.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    print("\n" + "=" * 60)
    print("COURSE:", file.parent.name)
    print("=" * 60)

    for row in rows[:2]:
        print("\nQuestion:", row["question"])
        print("A:", row["option_a"])
        print("B:", row["option_b"])
        print("C:", row["option_c"])
        print("D:", row["option_d"])
        print("Correct:", row["correct"])
        print("Explanation:", row["explanation"])
