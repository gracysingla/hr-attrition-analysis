-- Does pay explain who leaves?
-- Group employees into monthly income bands and evaluate attrition.

SELECT
    CASE
        WHEN MonthlyIncome <  3000  THEN 'Under 3k'
        WHEN MonthlyIncome <  6000  THEN '3k-6k'
        WHEN MonthlyIncome < 10000  THEN '6k-10k'
        ELSE '10k+'
    END                                                           AS income_band,
    COUNT(*)                                                      AS headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)            AS left_company,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1)
                                                                  AS attrition_rate_pct
FROM employees
GROUP BY income_band
ORDER BY MIN(MonthlyIncome);
