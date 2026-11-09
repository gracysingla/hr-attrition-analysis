-- Which job roles are the worst performers inside their own department?
--
-- Two things happen here:
--   1. The CTE (the WITH block) works out headcount and leavers per job role.
--   2. Window functions add intra-department ranking and the true weighted 
--      department baseline rate next to each row for direct comparison.

WITH role_stats AS (
    SELECT
        Department,
        JobRole,
        COUNT(*)                                                      AS headcount,
        SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)            AS left_company,
        ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1)
                                                                      AS attrition_rate_pct
    FROM employees
    GROUP BY Department, JobRole
)
SELECT
    Department,
    JobRole,
    headcount,
    left_company,
    attrition_rate_pct,
    RANK() OVER (PARTITION BY Department ORDER BY attrition_rate_pct DESC)
                                                                      AS rank_in_dept,
    ROUND(100.0 * SUM(left_company) OVER (PARTITION BY Department) / SUM(headcount) OVER (PARTITION BY Department), 1)
                                                                      AS dept_avg_rate
FROM role_stats
ORDER BY Department, rank_in_dept;
