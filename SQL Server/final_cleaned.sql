USE EV_India_Analysis;
GO

CREATE OR ALTER VIEW vw_ChargingStations_Clean AS
WITH PreCalculatedCosts AS (
    -- First, calculate the cost for each row, applying all our rules.
    SELECT *,
        CASE
            WHEN ID = 308862 THEN 30.00
            WHEN ID = 308873 THEN 60.00
            ELSE 
                COALESCE(
                    TRY_CAST(
                        dbo.fn_StripNonNumeric(UsageCost) AS DECIMAL(10, 2)
                    ), 
                    0
                )
        END AS CalculatedCost
    FROM dbo.ChargingStations
),
MeanCalculation AS (
    -- Second, calculate the single average value from all non-zero costs.
    SELECT AVG(NULLIF(CalculatedCost, 0)) AS MeanUsageCost
    FROM PreCalculatedCosts
)
-- Finally, build the view using these calculations.
SELECT
    p.ID,
    p.AddressInfo_Title,
    UPPER(ISNULL(p.AddressInfo_Town, 'Unknown')) AS AddressInfo_Town,
    UPPER(
        CASE 
            WHEN p.AddressInfo_StateOrProvince = 'KA' THEN 'Karnataka'
            ELSE ISNULL(p.AddressInfo_StateOrProvince, 'Unknown')
        END
    ) AS AddressInfo_StateOrProvince,
    p.AddressInfo_Latitude,
    p.AddressInfo_Longitude,
    REPLACE(REPLACE(p.OperatorInfo_Title, '(', ''), ')', '') AS OperatorInfo_Title,
    p.NumberOfPoints,
    p.UsageType_Title,
    -- Apply the imputation: if the cost is 0, use the mean; otherwise, use the calculated cost.
    ISNULL(
        CASE
            WHEN p.CalculatedCost = 0 THEN m.MeanUsageCost
            ELSE p.CalculatedCost
        END,
    0) AS UsageCost_per_kWh,
    p.StatusType_Title,
    p.DateLastStatusUpdate,
    p.GeoLocation,
    p.PricingType
FROM 
    PreCalculatedCosts p,
    MeanCalculation m;
GO