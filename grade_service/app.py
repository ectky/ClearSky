from flask import Flask, request, jsonify
from db import create_table_if_not_exists, insert_grades
import sqlite3
import re
import pandas as pd

app = Flask(__name__)


@app.route("/save", methods=["POST"])
def save_grades():
    print("AAAAAA")
    data = request.get_json()
    grades = data.get("grades")
    message = data.get("message")
    course_name = data.get("course_name")
    examine_period = data.get("examine_period")
    table_base = f"{course_name}_{examine_period}".replace(" ", "_").lower()
    grades_table = f"grades_{table_base}"
    meta_table = f"meta_{table_base}"

    if not grades:
        return jsonify({"error": "Missing table_name or grades"}), 400

    try:
        conn = sqlite3.connect("grades.db")
        create_table_if_not_exists(conn, grades_table, grades[0].keys())
        insert_grades(conn, grades_table, grades)

        # 2. Create and insert into metadata table
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS "{meta_table}" (
                "course_name" TEXT,
                "examine_period" TEXT,
                "num_grades" INTEGER,
                "message" TEXT
            )
        """
        )
        conn.execute(
            f"""
            DELETE FROM "{meta_table}"
        """
        )  # ensure no duplicates
        conn.execute(
            f"""
            INSERT INTO "{meta_table}" ("course_name", "examine_period", "num_grades", "message")
            VALUES (?, ?, ?, ?)
        """,
            (course_name, examine_period, len(grades), message),
        )

        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success"}), 200


def sanitize_name(name: str) -> str:
    return re.sub(r"\W+", "_", name.strip().lower())


@app.route("/grades", methods=["GET"])
def get_grades():
    course_name = request.args.get("course_name")
    examine_period = request.args.get("examine_period")

    if not course_name or not examine_period:
        return jsonify({"error": "Missing parameters"}), 400

    table_base = f"{course_name}_{examine_period}".replace(" ", "_").lower()
    grades_table = f"grades_{table_base}"
    meta_table = f"meta_{table_base}"

    try:
        conn = sqlite3.connect("grades.db")
        grades_df = pd.read_sql_query(f'SELECT * FROM "{grades_table}"', conn)
        meta_df = pd.read_sql_query(f'SELECT * FROM "{meta_table}"', conn)
        metadata = meta_df.to_dict(orient="records")[0]

        conn.close()

        return jsonify(
            {"metadata": metadata, "grades": grades_df.to_dict(orient="records")}
        )
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route("/available_tables", methods=["GET"])
def available_tables():
    conn = sqlite3.connect("grades.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [row[0] for row in cursor.fetchall()]
    conn.close()
    parsed = []
    for name in table_names:
        if name.startswith("grades_"):
            parts = name.split("_", 2)
            if len(parts) == 3:
                parsed.append({"course_name": parts[1], "examine_period": parts[2]})

    return jsonify(parsed)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
