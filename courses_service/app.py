from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


@app.route("/courses", methods=["GET"])
def get_courses():
    # user_id = request.args.get("user_id", type=int)
    # is_superuser = request.args.get("is_superuser", type=int)

    try:
        conn = sqlite3.connect("./courses.db")
        cursor = conn.cursor()

        # if is_superuser:
        #     cursor.execute("SELECT id, name FROM courses")
        # else:
        #     cursor.execute(
        #         "SELECT id, name FROM courses WHERE owner_id = ?", (user_id,)
        #     )
        cursor.execute("SELECT id, name FROM courses")

        courses = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(courses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/courses", methods=["POST"])
def add_course():
    data = request.get_json()
    course_id = data.get("id")
    course_name = data.get("name")

    if not course_id or not course_name:
        return jsonify({"error": "Missing id or name"}), 400

    try:
        conn = sqlite3.connect("./courses.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)
        cursor.execute("INSERT INTO courses (id, name) VALUES (?, ?)", (course_id, course_name))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
