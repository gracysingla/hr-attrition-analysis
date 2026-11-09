-- Two working-conditions factors (OverTime and BusinessTravel), checked side by side.

SELECT
    OverTime,
    BusinessTravel,
    COUNT(*)                                                      AS headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)            AS left_company,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1)
                                                                  AS attrition_rate_pct
FROM employees
GROUP BY OverTime, BusinessTravel
HAVING COUNT(*) >= 30
ORDER BY attrition_rate_pct DESC;
