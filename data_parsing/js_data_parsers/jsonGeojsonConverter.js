const convertJsonToGeojson = (data) => ({type: "FeatureCollection", features: data.map(stop => ({
    type: "Feature",
    geometry: { type: "Point", coordinates: [stop["lon"], stop["lat"]] },
    properties: { ...stop }
  }))})

const convertGeojsonToJson = data => data.features.map(stop => stop.properties)

module.exports.convertJsonToGeojson = convertJsonToGeojson
module.exports.convertGeojsonToJson = convertGeojsonToJson