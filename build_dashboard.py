"""
Builds a single dashboard image from the same queries used in the SQL analysis.

Usage:  python build_dashboard.py
Output: output/dashboard.png
"""

import sqlite3

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DB = "hr.db"
INK = "#1f2a33"
MUTED = "#8a97a3"
BAR = "#2f7d8f"
HI = "#c94f3d"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#d6dce1",
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def q(conn, sql):
    cur = conn.execute(sql)
    return [d[0] for d in cur.description], cur.fetchall()


def barh(ax, labels, values, title, highlight_max=True):
    colors = [BAR] * len(values)
    if highlight_max and values:
        colors[values.index(max(values))] = HI
    bars = ax.barh(labels, values, color=colors, height=0.6)
    ax.invert_yaxis()
    ax.set_title(title, fontsize=11, weight="bold", loc="left", pad=10)
    ax.set_xlim(0, max(values) * 1.25)
    ax.xaxis.set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=9)
    for b, v in zip(bars, values):
        ax.text(b.get_width() + max(values) * 0.02, b.get_y() + b.get_height() / 2,
                f"{v}%", va="center", fontsize=9, color=INK)


def main():
    conn = sqlite3.connect(DB)

    fig = plt.figure(figsize=(13, 8.5))
    fig.patch.set_facecolor("white")
    gs = fig.add_gridspec(3, 2, height_ratios=[0.30, 1, 1],
                          hspace=0.55, wspace=0.38,
                          left=0.13, right=0.96, top=0.95, bottom=0.07)

    # ---- headline numbers ----
    _, rows = q(conn, open("queries/01_overall_attrition.sql").read())
    total, left, rate = rows[0]

    head = fig.add_subplot(gs[0, :])
    head.axis("off")
    head.text(0, 0.78, "Employee Attrition Analysis", fontsize=20, weight="bold", color=INK)
    head.text(0, 0.34, "Where the organisation is losing people, and what those leavers have in common",
              fontsize=10.5, color=MUTED)

    for i, (label, value) in enumerate(
        [("Employees", f"{total:,}"), ("Left", f"{left:,}"), ("Attrition rate", f"{rate}%")]
    ):
        x = 0.62 + i * 0.13
        head.text(x, 0.72, value, fontsize=17, weight="bold", color=HI if i == 2 else INK)
        head.text(x, 0.30, label, fontsize=9, color=MUTED)

    # ---- department ----
    _, rows = q(conn, open("queries/02_attrition_by_department.sql").read())
    ax = fig.add_subplot(gs[1, 0])
    barh(ax, [r[0].replace(" & ", " &\n") for r in rows], [r[3] for r in rows],
         "Attrition rate by department")

    # ---- tenure ----
    _, rows = q(conn, open("queries/03_tenure_bands.sql").read())
    ax = fig.add_subplot(gs[1, 1])
    barh(ax, [r[0] for r in rows], [r[3] for r in rows],
         "Attrition rate by length of service")

    # ---- income ----
    _, rows = q(conn, open("queries/05_income_bands.sql").read())
    ax = fig.add_subplot(gs[2, 0])
    barh(ax, [r[0] for r in rows], [r[2] for r in rows],
         "Attrition rate by monthly income band")

    # ---- worst roles ----
    _, rows = q(conn, """
        SELECT JobRole,
               ROUND(100.0 * SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*), 1)
        FROM employees GROUP BY JobRole
        ORDER BY 2 DESC LIMIT 6
    """)
    ax = fig.add_subplot(gs[2, 1])
    barh(ax, [r[0] for r in rows], [r[1] for r in rows],
         "Highest attrition job roles")

    fig.savefig("output/dashboard.png", dpi=160, facecolor="white")
    print("Wrote output/dashboard.png")
    conn.close()


if __name__ == "__main__":
    main()
