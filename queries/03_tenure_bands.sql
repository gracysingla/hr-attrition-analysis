-- When do people leave? Group employees into length-of-service bands.
-- CASE is used here to build the bands themselves, not just to count.

SELECT
    CASE
        WHEN YearsAtCompany <= 1  THEN '0-1 years'
        WHEN YearsAtCompany <= 4  THEN '2-4 years'
        WHEN YearsAtCompany <= 9  THEN '5-9 years'
        ELSE '10+ years'
    END                                                           AS tenure_band,
    COUNT(*)                                                      AS headcount,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)            AS left_company,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1)
                                                                  AS attrition_rate_pct
FROM employees
GROUP BY tenure_band
ORDER BY MIN(YearsAtCompany);
