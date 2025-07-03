from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session handling

import os

EXCEL_PARSER_URL = os.environ.get("EXCEL_PARSER_URL")
GRADE_SERVICE_URL = os.environ.get("GRADE_SERVICE_URL")


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
        if not file:
            return "No file uploaded", 400

        files = {"file": (file.filename, file.stream, file.content_type)}
        response = requests.post(EXCEL_SERVICE_URL + "/parse", files=files)

        if response.status_code == 200:
            parsed_data = response.json()
            return render_template("upload_confirm.html", data=parsed_data)
        else:
            error_message = response.text
            return render_template("upload.html", error=error_message)

    return render_template("upload.html")


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


@app.route("/stats")
def stats():
    course_name = request.args.get("course_name")
    examine_period = request.args.get("examine_period")

    if not course_name or not examine_period:
        return render_template("error.html", message="Brak wymaganych parametrów.")

    try:
        grades_resp = requests.get(
            f"{GRADE_SERVICE_URL}/grades",
            params={"course_name": course_name, "examine_period": examine_period},
        )
        if grades_resp.status_code != 200:
            return render_template("error.html", message="Nie udało się pobrać ocen.")
        grades_data = grades_resp.json()

        analyze_resp = requests.post(
            f"{EXCEL_SERVICE_URL}/analyze", json={"data": grades_data}
        )
        if analyze_resp.status_code != 200:
            return render_template(
                "error.html",
                message="Nie udało się wygenerować statystyk.",
                test=analyze_resp.json(),
            )

        stats_data = analyze_resp.json()

        return render_template(
            "stats.html",
            course_name=course_name,
            examine_period=examine_period,
            title=stats_data["title"],
            stats=stats_data["stats"],
            plot_png=stats_data["plot_png"],
            table=stats_data["table"],
            message=stats_data["metadata"].get("message", ""),
            grade_number=stats_data["metadata"].get("grade_number", ""),
        )

    except Exception as e:
        return render_template("error.html", message=f"Błąd: {e}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)