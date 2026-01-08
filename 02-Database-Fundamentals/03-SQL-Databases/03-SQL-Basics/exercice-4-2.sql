WITH duplicates AS (
  SELECT id, COUNT(*) AS num_records
  FROM movies_metadata
  GROUP BY id
  HAVING COUNT(*) > 1
)
SELECT m.*, d.num_records
FROM movies_metadata m
JOIN duplicates d ON m.id = d.id
ORDER BY m.id;
