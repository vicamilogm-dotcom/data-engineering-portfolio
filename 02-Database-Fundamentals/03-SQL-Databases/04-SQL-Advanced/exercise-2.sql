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
ORDER BY release_year DESC;
