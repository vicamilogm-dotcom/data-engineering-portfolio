--- Discount performance: mejor oferta especial por ventas
SELECT
  f.SpecialOfferKey,
  d.Description,
  SUM(f.LineTotal) AS TotalSales,
  d.DiscountPct
FROM sales_mart.SalesOrderItemFact f
JOIN sales_mart.SpecialOfferDim d
  ON f.SpecialOfferKey = d.SpecialOfferKey
GROUP BY
  f.SpecialOfferKey, d.Description, d.DiscountPct
ORDER BY
  TotalSales DESC;

--- Group performance: mejores grupos (North America, Europe, Pacific...)
SELECT
  t.OverallGroup AS SalesGroup,
  SUM(f.LineTotal) AS TotalSales
FROM sales_mart.SalesOrderItemFact f
JOIN sales_mart.TerritoryDim t
  ON f.TerritoryKey = t.TerritoryKey
GROUP BY
  SalesGroup
ORDER BY
  TotalSales DESC;
