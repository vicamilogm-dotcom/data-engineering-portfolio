ALTER TABLE ratings
ADD COLUMN IF NOT EXISTS created_at_utc TIMESTAMP;

UPDATE ratings
SET created_at_utc = to_timestamp(timestamp) AT TIME ZONE 'UTC'
WHERE created_at_utc IS NULL;
