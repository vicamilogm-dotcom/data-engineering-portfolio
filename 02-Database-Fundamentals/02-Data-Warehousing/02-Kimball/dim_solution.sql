--- SpecialOfferDim
CREATE OR REPLACE TABLE sales_mart.SpecialOfferDim AS
SELECT DISTINCT
  SpecialOfferID AS SpecialOfferKey,
  Description,
  DiscountPct
FROM adventure_works_raw.SpecialOffer;

--- DateDim
CREATE OR REPLACE TABLE sales_mart.DateDim AS
SELECT DISTINCT
  CAST(FORMAT_TIMESTAMP('%Y%m%d', ModifiedDate) AS INT64) AS DateKey,
  ModifiedDate AS Date,
  EXTRACT(YEAR FROM ModifiedDate) AS Year,
  EXTRACT(QUARTER FROM ModifiedDate) AS Quarter,
  EXTRACT(MONTH FROM ModifiedDate) AS Month,
  EXTRACT(DAY FROM ModifiedDate) AS Day
FROM adventure_works_raw.SalesOrderDetail;

--- TerritoryDim
CREATE OR REPLACE TABLE sales_mart.TerritoryDim AS
SELECT DISTINCT
  TerritoryID AS TerritoryKey,
  Name,
  CountryRegionCode,
  `Group` as OverallGroup
FROM adventure_works_raw.SalesTerritory;
