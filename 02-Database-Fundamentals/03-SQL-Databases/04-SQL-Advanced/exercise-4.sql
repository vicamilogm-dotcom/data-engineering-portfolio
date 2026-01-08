SELECT
  SUM(
    CASE
      WHEN budget IS NULL OR revenue IS NULL OR budget = 0 OR revenue = 0 THEN 1
      ELSE 0
    END
  )::int AS num_records_bad,
  COUNT(*)::int AS num_records_total,
  ROUND(
    (
      SUM(
        CASE
          WHEN budget IS NULL OR revenue IS NULL OR budget = 0 OR revenue = 0 THEN 1
          ELSE 0
        END
      )::numeric
      / COUNT(*)::numeric
    ) * 100,
    0
  )::int AS perc_records_bad
FROM movies_metadata;
