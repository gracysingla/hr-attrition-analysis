"""
Loads the employee CSV into a SQLite database and runs every query in /queries.

SQLite is used so the project runs with no database install. The SQL itself is
standard and runs unchanged in MySQL Workbench if you'd rather use that.

Usage:  python run_analysis.py
"""

import csv
import glob
import os
import sqlite3

DB = "hr.db"
CSV = "data/employees.csv"

NUMERIC = {
    "EmployeeID", "Age", "JobSatisfaction", "MonthlyIncome",
    "TotalWorkingYears", "WorkLifeBalance", "YearsAtCompany",
    "YearsSinceLastPromotion",
}


def load():
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)

    with open(CSV) as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        coltypes = ", ".join(
            f"{c} {'INTEGER' if c in NUMERIC else 'TEXT'}" for c in columns
        )
        conn.execute(f"CREATE TABLE employees ({coltypes})")

        placeholders = ", ".join("?" for _ in columns)
        rows = [
            tuple(int(r[c]) if c in NUMERIC else r[c] for c in columns)
            for r in reader
        ]
        conn.executemany(f"INSERT INTO employees VALUES ({placeholders})", rows)

    conn.commit()
    print(f"Loaded {len(rows)} rows into {DB}\n")
    return conn


def show(conn, path):
    sql = open(path).read()
    title = os.path.basename(path).replace(".sql", "").replace("_", " ")

    print("=" * 78)
    print(title.upper())
    print("=" * 78)

    cur = conn.execute(sql)
    headers = [d[0] for d in cur.description]
    rows = cur.fetchall()

    widths = [
        max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
        for i, h in enumerate(headers)
    ]
    print("  ".join(str(h).ljust(w) for h, w in zip(headers, widths)))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print("  ".join(str(v).ljust(w) for v, w in zip(r, widths)))
    print()


if __name__ == "__main__":
    conn = load()
    for path in sorted(glob.glob("queries/*.sql")):
        show(conn, path)
    conn.close()
