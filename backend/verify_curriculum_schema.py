
from sqlalchemy import inspect, text
from app.db.database import engine

inspector = inspect(engine)

tables_to_check = [
    "categories",
    "courses",
    "topics",
    "quizzes",
    "questions",
]

print("\n========== DATABASE SCHEMA VERIFICATION ==========\n")

for table in tables_to_check:
    if not inspector.has_table(table):
        print(f"❌ Missing table: {table}")
        continue

    print(f"\n✅ Table: {table}")

    columns = inspector.get_columns(table)

    for column in columns:
        print(f"   - {column['name']}")

print("\n========== COURSE DATA COUNTS ==========\n")

with engine.connect() as connection:
    for table in tables_to_check:
        result = connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        )
        print(f"{table}: {result.scalar()}")

    users = connection.execute(
        text("SELECT COUNT(*) FROM users")
    )
    print(f"Existing user accounts: {users.scalar()}")

print("\n========== CATEGORY FOREIGN KEY ==========\n")

foreign_keys = inspector.get_foreign_keys("courses")

for fk in foreign_keys:
    if fk["constrained_columns"] == ["category_id"]:
        print(f"Name: {fk['name']}")
        print(f"References: {fk['referred_table']}")
        print(f"Referenced columns: {fk['referred_columns']}")

print("\n========== VERIFICATION COMPLETE ==========")

engine.dispose()
