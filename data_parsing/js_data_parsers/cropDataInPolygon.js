const turf = require("@turf/turf");

const filterPointersToRedundantStops = (geoJsonStopsData) => {
    const existingStops = geoJsonStopsData.features.map(stop => stop.properties.id)
    return geoJsonStopsData.features.map(stop =>
        ({...stop, properties: {...stop.properties, connections:
                    stop.properties.connections.filter(stopId => existingStops.includes(stopId))}}))
}

const cropGeoDataToPolygon = async (geoJsonStopsData, getPolygon) => {
    const polygonToCrop = await getPolygon()
    if (!polygonToCrop) throw Error("No polygon specified")

    const dataWithinPolygon = turf.pointsWithinPolygon(geoJsonStopsData, polygonToCrop)
    return {...dataWithinPolygon, features: filterPointersToRedundantStops(dataWithinPolygon)}
}

module.exports = cropGeoDataToPolygon


