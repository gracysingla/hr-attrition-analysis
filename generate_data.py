"""
Generates a realistic HR dataset for the attrition analysis.

Column names match the widely used IBM HR Analytics Employee Attrition dataset,
so if you download that CSV from Kaggle you can drop it in as data/employees.csv
and every query in this project will still run unchanged.
"""

import csv
import random

random.seed(42)

DEPARTMENTS = {
    "Sales": ["Sales Executive", "Sales Representative", "Manager"],
    "Research & Development": [
        "Research Scientist", "Laboratory Technician", "Manufacturing Director",
        "Healthcare Representative", "Research Director", "Manager",
    ],
    "Human Resources": ["Human Resources", "Manager"],
}

# Base attrition likelihood per department
DEPT_RISK = {"Sales": 0.065, "Research & Development": 0.030, "Human Resources": 0.055}

# Roles that churn more than their department average
HIGH_CHURN_ROLES = {"Sales Representative": 0.13, "Laboratory Technician": 0.05}

EDUCATION_FIELDS = [
    "Life Sciences", "Medical", "Marketing", "Technical Degree", "Other", "Human Resources",
]
TRAVEL = ["Non-Travel", "Travel_Rarely", "Travel_Frequently"]
MARITAL = ["Single", "Married", "Divorced"]


def income_for(role, years_at_company):
    base = {
        "Sales Representative": 2600, "Laboratory Technician": 3200,
        "Human Resources": 4200, "Sales Executive": 6500,
        "Research Scientist": 4900, "Healthcare Representative": 7400,
        "Manufacturing Director": 7300, "Manager": 17200, "Research Director": 16000,
    }[role]
    growth = 1 + (years_at_company * 0.035)
    return int(base * growth * random.uniform(0.85, 1.2))


def make_row(emp_id):
    dept = random.choices(
        list(DEPARTMENTS), weights=[0.31, 0.63, 0.06]
    )[0]
    role = random.choice(DEPARTMENTS[dept])

    age = random.randint(19, 60)
    total_working_years = max(0, min(age - 19, int(random.expovariate(1 / 10))))
    years_at_company = max(0, min(total_working_years, int(random.expovariate(1 / 6))))
    years_since_promotion = min(years_at_company, int(random.expovariate(1 / 2)))

    monthly_income = income_for(role, years_at_company)
    overtime = "Yes" if random.random() < 0.28 else "No"
    travel = random.choices(TRAVEL, weights=[0.10, 0.71, 0.19])[0]
    satisfaction = random.randint(1, 4)
    work_life = random.randint(1, 4)

    # --- attrition probability: built from a few real drivers ---
    p = DEPT_RISK[dept]
    p += HIGH_CHURN_ROLES.get(role, 0)

    if years_at_company <= 1:
        p += 0.11                       # newest employees leave most
    elif years_at_company <= 4:
        p += 0.02
    elif years_at_company >= 10:
        p -= 0.04

    if monthly_income < 3000:
        p += 0.055                      # low pay band churns
    elif monthly_income > 10000:
        p -= 0.03

    if overtime == "Yes":
        p += 0.055
    if travel == "Travel_Frequently":
        p += 0.04
    if satisfaction <= 2:
        p += 0.035
    if work_life == 1:
        p += 0.03
    if age < 25:
        p += 0.04

    p = max(0.01, min(0.92, p))
    attrition = "Yes" if random.random() < p else "No"

    return {
        "EmployeeID": emp_id,
        "Age": age,
        "Attrition": attrition,
        "BusinessTravel": travel,
        "Department": dept,
        "EducationField": random.choice(EDUCATION_FIELDS),
        "Gender": random.choice(["Male", "Female"]),
        "JobRole": role,
        "JobSatisfaction": satisfaction,
        "MaritalStatus": random.choice(MARITAL),
        "MonthlyIncome": monthly_income,
        "OverTime": overtime,
        "TotalWorkingYears": total_working_years,
        "WorkLifeBalance": work_life,
        "YearsAtCompany": years_at_company,
        "YearsSinceLastPromotion": years_since_promotion,
    }


def main(n=1470, path="data/employees.csv"):
    rows = [make_row(1000 + i) for i in range(n)]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    left = sum(1 for r in rows if r["Attrition"] == "Yes")
    print(f"Wrote {len(rows)} rows to {path}")
    print(f"Attrition: {left} of {len(rows)} ({100 * left / len(rows):.1f}%)")


if __name__ == "__main__":
    main()
