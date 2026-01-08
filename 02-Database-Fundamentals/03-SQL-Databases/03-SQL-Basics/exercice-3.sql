SELECT *
FROM movies_metadata
WHERE adult IS NULL
   OR adult NOT IN (TRUE, FALSE);
