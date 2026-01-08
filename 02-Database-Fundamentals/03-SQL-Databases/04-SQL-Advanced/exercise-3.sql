WITH yearly AS (
  SELECT
    EXTRACT(YEAR FROM release_date)::int AS release_year,
    ROUND(AVG(revenue)::numeric, 0)::bigint AS avg_revenue,
    ROUND(AVG((revenue - budget))::numeric, 0)::bigint AS avg_profit_absolute,
    ROUND(AVG(((revenue - budget)::numeric / budget::numeric))::numeric, 2) AS avg_profit_perc
  FROM movies_metadata
  WHERE release_date IS NOT NULL
    AND budget IS NOT NULL
    AND revenue IS NOT NULL
    AND budget > 10000
    AND revenue > 10000
  GROUP BY 1
),
with_prev AS (
  SELECT
    release_year,
    avg_revenue,
    avg_profit_absolute,
    LAG(avg_profit_absolute) OVER (ORDER BY release_year) AS prev_avg_profit_absolute,
    avg_profit_perc
  FROM yearly
)
SELECT
  release_year,
  avg_revenue,
  avg_profit_absolute,
  ROUND(
    ((avg_profit_absolute - prev_avg_profit_absolute)::numeric / NULLIF(prev_avg_profit_absolute, 0)::numeric) * 100,
    0
  )::int AS avg_profit_absolute_perc_growth_yoy,
  avg_profit_perc
FROM with_prev
ORDER BY release_year DESC;
