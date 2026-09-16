-- Which departments lose the most people?
-- GROUP BY collapses all the rows into one summary row per department.

SELECT
    Department,
    COUNT(*)                                                      AS headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)            AS left_company,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1)
                                                                  AS attrition_rate_pct
FROM employees
GROUP BY Department
ORDER BY attrition_rate_pct DESC;
