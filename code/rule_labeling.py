import mysql.connector
import pandas as pd

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="user123",
    database="career_path_db"
)

print("Connected to database")

# Load features
df = pd.read_sql("SELECT * FROM student_features_v2", conn)

# Career mapping (update IDs if needed)
CAREER_MAP = {
    "Science": 1,
    "Commerce": 2,
    "Arts": 3,
    "Engineer": 4,
    "Doctor": 5,
    "CA": 6,
    "Artist": 7,
    "Sports Professional": 8
}

def assign_career(row):
    cls = row["class"]

    avg_ac = row["avg_academic_score"] or 0
    avg_sp = row["avg_sports_score"] or 0
    avg_ex = row["avg_extra_score"] or 0

    ac_cnt = row["academic_activity_count"]
    sp_cnt = row["sports_activity_count"]
    ex_cnt = row["extra_activity_count"]

    # -------- STREAM LOGIC (<=10) --------
    if cls <= 10:
        if avg_ac >= 75 and ac_cnt >= ex_cnt:
            return CAREER_MAP["Science"]

        elif avg_ex >= 70 and ex_cnt > ac_cnt:
            return CAREER_MAP["Arts"]

        elif avg_ac >= 65 and avg_ex >= 60:
            return CAREER_MAP["Commerce"]

        elif avg_sp >= 70 and sp_cnt >= ac_cnt:
            return CAREER_MAP["Sports Professional"]

        else:
            return CAREER_MAP["Arts"]

    # -------- PROFESSION LOGIC (>=11) --------
    else:
        if avg_ac >= 80 and ac_cnt >= 3:
            return CAREER_MAP["Engineer"]

        elif avg_ac >= 75 and avg_ex >= 60:
            return CAREER_MAP["Doctor"]

        elif avg_ac >= 70 and ex_cnt >= 2:
            return CAREER_MAP["CA"]

        elif avg_ex >= 75 and ex_cnt >= ac_cnt:
            return CAREER_MAP["Artist"]

        elif avg_sp >= 75:
            return CAREER_MAP["Sports Professional"]

        else:
            return CAREER_MAP["Artist"]

# Apply logic
df["new_actual_career_id"] = df.apply(assign_career, axis=1)

# Write to DB
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute(
        """
        UPDATE Student
        SET actual_career_id = %s
        WHERE student_id = %s
        """,
        (int(row["new_actual_career_id"]), int(row["student_id"]))
    )

conn.commit()
print("actual_career_id updated using logical rules")

conn.close()
print("DB connection closed")
