import csv

file_path = "learning_material/resource_index.csv"

with open(file_path, "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

print("CSV COLUMNS:")
print(reader.fieldnames)

print("\nTOTAL TOPICS:", len(rows))

topic_ids = [row["Topic_id"] for row in rows]

print("DUPLICATE TOPIC IDs:", len(topic_ids) != len(set(topic_ids)))

print("\nMISSING VALUES:")

for row in rows:
    for column in reader.fieldnames:
        if not row.get(column, "").strip():
            print(row.get("Topic_id"), "->", column)

print("\nCOURSE IDs:")
print(set(row["Course_ID"] for row in rows))