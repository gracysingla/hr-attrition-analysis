-- Which job roles are the worst performers inside their own department?
--
-- Two things happen here:
--   1. The CTE (the WITH block) works out the attrition rate per job role first.
--      It is just a named temporary result, so the main query stays readable.
--   2. The window functions add a ranking and a department average NEXT TO
--      every row, without collapsing the rows the way GROUP BY would.
--      PARTITION BY Department restarts the ranking for each department.

WITH role_stats AS (
    SELECT
        Department,
        JobRole,
        COUNT(*)                                                  AS headcount,
        ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1)
                                                                  AS attrition_rate_pct
    FROM employees
    GROUP BY Department, JobRole
)
SELECT
    Department,
    JobRole,
    headcount,
    attrition_rate_pct,
    RANK()      OVER (PARTITION BY Department ORDER BY attrition_rate_pct DESC)
                                                                  AS rank_in_dept,
    ROUND(AVG(attrition_rate_pct) OVER (PARTITION BY Department), 1)
                                                                  AS dept_avg_rate
FROM role_stats
ORDER BY Department, rank_in_dept;
