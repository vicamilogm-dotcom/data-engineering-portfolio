SELECT COUNT(*)
FROM ikea_products
WHERE textsearchable_raw_product_details_text @@ to_tsquery('chair & armrest');
