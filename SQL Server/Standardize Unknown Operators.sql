UPDATE ChargingStations
SET OperatorInfo_Title = 'Unknown'
WHERE
    OperatorInfo_Title IS NULL OR OperatorInfo_Title = '';