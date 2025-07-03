from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session handling

import os

EXCEL_SERVICE_URL = os.environ.get("EXCEL_PARSER_URL", "http://localhost:5001")
GRADE_SERVICE_URL = os.environ.get("GRADE_SERVICE_URL", "http://localhost:5002")
COURSES_SERVICE_URL = os.environ.get("COURSES_SERVICE_URL", "http://localhost:5004")

@app.route("/")
def index():
    try:
        print("HERE")
        resp = requests.get(f"{GRADE_SERVICE_URL}/available_tables")
        if resp.status_code == 200:
            available_tables = resp.json()
        else:
            available_tables = []
    except Exception as e:
        available_tables = []

    return render_template("index.html", available_tables=available_tables)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        course_id = request.form.get("course_id")
        if not file:
            return "No file uploaded", 400

        files = {"file": (file.filename, file.stream, file.content_type)}
        response = requests.post(EXCEL_SERVICE_URL + "/parse", files=files)

        if response.status_code == 200:
            parsed_data = response.json()
            parsed_data["course_id"] = course_id
            return render_template("upload_confirm.html", data=parsed_data)
        else:
            error_message = response.text
            return render_template("upload.html", error=error_message)
    else:
        try:
            response = requests.get(
                f"{COURSES_SERVICE_URL}/courses",
                # params={"user_id": user_id, "is_superuser": int(is_superuser)}
            )
            courses = response.json() if response.status_code == 200 else []
            print(response.json())
        except Exception as e:
            print("Error contacting courses service:", e)
            courses = []

        return render_template("upload.html", courses=courses)


@app.route("/confirm_upload", methods=["POST"])
def confirm_upload():
    import json

    parsed_json_str = request.form.get("parsed_data")
    if not parsed_json_str:
        return render_template("error.html", message="Brak danych do zapisania.")

    try:
        parsed_data = json.loads(parsed_json_str)
    except Exception as e:
        return render_template("error.html", message=f"Błąd parsowania danych: {e}")
    message = request.form.get("message", "")
    parsed_data["message"] = message
    response = requests.post(GRADE_SERVICE_URL + "/save", json=parsed_data)

    if response.status_code == 200:
        return redirect(url_for("index"))
    else:
        return render_template("error.html", message="Nie udało się zapisać danych.")



@app.route("/stats", methods=["GET", "POST"])
def stats():
    allowed_course_ids = [1, 2, 3]

    if request.method == "POST":
        course_id = request.form.get("course_id", type=int)
    else:
        course_id = request.args.get("course_id", type=int)

    if not course_id or course_id not in allowed_course_ids:
        return render_template("error.html", message="Nieprawidłowy lub brakujący course_id (dozwolone: 1, 2, 3).")

    try:
        grades_resp = requests.get(
            f"{GRADE_SERVICE_URL}/grades",
            params={"course_id": course_id}
        )
        if grades_resp.status_code != 200:
            return render_template("error.html", message="Nie udało się pobrać ocen.")

        grades_data = grades_resp.json()

        analyze_resp = requests.post(
            f"{EXCEL_SERVICE_URL}/analyze", json={"data": grades_data}
        )
        if analyze_resp.status_code != 200:
            return render_template("error.html", message="Nie udało się wygenerować statystyk.")

        stats_data = analyze_resp.json()

        return render_template(
            "stats.html",
            course_name=stats_data["metadata"].get("course_name", ""),
            examine_period=stats_data["metadata"].get("examine_period", ""),
            course_id=course_id,
            title=stats_data["title"],
            stats=stats_data["stats"],
            plot_png=stats_data["plot_png"],
            table=stats_data["table"],
            message=stats_data["metadata"].get("message", ""),
            grade_number=stats_data["metadata"].get("grade_number", ""),
        )

    except Exception as e:
        return render_template("error.html", message=f"Błąd: {e}")



@app.route("/course/<int:course_id>")
def course_detail(course_id):

    try:
        course_resp = requests.get(f"{COURSES_SERVICE_URL}/courses")
        courses = course_resp.json() if course_resp.status_code == 200 else []
        course = next((c for c in courses if c["id"] == course_id), None)
        if not course:
            return render_template("error.html", message="Nie znaleziono kursu.")
    except Exception as e:
        return render_template("error.html", message=f"Błąd pobierania kursu: {e}")


    try:
        grades_resp = requests.get(f"{GRADE_SERVICE_URL}/grades", params={"course_id": course_id, "course_name": course["name"], "examine_period": ""})
        if grades_resp.status_code != 200:
            grades = []
            metadata = {}
        else:
            data = grades_resp.json()
            grades = data.get("grades", [])
            metadata = data.get("metadata", {})
    except Exception as e:
        grades = []
        metadata = {}

    return render_template("course_detail.html", course=course, grades=grades, metadata=metadata)

@app.route("/choose_course")
def choose_course():
    
    return render_template("choose_course.html")



@app.route("/stats_redirect", methods=["POST"])
def stats_redirect():
    course_id = request.form.get("course_id")
    return redirect(url_for("stats", course_id=course_id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

