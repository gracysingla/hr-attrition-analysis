-- How many people are there, how many left, and what share is that?
-- CASE turns the text column "Yes"/"No" into a 1/0 we can add up.

SELECT
    COUNT(*)                                                      AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)            AS left_company,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1)
                                                                  AS attrition_rate_pct
FROM employees;
