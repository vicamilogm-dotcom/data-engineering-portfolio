SELECT
  id,
  COUNT(*) AS num_records
FROM movies_metadata
GROUP BY id
HAVING COUNT(*) > 1
ORDER BY num_records DESC, id;
