SELECT DISTINCT
  r.movie_id AS movie_id_ratings_table
FROM ratings r
LEFT JOIN movies_metadata m
  ON r.movie_id = m.id
WHERE m.id IS NULL
ORDER BY r.movie_id;
