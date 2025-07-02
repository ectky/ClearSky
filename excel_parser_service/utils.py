from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import re
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import io
import base64


expected_columns = [
    "Αριθμός Μητρώου",  # Registration Number
    "Ονοματεπώνυμο",  # Full Name
    "Ακαδημαϊκό E-mail",  # Academic Email
    "Περίοδος δήλωσης",  # Declaration Period
    "Τμήμα Τάξης",  # Class Department
    "Κλίμακα βαθμολόγησης",  # Grading Scale
    "Βαθμολογία",  # Grade
]


def validate_excel_schema(filepath, expected_columns, skiprows=2):
    try:
        df = pd.read_excel(filepath, skiprows=skiprows)

        actual_columns = df.columns.tolist()

        # Normalize spaces (optional)
        actual_columns = [col.strip() for col in actual_columns]

        missing_cols = [col for col in expected_columns if col not in actual_columns]
        extra_cols = [col for col in actual_columns if col not in expected_columns]

        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        print("✅ Excel schema is valid.")
        return df  # return df if schema is okay

    except Exception as e:
        raise ValueError(f"❌ Excel schema validation failed: {e}")


def parse_and_transform_excel(file_path):
    df_all = pd.read_excel(file_path, header=None)
    title_row = df_all.iloc[0]
    title = None
    for cell in title_row:
        if pd.notna(cell):
            title = str(cell)
            break
    df_data = pd.read_excel(file_path, header=2)
    df_data = df_data.dropna(how="all").dropna(axis=1, how="all")
    df_data.rename(
        columns={
            "Αριθμός Μητρώου": "student_id",
            "Ονοματεπώνυμο": "full_name",
            "Ακαδημαϊκό E-mail": "academic_email",
            "Περίοδος δήλωσης": "declaration_period",
            "Τμήμα Τάξης": "class_section",
            "Κλίμακα βαθμολόγησης": "grading_scale",
            "Βαθμολογία": "grade",
        },
        inplace=True,
    )

    return title, df_data, len(df_data), df_data["declaration_period"][0]


def generate_grade_stats_and_plot(df, grade_col="grade"):
    # Upewnij się, że kolumna z ocenami jest numeryczna (np. float)
    grades = pd.to_numeric(df[grade_col], errors="coerce").dropna()
    grades = grades.astype(int)
    # Statystyki opisowe
    stats = {
        "count": len(grades),
        "mean": grades.mean(),
        "median": grades.median(),
        "min": grades.min(),
        "max": grades.max(),
    }
    grades = grades[(grades >= 1) & (grades <= 10)]
    bin_edges = np.arange(0.5, 10.5 + 1)  # 0.5 to 10.5 → bins centered on 1–10

    plt.figure(figsize=(6, 4))
    plt.hist(grades, bins=bin_edges, edgecolor="black", rwidth=0.8, align="mid")
    plt.xticks(range(1, 11))
    plt.title("Grades distribution")
    plt.xlabel("Grade")
    plt.ylabel("Studnets number")
    plt.grid(axis="y", alpha=0.75)

    # Zapisz wykres do pamięci jako obraz base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return stats, image_base64


def sanitize_name(name: str) -> str:
    # Zamiana spacji i innych znaków na "_", małe litery, tylko a-z0-9_
    return re.sub(r"\W+", "_", name.strip().lower())


def create_table_if_not_exists(conn, table_name):
    sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        student_id TEXT,
        full_name TEXT,
        academic_email TEXT,
        declaration_period TEXT,
        class_section TEXT,
        grading_scale TEXT,
        grade TEXT
    )
    """
    conn.execute(sql)
    conn.commit()


def insert_grades(conn, table_name, grades):
    # grades to lista słowników z kluczami odpowiadającymi kolumnom
    sql = f"""
    INSERT INTO {table_name} 
    (student_id, full_name, academic_email, declaration_period, class_section, grading_scale, grade)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    data = [
        (
            g.get("Αριθμός Μητρώου", ""),
            g.get("Ονοματεπώνυμο", ""),
            g.get("Ακαδημαϊκό E-mail", ""),
            g.get("Περίοδος δήλωσης", ""),
            g.get("Τμήμα Τάξης", ""),
            g.get("Κλίμακα βαθμολόγησης", ""),
            g.get("Βαθμολογία", ""),
        )
        for g in grades
    ]
    conn.executemany(sql, data)
    conn.commit()
