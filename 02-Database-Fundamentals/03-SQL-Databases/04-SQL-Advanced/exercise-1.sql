SELECT
  id,
  (revenue - budget) AS profit_absolute,
  ROUND(((revenue - budget)::numeric / budget::numeric), 2) AS profit_percentage
FROM movies_metadata
WHERE budget IS NOT NULL
  AND revenue IS NOT NULL
  AND budget > 10000
  AND revenue > 10000
ORDER BY profit_percentage DESC, id ASC;
