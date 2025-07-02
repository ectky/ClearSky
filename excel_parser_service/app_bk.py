from flask import Flask, request, render_template, redirect, url_for
import os
import pandas as pd
import re
import sqlite3
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import io
import base64
from utils import *

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    course_name = request.form["course_name"]
    grade_number = request.form["grade_number"]
    examine_period = request.form["examine_period"]
    message = request.form["message"]
    file = request.files["file"]

    if not file or not file.filename.endswith(".xlsx"):
        return "Invalid file format. Please upload an .xlsx file.", 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Parse the file (replace this with your own logic)
    try:
        try:
            df = validate_excel_schema(file_path, expected_columns)
            title, df = parse_and_transform_excel(file_path)
            table_name = (
                f"grades_{sanitize_name(course_name)}_{sanitize_name(examine_period)}"
            )

            conn = sqlite3.connect("grades.db")
            create_table_if_not_exists(conn, table_name)

            # Zamiana dataframe na listę słowników
            grades_list = df.to_dict(orient="records")
            stats, plot_png = generate_grade_stats_and_plot(df)

            insert_grades(conn, table_name, grades_list)
            conn.close()
        except ValueError as e:
            return render_template("upload.html", error_message=str(e))
    except Exception as e:
        return render_template("upload.html", error_message=str(e))

    return render_template(
        "results.html",
        course_name=course_name,
        grade_number=grade_number,
        examine_period=examine_period,
        message=message,
        title=title,
        grades_list=grades_list,
        stats=stats,
        plot_png=plot_png,
        table=df.to_html(index=False, classes="table table-bordered"),
    )


if __name__ == "__main__":
    app.run(debug=True)
