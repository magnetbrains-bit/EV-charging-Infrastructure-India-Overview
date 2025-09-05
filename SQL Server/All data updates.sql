USE EV_India_Analysis;
GO

PRINT 'Step 1: Updating GeoLocation data...';
UPDATE ChargingStations
SET GeoLocation = geography::Point(AddressInfo_Latitude, AddressInfo_Longitude, 4326)
WHERE
    AddressInfo_Latitude IS NOT NULL
    AND AddressInfo_Longitude IS NOT NULL;
GO

PRINT 'Step 2: Standardizing Operator names...';
UPDATE ChargingStations
SET OperatorInfo_Title = 'Unknown'
WHERE
    OperatorInfo_Title IS NULL OR OperatorInfo_Title = '';
GO

PRINT 'Step 3: Populating the PricingType column...';
UPDATE ChargingStations
SET PricingType =
    CASE
        WHEN UsageCost IS NULL THEN 'Unknown'
        WHEN UsageCost = '' THEN 'Unknown'
        WHEN UsageCost LIKE '%Free%' THEN 'Free'
        ELSE 'Paid'
    END;
GO

PRINT 'Step 4: Creating the final, clean view for Power BI...';
DROP VIEW IF EXISTS vw_ChargingStations_Clean;
GO

CREATE VIEW vw_ChargingStations_Clean AS
SELECT
    ID,
    AddressInfo_Title,
    AddressInfo_Town,
    AddressInfo_StateOrProvince,
    AddressInfo_Latitude,
    AddressInfo_Longitude,
    OperatorInfo_Title,
    NumberOfPoints,
    UsageType_Title,
    UsageCost,
    StatusType_Title,
    DateLastStatusUpdate,
    GeoLocation,
    PricingType
FROM
    dbo.ChargingStations;
GO

PRINT 'Setup complete. The view vw_ChargingStations_Clean is now ready for Power BI.';