const turf = require("@turf/turf");

const CROP_RADIUS = 10; // km

const cropGeoDataInRadius = geoJsonStopsData => {
    const centroid = turf.centerOfMass({
      type: "FeatureCollection",
      features: geoJsonStopsData
    });
    const buffered = turf.buffer(centroid, CROP_RADIUS, {
      units: "kilometers"
    });
    return turf.pointsWithinPolygon(
      {
        type: "FeatureCollection",
        features: geoJsonStopsData
      },
      buffered
    );
}

module.exports = cropGeoDataInRadius