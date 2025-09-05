UPDATE ChargingStations
SET GeoLocation = geography::Point(AddressInfo_Latitude, AddressInfo_Longitude, 4326)
WHERE
    AddressInfo_Latitude IS NOT NULL
    AND AddressInfo_Longitude IS NOT NULL;