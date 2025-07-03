import sqlite3


def create_table_if_not_exists(conn, table_name, columns):
    col_defs = ", ".join([f'"{col}" TEXT' for col in columns])
    query = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({col_defs})'
    conn.execute(query)
    conn.commit()


def insert_grades(conn, table_name, grades, course_id):
    if not grades:
        return

    columns = list(grades[0].keys()) + ["course_id"]
    placeholders = ", ".join(["?"] * len(columns))
    col_names = ", ".join([f'"{col}"' for col in columns])
    values = [
        tuple(str(row[col]) if col != "course_id" else course_id for col in columns)
        for row in grades
    ]

    query = f'INSERT INTO "{table_name}" ({col_names}) VALUES ({placeholders})'
    conn.executemany(query, values)
    conn.commit()
