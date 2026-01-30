import mysql.connector
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import joblib

MODEL_PATH = "career_model.pkl"

# ---------------- DB CONNECTION ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="user123",
    database="career_path_db"
)

print("Connected to DB")

# ---------------- LOAD DATA ----------------
features_df = pd.read_sql("SELECT * FROM student_features_v2", conn)

labels_df = pd.read_sql("""
    SELECT student_id, actual_career_id
    FROM Student
    WHERE actual_career_id IS NOT NULL
""", conn)

data = features_df.merge(labels_df, on="student_id")

# Handle nulls
data["avg_academic_score"] = data["avg_academic_score"].fillna(0)
data["avg_sports_score"] = data["avg_sports_score"].fillna(0)
data["avg_extra_score"] = data["avg_extra_score"].fillna(0)

# ---------------- FEATURES ----------------
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

y = data["actual_career_id"]

# ---------------- TRAIN-TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- TRAIN MODEL ----------------
model = DecisionTreeClassifier(max_depth=6, random_state=42)
model.fit(X_train, y_train)

# ---------------- EVALUATION ----------------
train_acc = accuracy_score(y_train, model.predict(X_train))
test_acc = accuracy_score(y_test, model.predict(X_test))

print("Training accuracy:", train_acc)
print("Test accuracy:", test_acc)

# ---------------- SAVE MODEL ----------------
joblib.dump(model, MODEL_PATH)
print("Model trained and saved")

conn.close()
print("DB connection closed")
