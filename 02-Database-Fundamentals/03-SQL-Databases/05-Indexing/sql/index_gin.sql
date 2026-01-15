ALTER TABLE ikea_products
ADD COLUMN IF NOT EXISTS textsearchable_raw_product_details_text tsvector
GENERATED ALWAYS AS (to_tsvector('english', raw_product_details_text)) STORED;

CREATE INDEX IF NOT EXISTS index_raw_product_details_text
ON ikea_products
USING GIN (textsearchable_raw_product_details_text);
