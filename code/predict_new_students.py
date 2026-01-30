import mysql.connector
import pandas as pd
import joblib
import sys

MODEL_PATH = "career_model.pkl"

# ---------------- DB CONNECTION ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="user123",
    database="career_path_db"
)

print("Connected to DB")

# ---------------- LOAD MODEL ----------------
model = joblib.load(MODEL_PATH)
print("Model loaded")

# ---------------- LOAD FEATURES ----------------
features_df = pd.read_sql("SELECT * FROM student_features_v2", conn)

# ---------------- FILTER NEW STUDENTS ----------------
students_df = pd.read_sql("""
    SELECT student_id
    FROM Student
    WHERE predicted_career_id IS NULL
""", conn)

if students_df.empty:
    print("No new students to predict")
    conn.close()
    sys.exit()

# Merge features
data = features_df.merge(students_df, on="student_id")

# Handle nulls
data["avg_academic_score"] = data["avg_academic_score"].fillna(0)
data["avg_sports_score"] = data["avg_sports_score"].fillna(0)
data["avg_extra_score"] = data["avg_extra_score"].fillna(0)

X = data[
    [
        "class",
        "avg_academic_score",
        "avg_sports_score",
        "avg_extra_score",
        "academic_activity_count",
        "sports_activity_count",
        "extra_activity_count",
        "total_activities"
    ]
]

# ---------------- PREDICT ----------------
preds = model.predict(X)
data["predicted_career_id"] = preds

# ---------------- UPDATE DB ----------------
cursor = conn.cursor()

for _, row in data.iterrows():
    cursor.execute(
        """
        UPDATE Student
        SET predicted_career_id = %s
        WHERE student_id = %s
        """,
        (int(row["predicted_career_id"]), int(row["student_id"]))
    )

conn.commit()
print("Predictions written to database")

conn.close()
print("DB connection closed")
