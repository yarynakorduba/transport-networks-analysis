const turf = require("@turf/turf");


const cropGeoDataInRadius = (geoJsonStopsData, centroid, cropRadius) => {
    const buffered = turf.buffer(centroid, cropRadius, {
      units: "kilometers"
    });
    return turf.pointsWithinPolygon(geoJsonStopsData, buffered);
}

module.exports = cropGeoDataInRadius