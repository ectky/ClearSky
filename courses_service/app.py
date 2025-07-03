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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
