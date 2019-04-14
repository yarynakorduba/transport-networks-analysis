const turf = require("@turf/turf");
const fetch = require("node-fetch");

const getPolygonOfBristol = () =>
    fetch(
        "https://mapit.mysociety.org/area/2561.geojson"
    )
        .then(res => res.json())
        .catch(err => console.log(err));

const filterPointersToRedundantStops = (geoJsonStopsData) => {
    const existingStops = geoJsonStopsData.features.map(stop => stop.properties.id)
    return geoJsonStopsData.features.map(stop =>
        ({...stop, properties: {...stop.properties, connections:
                    stop.properties.connections.filter(stopId => existingStops.includes(stopId))}}))
}

const cropGeoDataToPolygon = async (geoJsonStopsData) => {
    const polygonToCrop = await getPolygonOfBristol()
    const dataWithinPolygon = turf.pointsWithinPolygon(geoJsonStopsData, polygonToCrop)
    console.log(dataWithinPolygon.type)
    return {...dataWithinPolygon, features: filterPointersToRedundantStops(dataWithinPolygon)}
}

module.exports = cropGeoDataToPolygon


