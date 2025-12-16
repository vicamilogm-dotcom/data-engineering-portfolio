-- SalesOrderItemFact
CREATE TABLE sales_mart.SalesOrderItemFact AS
SELECT
  SD.SalesOrderDetailID       AS SalesOrderDetailKey,
  SH.SalesOrderID             AS SalesOrderKey,
  SD.SpecialOfferID           AS SpecialOfferKey,
  SH.Status                   AS SalesOrderStatusKey,
  SH.OnlineOrderFlag          AS SalesOnlineOrderFlag,
  SH.AccountNumber            AS SalesOrderAccountNumber,
  SH.CustomerID               AS SalesOrderCustomerKey,
  IFNULL(SH.SalesPersonID, 0) AS SalesPersonKey,
  SH.TerritoryID              AS TerritoryKey,
  SH.BillToAddressID          AS BillToAddressKey,
  SH.ShipToAddressID          AS ShipToAddressKey,
  SH.ShipMethodID             AS ShipMethodKey,
  CAST(FORMAT_TIMESTAMP('%Y%m%d', SD.ModifiedDate) AS INT64) AS SalesOrderDetailModifiedDateKey,
  CAST(FORMAT_TIMESTAMP('%Y%m%d', SH.OrderDate)    AS INT64) AS SalesOrderDateKey,
  CAST(FORMAT_TIMESTAMP('%Y%m%d', SH.DueDate)      AS INT64) AS SalesOrderDueDateKey,
  CAST(FORMAT_TIMESTAMP('%Y%m%d', SH.ShipDate)     AS INT64) AS SalesOrderShipDateKey,
  CAST(FORMAT_TIMESTAMP('%Y%m%d', SH.ModifiedDate) AS INT64) AS SalesOrderModifiedDateKey,
  SD.OrderQty,
  SD.UnitPrice,
  SD.UnitPriceDiscount,
  SD.LineTotal,
  SH.SubTotal  AS SalesOrderSubTotal,
  SH.TaxAmt    AS SalesOrderTaxAmount,
  SH.Freight   AS SalesOrderFreightAmount,
  SH.TotalDue  AS SalesOrderTotalDueAmount
FROM adventure_works_raw.SalesOrderDetail SD
LEFT JOIN adventure_works_raw.SalesOrderHeader SH
  ON SD.SalesOrderID = SH.SalesOrderID;

--- MonthlyTerritoryPerformanceFact
CREATE OR REPLACE TABLE sales_mart.MonthlySalesSnapshotFact AS
SELECT
  LEFT(CAST(SalesOrderDateKey AS STRING), 6) AS MonthYear,
  TerritoryKey,
  SUM(LineTotal) AS MonthlySalesAmount,
  SUM(OrderQty)  AS MonthlyQuantitySold
FROM sales_mart.SalesOrderItemFact
GROUP BY
  LEFT(CAST(SalesOrderDateKey AS STRING), 6),
  TerritoryKey;
