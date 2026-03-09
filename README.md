# Student Career Prediction System

This project is a machine learning-based system designed to predict the most suitable career path for students based on their academic, sports, and extracurricular performance.

## Project Structure

- `code/`
  - `rule_labeling.py`: Applies logical rules based on students' performance across various activities to assign a generic career path (ground truth for training).
  - `train_model.py`: Fetches student features and assigned career labels from the MySQL database, trains a Decision Tree Classifier (`sklearn`), and saves the model.
  - `predict_new_students.py`: Uses the trained model to predict career paths for new students existing in the database without an assigned path.
- `dataset/`: Contains the raw CSV datasets (`student.csv`, `activity.csv`, `career.csv`) which store student demographics, activities, and career choices.
- `model/`: Directory storing the trained machine learning model (`career_model.pkl`).
- `ER_DBMS_updated.png`: Entity-Relationship diagram for the database schema used in the project.

## Prerequisites

- **Python 3.x**
- **MySQL Database**: The system reads and writes to a MySQL database named `career_path_db`.
- **Python Libraries**: `mysql-connector-python`, `pandas`, `scikit-learn`, `joblib`.

## Setup and Usage

1. **Database Setup**:
   Ensure you have a MySQL server running with a database named `career_path_db`. The credentials expected by default are:
   - Host: `localhost`
   - User: `root`
   - Password: `user123`
   
   The database should contain a table `student_features_v2` for features and a `Student` table to hold the `actual_career_id` and `predicted_career_id`.

2. **Labeling Data**:
   Run `rule_labeling.py` to populate the `actual_career_id` in the database based on predefined rules.
   ```bash
   python code/rule_labeling.py
   ```

3. **Training the Model**:
   Run `train_model.py` to train the Decision Tree Classifier on the labeled data.
   ```bash
   python code/train_model.py
   ```
   *The trained model will be saved as `career_model.pkl` in the root directory.*

4. **Predicting for New Students**:
   Run `predict_new_students.py` to infer the career paths for students who do not yet have a prediction.
   ```bash
   python code/predict_new_students.py
   ```

## Career Paths Mapped
1. Science
2. Commerce
3. Arts
4. Engineer
5. Doctor
6. CA (Chartered Accountant)
7. Artist
8. Sports Professional

## License
Feel free to use and modify the specific configurations to fit your database setup.
