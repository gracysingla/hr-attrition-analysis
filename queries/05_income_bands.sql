-- Does pay explain who leaves?

SELECT
    CASE
        WHEN MonthlyIncome <  3000  THEN 'Under 3k'
        WHEN MonthlyIncome <  6000  THEN '3k-6k'
        WHEN MonthlyIncome < 10000  THEN '6k-10k'
        ELSE '10k+'
    END                                                           AS income_band,
    COUNT(*)                                                      AS headcount,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1)
                                                                  AS attrition_rate_pct
FROM employees
GROUP BY income_band
ORDER BY MIN(MonthlyIncome);
