# Data parsing workflow

1. Parse ATCO-CIF files to JSON format via atco reader
2. Parse JSON into two files:
    
    a) \<city>Routes.json with the route list of the form:
    ```
    [{
    id: String,
    routeName: String,
    stops: Array<stopIds>,
    direction: String,
    vehicleType: String
    }, ...]
    ```
    b) \<city>Stops.json with the station list of the form:
    ```
    [{
    id: String,
    label: String,
    easting | lat: String,
    northing | lon: String,
    stationType: String,
    routes: Array,
    connections: Array
    }, ...]
    ```
3. Parse \<city>Stops.json to \<city>Stops.geojson
4. Cut geojson points outside of city polygon and
 generate \<city>StopsBounded.geojson
5. Filter \<city>StopsBounded.geojson 
and \<city>Routes.json to remove redundant 
stops from the properties
6. Cluster \<city>StopsBounded.geojson ---> 
\<city>StopsBoundedClustered.geojson
7. Convert \<city>StopsBoundedClustered.geojson 
to  \<city>StopsBoundedParsed.json

___

### Lviv boundaries
https://github.com/kameristov/lvivmaps

### Bristol boundaries
https://mapit.mysociety.org/area/2561.geojson 


To find city boundaries you can also use 
https://www.openstreetmap.org
 
