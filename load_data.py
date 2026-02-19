import csv
from app import app, db, Question

# I'm creating an application context so database operations can run safely
with app.app_context():

    # I'm opening the CSV file
    with open("Mathematics-questions-dataset.csv", newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            question = Question(
                question_text=row["question_text"],
                topic=row["topic"],
                method=row["method"],
                method_reason=row["method_reason"]
            )

            db.session.add(question)

        # I'm committing all inserted questions to the database
        db.session.commit()

    print("✅ Data successfully loaded into the database.")