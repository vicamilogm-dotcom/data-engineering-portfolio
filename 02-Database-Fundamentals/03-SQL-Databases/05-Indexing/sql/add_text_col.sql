ALTER TABLE ikea_products
ADD COLUMN IF NOT EXISTS raw_product_details_text text;

UPDATE ikea_products
SET raw_product_details_text = regexp_replace(raw_product_details, E'<[^>]+>', ' ', 'gi')
WHERE raw_product_details_text IS NULL;
