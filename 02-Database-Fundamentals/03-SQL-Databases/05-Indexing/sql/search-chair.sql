SELECT COUNT(*)
FROM ikea_products
WHERE raw_product_details ILIKE '%chair%'
  AND raw_product_details ILIKE '%armrest%';
