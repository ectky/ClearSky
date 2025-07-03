from flask import Flask, request, jsonify
import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")
from utils import *

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()["data"]
    if not data or "grades" not in data:
        return jsonify({"error": "Brak danych ocen"}), 400
    print(data["metadata"])
    try:
        df = pd.DataFrame(data["grades"])
        stats, plot_png = generate_grade_stats_and_plot(df)
        print(data["metadata"])

        return jsonify(
            {
                "title": "Statystyki wygenerowane z ocen",
                "stats": {
                    "count": int(stats["count"]),
                    "min": float(stats["min"]),
                    "max": float(stats["max"]),
                    "mean": float(stats["mean"]),
                    "median": float(stats["median"]),
                },
                "metadata": {
                    "message": data["metadata"].get("message", ""),
                    "grade_number": data["metadata"].get("num_grades", ""),
                    "course_name": data["metadata"].get("course_name", ""),
                    "examine_period": data["metadata"].get("examine_period", ""),
                },
                "plot_png": plot_png,
                "table": df.to_html(index=False, classes="table table-bordered"),
            }
        )
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route("/parse", methods=["POST"])
def parse_excel():
    # course_name = request.form.get("course_name")
    # grade_number = request.form.get("grade_number")
    # examine_period = request.form.get("examine_period")
    file = request.files.get("file")

    if not file or not file.filename.endswith(".xlsx"):
        return jsonify({"status": "error", "message": "Invalid file format"}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    try:
        df = validate_excel_schema(file_path, expected_columns)
        title, df, num, period = parse_and_transform_excel(file_path)

        grades_list = df.to_dict(orient="records")
        stats, plot_png = generate_grade_stats_and_plot(df)
        # message = "test"
        # print(grades_list)
        return jsonify(
            {
                "status": "ok",
                "course_name": title,
                "grade_number": num,
                "examine_period": period,
                "title": title,
                "grades": grades_list,
                "statistics": {
                    "count": int(stats["count"]),
                    "min": float(stats["min"]),
                    "max": float(stats["max"]),
                    "mean": float(stats["mean"]),
                    "median": float(stats["median"]),
                },
                "histogram_base64": plot_png,
            }
        )

    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        # return jsonify({"status": "error", "message": str(e)}), 500
        raise


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5002)
